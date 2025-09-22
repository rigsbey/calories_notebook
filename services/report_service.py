import logging
from datetime import datetime, timedelta
from typing import Dict, List
from services.firebase_service import FirebaseService
from utils import format_nutrition_info

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self):
        self.firebase = FirebaseService()
    
    async def generate_daily_report(self, user_id: int, date: str = None) -> str:
        """Генерирует дневной отчет"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Получаем анализы за день
            analyses = await self.firebase.get_daily_analyses(user_id, date)
            
            if not analyses:
                return f"📅 Итоги дня ({date})\n\n❌ За этот день не было записей о питании."
            
            # Агрегируем данные
            total_nutrition = await self.firebase.aggregate_daily_nutrition(analyses)
            
            # Формируем отчет
            report = self._format_daily_report(date, total_nutrition, len(analyses))
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
            # Получаем анализы за неделю
            analyses = await self.firebase.get_weekly_analyses(user_id, start_date)
            
            if not analyses:
                return f"📅 Итоги недели ({start_date})\n\n❌ За эту неделю не было записей о питании."
            
            # Агрегируем данные
            total_nutrition = await self.firebase.aggregate_daily_nutrition(analyses)
            
            # Формируем отчет
            report = self._format_weekly_report(start_date, total_nutrition, len(analyses))
            return report
            
        except Exception as e:
            logger.error(f"Ошибка генерации недельного отчета: {e}")
            return f"❌ Ошибка при генерации отчета за неделю {start_date}"
    
    def _format_daily_report(self, date: str, nutrition: Dict, analysis_count: int) -> str:
        """Форматирует дневной отчет"""
        # Нормы для взрослого человека (примерные)
        daily_norms = {
            'calories': 2200,
            'proteins': 120,
            'fats': 75,
            'carbs': 250
        }
        
        report = f"📅 Итоги дня ({date})\n"
        report += f"📊 Проанализировано приемов пищи: {analysis_count}\n\n"
        
        # КБЖУ
        report += "🔥 Калории: "
        report += f"{nutrition['calories']} ккал (из {daily_norms['calories']})\n"
        
        report += "🥩 Белки: "
        report += f"{nutrition['proteins']:.1f} г / {daily_norms['proteins']} г\n"
        
        report += "🥑 Жиры: "
        report += f"{nutrition['fats']:.1f} г / {daily_norms['fats']} г\n"
        
        report += "🌾 Углеводы: "
        report += f"{nutrition['carbs']:.1f} г / {daily_norms['carbs']} г\n\n"
        
        # Витамины
        if nutrition['vitamins']:
            report += "💊 Витамины и минералы:\n"
            for vitamin, percentage in nutrition['vitamins'].items():
                report += f"• {vitamin}: {percentage}%\n"
        else:
            report += "💊 Витамины: не указаны\n"
        
        return report
    
    def _format_weekly_report(self, start_date: str, nutrition: Dict, analysis_count: int) -> str:
        """Форматирует недельный отчет"""
        # Нормы для недели (умножаем на 7)
        weekly_norms = {
            'calories': 2200 * 7,
            'proteins': 120 * 7,
            'fats': 75 * 7,
            'carbs': 250 * 7
        }
        
        report = f"📅 Итоги недели ({start_date})\n"
        report += f"📊 Проанализировано приемов пищи: {analysis_count}\n\n"
        
        # КБЖУ
        report += "🔥 Калории: "
        report += f"{nutrition['calories']} ккал (из {weekly_norms['calories']})\n"
        
        report += "🥩 Белки: "
        report += f"{nutrition['proteins']:.1f} г / {weekly_norms['proteins']} г\n"
        
        report += "🥑 Жиры: "
        report += f"{nutrition['fats']:.1f} г / {weekly_norms['fats']} г\n"
        
        report += "🌾 Углеводы: "
        report += f"{nutrition['carbs']:.1f} г / {weekly_norms['carbs']} г\n\n"
        
        # Витамины
        if nutrition['vitamins']:
            report += "💊 Витамины и минералы:\n"
            for vitamin, percentage in nutrition['vitamins'].items():
                report += f"• {vitamin}: {percentage}%\n"
        else:
            report += "💊 Витамины: не указаны\n"
        
        return report
    
    async def send_daily_reports_to_all_users(self, bot):
        """Отправляет дневные отчеты всем пользователям"""
        try:
            users = await self.firebase.get_all_users()
            date = datetime.now().strftime('%Y-%m-%d')
            
            for user_id in users:
                try:
                    report = await self.generate_daily_report(user_id, date)
                    await bot.send_message(user_id, report)
                    logger.info(f"Отчет отправлен пользователю {user_id}")
                except Exception as e:
                    logger.error(f"Ошибка отправки отчета пользователю {user_id}: {e}")
            
            logger.info(f"Дневные отчеты отправлены {len(users)} пользователям")
            
        except Exception as e:
            logger.error(f"Ошибка отправки дневных отчетов: {e}")
