import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple
from enum import Enum
from firebase_admin import firestore
from services.firebase_service import FirebaseService

logger = logging.getLogger(__name__)

class SubscriptionType(Enum):
    LITE = "lite"
    TRIAL = "trial"
    PRO = "pro"

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class PaymentType(Enum):
    SUBSCRIPTION = "subscription"
    STARS = "stars"
    TRIAL = "trial"

class SubscriptionService:
    def __init__(self):
        self.firebase_service = FirebaseService()
        
        # Конфигурация тарифных планов
        self.PLAN_LIMITS = {
            SubscriptionType.LITE: {
                "daily_photos": 5,
                "monthly_photos": 5 * 30,  # грубая оценка
                "history_days": 7,
                "features": ["basic_analysis", "daily_report"],
                "multi_dish": False,
                "vitamins": False,
                "export": False,
                "calendar": False,
                "priority_queue": False
            },
            SubscriptionType.TRIAL: {
                "daily_photos": 200,
                "monthly_photos": 200,
                "history_days": -1,  # без ограничений
                "features": ["basic_analysis", "multi_dish", "vitamins", "smart_tips", 
                           "full_reports", "export", "calendar"],
                "multi_dish": True,
                "vitamins": True,
                "export": True,
                "calendar": True,
                "priority_queue": True
            },
            SubscriptionType.PRO: {
                "daily_photos": 200,
                "monthly_photos": 200,
                "history_days": -1,  # без ограничений
                "features": ["basic_analysis", "multi_dish", "vitamins", "smart_tips", 
                           "full_reports", "export", "calendar"],
                "multi_dish": True,
                "vitamins": True,
                "export": True,
                "calendar": True,
                "priority_queue": True
            }
        }
        
        # Цены в рублях
        self.PRICES = {
            "pro_monthly": 399,  # Адаптированная цена для СНГ
            "pro_quarterly": 999,  # 3 месяца
            "pro_yearly": 2990,  # Год со скидкой
        }
        
        # Цены в Stars
        self.STARS_PRICES = {
            "extra_10_analyses": 99,  # +10 анализов
            "multi_dish_24h": 149,   # Мульти-тарелка на 24ч  
            "pdf_report": 199,       # PDF отчет за неделю
        }

    async def get_user_subscription(self, user_id: int) -> Dict:
        """Получает информацию о подписке пользователя"""
        try:
            user_data = await self.firebase_service.get_user_info(user_id)
            
            # Инициализация подписки для новых пользователей
            if not user_data.get('subscription_type'):
                await self._init_user_subscription(user_id)
                user_data = await self.firebase_service.get_user_info(user_id)
            
            subscription = {
                'type': user_data.get('subscription_type', 'lite'),
                'status': user_data.get('subscription_status', 'active'),
                'end_date': user_data.get('subscription_end_date'),
                'daily_photo_count': user_data.get('daily_photo_count', 0),
                'monthly_photo_count': user_data.get('monthly_photo_count', 0),
                'last_reset_date': user_data.get('last_reset_date'),
            }
            
            # Проверяем актуальность подписки
            await self._validate_subscription_status(user_id, subscription)
            
            return subscription
            
        except Exception as e:
            logger.error(f"Ошибка получения подписки пользователя {user_id}: {e}")
            # Возвращаем базовую подписку в случае ошибки
            return {
                'type': 'lite',
                'status': 'active',
                'end_date': None,
                'daily_photo_count': 0,
                'monthly_photo_count': 0,
                'last_reset_date': None
            }

    async def _init_user_subscription(self, user_id: int):
        """Инициализирует подписку для нового пользователя"""
        try:
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            subscription_data = {
                'subscription_type': 'lite',
                'subscription_status': 'active',
                'subscription_end_date': None,
                'daily_photo_count': 0,
                'monthly_photo_count': 0,
                'last_reset_date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                'created_at': datetime.now(timezone.utc)
            }
            user_ref.set(subscription_data, merge=True)
            logger.info(f"Инициализирована подписка Lite для пользователя {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации подписки: {e}")

    async def _validate_subscription_status(self, user_id: int, subscription: Dict):
        """Валидирует статус подписки и обновляет при необходимости"""
        try:
            now = datetime.now(timezone.utc)
            
            # Проверяем истечение подписки
            if subscription.get('end_date'):
                end_date = subscription['end_date']
                if isinstance(end_date, str):
                    end_date = datetime.fromisoformat(end_date)
                
                # Убеждаемся, что end_date имеет timezone
                if end_date.tzinfo is None:
                    end_date = end_date.replace(tzinfo=timezone.utc)
                
                if end_date <= now and subscription['status'] == 'active':
                    # Подписка истекла, переводим на Lite
                    await self._downgrade_to_lite(user_id)
                    subscription['type'] = 'lite'
                    subscription['status'] = 'active'
            
            # Сброс дневных счетчиков
            last_reset = subscription.get('last_reset_date')
            if last_reset:
                if isinstance(last_reset, str):
                    last_reset_date = datetime.strptime(last_reset, '%Y-%m-%d').date()
                else:
                    last_reset_date = last_reset.date()
                
                if last_reset_date < now.date():
                    await self._reset_daily_counters(user_id)
            
        except Exception as e:
            logger.error(f"Ошибка валидации подписки: {e}")

    async def _reset_daily_counters(self, user_id: int):
        """Сбрасывает дневные счетчики"""
        try:
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_ref.update({
                'daily_photo_count': 0,
                'last_reset_date': datetime.now(timezone.utc).strftime('%Y-%m-%d')
            })
            logger.info(f"Сброшены дневные счетчики для пользователя {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка сброса счетчиков: {e}")

    async def _downgrade_to_lite(self, user_id: int):
        """Переводит пользователя на план Lite"""
        try:
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_ref.update({
                'subscription_type': 'lite',
                'subscription_status': 'active',
                'subscription_end_date': None,
            })
            logger.info(f"Пользователь {user_id} переведен на план Lite")
            
        except Exception as e:
            logger.error(f"Ошибка перевода на Lite: {e}")

    async def can_analyze_photo(self, user_id: int) -> Tuple[bool, str]:
        """Проверяет, может ли пользователь анализировать фото"""
        try:
            subscription = await self.get_user_subscription(user_id)
            subscription_type = SubscriptionType(subscription['type'])
            
            # Получаем лимиты для текущего тарифа
            limits = self.PLAN_LIMITS[subscription_type]
            daily_count = subscription['daily_photo_count']
            
            if daily_count >= limits['daily_photos']:
                return False, f"Достигнут дневной лимит ({limits['daily_photos']} фото/день)"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Ошибка проверки лимитов: {e}")
            return False, "Ошибка проверки лимитов"

    async def increment_photo_count(self, user_id: int) -> bool:
        """Увеличивает счетчик анализов фото"""
        try:
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_ref.update({
                'daily_photo_count': firestore.Increment(1),
                'monthly_photo_count': firestore.Increment(1),
            })
            return True
            
        except Exception as e:
            logger.error(f"Ошибка обновления счетчиков: {e}")
            return False

    async def can_use_feature(self, user_id: int, feature: str) -> Tuple[bool, str]:
        """Проверяет доступность конкретной функции"""
        try:
            subscription = await self.get_user_subscription(user_id)
            subscription_type = SubscriptionType(subscription['type'])
            
            limits = self.PLAN_LIMITS[subscription_type]
            
            if feature == "multi_dish":
                if not limits['multi_dish']:
                    return False, "Мульти-тарелка доступна только в Pro"
                    
            elif feature == "export":
                if not limits['export']:
                    return False, "Экспорт доступен только в Pro"
                    
            elif feature == "calendar":
                if not limits['calendar']:
                    return False, "Синхронизация с календарем доступна в Pro"
                    
            elif feature == "vitamins":
                if not limits['vitamins']:
                    return False, "Подробная информация о витаминах в Pro"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Ошибка проверки функции {feature}: {e}")
            return False, "Ошибка проверки доступа"

    async def start_trial(self, user_id: int) -> bool:
        """Запускает 7-дневный триал Pro"""
        try:
            subscription = await self.get_user_subscription(user_id)
            
            # Проверяем, не использовал ли пользователь уже триал
            user_data = await self.firebase_service.get_user_info(user_id)
            if user_data.get('trial_used', False):
                return False
            
            # Устанавливаем триал на 7 дней
            end_date = datetime.now(timezone.utc) + timedelta(days=7)
            
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_ref.update({
                'subscription_type': 'trial',
                'subscription_status': 'active',
                'subscription_end_date': end_date,
                'trial_used': True,
                'trial_start_date': datetime.now(timezone.utc)
            })
            
            logger.info(f"Запущен триал для пользователя {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка запуска триала: {e}")
            return False

    async def activate_pro_subscription(self, user_id: int, duration_months: int) -> bool:
        """Активирует Pro подписку"""
        try:
            end_date = datetime.now(timezone.utc) + timedelta(days=30 * duration_months)
            
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_ref.update({
                'subscription_type': 'pro',
                'subscription_status': 'active',
                'subscription_end_date': end_date,
                'pro_activated_at': datetime.now(timezone.utc)
            })
            
            logger.info(f"Активирована Pro подписка на {duration_months} мес. для пользователя {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка активации Pro: {e}")
            return False

    async def add_stars_analyses(self, user_id: int, count: int) -> bool:
        """Добавляет дополнительные анализы за Stars"""
        try:
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_data = await self.firebase_service.get_user_info(user_id)
            
            current_bonus = user_data.get('bonus_analyses', 0)
            user_ref.update({
                'bonus_analyses': current_bonus + count,
                'last_stars_purchase': datetime.now(timezone.utc)
            })
            
            logger.info(f"Добавлено {count} бонусных анализов для пользователя {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка добавления бонусных анализов: {e}")
            return False

    async def save_payment(self, payment_data: Dict) -> bool:
        """Сохраняет информацию о платеже"""
        try:
            payments_ref = self.firebase_service.db.collection('payments')
            payment_data['created_at'] = datetime.now(timezone.utc)
            payments_ref.add(payment_data)
            
            logger.info(f"Сохранен платеж для пользователя {payment_data.get('user_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сохранения платежа: {e}")
            return False

    def get_plan_limits(self, subscription_type: str) -> Dict:
        """Возвращает лимиты для указанного плана"""
        try:
            sub_type = SubscriptionType(subscription_type)
            return self.PLAN_LIMITS[sub_type]
        except (ValueError, KeyError):
            return self.PLAN_LIMITS[SubscriptionType.LITE]

    def get_pricing_info(self) -> Dict:
        """Возвращает информацию о ценах"""
        return {
            "subscriptions": self.PRICES,
            "stars": self.STARS_PRICES
        }

    async def get_daily_photo_count(self, user_id: int) -> int:
        """Получает количество фото, проанализированных сегодня"""
        try:
            subscription = await self.get_user_subscription(user_id)
            return subscription.get('daily_photo_count', 0)
        except Exception as e:
            logger.error(f"Ошибка получения дневного счетчика: {e}")
            return 0
