import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from services.subscription_service import SubscriptionService
from services.payment_service import PaymentService
from utils import error_handler

logger = logging.getLogger(__name__)

# Создаем роутер для обработчиков платежей
payments_router = Router()

# Инициализируем сервисы
subscription_service = SubscriptionService()
payment_service = PaymentService()

@payments_router.message(Command("pro"))
@error_handler
async def pro_info_handler(message: Message):
    """Показывает информацию о Pro подписке"""
    subscription = await subscription_service.get_user_subscription(message.from_user.id)
    current_plan = subscription['type']
    
    if current_plan == "pro":
        await message.answer(
            "🌟 **У вас уже есть Pro подписка!**\n\n"
            "✅ **Доступные функции:**\n"
            "• До 200 фото в месяц\n"
            "• Мульти-тарелка (несколько блюд)\n"
            "• Подробные витамины и микроэлементы\n"
            "• Экспорт в PDF/CSV\n"
            "• Синхронизация с Google Calendar\n"
            "• Полные отчеты за неделю/месяц\n"
            "• Приоритетная очередь\n\n"
            "📸 Отправьте фото еды для анализа!",
            parse_mode="Markdown"
        )
        return
    
    elif current_plan == "trial":
        await message.answer(
            "🚀 **У вас активен 7-дневный триал Pro!**\n\n"
            "✅ **Доступно всё Pro:**\n"
            "• До 200 фото в месяц\n"
            "• Мульти-тарелка\n"
            "• Витамины и микроэлементы\n"
            "• Экспорт и календарь\n\n"
            "📅 После окончания триала станет доступна покупка подписки.\n\n"
            "📸 Используйте все возможности Pro прямо сейчас!",
            parse_mode="Markdown"
        )
        return
    
    # Показываем пейволл для Lite пользователей
    await show_paywall(
        message,
        title="🌟 Обновиться до Pro?",
        description="Разблокируйте все возможности анализа питания:",
        features=[
            "• До 200 фото в месяц",
            "• Мульти-тарелка (несколько блюд)",
            "• Детальные витамины и микроэлементы", 
            "• Экспорт в PDF/CSV",
            "• Синхронизация с Google Calendar",
            "• Полные отчеты за неделю/месяц",
            "• Приоритетная очередь"
        ]
    )

@payments_router.callback_query(F.data == "show_paywall")
@error_handler
async def generic_paywall_handler(callback: CallbackQuery):
    """Показывает основной пейволл"""
    await callback.answer()
    
    await show_paywall(
        callback.message,
        title="⭐ Лимит Lite исчерпан",
        description="🚀 **Pro** откроет все возможности:",
        features=[
            "• До 200 фото в месяц вместо 5/день",
            "• Мульти-тарелка (несколько блюд)", 
            "• Детальные витамины + умные советы",
            "• Экспорт в PDF/CSV",
            "• Интеграция с Google Calendar",
            "• Полные отчеты за неделю",
            "• Приоритетная очередь"
        ]
    )

async def show_paywall(message_or_callback, title: str, description: str, features: list):
    """Универсальная функция показа пейволла"""
    subscription = await subscription_service.get_user_subscription(message_or_callback.from_user.id)
    current_plan = subscription['type']
    
    # Формируем сообщение
    text = f"{title}\n\n{description}\n\n" + "\n".join(features)
    
    # Добавляем информацию о текущем использовании
    daily_count = subscription['daily_photo_count']
    text += f"\n\n📊 **Сегодня использовано:** {daily_count}/5 фото"
    
    # Получаем клавиатуру с вариантами оплаты
    keyboard = payment_service.get_subscription_keyboard(current_plan)
    
    if hasattr(message_or_callback, 'edit_text'):
        await message_or_callback.edit_text(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await message_or_callback.answer(text, parse_mode="Markdown", reply_markup=keyboard)

@payments_router.callback_query(F.data == "start_trial")
@payments_router.callback_query(F.data == "start_pro_trial")
@error_handler 
async def start_trial_handler(callback: CallbackQuery):
    """Запуск 7-дневного триала"""
    await callback.answer()
    
    success = await subscription_service.start_trial(callback.from_user.id)
    
    if success:
        await callback.message.edit_text(
            "🎉 **Триал активирован!**\n\n"
            "✅ **7 дней Pro бесплатно**\n"
            "🌟 Все функции Pro разблокированы\n"
            "📅 Автоматическое продление отключено\n\n"
            "**Теперь доступно:**\n"
            "• До 200 фото в месяц\n"
            "• Мульти-тарелка\n"
            "• Витамины и микроэлементы\n"
            "• Экспорт в PDF/CSV\n"
            "• Google Calendar\n\n"
            "📸 Отправьте фото еды для анализа!",
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            "❌ **Триал недоступен**\n\n"
            "Возможные причины:\n"
            "• Триал уже был использован\n"
            "• Техническая ошибка\n\n"
            "💳 Выберите платную подписку:",
            parse_mode="Markdown",
            reply_markup=payment_service.get_subscription_keyboard("lite")
        )

@payments_router.callback_query(F.data.startswith("buy_pro_"))
@payments_router.callback_query(F.data == "buy_pro_monthly")
@payments_router.callback_query(F.data == "buy_pro_annual")
@error_handler
async def buy_pro_handler(callback: CallbackQuery):
    """Обработчик покупки Pro подписки"""
    await callback.answer()
    
    # Извлекаем количество месяцев из callback_data
    if callback.data == "buy_pro_monthly":
        duration = 1
    elif callback.data == "buy_pro_annual":
        duration = 12
    else:
        duration = int(callback.data.split("_")[-1])
    
    # Создаем счет для оплаты
    result = await payment_service.create_subscription_payment(
        callback.from_user.id, 
        "pro", 
        duration
    )
    
    if result["success"]:
        await callback.message.edit_text(
            "💳 **Счет создан!**\n\n"
            f"📦 Товар: Pro подписка ({duration} мес.)\n"
            f"💰 Сумма: {result['amount']} ₽\n\n"
            "🔒 Оплата проходит через защищенный Telegram Payments\n"
            "✅ Подписка активируется автоматически после оплаты",
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            f"❌ Ошибка создания счета:\n{result['error']}\n\n"
            "Попробуйте позже или обратитесь в поддержку.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Попробовать снова", callback_data="show_paywall")]
            ])
        )

