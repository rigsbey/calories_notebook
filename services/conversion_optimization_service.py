import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from services.firebase_service import FirebaseService
from services.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)

class ConversionOptimizationService:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.subscription_service = SubscriptionService()
        
        # Триггеры конверсии
        self.CONVERSION_TRIGGERS = {
            "first_analysis": {
                "message": "🎉 **Первый анализ завершен!**\n\n✨ Понравился результат?",
                "cta": "🚀 Попробуйте Pro бесплатно 7 дней!",
                "features": ["• Детальные витамины", "• Мульти-тарелка", "• Экспорт отчетов"]
            },
            "limit_reached": {
                "message": "📊 **Дневной лимит исчерпан**\n\n😊 Вы уже проанализировали 5 фото сегодня!",
                "cta": "🌟 Pro снимет все ограничения!",
                "features": ["• До 200 фото в месяц", "• Мульти-тарелка", "• Персональные цели"]
            },
            "streak_motivation": {
                "message": "🔥 **Отличная серия!**\n\nВы анализируете еду уже несколько дней подряд!",
                "cta": "💪 Продолжайте с Pro!",
                "features": ["• Отслеживание прогресса", "• Умные рекомендации", "• Мотивация"]
            },
            "weekend_reminder": {
                "message": "📅 **Выходные - время для себя!**\n\nНе забывайте следить за питанием!",
                "cta": "🎯 Установите цель в Pro!",
                "features": ["• Персональные цели", "• Рекомендации ИИ", "• Прогресс"]
            }
        }

    async def get_user_conversion_context(self, user_id: int) -> Dict:
        """Получает контекст пользователя для персонализации конверсии"""
        try:
            # Получаем данные пользователя
            user_data = await self.firebase_service.get_user_info(user_id)
            subscription = await self.subscription_service.get_user_subscription(user_id)
            
            # Анализируем активность
            today = datetime.now().strftime('%Y-%m-%d')
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            today_analyses = await self.firebase_service.get_daily_analyses(user_id, today)
            week_analyses = await self.firebase_service.get_weekly_analyses(user_id, week_ago)
            
            # Подсчитываем серию дней
            streak_days = await self._calculate_streak_days(user_id)
            
            # Определяем лучший триггер
            best_trigger = await self._determine_best_trigger(
                user_id, subscription, len(today_analyses), len(week_analyses), streak_days
            )
            
            return {
                "user_id": user_id,
                "subscription_type": subscription.get('type', 'lite'),
                "daily_count": len(today_analyses),
                "weekly_count": len(week_analyses),
                "streak_days": streak_days,
                "best_trigger": best_trigger,
                "is_weekend": datetime.now().weekday() >= 5,
                "is_first_time": len(week_analyses) <= 1
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения контекста конверсии: {e}")
            return {
                "user_id": user_id,
                "subscription_type": "lite",
                "daily_count": 0,
                "weekly_count": 0,
                "streak_days": 0,
                "best_trigger": "first_analysis",
                "is_weekend": False,
                "is_first_time": True
            }

    async def _calculate_streak_days(self, user_id: int) -> int:
        """Подсчитывает количество дней подряд с анализами"""
        try:
            streak = 0
            current_date = datetime.now().date()
            
            for i in range(30):  # Проверяем последние 30 дней
                check_date = current_date - timedelta(days=i)
                analyses = await self.firebase_service.get_daily_analyses(
                    user_id, check_date.strftime('%Y-%m-%d')
                )
                
                if analyses:
                    streak += 1
                else:
                    break
            
            return streak
            
        except Exception as e:
            logger.error(f"Ошибка подсчета серии дней: {e}")
            return 0

    async def _determine_best_trigger(self, user_id: int, subscription: Dict, 
                                    daily_count: int, weekly_count: int, streak_days: int) -> str:
        """Определяет лучший триггер конверсии"""
        try:
            subscription_type = subscription.get('type', 'lite')
            
            # Если уже Pro, не показываем триггеры
            if subscription_type in ['pro', 'trial']:
                return "none"
            
            # Первый анализ - показываем вау-эффект
            if weekly_count <= 1:
                return "first_analysis"
            
            # Лимит исчерпан - показываем пейволл
            if daily_count >= 5:
                return "limit_reached"
            
            # Хорошая серия - мотивируем продолжать
            if streak_days >= 3:
                return "streak_motivation"
            
            # Выходные - напоминаем о целях
            if datetime.now().weekday() >= 5:
                return "weekend_reminder"
            
            # По умолчанию - первый анализ
            return "first_analysis"
            
        except Exception as e:
            logger.error(f"Ошибка определения триггера: {e}")
            return "first_analysis"

    async def generate_personalized_paywall(self, user_id: int) -> Dict:
        """Генерирует персонализированный пейволл"""
        try:
            context = await self.get_user_conversion_context(user_id)
            
            if context["best_trigger"] == "none":
                return None
            
            trigger_config = self.CONVERSION_TRIGGERS[context["best_trigger"]]
            
            # Персонализируем сообщение
            personalized_message = await self._personalize_message(trigger_config, context)
            
            return {
                "title": personalized_message["title"],
                "description": personalized_message["description"],
                "features": personalized_message["features"],
                "cta": personalized_message["cta"],
                "urgency": personalized_message.get("urgency", False),
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Ошибка генерации персонализированного пейволла: {e}")
            return None

    async def _personalize_message(self, trigger_config: Dict, context: Dict) -> Dict:
        """Персонализирует сообщение под контекст пользователя"""
        try:
            base_message = trigger_config["message"]
            base_cta = trigger_config["cta"]
            base_features = trigger_config["features"]
            
            # Персонализация в зависимости от контекста
            if context["best_trigger"] == "first_analysis":
                title = "🎉 Добро пожаловать!"
                description = f"{base_message}\n\n🌟 **Pro** откроет все возможности:"
                urgency = False
                
            elif context["best_trigger"] == "limit_reached":
                title = "📊 Лимит исчерпан"
                description = f"{base_message}\n\n⏰ Лимит сбросится завтра в 00:00\n\n🌟 **Pro** снимет все ограничения:"
                urgency = True
                
            elif context["best_trigger"] == "streak_motivation":
                title = "🔥 Отличная серия!"
                description = f"{base_message}\n\n📈 Уже {context['streak_days']} дней подряд!\n\n💪 **Pro** поможет достичь цели:"
                urgency = False
                
            elif context["best_trigger"] == "weekend_reminder":
                title = "📅 Выходные - время для себя!"
                description = f"{base_message}\n\n🎯 Не забывайте о здоровом питании!\n\n🌟 **Pro** добавит мотивации:"
                urgency = False
                
            else:
                title = "🌟 Обновиться до Pro?"
                description = f"{base_message}\n\n🌟 **Pro** откроет все возможности:"
                urgency = False
            
            # Добавляем персонализированные фичи
            personalized_features = base_features.copy()
            
            if context["streak_days"] >= 3:
                personalized_features.append("• Отслеживание прогресса")
            
            if context["weekly_count"] >= 5:
                personalized_features.append("• Экспорт отчетов")
            
            if context["is_weekend"]:
                personalized_features.append("• Мотивационные напоминания")
            
            return {
                "title": title,
                "description": description,
                "features": personalized_features,
                "cta": base_cta,
                "urgency": urgency
            }
            
        except Exception as e:
            logger.error(f"Ошибка персонализации сообщения: {e}")
            return {
                "title": "🌟 Обновиться до Pro?",
                "description": "Разблокируйте все возможности анализа питания:",
                "features": ["• До 200 фото в месяц", "• Мульти-тарелка", "• Персональные цели"],
                "cta": "🚀 Попробуйте Pro бесплатно!",
                "urgency": False
            }

    async def track_conversion_event(self, user_id: int, event_type: str, data: Dict = None):
        """Отслеживает события конверсии"""
        try:
            event_data = {
                "user_id": user_id,
                "event_type": event_type,
                "timestamp": datetime.now(),
                "data": data or {}
            }
            
            # Сохраняем в Firebase
            events_ref = self.firebase_service.db.collection('conversion_events')
            events_ref.add(event_data)
            
            logger.info(f"Событие конверсии отслежено: {event_type} для пользователя {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка отслеживания события конверсии: {e}")

    async def get_conversion_stats(self) -> Dict:
        """Получает статистику конверсии"""
        try:
            # Получаем события за последние 30 дней
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            events_ref = self.firebase_service.db.collection('conversion_events')
            query = events_ref.where('timestamp', '>=', thirty_days_ago)
            docs = query.stream()
            
            events = []
            for doc in docs:
                events.append(doc.to_dict())
            
            # Анализируем статистику
            total_events = len(events)
            unique_users = len(set(event['user_id'] for event in events))
            
            event_types = {}
            for event in events:
                event_type = event['event_type']
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            return {
                "period_days": 30,
                "total_events": total_events,
                "unique_users": unique_users,
                "event_types": event_types,
                "conversion_rate": unique_users / max(total_events, 1) * 100
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения статистики конверсии: {e}")
            return {
                "period_days": 30,
                "total_events": 0,
                "unique_users": 0,
                "event_types": {},
                "conversion_rate": 0
            }
