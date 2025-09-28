import logging
from datetime import datetime, time
import pytz
from typing import Dict, List
from services.firebase_service import FirebaseService

logger = logging.getLogger(__name__)

class TimezoneService:
    def __init__(self):
        self.firebase = FirebaseService()
    
    def get_user_timezone(self, user_id: int) -> str:
        """Получает часовой пояс пользователя, по умолчанию UTC"""
        # Здесь можно добавить логику определения часового пояса по геолокации
        # Пока используем UTC как значение по умолчанию
        return 'UTC'
    
    def get_timezone_offset(self, timezone_str: str) -> int:
        """Получает смещение часового пояса в часах относительно UTC"""
        try:
            tz = pytz.timezone(timezone_str)
            now = datetime.now(tz)
            offset = now.utcoffset().total_seconds() / 3600
            return int(offset)
        except Exception as e:
            logger.error(f"Ошибка получения смещения для часового пояса {timezone_str}: {e}")
            return 0
    
    def get_local_time_20_00_utc(self, timezone_str: str) -> time:
        """Вычисляет время в UTC, когда в указанном часовом поясе 20:00"""
        try:
            tz = pytz.timezone(timezone_str)
            # Создаем время 20:00 в указанном часовом поясе
            local_time_20_00 = time(20, 0)
            
            # Получаем текущую дату в указанном часовом поясе
            now_local = datetime.now(tz)
            local_datetime_20_00 = datetime.combine(now_local.date(), local_time_20_00)
            
            # Конвертируем в UTC
            utc_datetime_20_00 = local_datetime_20_00.astimezone(pytz.UTC)
            
            return utc_datetime_20_00.time()
        except Exception as e:
            logger.error(f"Ошибка вычисления времени для часового пояса {timezone_str}: {e}")
            return time(20, 0)  # По умолчанию 20:00 UTC
    
    async def get_users_by_notification_time(self) -> Dict[time, List[Dict]]:
        """Группирует пользователей по времени отправки уведомлений"""
        try:
            users = await self.firebase.get_users_with_timezones()
            users_by_time = {}
            
            for user in users:
                timezone_str = user.get('timezone', 'UTC')
                notification_time = self.get_local_time_20_00_utc(timezone_str)
                
                if notification_time not in users_by_time:
                    users_by_time[notification_time] = []
                
                users_by_time[notification_time].append(user)
            
            return users_by_time
        except Exception as e:
            logger.error(f"Ошибка группировки пользователей по времени: {e}")
            return {}
    
    def get_common_timezones(self) -> List[str]:
        """Возвращает список популярных часовых поясов"""
        return [
            'UTC',
            'Europe/Moscow',      # Москва (UTC+3)
            'Europe/Kiev',        # Киев (UTC+2)
            'Europe/Minsk',       # Минск (UTC+3)
            'Europe/London',      # Лондон (UTC+0/+1)
            'Europe/Berlin',      # Берлин (UTC+1/+2)
            'Europe/Paris',       # Париж (UTC+1/+2)
            'America/New_York',   # Нью-Йорк (UTC-5/-4)
            'America/Los_Angeles', # Лос-Анджелес (UTC-8/-7)
            'Asia/Tokyo',         # Токио (UTC+9)
            'Asia/Shanghai',      # Шанхай (UTC+8)
            'Asia/Dubai',         # Дубай (UTC+4)
            'Australia/Sydney',   # Сидней (UTC+10/+11)
        ]
    
    def format_timezone_name(self, timezone_str: str) -> str:
        """Форматирует название часового пояса для отображения пользователю"""
        timezone_names = {
            'UTC': 'UTC (Всемирное время)',
            'Europe/Moscow': 'Москва (UTC+3)',
            'Europe/Kiev': 'Киев (UTC+2)',
            'Europe/Minsk': 'Минск (UTC+3)',
            'Europe/London': 'Лондон (UTC+0/+1)',
            'Europe/Berlin': 'Берлин (UTC+1/+2)',
            'Europe/Paris': 'Париж (UTC+1/+2)',
            'America/New_York': 'Нью-Йорк (UTC-5/-4)',
            'America/Los_Angeles': 'Лос-Анджелес (UTC-8/-7)',
            'Asia/Tokyo': 'Токио (UTC+9)',
            'Asia/Shanghai': 'Шанхай (UTC+8)',
            'Asia/Dubai': 'Дубай (UTC+4)',
            'Australia/Sydney': 'Сидней (UTC+10/+11)',
        }
        return timezone_names.get(timezone_str, timezone_str)
