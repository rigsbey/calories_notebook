import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from aiogram import Bot
from aiogram.types import LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from services.subscription_service import SubscriptionService
from config import BOT_TOKEN

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self, bot: Bot = None):
        self.bot = bot or Bot(token=BOT_TOKEN)
        self.subscription_service = SubscriptionService()
        
        # Конфигурация платежных провайдеров
        # Для Telegram Stars используем специальный провайдер
        self.PAYMENT_PROVIDER_TOKEN = ""  # Для Stars не нужен provider_token
        
        # Для обычных платежей (если понадобятся в будущем)
        # self.PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")

    async def create_subscription_payment(self, user_id: int, plan: str, duration: int) -> Dict:
        """Создает счет для оплаты подписки"""
        try:
            pricing = self.subscription_service.get_pricing_info()
            
            # Определяем цену и описание
            if plan == "pro" and duration == 1:
                amount = pricing["subscriptions"]["pro_monthly"]
                title = "🌟 Pro подписка - месяц"
                description = "200 фото/мес, мульти-тарелка, витамины, экспорт, календарь"
            elif plan == "pro" and duration == 3:
                amount = pricing["subscriptions"]["pro_quarterly"]
                title = "🌟 Pro подписка - 3 месяца"
                description = "200 фото/мес, все функции Pro. Выгода 33%!"
            elif plan == "pro" and duration == 12:
                amount = pricing["subscriptions"]["pro_yearly"]
                title = "🌟 Pro подписка - год"
                description = "200 фото/мес, все функции Pro. Выгода 50%!"
            else:
                return {"success": False, "error": "Неизвестный план подписки"}
            
            # Создаем список цен для Telegram Payments
            prices = [LabeledPrice(label=title, amount=amount * 100)]  # В копейках
            
            payload = f"subscription_{plan}_{duration}_{user_id}_{datetime.now().timestamp()}"
            
            # Отправляем счет
            await self.bot.send_invoice(
                chat_id=user_id,
                title=title,
                description=description,
                payload=payload,
                provider_token=self.PAYMENT_PROVIDER_TOKEN,
                currency="RUB",
                prices=prices,
                max_tip_amount=0,
                suggested_tip_amounts=[],
                photo_url="https://calories.toxiguard.site/og-image.jpg",
                photo_size=512,
                photo_width=512,
                photo_height=512,
                need_name=False,
                need_phone_number=False,
                need_email=False,
                need_shipping_address=False,
                send_phone_number_to_provider=False,
                send_email_to_provider=False,
                is_flexible=False,
            )
            
            return {
                "success": True,
                "payload": payload,
                "amount": amount
            }
            
        except Exception as e:
            logger.error(f"Ошибка создания счета: {e}")
            return {"success": False, "error": str(e)}

    async def process_successful_payment(self, payment_info: Dict) -> bool:
        """Обрабатывает успешный платеж"""
        try:
            payload = payment_info.get('invoice_payload', '')
            total_amount = payment_info.get('total_amount', 0)
            
            # Парсим payload
            parts = payload.split('_')
            if len(parts) < 4:
                logger.error(f"Неверный формат payload: {payload}")
                return False
            
            payment_type = parts[0]
            
            # Обработка Stars платежей
            if payment_type == "stars":
                product = parts[1]
                user_id = int(parts[2])
                stars_amount = total_amount  # Для Stars amount уже в правильном формате
                
                # Сохраняем информацию о Stars платеже
                payment_data = {
                    'user_id': user_id,
                    'payment_type': 'stars',
                    'product': product,
                    'stars_amount': stars_amount,
                    'currency': 'XTR',  # Telegram Stars
                    'status': 'completed',
                    'telegram_payment_charge_id': payment_info.get('telegram_payment_charge_id'),
                    'provider_payment_charge_id': payment_info.get('provider_payment_charge_id'),
                    'created_at': datetime.now()
                }
                
                await self.subscription_service.save_payment(payment_data)
                
                # Активируем покупку
                success = await self.process_stars_payment(user_id, product, stars_amount)
                
                if success:
                    await self.bot.send_message(
                        user_id,
                        f"🎉 **Покупка завершена!**\n\n"
                        f"⭐ Потрачено: {stars_amount} Stars\n"
                        f"✅ Товар активирован!\n\n"
                        f"📸 Можете использовать новые возможности!",
                        parse_mode="Markdown"
                    )
                    return True
                else:
                    logger.error(f"Не удалось активировать Stars покупку для пользователя {user_id}")
                    await self.bot.send_message(
                        user_id,
                        "❌ Произошла ошибка при активации покупки. "
                        "Обратитесь в поддержку."
                    )
                    return False
            
            # Обработка обычных подписок (RUB)
            elif payment_type == "subscription":
                plan = parts[1]
                duration = int(parts[2])
                user_id = int(parts[3])
                total_amount = total_amount // 100  # Из копеек в рубли
            
                # Сохраняем информацию о платеже
                payment_data = {
                    'user_id': user_id,
                    'payment_type': payment_type,
                    'plan': plan,
                    'duration': duration,
                    'amount': total_amount,
                    'currency': 'RUB',
                    'status': 'completed',
                    'telegram_payment_charge_id': payment_info.get('telegram_payment_charge_id'),
                    'provider_payment_charge_id': payment_info.get('provider_payment_charge_id'),
                    'created_at': datetime.now()
                }
            
            await self.subscription_service.save_payment(payment_data)
            
            # Активируем подписку
            if payment_type == "subscription" and plan == "pro":
                success = await self.subscription_service.activate_pro_subscription(user_id, duration)
                
                if success:
                    await self.bot.send_message(
                        user_id,
                        "🎉 **Поздравляем!**\n\n"
                        f"✅ Pro подписка активирована на {duration} мес.\n"
                        f"💰 Сумма: {total_amount} ₽\n\n"
                        "🌟 **Теперь доступны:**\n"
                        "• До 200 фото в месяц\n"
                        "• Мульти-тарелка (несколько блюд на фото)\n"
                        "• Детальная информация о витаминах\n"
                        "• Экспорт в PDF/CSV\n"
                        "• Синхронизация с Google Calendar\n"
                        "• Приоритетная очередь\n\n"
                        "📸 Отправьте фото еды для анализа!",
                        parse_mode="Markdown"
                    )
                    return True
                else:
                    logger.error(f"Не удалось активировать подписку для пользователя {user_id}")
                    await self.bot.send_message(
                        user_id,
                        "❌ Произошла ошибка при активации подписки. "
                        "Обратитесь в поддержку."
                    )
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка обработки платежа: {e}")
            return False

    async def create_stars_payment_invoice(self, user_id: int, product: str, stars_amount: int) -> Dict:
        """Создает счет за Telegram Stars"""
        try:
            
            product_names = {
                "extra_10_analyses": "💫 +10 дополнительных анализов",
                "multi_dish_24h": "🍽️ Мульти-тарелка на 24 часа",  
                "pdf_report": "📄 PDF отчет за неделю"
            }
            
            product_name = product_names.get(product, "Неизвестный товар")
            title = f"⭐ {product_name}"
            description = f"Покупка за {stars_amount} Telegram Stars"
            
            # Создаем список цен для Telegram Stars
            prices = [LabeledPrice(label=product_name, amount=stars_amount)]  # В Stars (не копейках!)
            
            payload = f"stars_{product}_{user_id}_{datetime.now().timestamp()}"
            
            # Отправляем счет за Stars (валюта XTR = Telegram Stars)
            await self.bot.send_invoice(
                chat_id=user_id,
                title=title,
                description=description,
                payload=payload,
                provider_token="",  # Для Stars не нужен provider_token
                currency="XTR",  # XTR = Telegram Stars
                prices=prices,
                max_tip_amount=0,
                suggested_tip_amounts=[],
                photo_url="https://calories.toxiguard.site/og-image.jpg",
                photo_size=512,
                photo_width=512,
                photo_height=512,
                need_name=False,
                need_phone_number=False,
                need_email=False,
                need_shipping_address=False,
                send_phone_number_to_provider=False,
                send_email_to_provider=False,
                is_flexible=False,
            )
            
            return {
                "success": True,
                "payload": payload,
                "stars_amount": stars_amount
            }
            
        except Exception as e:
            logger.error(f"Ошибка создания Stars счета: {e}", exc_info=True)
            error_msg = str(e)
            
            # Специальная обработка для ошибки провайдера
            if "PAYMENT_PROVIDER_INVALID" in error_msg:
                error_msg = "Провайдер платежей не настроен. Обратитесь к администратору для настройки Stars платежей в BotFather."
            elif "Bad Request" in error_msg:
                error_msg = f"Ошибка запроса к Telegram: {error_msg}"
            
            return {"success": False, "error": error_msg}

    async def create_stars_payment(self, user_id: int, product: str) -> InlineKeyboardMarkup:
        """Создает кнопку для покупки за Stars"""
        try:
            pricing = self.subscription_service.get_pricing_info()
            stars_prices = pricing["stars"]
            
            if product == "extra_10_analyses":
                price = stars_prices["extra_10_analyses"]
                title = "💫 +10 анализов"
                description = "Дополнительные 10 анализов еды"
            elif product == "multi_dish_24h":
                price = stars_prices["multi_dish_24h"]
                title = "🍽️ Мульти-тарелка 24ч"
                description = "Анализ нескольких блюд на одном фото (24 часа)"
            elif product == "pdf_report":
                price = stars_prices["pdf_report"]
                title = "📄 PDF отчет"
                description = "Подробный отчет за неделю в PDF"
            else:
                return None
            
            # Создаем кнопку для Stars
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text=f"⭐ Купить за {price} Stars",
                    callback_data=f"buy_stars_{product}_{price}"
                )],
                [InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="cancel_payment"
                )]
            ])
            
            return keyboard
            
        except Exception as e:
            logger.error(f"Ошибка создания Stars платежа: {e}")
            return None

    async def process_stars_payment(self, user_id: int, product: str, stars_amount: int) -> bool:
        """Обрабатывает покупку за Stars"""
        try:
            # Здесь должна быть логика списания Stars через Telegram Bot API
            # В текущей версии API нет прямой поддержки Stars payments
            # Это placeholder для будущей реализации
            
            if product == "extra_10_analyses":
                success = await self.subscription_service.add_stars_analyses(user_id, 10)
                if success:
                    await self.bot.send_message(
                        user_id,
                        f"✅ **Покупка завершена!**\n\n"
                        f"🌟 Потрачено: {stars_amount} Stars\n"
                        f"💫 Получено: +10 дополнительных анализов\n\n"
                        f"📸 Теперь можете анализировать больше фото!",
                        parse_mode="Markdown"
                    )
                return success
                
            elif product == "multi_dish_24h":
                # Временно активируем мульти-тарелку на 24 часа
                from firebase_admin import firestore
                user_ref = self.subscription_service.firebase_service.db.collection('users').document(str(user_id))
                
                expire_time = datetime.now() + timedelta(hours=24)
                user_ref.update({
                    'temp_multi_dish_expires': expire_time
                })
                
                await self.bot.send_message(
                    user_id,
                    f"✅ **Мульти-тарелка активирована!**\n\n"
                    f"🌟 Потрачено: {stars_amount} Stars\n"
                    f"🍽️ Доступ: 24 часа\n"
                    f"⏰ До: {expire_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"📸 Отправляйте фото с несколькими блюдами!",
                    parse_mode="Markdown"
                )
                return True
                
            elif product == "pdf_report":
                # Генерируем PDF отчет
                await self.bot.send_message(
                    user_id,
                    f"✅ **PDF отчет создается!**\n\n"
                    f"🌟 Потрачено: {stars_amount} Stars\n"
                    f"📄 Отчет будет готов через несколько минут\n\n"
                    f"📧 PDF файл будет отправлен в этот чат",
                    parse_mode="Markdown"
                )
                # TODO: Реализовать генерацию PDF
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Ошибка обработки Stars платежа: {e}")
            return False

    def get_subscription_keyboard(self, current_plan: str = "lite") -> InlineKeyboardMarkup:
        """Создает клавиатуру с вариантами подписки"""
        keyboard_buttons = []
        
        if current_plan == "lite":
            # Предлагаем триал
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="🚀 7 дней Pro бесплатно",
                    callback_data="start_trial"
                )
            ])
        
        # Варианты подписки
        pricing = self.subscription_service.get_pricing_info()
        keyboard_buttons.extend([
            [InlineKeyboardButton(
                text=f"💳 Pro месяц - {pricing['subscriptions']['pro_monthly']}₽",
                callback_data="buy_pro_1"
            )],
            [InlineKeyboardButton(
                text=f"💳 Pro 3 мес - {pricing['subscriptions']['pro_quarterly']}₽ (-33%)",
                callback_data="buy_pro_3"
            )],
            [InlineKeyboardButton(
                text=f"💳 Pro год - {pricing['subscriptions']['pro_yearly']}₽ (-50%)",
                callback_data="buy_pro_12"
            )]
        ])
        
        # Stars опции
        keyboard_buttons.extend([
            [InlineKeyboardButton(
                text="⭐ Или купить за Stars",
                callback_data="stars_options"
            )],
            [InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="cancel_payment"
            )]
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    def get_stars_keyboard(self) -> InlineKeyboardMarkup:
        """Создает клавиатуру с покупками за Stars"""
        pricing = self.subscription_service.get_pricing_info()
        stars_prices = pricing["stars"]
        
        keyboard_buttons = [
            [InlineKeyboardButton(
                text=f"💫 +10 анализов - {stars_prices['extra_10_analyses']}⭐",
                callback_data="buy_stars_extra_10_analyses"
            )],
            [InlineKeyboardButton(
                text=f"🍽️ Мульти-тарелка 24ч - {stars_prices['multi_dish_24h']}⭐",
                callback_data="buy_stars_multi_dish_24h"
            )],
            [InlineKeyboardButton(
                text=f"📄 PDF отчет - {stars_prices['pdf_report']}⭐",
                callback_data="buy_stars_pdf_report"
            )],
            [InlineKeyboardButton(
                text="⬅️ Назад к подпискам",
                callback_data="back_to_subscriptions"
            )],
            [InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="cancel_payment"
            )]
        ]
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
