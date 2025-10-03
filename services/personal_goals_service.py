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
        
        # Детальная логика целей согласно новому плану
        self.GOAL_CONFIG = {
            GoalType.WEIGHT_LOSS: {
                "name": "📉 Похудение",
                "deficit_percent": 0.175,  # 17.5% дефицит (15-20% среднее)
                "protein_per_kg": 2.2,     # 2.2г белка на кг веса
                "fat_percent": 0.25,       # 25% жиров
                "carbs_percent": 0.35,     # 35% углеводов (меньше для дефицита)
                "description": "Дефицит калорий для здорового похудения",
                "free_features": [
                    "Расчет дневной нормы калорий",
                    "Отслеживание прогресса по калориям",
                    "Напоминания о норме"
                ],
                "premium_features": [
                    "ИИ-рекомендации по питанию",
                    "Советы как не срываться",
                    "Анализ недели (дефицит дней)",
                    "Персональные советы по белку"
                ]
            },
            GoalType.WEIGHT_GAIN: {
                "name": "📈 Набор веса", 
                "surplus_percent": 0.175,  # 17.5% профицит (15-20% среднее)
                "protein_per_kg": 1.8,     # 1.8г белка на кг веса
                "fat_percent": 0.30,       # 30% жиров (больше для калорийности)
                "carbs_percent": 0.50,     # 50% углеводов (больше для энергии)
                "description": "Профицит калорий для здорового набора веса",
                "free_features": [
                    "Расчет дневной нормы калорий",
                    "Отслеживание прогресса по калориям"
                ],
                "premium_features": [
                    "Советы по высококалорийным продуктам",
                    "Анализ недели (дни с профицитом)",
                    "График веса",
                    "Рекомендации по перекусам"
                ]
            },
            GoalType.MAINTENANCE: {
                "name": "⚖️ Поддержание веса",
                "deficit_percent": 0,      # без дефицита/профицита
                "surplus_percent": 0,
                "protein_per_kg": 1.6,     # 1.6г белка на кг веса
                "fat_percent": 0.30,       # 30% жиров
                "carbs_percent": 0.45,     # 45% углеводов
                "description": "Баланс калорий для поддержания веса",
                "free_features": [
                    "Расчет дневной нормы калорий",
                    "Отслеживание баланса калорий"
                ],
                "premium_features": [
                    "Анализ качества рациона",
                    "Отслеживание отклонений (±10%)",
                    "Советы по улучшению питания",
                    "Тренд стабильности веса"
                ]
            },
            GoalType.MUSCLE_GAIN: {
                "name": "💪 Набор мышц",
                "surplus_percent": 0.125,  # 12.5% профицит (10-15% среднее)
                "protein_per_kg": 2.0,     # 2г белка на кг веса
                "fat_percent": 0.25,       # 25% жиров
                "carbs_percent": 0.50,     # 50% углеводов (для энергии)
                "description": "Профицит калорий с акцентом на белки для роста мышц",
                "free_features": [
                    "Расчет дневной нормы калорий",
                    "Отслеживание белка"
                ],
                "premium_features": [
                    "Рекомендации по приемам пищи",
                    "Советы по питанию до/после тренировки",
                    "Отслеживание прогресса по белку",
                    "Корректировка под тренировки"
                ]
            },
            GoalType.HEALTH_IMPROVEMENT: {
                "name": "🏥 Улучшение здоровья",
                "deficit_percent": 0,      # без дефицита/профицита
                "surplus_percent": 0,
                "protein_per_kg": 1.6,     # 1.6г белка на кг веса
                "fat_percent": 0.30,       # 30% жиров
                "carbs_percent": 0.45,     # 45% углеводов
                "description": "Фокус на витаминах, минералах и качестве питания",
                "free_features": [
                    "Расчет дневной нормы калорий",
                    "Базовые витамины (C, кальций)"
                ],
                "premium_features": [
                    "Полный отчет по витаминам и минералам",
                    "Персональные советы по нутриентам",
                    "История нутриентов за неделю",
                    "Рекомендации по продуктам"
                ]
            }
        }

    async def set_user_goal(self, user_id: int, goal_type: str, target_weight: Optional[float] = None, 
                           current_weight: Optional[float] = None, height: Optional[float] = None,
                           age: Optional[int] = None, activity_level: str = "moderate", 
                           gender: str = "male") -> bool:
        """Устанавливает персональную цель пользователя"""
        try:
            # Валидируем тип цели
            try:
                goal_enum = GoalType(goal_type)
            except ValueError:
                logger.error(f"Неверный тип цели: {goal_type}")
                return False
            
            # Рассчитываем базовые потребности
            daily_calories, macro_nutrients = await self._calculate_daily_calories(
                current_weight, height, age, activity_level, goal_enum, gender
            )
            
            goal_config = self.GOAL_CONFIG[goal_enum]
            
            goal_data = {
                'goal_type': goal_type,
                'goal_name': goal_config['name'],
                'description': goal_config['description'],
                'target_weight': target_weight,
                'current_weight': current_weight,
                'height': height,
                'age': age,
                'gender': gender,
                'activity_level': activity_level,
                'daily_calories': daily_calories,
                'macro_nutrients': macro_nutrients,
                'free_features': goal_config['free_features'],
                'premium_features': goal_config['premium_features'],
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
                                      age: Optional[int], activity_level: str, goal_type: GoalType, 
                                      gender: str = "male") -> Tuple[int, Dict]:
        """Рассчитывает дневную норму калорий и БЖУ согласно новой логике"""
        try:
            if not all([weight, height, age]):
                # Возвращаем средние значения если данных нет
                tdee = 2000
            else:
                # Формула Миффлина-Сан Жеора
                if gender.lower() == "female":
                    bmr = 10 * weight + 6.25 * height - 5 * age - 161
                else:  # male
                    bmr = 10 * weight + 6.25 * height - 5 * age + 5
                
                # Коэффициенты активности
                activity_multipliers = {
                    "sedentary": 1.2,    # малоподвижный
                    "light": 1.375,      # легкая активность
                    "moderate": 1.55,    # умеренная активность
                    "active": 1.725,     # высокая активность
                    "very_active": 1.9   # очень высокая активность
                }
                
                multiplier = activity_multipliers.get(activity_level, 1.55)
                tdee = int(bmr * multiplier)
            
            # Применяем коррекцию в зависимости от цели
            goal_config = self.GOAL_CONFIG[goal_type]
            
            if goal_config.get('deficit_percent', 0) > 0:
                # Дефицит для похудения
                deficit = int(tdee * goal_config['deficit_percent'])
                daily_calories = tdee - deficit
            elif goal_config.get('surplus_percent', 0) > 0:
                # Профицит для набора веса/мышц
                surplus = int(tdee * goal_config['surplus_percent'])
                daily_calories = tdee + surplus
            else:
                # Поддержание веса
                daily_calories = tdee
            
            daily_calories = max(daily_calories, 1200)  # Минимум 1200 калорий
            
            # Рассчитываем БЖУ согласно цели
            target_proteins = weight * goal_config['protein_per_kg'] if weight else 120
            target_fats = daily_calories * goal_config['fat_percent'] / 9  # 9 ккал/г жира
            target_carbs = daily_calories * goal_config['carbs_percent'] / 4  # 4 ккал/г углеводов
            
            macro_nutrients = {
                'proteins': round(target_proteins, 1),
                'fats': round(target_fats, 1), 
                'carbs': round(target_carbs, 1)
            }
            
            return daily_calories, macro_nutrients
            
        except Exception as e:
            logger.error(f"Ошибка расчета калорий: {e}")
            return 2000, {'proteins': 120, 'fats': 67, 'carbs': 225}

    async def get_user_goal(self, user_id: int) -> Optional[Dict]:
        """Получает персональную цель пользователя"""
        try:
            user_data = await self.firebase_service.get_user_info(user_id)
            return user_data.get('personal_goal')
        except Exception as e:
            logger.error(f"Ошибка получения цели: {e}")
            return None

    async def generate_smart_recommendations(self, user_id: int, daily_nutrition: Dict, is_premium: bool = False) -> str:
        """Генерирует умные рекомендации на основе цели и текущего питания"""
        try:
            goal = await self.get_user_goal(user_id)
            if not goal:
                return "🎯 Установите персональную цель для получения рекомендаций!"
            
            goal_type = GoalType(goal['goal_type'])
            daily_calories = goal.get('daily_calories', 2000)
            macro_nutrients = goal.get('macro_nutrients', {})
            
            # Анализируем текущее питание
            current_calories = daily_nutrition.get('calories', 0)
            current_proteins = daily_nutrition.get('proteins', 0)
            current_fats = daily_nutrition.get('fats', 0)
            current_carbs = daily_nutrition.get('carbs', 0)
            
            recommendations = []
            
            # Базовые рекомендации (для всех пользователей)
            calorie_percent = (current_calories / daily_calories * 100) if daily_calories > 0 else 0
            
            if calorie_percent < 70:
                recommendations.append(f"📈 Вы на {calorie_percent:.0f}% от дневной нормы. Добавьте полезный перекус!")
            elif calorie_percent > 130:
                recommendations.append(f"📉 Вы превысили норму на {calorie_percent-100:.0f}%. Рекомендую легкий ужин.")
            
            # Premium рекомендации
            if is_premium:
                # Детальный анализ БЖУ
                target_proteins = macro_nutrients.get('proteins', 120)
                target_fats = macro_nutrients.get('fats', 67)
                target_carbs = macro_nutrients.get('carbs', 225)
                
                if current_proteins < target_proteins * 0.8:
                    protein_diff = target_proteins - current_proteins
                    recommendations.append(f"🥩 Мало белка! Добавьте {protein_diff:.0f}г: курица, творог, яйца.")
                
                # Специфичные рекомендации по цели
                if goal_type == GoalType.WEIGHT_LOSS:
                    if current_calories > daily_calories:
                        recommendations.append("💪 Для похудения: больше белка, меньше простых углеводов.")
                    recommendations.append("🧠 Совет: пейте воду перед едой, это поможет контролировать аппетит.")
                    
                elif goal_type == GoalType.WEIGHT_GAIN:
                    if current_calories < daily_calories * 0.9:
                        recommendations.append("🥜 Для набора веса: добавьте орехи, авокадо, оливковое масло.")
                        
                elif goal_type == GoalType.MUSCLE_GAIN:
                    if current_proteins < target_proteins:
                        recommendations.append("💪 Для набора мышц: белок после тренировки - ключ к росту!")
                        
                elif goal_type == GoalType.HEALTH_IMPROVEMENT:
                    recommendations.append("🥬 Фокус на витаминах: больше овощей и фруктов разных цветов.")
                    
                # ИИ рекомендации только для Premium
                ai_recommendations = await self._generate_ai_recommendations(
                    goal_type, daily_nutrition, goal
                )
                if ai_recommendations:
                    recommendations.append(ai_recommendations)
            else:
                # Базовая рекомендация для Free
                recommendations.append("⭐ В Pro версии: персональные советы ИИ и детальный анализ БЖУ!")
            
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

    async def get_goal_info(self, goal_type: str) -> Optional[Dict]:
        """Получает информацию о конкретной цели"""
        try:
            goal_enum = GoalType(goal_type)
            return self.GOAL_CONFIG.get(goal_enum)
        except ValueError:
            return None

    async def get_daily_progress_summary(self, user_id: int, daily_nutrition: Dict) -> str:
        """Генерирует краткую сводку прогресса за день"""
        try:
            goal = await self.get_user_goal(user_id)
            if not goal:
                return "🎯 Установите персональную цель для отслеживания прогресса!"
            
            daily_calories = goal.get('daily_calories', 2000)
            current_calories = daily_nutrition.get('calories', 0)
            calorie_percent = (current_calories / daily_calories * 100) if daily_calories > 0 else 0
            
            goal_name = goal.get('goal_name', 'Цель')
            
            if calorie_percent >= 90 and calorie_percent <= 110:
                status = "✅ Отлично!"
            elif calorie_percent < 70:
                status = f"📈 Недобор {100-calorie_percent:.0f}%"
            elif calorie_percent > 130:
                status = f"📉 Превышение {calorie_percent-100:.0f}%"
            else:
                status = "👍 Хорошо!"
            
            return f"🎯 **{goal_name}**\n📊 Прогресс: {calorie_percent:.0f}% ({current_calories}/{daily_calories} ккал)\n{status}"
            
        except Exception as e:
            logger.error(f"Ошибка генерации сводки: {e}")
            return "❌ Ошибка расчета прогресса"

    async def get_weekly_analysis(self, user_id: int, days: int = 7) -> Dict:
        """Анализирует недельный прогресс по цели"""
        try:
            goal = await self.get_user_goal(user_id)
            if not goal:
                return {"error": "Цель не установлена"}
            
            goal_type = GoalType(goal['goal_type'])
            goal_config = self.GOAL_CONFIG[goal_type]
            
            # Получаем данные за неделю
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            analyses = await self.firebase_service.get_weekly_analyses(
                user_id, start_date.strftime('%Y-%m-%d')
            )
            
            if not analyses:
                return {"error": "Нет данных за период"}
            
            # Анализируем прогресс по дням
            daily_target = goal.get('daily_calories', 2000)
            success_days = 0
            
            for analysis in analyses:
                daily_calories = analysis.get('calories', 0)
                if goal_type == GoalType.WEIGHT_LOSS:
                    # Для похудения считаем успешным день с дефицитом
                    if daily_calories <= daily_target:
                        success_days += 1
                elif goal_type in [GoalType.WEIGHT_GAIN, GoalType.MUSCLE_GAIN]:
                    # Для набора веса/мышц считаем успешным день с профицитом
                    if daily_calories >= daily_target:
                        success_days += 1
                else:
                    # Для поддержания и здоровья считаем успешным день в пределах ±10%
                    if 0.9 * daily_target <= daily_calories <= 1.1 * daily_target:
                        success_days += 1
            
            success_rate = (success_days / len(analyses)) * 100
            
            analysis = {
                'goal_name': goal_config['name'],
                'goal_type': goal_type.value,
                'period_days': len(analyses),
                'success_days': success_days,
                'success_rate': round(success_rate, 1),
                'daily_target': daily_target,
                'avg_calories': round(sum(a.get('calories', 0) for a in analyses) / len(analyses), 0)
            }
            
            # Добавляем специфичные метрики для каждой цели
            if goal_type == GoalType.WEIGHT_LOSS:
                analysis['deficit_days'] = success_days
                analysis['message'] = f"Вы были в дефиците {success_days} из {len(analyses)} дней"
            elif goal_type in [GoalType.WEIGHT_GAIN, GoalType.MUSCLE_GAIN]:
                analysis['surplus_days'] = success_days
                analysis['message'] = f"Вы добрали калории {success_days} из {len(analyses)} дней"
            else:
                analysis['balanced_days'] = success_days
                analysis['message'] = f"Вы держали баланс {success_days} из {len(analyses)} дней"
            
            return analysis
            
        except Exception as e:
            logger.error(f"Ошибка недельного анализа: {e}")
            return {"error": "Ошибка анализа"}