@payments_router.callback_query(F.data == "stars_options")
@error_handler
async def stars_options_handler(callback: CallbackQuery):
    """Показывает варианты покупок за Stars"""
    await callback.answer()
    
    keyboard = payment_service.get_stars_keyboard()
    
    await callback.message.edit_text(
        "⭐ **Покупки за Stars**\n\n"
        "🌟 Stars — внутренняя валюта Telegram\n"
        "💫 Покупайте только нужные функции\n"
        "🚀 Мгновенная активация\n\n"
        "**Доступные покупки:**\n"
        "💫 **+10 анализов** — дополнительные фото\n"
        "🍽️ **Мульти-тарелка 24ч** — несколько блюд на фото\n"
        "📄 **PDF отчет** — красивый отчет за неделю",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@payments_router.callback_query(F.data.startswith("buy_stars_"))
@error_handler
async def buy_stars_handler(callback: CallbackQuery):
    """Обработчик покупок за Stars"""
    await callback.answer()
    
    # Извлекаем продукт из callback_data
    product = callback.data.replace("buy_stars_", "")
    
    # Пока Telegram Stars API недоступен, показываем заглушку
    pricing = subscription_service.get_pricing_info()
    price = pricing["stars"].get(product, 0)
    
    product_names = {
        "extra_10_analyses": "💫 +10 дополнительных анализов",
        "multi_dish_24h": "🍽️ Мульти-тарелка на 24 часа",  
        "pdf_report": "📄 PDF отчет за неделю"
    }
    
    product_name = product_names.get(product, "Неизвестный товар")
    
    # Создаем реальный счет за Stars
    result = await payment_service.create_stars_payment_invoice(
        callback.from_user.id, 
        product, 
        price
    )
    
    if result["success"]:
        await callback.message.edit_text(
            f"⭐ **Покупка за Stars**\n\n"
            f"🛒 Товар: {product_name}\n"
            f"💰 Цена: {price} Stars\n\n"
            f"✅ Счет создан! Проверьте сообщения выше для оплаты.",
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            f"❌ **Ошибка создания счета**\n\n"
            f"Не удалось создать счет для покупки {product_name}.\n\n"
            f"💳 Попробуйте обычную подписку Pro:",
            parse_mode="Markdown",
            reply_markup=payment_service.get_subscription_keyboard("lite")
        )

@payments_router.callback_query(F.data == "back_to_subscriptions")
@error_handler
async def back_to_subscriptions_handler(callback: CallbackQuery):
    """Возврат к вариантам подписки"""
    await callback.answer()
    
    await show_paywall(
        callback.message,
        title="🌟 Выберите подписку",
        description="Разблокируйте все возможности Pro:",
        features=[
            "• До 200 фото в месяц",
            "• Мульти-тарелка",
            "• Витамины и микроэлементы",
            "• Экспорт в PDF/CSV", 
            "• Google Calendar",
            "• Полные отчеты"
        ]
    )

@payments_router.callback_query(F.data == "show_status")
@error_handler
async def show_status_handler(callback: CallbackQuery):
    """Показать статус подписки через callback"""
    await callback.answer()
    
    # Импортируем обработчик из handlers.py
    from handlers import status_handler
    await status_handler(callback.message)

@payments_router.callback_query(F.data == "cancel_payment")
@error_handler
async def cancel_payment_handler(callback: CallbackQuery):
    """Отмена платежа"""
    await callback.answer()
    
    await callback.message.edit_text(
        "❌ **Покупка отменена**\n\n"
        "📸 Можете продолжить использовать бесплатный план Lite\n"
        "🌟 Или вернуться к выбору подписки через команду /pro",
        parse_mode="Markdown"
    )

@payments_router.pre_checkout_query()
@error_handler
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    """Обработка предварительной проверки платежа"""
    try:
        # Здесь можно добавить дополнительные проверки
        await pre_checkout_query.answer(ok=True)
        logger.info(f"Pre-checkout OK для пользователя {pre_checkout_query.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка pre-checkout: {e}")
        await pre_checkout_query.answer(
            ok=False, 
            error_message="Произошла ошибка. Попробуйте позже."
        )

@payments_router.message(F.successful_payment)
@error_handler
async def successful_payment_handler(message: Message):
    """Обработка успешного платежа"""
    try:
        payment_info = {
            'invoice_payload': message.successful_payment.invoice_payload,
            'total_amount': message.successful_payment.total_amount,
            'telegram_payment_charge_id': message.successful_payment.telegram_payment_charge_id,
            'provider_payment_charge_id': message.successful_payment.provider_payment_charge_id,
        }
        
        success = await payment_service.process_successful_payment(payment_info)
        
        if not success:
            await message.answer(
                "❌ Произошла ошибка при обработке платежа. "
                "Обратитесь в поддержку с ID платежа: "
                f"{payment_info['telegram_payment_charge_id']}"
            )
            
    except Exception as e:
        logger.error(f"Ошибка обработки успешного платежа: {e}")
        await message.answer(
            "❌ Произошла ошибка при обработке платежа. "
            "Обратитесь в поддержку."
        )
