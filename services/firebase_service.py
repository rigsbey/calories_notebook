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
    
    async def save_analysis(self, user_id: int, analysis_data: Dict) -> bool:
        """Сохраняет анализ питания в Firestore"""
        try:
            doc_ref = self.db.collection('users').document(str(user_id)).collection('analyses').document()
            analysis_data['timestamp'] = datetime.now()
            analysis_data['date'] = datetime.now().strftime('%Y-%m-%d')
            
            doc_ref.set(analysis_data)
            logger.info(f"Анализ сохранен для пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения анализа: {e}")
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
