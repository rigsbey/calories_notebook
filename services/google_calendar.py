import logging
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import pickle
from config import GOOGLE_CREDENTIALS_PATH

logger = logging.getLogger(__name__)

class GoogleCalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    TOKEN_FILE = 'token.pickle'
    
    def __init__(self):
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Аутентификация в Google Calendar API"""
        creds = None
        
        # Загружаем сохраненные токены
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # Если токены недействительны или отсутствуют
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Ошибка обновления токена: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(GOOGLE_CREDENTIALS_PATH):
                    logger.error(f"Файл credentials.json не найден по пути: {GOOGLE_CREDENTIALS_PATH}")
                    return
                
                try:
                    flow = Flow.from_client_secrets_file(
                        GOOGLE_CREDENTIALS_PATH, self.SCOPES)
                    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
                    
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    logger.info(f"Перейдите по ссылке для авторизации: {auth_url}")
                    
                    # В реальном приложении здесь должна быть интеграция с веб-интерфейсом
                    # Для демонстрации оставляем заглушку
                    logger.warning("Требуется ручная авторизация Google Calendar")
                    return
                    
                except Exception as e:
                    logger.error(f"Ошибка авторизации: {e}")
                    return
        
        # Сохраняем токены
        if creds:
            with open(self.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
            
            try:
                self.service = build('calendar', 'v3', credentials=creds)
                logger.info("Google Calendar API успешно инициализирован")
            except Exception as e:
                logger.error(f"Ошибка создания сервиса Calendar: {e}")
    
    async def create_meal_event(self, description: str, user_id: int) -> bool:
        """
        Создает событие о приеме пищи в Google Calendar
        
        Args:
            description: описание с КБЖУ и витаминами
            user_id: ID пользователя Telegram
            
        Returns:
            True если событие создано успешно, False в противном случае
        """
        if not self.service:
            logger.error("Google Calendar сервис не инициализирован")
            return False
        
        try:
            now = datetime.now(timezone.utc)
            
            event = {
                'summary': 'Прием пищи',
                'description': f"Пользователь: {user_id}\n\n{description}",
                'start': {
                    'dateTime': now.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': now.isoformat(),
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [],
                },
            }
            
            # Создаем событие в основном календаре
            created_event = self.service.events().insert(
                calendarId='primary', 
                body=event
            ).execute()
            
            logger.info(f"Событие создано: {created_event.get('htmlLink')}")
            return True
            
        except HttpError as e:
            logger.error(f"HTTP ошибка при создании события: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при создании события в календаре: {e}")
            return False
    
    def is_available(self) -> bool:
        """Проверяет доступность Google Calendar API"""
        return self.service is not None
