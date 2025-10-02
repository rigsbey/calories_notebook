import logging
from datetime import datetime, timedelta
from typing import Dict, List
from services.firebase_service import FirebaseService
from services.personal_goals_service import PersonalGoalsService
from utils import format_nutrition_info

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self):
        self.firebase = FirebaseService()
        self.personal_goals = PersonalGoalsService()
    
    async def generate_daily_report(self, user_id: int, date: str = None) -> str:
        """Генерирует дневной отчет"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Получаем информацию о пользователе
            user_info = await self.firebase.get_user_info(user_id)
            user_display = self._get_user_display_name(user_info, user_id)
            
            # Получаем анализы за день
            analyses = await self.firebase.get_daily_analyses(user_id, date)
            
            if not analyses:
                return f"📅 Итоги дня ({date})\n👤 {user_display}\n\n❌ За этот день не было записей о питании."
            
            # Агрегируем данные
            total_nutrition = await self.firebase.aggregate_daily_nutrition(analyses)
            
            # Формируем отчет
            report = await self._format_daily_report(user_id, date, total_nutrition, len(analyses), user_display)
            return report
            
        except Exception as e:
            logger.error(f"Ошибка генерации дневного отчета: {e}")
            return f"❌ Ошибка при генерации отчета за {date}"
    
    async def generate_weekly_report(self, user_id: int, start_date: str = None) -> str:
        """Генерирует недельный отчет"""
        if not start_date:
            # Начинаем с понедельника текущей недели
            today = datetime.now()
            start_date = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
        
        try:
            # Получаем информацию о пользователе
            user_info = await self.firebase.get_user_info(user_id)
            user_display = self._get_user_display_name(user_info, user_id)
            
            # Получаем анализы за неделю
            analyses = await self.firebase.get_weekly_analyses(user_id, start_date)
            
            if not analyses:
                return f"📅 Итоги недели ({start_date})\n👤 {user_display}\n\n❌ За эту неделю не было записей о питании."
            
            # Агрегируем данные
            total_nutrition = await self.firebase.aggregate_daily_nutrition(analyses)
            
            # Формируем отчет
            report = await self._format_weekly_report(user_id, start_date, total_nutrition, len(analyses), user_display)
            return report
            
        except Exception as e:
            logger.error(f"Ошибка генерации недельного отчета: {e}")
            return f"❌ Ошибка при генерации отчета за неделю {start_date}"
    
    def _get_user_display_name(self, user_info: Dict, user_id: int) -> str:
        """Получает отображаемое имя пользователя"""
        if not user_info:
            return f"ID: {user_id}"
        
        # Приоритет: username -> first_name -> user_id
        if user_info.get('username'):
            return f"@{user_info['username']}"
        elif user_info.get('first_name'):
            name = user_info['first_name']
            if user_info.get('last_name'):
                name += f" {user_info['last_name']}"
            return name
        else:
            return f"ID: {user_id}"
    
    async def _format_daily_report(self, user_id: int, date: str, nutrition: Dict, analysis_count: int, user_display: str = None) -> str:
        """Форматирует дневной отчет"""
        # Получаем персональную цель пользователя
        goal = await self.personal_goals.get_user_goal(user_id)
        
        if goal:
            # Используем персональные нормы
            daily_calories = goal.get('daily_calories', 2200)
            goal_type_names = {
                "weight_loss": "📉 Похудение",
                "weight_gain": "📈 Набор веса", 
                "maintenance": "⚖️ Поддержание веса",
                "muscle_gain": "💪 Набор мышц",
                "health_improvement": "🏥 Улучшение здоровья"
            }
            goal_name = goal_type_names.get(goal['goal_type'], goal['goal_type'])
        else:
            # Стандартные нормы
            daily_calories = 2200
            goal_name = None
        
        # Рассчитываем нормы БЖУ
        protein_ratio = 0.25 if not goal else 0.25  # Можно настроить под цель
        fat_ratio = 0.30 if not goal else 0.30
        carb_ratio = 0.45 if not goal else 0.45
        
        daily_proteins = daily_calories * protein_ratio / 4  # 4 ккал/г белка
        daily_fats = daily_calories * fat_ratio / 9  # 9 ккал/г жира
        daily_carbs = daily_calories * carb_ratio / 4  # 4 ккал/г углеводов
        
        report = f"📅 Итоги дня ({date})\n"
        if user_display:
            report += f"👤 {user_display}\n"
        if goal_name:
            report += f"🎯 Цель: {goal_name}\n"
        report += f"📊 Проанализировано приемов пищи: {analysis_count}\n\n"
        
        # КБЖУ с персональными нормами
        report += "🔥 Калории: "
        report += f"{nutrition['calories']} ккал (из {daily_calories})\n"
        
        report += "🥩 Белки: "
        report += f"{nutrition['proteins']:.1f} г / {daily_proteins:.1f} г\n"
        
        report += "🥑 Жиры: "
        report += f"{nutrition['fats']:.1f} г / {daily_fats:.1f} г\n"
        
        report += "🌾 Углеводы: "
        report += f"{nutrition['carbs']:.1f} г / {daily_carbs:.1f} г\n\n"
        
        # Витамины
        if nutrition['vitamins']:
            report += "💊 Витамины и минералы:\n"
            for vitamin, percentage in nutrition['vitamins'].items():
                report += f"• {vitamin}: {percentage}%\n"
        else:
            report += "💊 Витамины: не указаны\n"
        
        # Добавляем персональные рекомендации для Pro пользователей
        try:
            from services.subscription_service import SubscriptionService
            subscription_service = SubscriptionService()
            subscription = await subscription_service.get_user_subscription(user_id)
            
            if subscription.get('type') in ['pro', 'trial'] and goal:
                recommendations = await self.personal_goals.generate_smart_recommendations(user_id, nutrition)
                if recommendations and "Ошибка" not in recommendations:
                    report += f"\n{recommendations}"
        except Exception as e:
            logger.warning(f"Не удалось добавить рекомендации в отчет: {e}")
        
        return report
    
    async def _format_weekly_report(self, user_id: int, start_date: str, nutrition: Dict, analysis_count: int, user_display: str = None) -> str:
        """Форматирует недельный отчет"""
        # Получаем персональную цель пользователя
        goal = await self.personal_goals.get_user_goal(user_id)
        
        if goal:
            # Используем персональные нормы
            daily_calories = goal.get('daily_calories', 2200)
            weekly_calories = daily_calories * 7
            goal_type_names = {
                "weight_loss": "📉 Похудение",
                "weight_gain": "📈 Набор веса", 
                "maintenance": "⚖️ Поддержание веса",
                "muscle_gain": "💪 Набор мышц",
                "health_improvement": "🏥 Улучшение здоровья"
            }
            goal_name = goal_type_names.get(goal['goal_type'], goal['goal_type'])
        else:
            # Стандартные нормы
            weekly_calories = 2200 * 7
            goal_name = None
        
        # Рассчитываем нормы БЖУ для недели
        protein_ratio = 0.25 if not goal else 0.25
        fat_ratio = 0.30 if not goal else 0.30
        carb_ratio = 0.45 if not goal else 0.45
        
        weekly_proteins = weekly_calories * protein_ratio / 4
        weekly_fats = weekly_calories * fat_ratio / 9
        weekly_carbs = weekly_calories * carb_ratio / 4
        
        report = f"📅 Итоги недели ({start_date})\n"
        if user_display:
            report += f"👤 {user_display}\n"
        if goal_name:
            report += f"🎯 Цель: {goal_name}\n"
        report += f"📊 Проанализировано приемов пищи: {analysis_count}\n\n"
        
        # КБЖУ с персональными нормами
        report += "🔥 Калории: "
        report += f"{nutrition['calories']} ккал (из {weekly_calories})\n"
        
        report += "🥩 Белки: "
        report += f"{nutrition['proteins']:.1f} г / {weekly_proteins:.1f} г\n"
        
        report += "🥑 Жиры: "
        report += f"{nutrition['fats']:.1f} г / {weekly_fats:.1f} г\n"
        
        report += "🌾 Углеводы: "
        report += f"{nutrition['carbs']:.1f} г / {weekly_carbs:.1f} г\n\n"
        
        # Витамины
        if nutrition['vitamins']:
            report += "💊 Витамины и минералы:\n"
            for vitamin, percentage in nutrition['vitamins'].items():
                report += f"• {vitamin}: {percentage}%\n"
        else:
            report += "💊 Витамины: не указаны\n"
        
        # Добавляем персональные рекомендации для Pro пользователей
        try:
            from services.subscription_service import SubscriptionService
            subscription_service = SubscriptionService()
            subscription = await subscription_service.get_user_subscription(user_id)
            
            if subscription.get('type') in ['pro', 'trial'] and goal:
                # Для недельного отчета показываем прогресс
                progress = await self.personal_goals.get_goal_progress(user_id, 7)
                if progress and 'error' not in progress:
                    avg_calories = progress.get('avg_calories', 0)
                    calorie_accuracy = progress.get('calorie_accuracy', 0)
                    
                    report += f"\n📊 **Прогресс за неделю:**\n"
                    report += f"• Средне калорий в день: {avg_calories:.0f}\n"
                    report += f"• Точность по калориям: {calorie_accuracy:.1f}%\n"
                    
                    if calorie_accuracy < 80:
                        report += f"💡 **Совет:** Старайтесь придерживаться дневной нормы калорий\n"
                    elif calorie_accuracy > 120:
                        report += f"💡 **Совет:** Следите за превышением калорий\n"
                    else:
                        report += f"✅ **Отлично!** Вы придерживаетесь нормы калорий\n"
        except Exception as e:
            logger.warning(f"Не удалось добавить прогресс в недельный отчет: {e}")
        
        return report
    
    async def send_daily_reports_to_all_users(self, bot):
        """Отправляет дневные отчеты всем пользователям"""
        try:
            users = await self.firebase.get_all_users()
            date = datetime.now().strftime('%Y-%m-%d')
            
            for user_id in users:
                try:
                    # Получаем информацию о пользователе для логирования
                    user_info = await self.firebase.get_user_info(user_id)
                    user_display = self._get_user_display_name(user_info, user_id)
                    
                    report = await self.generate_daily_report(user_id, date)
                    await bot.send_message(user_id, report)
                    logger.info(f"Отчет отправлен пользователю {user_display} (ID: {user_id})")
                except Exception as e:
                    logger.error(f"Ошибка отправки отчета пользователю {user_id}: {e}")
            
            logger.info(f"Дневные отчеты отправлены {len(users)} пользователям")
            
        except Exception as e:
            logger.error(f"Ошибка отправки дневных отчетов: {e}")
    
    async def send_daily_reports_to_users(self, bot, users):
        """Отправляет дневные отчеты конкретным пользователям"""
        try:
            date = datetime.now().strftime('%Y-%m-%d')
            
            for user in users:
                try:
                    user_id = user['user_id']
                    user_display = self._get_user_display_name(user, user_id)
                    
                    report = await self.generate_daily_report(user_id, date)
                    await bot.send_message(user_id, report)
                    logger.info(f"Отчет отправлен пользователю {user_display} (ID: {user_id})")
                except Exception as e:
                    logger.error(f"Ошибка отправки отчета пользователю {user_id}: {e}")
            
            logger.info(f"Дневные отчеты отправлены {len(users)} пользователям")
            
        except Exception as e:
            logger.error(f"Ошибка отправки дневных отчетов: {e}")


