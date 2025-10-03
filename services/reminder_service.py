import logging
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional
from enum import Enum
from services.firebase_service import FirebaseService
from services.subscription_service import SubscriptionService
from services.personal_goals_service import PersonalGoalsService

logger = logging.getLogger(__name__)

class ReminderType(Enum):
    WATER = "water"
    MEAL = "meal"
    CALORIE_LIMIT = "calorie_limit"
    GOAL_PROGRESS = "goal_progress"
    MOTIVATION = "motivation"

class ReminderService:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.subscription_service = SubscriptionService()
        self.personal_goals_service = PersonalGoalsService()
        
        # Настройки напоминаний
        self.REMINDER_TIMES = {
            ReminderType.WATER: [9, 12, 15, 18, 21],  # Часы для напоминаний о воде
            ReminderType.MEAL: [8, 13, 19],  # Часы для напоминаний о еде
            ReminderType.CALORIE_LIMIT: [20],  # Вечернее напоминание о лимите калорий
            ReminderType.GOAL_PROGRESS: [22],  # Вечерний отчет о прогрессе
            ReminderType.MOTIVATION: [7, 19]  # Утренняя и вечерняя мотивация
        }
        
        # Шаблоны сообщений
        self.MESSAGE_TEMPLATES = {
            ReminderType.WATER: [
                "💧 **Время пить воду!**\n\nВыпейте стакан воды для поддержания водного баланса.",
                "🚰 **Напоминание о воде**\n\nНе забывайте пить воду в течение дня!",
                "💦 **Водный баланс**\n\nСтакан воды поможет вам чувствовать себя лучше."
            ],
            ReminderType.MEAL: [
                "🍽️ **Время обеда!**\n\nНе забудьте проанализировать ваш обед через бота.",
                "🥗 **Время ужина**\n\nОтправьте фото ужина для анализа КБЖУ.",
                "🌅 **Время завтрака**\n\nНачните день с анализа завтрака!"
            ],
            ReminderType.CALORIE_LIMIT: [
                "📊 **Проверьте калории**\n\nПосмотрите, сколько калорий вы употребили сегодня.",
                "⚖️ **Баланс калорий**\n\nОсталось ли место для вечернего перекуса?",
                "🎯 **Цель на день**\n\nВы на правильном пути к вашей цели?"
            ],
            ReminderType.GOAL_PROGRESS: [
                "📈 **Прогресс за день**\n\nПосмотрите, как вы продвинулись к цели сегодня.",
                "🎯 **Итоги дня**\n\nКоманда /day покажет ваш прогресс.",
                "💪 **Мотивация**\n\nКаждый день приближает вас к цели!"
            ],
            ReminderType.MOTIVATION: [
                "🌅 **Доброе утро!**\n\nСегодня отличный день для работы над вашими целями!",
                "🌙 **Добрый вечер**\n\nГордитесь тем, что сделали для своего здоровья сегодня!",
                "💪 **Мотивация**\n\nПомните: каждый шаг к здоровому питанию важен!"
            ]
        }

    async def get_user_reminders(self, user_id: int) -> Dict:
        """Получает настройки напоминаний пользователя"""
        try:
            user_data = await self.firebase_service.get_user_info(user_id)
            reminders = user_data.get('reminders', {})
            
            # Устанавливаем значения по умолчанию
            default_reminders = {
                'water_reminders': True,
                'meal_reminders': True,
                'calorie_reminders': True,
                'progress_reminders': True,
                'motivation_reminders': True,
                'reminder_timezone': 'UTC',
                'last_reminder_sent': None
            }
            
            # Объединяем с пользовательскими настройками
            for key, value in default_reminders.items():
                if key not in reminders:
                    reminders[key] = value
            
            return reminders
            
        except Exception as e:
            logger.error(f"Ошибка получения напоминаний пользователя {user_id}: {e}")
            return {
                'water_reminders': True,
                'meal_reminders': True,
                'calorie_reminders': True,
                'progress_reminders': True,
                'motivation_reminders': True,
                'reminder_timezone': 'UTC',
                'last_reminder_sent': None
            }

    async def update_user_reminders(self, user_id: int, reminder_settings: Dict) -> bool:
        """Обновляет настройки напоминаний пользователя"""
        try:
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_ref.set({
                'reminders': reminder_settings
            }, merge=True)
            
            logger.info(f"Настройки напоминаний обновлены для пользователя {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка обновления напоминаний: {e}")
            return False

    async def should_send_reminder(self, user_id: int, reminder_type: ReminderType) -> bool:
        """Проверяет, нужно ли отправить напоминание"""
        try:
            # Проверяем подписку (исключение для водных напоминаний - отправляем всем)
            if reminder_type != ReminderType.WATER:
                subscription = await self.subscription_service.get_user_subscription(user_id)
                if subscription.get('type') == 'lite':
                    return False
            
            # Получаем настройки пользователя
            reminders = await self.get_user_reminders(user_id)
            
            # Проверяем, включены ли напоминания этого типа
            reminder_key = f"{reminder_type.value}_reminders"
            if not reminders.get(reminder_key, True):
                return False
            
            # Проверяем время последнего напоминания
            last_sent = reminders.get('last_reminder_sent')
            if last_sent:
                last_sent_time = datetime.fromisoformat(last_sent) if isinstance(last_sent, str) else last_sent
                # Не отправляем чаще чем раз в час
                if datetime.now() - last_sent_time < timedelta(hours=1):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка проверки напоминания: {e}")
            return False

    async def generate_reminder_message(self, user_id: int, reminder_type: ReminderType) -> str:
        """Генерирует сообщение напоминания"""
        try:
            templates = self.MESSAGE_TEMPLATES[reminder_type]
            import random
            base_message = random.choice(templates)
            
            # Персонализируем сообщение
            if reminder_type == ReminderType.CALORIE_LIMIT:
                # Добавляем информацию о текущих калориях
                today = datetime.now().strftime('%Y-%m-%d')
                analyses = await self.firebase_service.get_daily_analyses(user_id, today)
                
                if analyses:
                    daily_nutrition = await self.firebase_service.aggregate_daily_nutrition(analyses)
                    current_calories = daily_nutrition.get('calories', 0)
                    
                    # Получаем цель пользователя
                    goal = await self.personal_goals_service.get_user_goal(user_id)
                    if goal:
                        daily_target = goal.get('daily_calories', 2000)
                        remaining = daily_target - current_calories
                        
                        if remaining > 0:
                            base_message += f"\n\n📊 **Сегодня:** {current_calories} ккал из {daily_target}\n"
                            base_message += f"🍽️ **Осталось:** {remaining} ккал"
                        else:
                            base_message += f"\n\n📊 **Сегодня:** {current_calories} ккал из {daily_target}\n"
                            base_message += f"⚠️ **Превышение:** {abs(remaining)} ккал"
            
            elif reminder_type == ReminderType.GOAL_PROGRESS:
                # Добавляем информацию о прогрессе
                goal = await self.personal_goals_service.get_user_goal(user_id)
                if goal:
                    goal_type_names = {
                        "weight_loss": "📉 Похудение",
                        "weight_gain": "📈 Набор веса", 
                        "maintenance": "⚖️ Поддержание веса",
                        "muscle_gain": "💪 Набор мышц",
                        "health_improvement": "🏥 Улучшение здоровья"
                    }
                    goal_name = goal_type_names.get(goal['goal_type'], goal['goal_type'])
                    base_message += f"\n\n🎯 **Ваша цель:** {goal_name}"
            
            return base_message
            
        except Exception as e:
            logger.error(f"Ошибка генерации напоминания: {e}")
            return self.MESSAGE_TEMPLATES[reminder_type][0]

    async def send_reminder(self, bot, user_id: int, reminder_type: ReminderType) -> bool:
        """Отправляет напоминание пользователю"""
        try:
            if not await self.should_send_reminder(user_id, reminder_type):
                return False
            
            message = await self.generate_reminder_message(user_id, reminder_type)
            
            # Добавляем кнопки для быстрого доступа
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            
            keyboard_buttons = []
            
            if reminder_type == ReminderType.MEAL:
                keyboard_buttons.append([InlineKeyboardButton(text="📸 Анализ еды", callback_data="analyze_food")])
            elif reminder_type == ReminderType.CALORIE_LIMIT:
                keyboard_buttons.append([InlineKeyboardButton(text="📊 Итоги дня", callback_data="daily_summary")])
            elif reminder_type == ReminderType.GOAL_PROGRESS:
                keyboard_buttons.append([InlineKeyboardButton(text="🎯 Мои цели", callback_data="show_goals")])
            
            keyboard_buttons.append([InlineKeyboardButton(text="🔕 Отключить напоминания", callback_data="disable_reminders")])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            await bot.send_message(user_id, message, parse_mode="Markdown", reply_markup=keyboard)
            
            # Обновляем время последнего напоминания
            await self.update_last_reminder_time(user_id)
            
            logger.info(f"Напоминание {reminder_type.value} отправлено пользователю {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки напоминания: {e}")
            return False

    async def update_last_reminder_time(self, user_id: int):
        """Обновляет время последнего напоминания"""
        try:
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_ref.set({
                'reminders.last_reminder_sent': datetime.now()
            }, merge=True)
            
        except Exception as e:
            logger.error(f"Ошибка обновления времени напоминания: {e}")

    async def get_users_for_reminder(self, reminder_type: ReminderType, current_hour: int) -> List[int]:
        """Получает список пользователей для отправки напоминания"""
        try:
            # Проверяем, нужно ли отправлять напоминание в это время
            reminder_hours = self.REMINDER_TIMES.get(reminder_type, [])
            if current_hour not in reminder_hours:
                return []
            
            # Получаем всех пользователей
            users = await self.firebase_service.get_users_with_timezones()
            
            # Фильтруем пользователей по подписке и настройкам
            target_users = []
            for user in users:
                user_id = user['user_id']
                
                # Проверяем подписку (исключение для водных напоминаний - отправляем всем)
                if reminder_type != ReminderType.WATER:
                    subscription = await self.subscription_service.get_user_subscription(user_id)
                    if subscription.get('type') == 'lite':
                        continue
                
                # Проверяем настройки напоминаний
                reminders = await self.get_user_reminders(user_id)
                reminder_key = f"{reminder_type.value}_reminders"
                if not reminders.get(reminder_key, True):
                    continue
                
                target_users.append(user_id)
            
            return target_users
            
        except Exception as e:
            logger.error(f"Ошибка получения пользователей для напоминания: {e}")
            return []

    async def send_motivational_message(self, bot, user_id: int) -> bool:
        """Отправляет мотивационное сообщение"""
        try:
            # Проверяем подписку
            subscription = await self.subscription_service.get_user_subscription(user_id)
            if subscription.get('type') == 'lite':
                return False
            
            # Получаем данные пользователя
            goal = await self.personal_goals_service.get_user_goal(user_id)
            today = datetime.now().strftime('%Y-%m-%d')
            analyses = await self.firebase_service.get_daily_analyses(user_id, today)
            
            # Генерируем персонализированное мотивационное сообщение
            if goal and analyses:
                daily_nutrition = await self.firebase_service.aggregate_daily_nutrition(analyses)
                current_calories = daily_nutrition.get('calories', 0)
                daily_target = goal.get('daily_calories', 2000)
                
                goal_type_names = {
                    "weight_loss": "похудения",
                    "weight_gain": "набора веса", 
                    "maintenance": "поддержания веса",
                    "muscle_gain": "набора мышц",
                    "health_improvement": "улучшения здоровья"
                }
                goal_name = goal_type_names.get(goal['goal_type'], "вашей цели")
                
                if current_calories > 0:
                    accuracy = (current_calories / daily_target) * 100
                    
                    if accuracy >= 80 and accuracy <= 120:
                        message = f"🎉 **Отличная работа!**\n\n"
                        message += f"Вы на правильном пути к {goal_name}!\n"
                        message += f"📊 Сегодня: {current_calories} ккал из {daily_target}\n"
                        message += f"✅ Точность: {accuracy:.1f}%\n\n"
                        message += f"💪 Продолжайте в том же духе!"
                    elif accuracy < 80:
                        message = f"💪 **Не сдавайтесь!**\n\n"
                        message += f"Каждый день приближает вас к {goal_name}!\n"
                        message += f"📊 Сегодня: {current_calories} ккал из {daily_target}\n"
                        message += f"🍽️ Добавьте полезный перекус!\n\n"
                        message += f"🌟 Завтра будет лучше!"
                    else:
                        message = f"🎯 **Следите за балансом!**\n\n"
                        message += f"Вы близко к {goal_name}!\n"
                        message += f"📊 Сегодня: {current_calories} ккал из {daily_target}\n"
                        message += f"⚖️ Следите за порциями\n\n"
                        message += f"💡 Каждый день - это новый шанс!"
                else:
                    message = f"🌅 **Начните день правильно!**\n\n"
                    message += f"Проанализируйте завтрак для достижения {goal_name}!\n"
                    message += f"📸 Отправьте фото еды для начала дня!"
            else:
                message = f"💪 **Мотивация на день!**\n\n"
                message += f"Каждый шаг к здоровому питанию важен!\n"
                message += f"📸 Анализируйте еду и следите за прогрессом!"
            
            await bot.send_message(user_id, message, parse_mode="Markdown")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки мотивационного сообщения: {e}")
            return False
