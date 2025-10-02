import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from services.firebase_service import FirebaseService
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class GoalType(Enum):
    WEIGHT_LOSS = "weight_loss"
    WEIGHT_GAIN = "weight_gain" 
    MAINTENANCE = "maintenance"
    MUSCLE_GAIN = "muscle_gain"
    HEALTH_IMPROVEMENT = "health_improvement"

class PersonalGoalsService:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.gemini_service = GeminiService()
        
        # Базовые рекомендации по калориям в зависимости от цели
        self.GOAL_CALORIES = {
            GoalType.WEIGHT_LOSS: {
                "deficit": 500,  # дефицит калорий для похудения
                "protein_ratio": 0.25,  # 25% белка
                "fat_ratio": 0.25,     # 25% жиров
                "carbs_ratio": 0.50    # 50% углеводов
            },
            GoalType.WEIGHT_GAIN: {
                "surplus": 300,  # профицит калорий для набора веса
                "protein_ratio": 0.30,  # 30% белка
                "fat_ratio": 0.25,     # 25% жиров
                "carbs_ratio": 0.45    # 45% углеводов
            },
            GoalType.MAINTENANCE: {
                "deficit": 0,    # поддержание веса
                "protein_ratio": 0.25,  # 25% белка
                "fat_ratio": 0.30,     # 30% жиров
                "carbs_ratio": 0.45    # 45% углеводов
            },
            GoalType.MUSCLE_GAIN: {
                "surplus": 200,  # небольшой профицит для набора мышц
                "protein_ratio": 0.35,  # 35% белка
                "fat_ratio": 0.20,     # 20% жиров
                "carbs_ratio": 0.45    # 45% углеводов
            },
            GoalType.HEALTH_IMPROVEMENT: {
                "deficit": 0,    # фокус на качестве питания
                "protein_ratio": 0.25,  # 25% белка
                "fat_ratio": 0.30,     # 30% жиров
                "carbs_ratio": 0.45    # 45% углеводов
            }
        }

    async def set_user_goal(self, user_id: int, goal_type: str, target_weight: Optional[float] = None, 
                           current_weight: Optional[float] = None, height: Optional[float] = None,
                           age: Optional[int] = None, activity_level: str = "moderate") -> bool:
        """Устанавливает персональную цель пользователя"""
        try:
            # Валидируем тип цели
            try:
                goal_enum = GoalType(goal_type)
            except ValueError:
                logger.error(f"Неверный тип цели: {goal_type}")
                return False
            
            # Рассчитываем базовые потребности
            daily_calories = await self._calculate_daily_calories(
                current_weight, height, age, activity_level, goal_enum
            )
            
            goal_data = {
                'goal_type': goal_type,
                'target_weight': target_weight,
                'current_weight': current_weight,
                'height': height,
                'age': age,
                'activity_level': activity_level,
                'daily_calories': daily_calories,
                'goal_set_at': datetime.now(),
                'last_updated': datetime.now()
            }
            
            # Сохраняем в Firebase
            user_ref = self.firebase_service.db.collection('users').document(str(user_id))
            user_ref.set({
                'personal_goal': goal_data
            }, merge=True)
            
            logger.info(f"Установлена цель {goal_type} для пользователя {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка установки цели: {e}")
            return False

    async def _calculate_daily_calories(self, weight: Optional[float], height: Optional[float], 
                                      age: Optional[int], activity_level: str, goal_type: GoalType) -> int:
        """Рассчитывает дневную норму калорий"""
        try:
            if not all([weight, height, age]):
                # Возвращаем средние значения если данных нет
                base_calories = 2000
            else:
                # Формула Миффлина-Сан Жеора
                if weight and height and age:
                    # Мужская формула (упрощенная, предполагаем мужской пол)
                    bmr = 10 * weight + 6.25 * height - 5 * age + 5
                else:
                    bmr = 2000
                
                # Коэффициенты активности
                activity_multipliers = {
                    "sedentary": 1.2,    # малоподвижный
                    "light": 1.375,      # легкая активность
                    "moderate": 1.55,    # умеренная активность
                    "active": 1.725,     # высокая активность
                    "very_active": 1.9   # очень высокая активность
                }
                
                multiplier = activity_multipliers.get(activity_level, 1.55)
                base_calories = int(bmr * multiplier)
            
            # Применяем коррекцию в зависимости от цели
            goal_config = self.GOAL_CALORIES[goal_type]
            
            if goal_config.get('deficit', 0) > 0:
                daily_calories = base_calories - goal_config['deficit']
            elif goal_config.get('surplus', 0) > 0:
                daily_calories = base_calories + goal_config['surplus']
            else:
                daily_calories = base_calories
            
            return max(daily_calories, 1200)  # Минимум 1200 калорий
            
        except Exception as e:
            logger.error(f"Ошибка расчета калорий: {e}")
            return 2000

    async def get_user_goal(self, user_id: int) -> Optional[Dict]:
        """Получает персональную цель пользователя"""
        try:
            user_data = await self.firebase_service.get_user_info(user_id)
            return user_data.get('personal_goal')
        except Exception as e:
            logger.error(f"Ошибка получения цели: {e}")
            return None

    async def generate_smart_recommendations(self, user_id: int, daily_nutrition: Dict) -> str:
        """Генерирует умные рекомендации на основе цели и текущего питания"""
        try:
            goal = await self.get_user_goal(user_id)
            if not goal:
                return "🎯 Установите персональную цель для получения рекомендаций!"
            
            goal_type = GoalType(goal['goal_type'])
            daily_calories = goal.get('daily_calories', 2000)
            
            # Анализируем текущее питание
            current_calories = daily_nutrition.get('calories', 0)
            current_proteins = daily_nutrition.get('proteins', 0)
            current_fats = daily_nutrition.get('fats', 0)
            current_carbs = daily_nutrition.get('carbs', 0)
            
            recommendations = []
            
            # Анализ калорий
            calorie_diff = current_calories - daily_calories
            if abs(calorie_diff) > 200:
                if calorie_diff > 0:
                    recommendations.append(f"📉 Сегодня на {calorie_diff:.0f} ккал больше нормы. Рекомендую легкий ужин.")
                else:
                    recommendations.append(f"📈 Сегодня на {abs(calorie_diff):.0f} ккал меньше нормы. Добавьте полезный перекус.")
            
            # Анализ БЖУ
            goal_config = self.GOAL_CALORIES[goal_type]
            target_proteins = daily_calories * goal_config['protein_ratio'] / 4  # 4 ккал/г белка
            target_fats = daily_calories * goal_config['fat_ratio'] / 9  # 9 ккал/г жира
            target_carbs = daily_calories * goal_config['carbs_ratio'] / 4  # 4 ккал/г углеводов
            
            if current_proteins < target_proteins * 0.8:
                protein_diff = target_proteins - current_proteins
                recommendations.append(f"🥩 Мало белка! Добавьте {protein_diff:.0f}г белка: курица, творог, яйца.")
            
            if current_fats < target_fats * 0.7:
                fat_diff = target_fats - current_fats
                recommendations.append(f"🥑 Мало жиров! Добавьте {fat_diff:.0f}г: орехи, авокадо, оливковое масло.")
            
            if current_carbs < target_carbs * 0.8:
                carb_diff = target_carbs - current_carbs
                recommendations.append(f"🍞 Мало углеводов! Добавьте {carb_diff:.0f}г: крупы, фрукты, овощи.")
            
            # Специфичные рекомендации по цели
            if goal_type == GoalType.WEIGHT_LOSS:
                if current_calories > daily_calories:
                    recommendations.append("💪 Для похудения: больше белка, меньше простых углеводов.")
            elif goal_type == GoalType.MUSCLE_GAIN:
                if current_proteins < target_proteins:
                    recommendations.append("💪 Для набора мышц: увеличьте белок до 1.6-2г на кг веса.")
            
            # Генерируем ИИ рекомендации через Gemini
            ai_recommendations = await self._generate_ai_recommendations(
                goal_type, daily_nutrition, goal
            )
            
            if ai_recommendations:
                recommendations.append(ai_recommendations)
            
            if not recommendations:
                return "✅ Отличное питание! Вы на правильном пути к цели!"
            
            return "🤖 **Персональные рекомендации:**\n\n" + "\n".join(f"• {rec}" for rec in recommendations)
            
        except Exception as e:
            logger.error(f"Ошибка генерации рекомендаций: {e}")
            return "❌ Ошибка генерации рекомендаций. Попробуйте позже."

    async def _generate_ai_recommendations(self, goal_type: GoalType, nutrition: Dict, goal: Dict) -> str:
        """Генерирует рекомендации через ИИ"""
        try:
            prompt = f"""
Ты - персональный нутрициолог. Проанализируй питание пользователя и дай конкретные рекомендации.

Цель пользователя: {goal_type.value}
Текущее питание за день:
- Калории: {nutrition.get('calories', 0)}
- Белки: {nutrition.get('proteins', 0)}г
- Жиры: {nutrition.get('fats', 0)}г  
- Углеводы: {nutrition.get('carbs', 0)}г

Дневная норма калорий: {goal.get('daily_calories', 2000)}

Дай 1-2 конкретных совета по улучшению питания для достижения цели. 
Будь дружелюбным и мотивирующим. Используй эмодзи.
Максимум 2 предложения.
"""
            
            response = await self.gemini_service.generate_text(prompt)
            return response.strip()
            
        except Exception as e:
            logger.error(f"Ошибка генерации ИИ рекомендаций: {e}")
            return ""

    async def get_goal_progress(self, user_id: int, days: int = 7) -> Dict:
        """Получает прогресс по цели за период"""
        try:
            goal = await self.get_user_goal(user_id)
            if not goal:
                return {"error": "Цель не установлена"}
            
            # Получаем анализы за период
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            analyses = await self.firebase_service.get_weekly_analyses(
                user_id, start_date.strftime('%Y-%m-%d')
            )
            
            if not analyses:
                return {"error": "Нет данных за период"}
            
            # Агрегируем данные
            total_nutrition = await self.firebase_service.aggregate_daily_nutrition(analyses)
            
            # Рассчитываем средние показатели
            avg_calories = total_nutrition['calories'] / days
            avg_proteins = total_nutrition['proteins'] / days
            avg_fats = total_nutrition['fats'] / days
            avg_carbs = total_nutrition['carbs'] / days
            
            daily_target = goal.get('daily_calories', 2000)
            
            progress = {
                'period_days': days,
                'avg_calories': round(avg_calories, 0),
                'avg_proteins': round(avg_proteins, 1),
                'avg_fats': round(avg_fats, 1),
                'avg_carbs': round(avg_carbs, 1),
                'calorie_target': daily_target,
                'calorie_accuracy': round((avg_calories / daily_target) * 100, 1),
                'goal_type': goal['goal_type'],
                'analyses_count': len(analyses)
            }
            
            return progress
            
        except Exception as e:
            logger.error(f"Ошибка получения прогресса: {e}")
            return {"error": "Ошибка расчета прогресса"}

    async def can_use_personal_goals(self, user_id: int) -> Tuple[bool, str]:
        """Проверяет доступность персональных целей"""
        try:
            from services.subscription_service import SubscriptionService
            subscription_service = SubscriptionService()
            
            subscription = await subscription_service.get_user_subscription(user_id)
            subscription_type = subscription.get('type', 'lite')
            
            if subscription_type == 'lite':
                return False, "Персональные цели доступны только в Pro"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Ошибка проверки доступа к целям: {e}")
            return False, "Ошибка проверки доступа"
