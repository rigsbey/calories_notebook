import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from aiohttp import web
from config import (
    GOOGLE_CREDENTIALS_PATH,
    GOOGLE_OAUTH_REDIRECT_PORT,
    GOOGLE_OAUTH_REDIRECT_PATH,
    GOOGLE_OAUTH_REDIRECT_BASE,
)
from services.firebase_service import FirebaseService

logger = logging.getLogger(__name__)


def _credentials_to_dict(credentials: Credentials) -> Dict:
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry': credentials.expiry.isoformat() if credentials.expiry else None,
    }


class GoogleCalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    CALENDAR_NAME = 'Календарь питания'

    def __init__(self):
        self.firebase = FirebaseService()
        self._pending_states: Dict[str, Flow] = {}
        self._app: Optional[web.Application] = None
        self._runner: Optional[web.AppRunner] = None
        self._site: Optional[web.TCPSite] = None
        self.redirect_uri = self._build_redirect_uri()

    def _build_redirect_uri(self) -> str:
        base = GOOGLE_OAUTH_REDIRECT_BASE.strip()
        if not base:
            return f"http://localhost:{GOOGLE_OAUTH_REDIRECT_PORT}{GOOGLE_OAUTH_REDIRECT_PATH}"
        return f"{base.rstrip('/')}{GOOGLE_OAUTH_REDIRECT_PATH}"

    async def _ensure_callback_server(self):
        if self._site:
            return
        self._app = web.Application()
        self._app.add_routes([web.get(GOOGLE_OAUTH_REDIRECT_PATH, self._oauth_callback)])
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, '0.0.0.0', GOOGLE_OAUTH_REDIRECT_PORT)
        await self._site.start()
        logger.info(f"OAuth callback сервер запущен на {self.redirect_uri}")

    async def _oauth_callback(self, request: web.Request) -> web.Response:
        try:
            code = request.rel_url.query.get('code')
            state = request.rel_url.query.get('state')
            if not code or not state:
                return web.Response(text="Missing code/state", status=400)

            flow = self._pending_states.pop(state, None)
            if flow is None:
                # Восстанавливаем flow на лету
                flow = Flow.from_client_secrets_file(
                    GOOGLE_CREDENTIALS_PATH,
                    scopes=self.SCOPES,
                    redirect_uri=self.redirect_uri
                )
                flow.fetch_token(code=code)
            else:
                flow.fetch_token(code=code)

            creds = flow.credentials
            user_id = int(state)

            await self.firebase.save_user_google_tokens(user_id, _credentials_to_dict(creds))

            # Убедимся, что у пользователя есть календарь
            await self._ensure_calendar(user_id, creds)

            return web.Response(text="Готово! Можете вернуться в Telegram и продолжить.")
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            return web.Response(text="Ошибка авторизации.", status=500)

    async def get_auth_url(self, user_id: int) -> str:
        await self._ensure_callback_server()
        try:
            flow = Flow.from_client_secrets_file(
                GOOGLE_CREDENTIALS_PATH,
                scopes=self.SCOPES,
                redirect_uri=self.redirect_uri
            )
            auth_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent',
                state=str(user_id)
            )
            self._pending_states[state] = flow
            return auth_url
        except Exception as e:
            logger.error(f"Ошибка создания auth URL: {e}")
            return "❌ Ошибка настройки OAuth. Проверьте credentials.json"

    async def _build_service_for_user(self, user_id: int) -> Optional[object]:
        tokens = await self.firebase.get_user_google_tokens(user_id)
        if not tokens:
            return None
        creds = Credentials(
            tokens.get('token'),
            refresh_token=tokens.get('refresh_token'),
            token_uri=tokens.get('token_uri'),
            client_id=tokens.get('client_id'),
            client_secret=tokens.get('client_secret'),
            scopes=tokens.get('scopes'),
        )
        try:
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                await self.firebase.save_user_google_tokens(user_id, _credentials_to_dict(creds))
        except Exception as e:
            logger.error(f"Ошибка обновления токена: {e}")
            return None
        return build('calendar', 'v3', credentials=creds, cache_discovery=False)

    async def _ensure_calendar(self, user_id: int, creds: Credentials) -> Optional[str]:
        calendar_id = await self.firebase.get_user_calendar_id(user_id)
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
        if calendar_id:
            # Проверим наличие календаря
            try:
                service.calendars().get(calendarId=calendar_id).execute()
                return calendar_id
            except Exception:
                logger.warning("Сохраненный calendar_id недействителен, создаем заново")

        # Пытаемся найти уже созданный ранее календарь по имени
        try:
            calendar_list = service.calendarList().list().execute()
            for item in calendar_list.get('items', []):
                if item.get('summary') == self.CALENDAR_NAME:
                    found_id = item.get('id')
                    await self.firebase.save_user_calendar_id(user_id, found_id)
                    return found_id
        except Exception as e:
            logger.warning(f"Не удалось прочитать список календарей: {e}")

        # Создаем новый календарь
        calendar = {
            'summary': self.CALENDAR_NAME,
            'timeZone': 'UTC'
        }
        created = service.calendars().insert(body=calendar).execute()
        new_id = created.get('id')
        await self.firebase.save_user_calendar_id(user_id, new_id)
        logger.info(f"Создан календарь '{self.CALENDAR_NAME}' для пользователя {user_id}")
        return new_id

    async def ensure_connected(self, user_id: int) -> bool:
        service = await self._build_service_for_user(user_id)
        return service is not None

    async def update_meal_event(self, user_id: int, event_id: str, title: str, description: str) -> bool:
        """Обновляет существующее событие в календаре"""
        try:
            tokens = await self.firebase.get_user_google_tokens(user_id)
            if not tokens:
                logger.info(f"Пользователь {user_id} не авторизован в Google")
                return False
            
            creds = Credentials(
                tokens.get('token'),
                refresh_token=tokens.get('refresh_token'),
                token_uri=tokens.get('token_uri'),
                client_id=tokens.get('client_id'),
                client_secret=tokens.get('client_secret'),
                scopes=tokens.get('scopes'),
            )
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                await self.firebase.save_user_google_tokens(user_id, _credentials_to_dict(creds))

            calendar_id = await self.firebase.get_user_calendar_id(user_id)
            if not calendar_id:
                logger.warning(f"У пользователя {user_id} нет календаря")
                return False

            service = build('calendar', 'v3', credentials=creds, cache_discovery=False)

            # Получаем существующее событие
            event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
            
            # Обновляем данные
            event['summary'] = title or 'Прием пищи'
            event['description'] = description or ''

            # Сохраняем обновленное событие
            updated_event = service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            logger.info(f"Событие обновлено: {updated_event.get('htmlLink')}")
            return True
        except HttpError as e:
            logger.error(f"HTTP ошибка при обновлении события: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при обновлении события: {e}")
            return False

    async def create_meal_event(self, user_id: int, title: str, description: str, event_time: datetime) -> bool:
        try:
            tokens = await self.firebase.get_user_google_tokens(user_id)
            if not tokens:
                logger.info(f"Пользователь {user_id} не авторизован в Google")
                return False
            creds = Credentials(
                tokens.get('token'),
                refresh_token=tokens.get('refresh_token'),
                token_uri=tokens.get('token_uri'),
                client_id=tokens.get('client_id'),
                client_secret=tokens.get('client_secret'),
                scopes=tokens.get('scopes'),
            )
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                await self.firebase.save_user_google_tokens(user_id, _credentials_to_dict(creds))

            calendar_id = await self._ensure_calendar(user_id, creds)

            service = build('calendar', 'v3', credentials=creds, cache_discovery=False)

            start_iso = event_time.astimezone(timezone.utc).isoformat()
            end_iso = (event_time + timedelta(minutes=1)).astimezone(timezone.utc).isoformat()

            event = {
                'summary': title or 'Прием пищи',
                'description': description or '',
                'start': {'dateTime': start_iso, 'timeZone': 'UTC'},
                'end': {'dateTime': end_iso, 'timeZone': 'UTC'},
            }
            created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
            logger.info(f"Событие создано: {created_event.get('htmlLink')}")
            return True
        except HttpError as e:
            logger.error(f"HTTP ошибка при создании события: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при создании события: {e}")
            return False

    async def update_latest_meal_event(self, user_id: int, title: str, description: str) -> bool:
        """Обновляет последнее событие пользователя за сегодня"""
        try:
            tokens = await self.firebase.get_user_google_tokens(user_id)
            if not tokens:
                logger.info(f"Пользователь {user_id} не авторизован в Google")
                return False
            
            creds = Credentials(
                tokens.get('token'),
                refresh_token=tokens.get('refresh_token'),
                token_uri=tokens.get('token_uri'),
                client_id=tokens.get('client_id'),
                client_secret=tokens.get('client_secret'),
                scopes=tokens.get('scopes'),
            )
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
                await self.firebase.save_user_google_tokens(user_id, _credentials_to_dict(creds))

            calendar_id = await self.firebase.get_user_calendar_id(user_id)
            if not calendar_id:
                logger.warning(f"У пользователя {user_id} нет календаря")
                return False

            service = build('calendar', 'v3', credentials=creds, cache_discovery=False)

            # Ищем последнее событие за сегодня
            today = datetime.now().strftime('%Y-%m-%d')
            time_min = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
            time_max = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'

            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            if not events:
                logger.warning(f"Не найдено событий за сегодня для пользователя {user_id}")
                return False

            # Берем последнее событие (самое позднее)
            latest_event = events[-1]
            event_id = latest_event['id']

            # Обновляем событие
            latest_event['summary'] = title or 'Прием пищи'
            latest_event['description'] = description or ''

            updated_event = service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=latest_event
            ).execute()
            
            logger.info(f"Последнее событие обновлено: {updated_event.get('htmlLink')}")
            return True
        except HttpError as e:
            logger.error(f"HTTP ошибка при обновлении последнего события: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при обновлении последнего события: {e}")
            return False
