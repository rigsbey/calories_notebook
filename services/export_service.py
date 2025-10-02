import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import io
import csv
from services.firebase_service import FirebaseService
from services.personal_goals_service import PersonalGoalsService
from services.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)

class ExportService:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.personal_goals_service = PersonalGoalsService()
        self.subscription_service = SubscriptionService()

    async def can_use_export(self, user_id: int) -> tuple[bool, str]:
        """Проверяет доступность экспорта"""
        try:
            subscription = await self.subscription_service.get_user_subscription(user_id)
            subscription_type = subscription.get('type', 'lite')
            
            if subscription_type == 'lite':
                return False, "Экспорт отчетов доступен только в Pro"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Ошибка проверки доступа к экспорту: {e}")
            return False, "Ошибка проверки доступа"

    async def generate_csv_report(self, user_id: int, days: int = 7) -> Optional[io.StringIO]:
        """Генерирует CSV отчет за период"""
        try:
            # Получаем данные за период
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            analyses = await self.firebase_service.get_weekly_analyses(
                user_id, start_date.strftime('%Y-%m-%d')
            )
            
            if not analyses:
                return None
            
            # Создаем CSV в памяти
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Заголовки
            headers = [
                'Дата', 'Время', 'Вес (г)', 'Калории', 'Белки (г)', 
                'Жиры (г)', 'Углеводы (г)', 'Анализ текста'
            ]
            writer.writerow(headers)
            
            # Данные
            for analysis in analyses:
                nutrition = self.firebase_service.parse_nutrition_data(
                    analysis.get('analysis_text', '')
                )
                
                timestamp = analysis.get('timestamp', datetime.now())
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp)
                
                row = [
                    timestamp.strftime('%Y-%m-%d'),
                    timestamp.strftime('%H:%M:%S'),
                    analysis.get('weight', ''),
                    nutrition.get('calories', 0),
                    nutrition.get('proteins', 0),
                    nutrition.get('fats', 0),
                    nutrition.get('carbs', 0),
                    analysis.get('analysis_text', '').replace('\n', ' ').replace('\r', ' ')
                ]
                writer.writerow(row)
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Ошибка генерации CSV отчета: {e}")
            return None

    async def generate_pdf_report(self, user_id: int, days: int = 7) -> Optional[bytes]:
        """Генерирует PDF отчет за период"""
        try:
            # Для простоты используем HTML-шаблон, который можно конвертировать в PDF
            html_content = await self._generate_html_report(user_id, days)
            
            if not html_content:
                return None
            
            # В реальном проекте здесь был бы код для конвертации HTML в PDF
            # Например, используя wkhtmltopdf или reportlab
            # Пока возвращаем HTML как bytes для демонстрации
            return html_content.encode('utf-8')
            
        except Exception as e:
            logger.error(f"Ошибка генерации PDF отчета: {e}")
            return None

    async def _generate_html_report(self, user_id: int, days: int) -> Optional[str]:
        """Генерирует HTML отчет"""
        try:
            # Получаем данные пользователя
            user_data = await self.firebase_service.get_user_info(user_id)
            user_display = self._get_user_display_name(user_data, user_id)
            
            # Получаем цель пользователя
            goal = await self.personal_goals_service.get_user_goal(user_id)
            
            # Получаем данные за период
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            analyses = await self.firebase_service.get_weekly_analyses(
                user_id, start_date.strftime('%Y-%m-%d')
            )
            
            if not analyses:
                return None
            
            # Агрегируем данные
            total_nutrition = await self.firebase_service.aggregate_daily_nutrition(analyses)
            
            # Рассчитываем средние показатели
            avg_calories = total_nutrition['calories'] / days
            avg_proteins = total_nutrition['proteins'] / days
            avg_fats = total_nutrition['fats'] / days
            avg_carbs = total_nutrition['carbs'] / days
            
            # HTML шаблон
            html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Отчет о питании - {user_display}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f5f5f5;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        border-bottom: 2px solid #4CAF50;
                        padding-bottom: 20px;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        color: #4CAF50;
                        margin: 0;
                    }}
                    .info {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 20px;
                        margin-bottom: 30px;
                    }}
                    .info-item {{
                        background-color: #f9f9f9;
                        padding: 15px;
                        border-radius: 5px;
                    }}
                    .info-item h3 {{
                        margin: 0 0 10px 0;
                        color: #333;
                    }}
                    .nutrition {{
                        display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        gap: 20px;
                        margin-bottom: 30px;
                    }}
                    .nutrition-item {{
                        background-color: #e8f5e8;
                        padding: 15px;
                        border-radius: 5px;
                        text-align: center;
                    }}
                    .nutrition-item h3 {{
                        margin: 0 0 10px 0;
                        color: #4CAF50;
                    }}
                    .nutrition-value {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #2e7d32;
                    }}
                    .vitamins {{
                        margin-bottom: 30px;
                    }}
                    .vitamins h3 {{
                        color: #4CAF50;
                        border-bottom: 1px solid #4CAF50;
                        padding-bottom: 10px;
                    }}
                    .vitamin-list {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 10px;
                    }}
                    .vitamin-item {{
                        background-color: #fff3e0;
                        padding: 10px;
                        border-radius: 5px;
                        text-align: center;
                    }}
                    .footer {{
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                        border-top: 1px solid #ddd;
                        padding-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 Отчет о питании</h1>
                        <p>Период: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}</p>
                    </div>
                    
                    <div class="info">
                        <div class="info-item">
                            <h3>👤 Пользователь</h3>
                            <p>{user_display}</p>
                        </div>
                        <div class="info-item">
                            <h3>📅 Период</h3>
                            <p>{days} дней</p>
                        </div>
                    </div>
            """
            
            # Добавляем информацию о цели
            if goal:
                goal_type_names = {
                    "weight_loss": "📉 Похудение",
                    "weight_gain": "📈 Набор веса", 
                    "maintenance": "⚖️ Поддержание веса",
                    "muscle_gain": "💪 Набор мышц",
                    "health_improvement": "🏥 Улучшение здоровья"
                }
                goal_name = goal_type_names.get(goal['goal_type'], goal['goal_type'])
                daily_target = goal.get('daily_calories', 2000)
                
                html += f"""
                    <div class="info">
                        <div class="info-item">
                            <h3>🎯 Цель</h3>
                            <p>{goal_name}</p>
                        </div>
                        <div class="info-item">
                            <h3>📊 Дневная норма</h3>
                            <p>{daily_target} ккал</p>
                        </div>
                    </div>
                """
            
            # Добавляем данные о питании
            html += f"""
                    <div class="nutrition">
                        <div class="nutrition-item">
                            <h3>🔥 Калории</h3>
                            <div class="nutrition-value">{avg_calories:.0f}</div>
                            <p>ккал/день</p>
                        </div>
                        <div class="nutrition-item">
                            <h3>🥩 Белки</h3>
                            <div class="nutrition-value">{avg_proteins:.1f}</div>
                            <p>г/день</p>
                        </div>
                        <div class="nutrition-item">
                            <h3>🥑 Жиры</h3>
                            <div class="nutrition-value">{avg_fats:.1f}</div>
                            <p>г/день</p>
                        </div>
                        <div class="nutrition-item">
                            <h3>🌾 Углеводы</h3>
                            <div class="nutrition-value">{avg_carbs:.1f}</div>
                            <p>г/день</p>
                        </div>
                    </div>
            """
            
            # Добавляем витамины
            if total_nutrition['vitamins']:
                html += """
                    <div class="vitamins">
                        <h3>💊 Витамины и минералы</h3>
                        <div class="vitamin-list">
                """
                
                for vitamin, percentage in total_nutrition['vitamins'].items():
                    html += f"""
                            <div class="vitamin-item">
                                <strong>{vitamin}</strong><br>
                                {percentage}%
                            </div>
                    """
                
                html += """
                        </div>
                    </div>
                """
            
            # Добавляем статистику
            html += f"""
                    <div class="info">
                        <div class="info-item">
                            <h3>📊 Статистика</h3>
                            <p>Проанализировано приемов пищи: {len(analyses)}</p>
                            <p>Средне в день: {len(analyses)/days:.1f}</p>
                        </div>
                        <div class="info-item">
                            <h3>📈 Прогресс</h3>
                            <p>Отчет сгенерирован: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>Отчет сгенерирован ботом анализа питания</p>
                        <p>Для получения подробных рекомендаций используйте команду /recommendations</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            logger.error(f"Ошибка генерации HTML отчета: {e}")
            return None

    def _get_user_display_name(self, user_info: Dict, user_id: int) -> str:
        """Получает отображаемое имя пользователя"""
        if not user_info:
            return f"ID: {user_id}"
        
        if user_info.get('username'):
            return f"@{user_info['username']}"
        elif user_info.get('first_name'):
            name = user_info['first_name']
            if user_info.get('last_name'):
                name += f" {user_info['last_name']}"
            return name
        else:
            return f"ID: {user_id}"

    async def generate_shareable_link(self, user_id: int, report_type: str = "weekly") -> Optional[str]:
        """Генерирует ссылку для шаринга отчета"""
        try:
            # В реальном проекте здесь была бы генерация уникальной ссылки
            # и сохранение отчета в облачном хранилище
            # Пока возвращаем заглушку
            
            report_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Здесь должен быть код для:
            # 1. Генерации отчета
            # 2. Сохранения в облачное хранилище (S3, Google Drive, etc.)
            # 3. Создания публичной ссылки
            
            # Заглушка
            shareable_link = f"https://calories.toxiguard.site/reports/{report_id}"
            
            logger.info(f"Сгенерирована ссылка для шаринга: {shareable_link}")
            return shareable_link
            
        except Exception as e:
            logger.error(f"Ошибка генерации ссылки для шаринга: {e}")
            return None

    async def get_export_options(self, user_id: int) -> Dict:
        """Возвращает доступные варианты экспорта"""
        try:
            can_export, message = await self.can_use_export(user_id)
            
            if not can_export:
                return {
                    "available": False,
                    "message": message,
                    "options": []
                }
            
            return {
                "available": True,
                "message": "",
                "options": [
                    {
                        "type": "csv",
                        "name": "CSV файл",
                        "description": "Таблица с данными за период",
                        "icon": "📊"
                    },
                    {
                        "type": "pdf",
                        "name": "PDF отчет",
                        "description": "Красивый отчет с графиками",
                        "icon": "📄"
                    },
                    {
                        "type": "share",
                        "name": "Поделиться",
                        "description": "Ссылка для отправки врачу/тренеру",
                        "icon": "🔗"
                    }
                ]
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения вариантов экспорта: {e}")
            return {
                "available": False,
                "message": "Ошибка получения вариантов экспорта",
                "options": []
            }
