import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
from config import FIREBASE_CREDENTIALS_PATH

logger = logging.getLogger(__name__)

class FirebaseService:
    def __init__(self):
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Инициализация Firebase"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            logger.info("Firebase инициализирован успешно")
        except Exception as e:
            logger.error(f"Ошибка инициализации Firebase: {e}")
            raise
    
    async def save_analysis(self, user_id: int, analysis_data: Dict) -> str:
        """Сохраняет анализ питания в Firestore и возвращает ID документа"""
        try:
            doc_ref = self.db.collection('users').document(str(user_id)).collection('analyses').document()
            analysis_data['timestamp'] = datetime.now()
            analysis_data['date'] = datetime.now().strftime('%Y-%m-%d')
            
            doc_ref.set(analysis_data)
            logger.info(f"Анализ сохранен для пользователя {user_id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Ошибка сохранения анализа: {e}")
            return None

    async def update_analysis(self, user_id: int, analysis_id: str, analysis_data: Dict) -> bool:
        """Обновляет существующий анализ"""
        try:
            doc_ref = self.db.collection('users').document(str(user_id)).collection('analyses').document(analysis_id)
            analysis_data['updated_at'] = datetime.now()
            
            doc_ref.update(analysis_data)
            logger.info(f"Анализ {analysis_id} обновлен для пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка обновления анализа: {e}")
            return False
    
    async def get_daily_analyses(self, user_id: int, date: str) -> List[Dict]:
        """Получает все анализы пользователя за день"""
        try:
            analyses_ref = self.db.collection('users').document(str(user_id)).collection('analyses')
            query = analyses_ref.where('date', '==', date)
            docs = query.stream()
            
            analyses = []
            for doc in docs:
                analysis = doc.to_dict()
                analysis['id'] = doc.id
                analyses.append(analysis)
            
            return analyses
        except Exception as e:
            logger.error(f"Ошибка получения анализов за день: {e}")
            return []
    
    async def get_weekly_analyses(self, user_id: int, start_date: str) -> List[Dict]:
        """Получает все анализы пользователя за неделю"""
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = start_dt + timedelta(days=7)
            
            analyses_ref = self.db.collection('users').document(str(user_id)).collection('analyses')
            query = analyses_ref.where('timestamp', '>=', start_dt).where('timestamp', '<', end_dt)
            docs = query.stream()
            
            analyses = []
            for doc in docs:
                analysis = doc.to_dict()
                analysis['id'] = doc.id
                analyses.append(analysis)
            
            return analyses
        except Exception as e:
            logger.error(f"Ошибка получения анализов за неделю: {e}")
            return []
    
    async def create_or_update_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None, timezone: str = None) -> bool:
        """Создает или обновляет данные пользователя в Firestore"""
        try:
            user_ref = self.db.collection('users').document(str(user_id))
            
            user_data = {
                'user_id': user_id,
                'created_at': datetime.now(),
                'last_activity': datetime.now()
            }
            
            if username:
                user_data['username'] = username
            if first_name:
                user_data['first_name'] = first_name
            if last_name:
                user_data['last_name'] = last_name
            if timezone:
                user_data['timezone'] = timezone
            
            # Используем merge=True чтобы не перезаписывать существующие данные
            user_ref.set(user_data, merge=True)
            logger.info(f"Пользователь {user_id} создан/обновлен с username: {username}, timezone: {timezone}")
            return True
        except Exception as e:
            logger.error(f"Ошибка создания/обновления пользователя: {e}")
            return False

    async def save_user_google_tokens(self, user_id: int, tokens: Dict) -> bool:
        """Сохраняет OAuth токены пользователя Google в Firestore"""
        try:
            user_ref = self.db.collection('users').document(str(user_id))
            data = {
                'google': {
                    'tokens': tokens,
                    'updated_at': datetime.now()
                }
            }
            user_ref.set(data, merge=True)
            logger.info(f"Google токены сохранены для пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения Google токенов: {e}")
            return False

    async def get_user_google_tokens(self, user_id: int) -> Optional[Dict]:
        """Возвращает OAuth токены Google пользователя"""
        try:
            doc = self.db.collection('users').document(str(user_id)).get()
            if not doc.exists:
                return None
            data = doc.to_dict()
            return (data.get('google') or {}).get('tokens')
        except Exception as e:
            logger.error(f"Ошибка получения Google токенов: {e}")
            return None

    async def save_user_calendar_id(self, user_id: int, calendar_id: str) -> bool:
        """Сохраняет идентификатор календаря питания пользователя"""
        try:
            user_ref = self.db.collection('users').document(str(user_id))
            data = {
                'google': {
                    'calendar_id': calendar_id,
                    'updated_at': datetime.now()
                }
            }
            user_ref.set(data, merge=True)
            logger.info(f"Сохранен calendar_id для пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения calendar_id: {e}")
            return False

    async def get_user_calendar_id(self, user_id: int) -> Optional[str]:
        """Возвращает идентификатор календаря питания пользователя, если есть"""
        try:
            doc = self.db.collection('users').document(str(user_id)).get()
            if doc.exists:
                data = doc.to_dict()
                google = data.get('google') or {}
                return google.get('calendar_id')
            return None
        except Exception as e:
            logger.error(f"Ошибка получения calendar_id: {e}")
            return None
    
    async def delete_user_google_tokens(self, user_id: int) -> bool:
        """Удаляет Google токены пользователя"""
        try:
            user_ref = self.db.collection('users').document(str(user_id))
            user_ref.update({
                'google.tokens': firestore.DELETE_FIELD
            })
            logger.info(f"Google токены удалены для пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления Google токенов: {e}")
            return False
    
    async def delete_user_calendar_id(self, user_id: int) -> bool:
        """Удаляет calendar_id пользователя"""
        try:
            user_ref = self.db.collection('users').document(str(user_id))
            user_ref.update({
                'google.calendar_id': firestore.DELETE_FIELD
            })
            logger.info(f"Calendar ID удален для пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления calendar_id: {e}")
            return False
    async def get_user_info(self, user_id: int) -> Dict:
        """Получает информацию о пользователе"""
        try:
            user_ref = self.db.collection('users').document(str(user_id))
            doc = user_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return {}
        except Exception as e:
            logger.error(f"Ошибка получения информации о пользователе: {e}")
            return {}

    async def get_all_users(self) -> List[int]:
        """Получает список всех пользователей"""
        try:
            users_ref = self.db.collection('users')
            docs = users_ref.stream()
            
            user_ids = []
            for doc in docs:
                user_ids.append(int(doc.id))
            
            return user_ids
        except Exception as e:
            logger.error(f"Ошибка получения списка пользователей: {e}")
            return []
    
    async def get_users_with_timezones(self) -> List[Dict]:
        """Получает список всех пользователей с их часовыми поясами"""
        try:
            users_ref = self.db.collection('users')
            docs = users_ref.stream()
            
            users = []
            for doc in docs:
                user_data = doc.to_dict()
                if user_data and 'user_id' in user_data:
                    users.append({
                        'user_id': user_data['user_id'],
                        'timezone': user_data.get('timezone', 'UTC'),
                        'username': user_data.get('username'),
                        'first_name': user_data.get('first_name'),
                        'last_name': user_data.get('last_name')
                    })
            
            return users
        except Exception as e:
            logger.error(f"Ошибка получения пользователей с часовыми поясами: {e}")
            return []
    
    def parse_nutrition_data(self, analysis_text: str) -> Dict:
        """Парсит данные о питании из текста анализа"""
        nutrition = {
            'calories': 0,
            'proteins': 0,
            'fats': 0,
            'carbs': 0,
            'vitamins': {}
        }
        
        try:
            lines = analysis_text.split('\n')
            for line in lines:
                line = line.strip()
                
                # Парсинг калорий
                if 'Калории:' in line:
                    import re
                    match = re.search(r'(\d+)', line)
                    if match:
                        nutrition['calories'] = int(match.group(1))
                
                # Парсинг белков
                elif 'Белки:' in line:
                    import re
                    match = re.search(r'(\d+(?:\.\d+)?)', line)
                    if match:
                        nutrition['proteins'] = float(match.group(1))
                
                # Парсинг жиров
                elif 'Жиры:' in line:
                    import re
                    match = re.search(r'(\d+(?:\.\d+)?)', line)
                    if match:
                        nutrition['fats'] = float(match.group(1))
                
                # Парсинг углеводов
                elif 'Углеводы:' in line:
                    import re
                    match = re.search(r'(\d+(?:\.\d+)?)', line)
                    if match:
                        nutrition['carbs'] = float(match.group(1))
                
                # Парсинг витаминов
                elif line.startswith('-') and '%' in line:
                    import re
                    match = re.search(r'- ([^:]+):\s*(\d+)%', line)
                    if match:
                        vitamin_name = match.group(1).strip()
                        percentage = int(match.group(2))
                        nutrition['vitamins'][vitamin_name] = percentage
        
        except Exception as e:
            logger.error(f"Ошибка парсинга данных о питании: {e}")
        
        return nutrition
    
    async def aggregate_daily_nutrition(self, analyses: List[Dict]) -> Dict:
        """Агрегирует данные о питании за день"""
        total = {
            'calories': 0,
            'proteins': 0,
            'fats': 0,
            'carbs': 0,
            'vitamins': {}
        }
        
        for analysis in analyses:
            nutrition = self.parse_nutrition_data(analysis.get('analysis_text', ''))
            
            total['calories'] += nutrition['calories']
            total['proteins'] += nutrition['proteins']
            total['fats'] += nutrition['fats']
            total['carbs'] += nutrition['carbs']
            
            # Агрегируем витамины (берем максимальное значение)
            for vitamin, percentage in nutrition['vitamins'].items():
                if vitamin in total['vitamins']:
                    total['vitamins'][vitamin] = max(total['vitamins'][vitamin], percentage)
                else:
                    total['vitamins'][vitamin] = percentage
        
        return total


