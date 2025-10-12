import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from services.report_service import ReportService
from services.timezone_service import TimezoneService
from services.reminder_service import ReminderService, ReminderType

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.report_service = ReportService()
        self.timezone_service = TimezoneService()
        self.reminder_service = ReminderService()
    
    async def start_scheduler(self):
        """Запускает планировщик с учетом часовых поясов"""
        try:
            # Получаем пользователей, сгруппированных по времени уведомлений
            users_by_time = await self.timezone_service.get_users_by_notification_time()
            
            # Добавляем задачи для каждого времени уведомлений
            job_count = 0
            for notification_time, users in users_by_time.items():
                if users:  # Только если есть пользователи для этого времени
                    hour = notification_time.hour
                    minute = notification_time.minute
                    
                    self.scheduler.add_job(
                        self._send_daily_reports_for_users,
                        CronTrigger(hour=hour, minute=minute),
                        args=[users],
                        id=f'daily_reports_{hour}_{minute}',
                        name=f'Отправка дневных отчетов в {hour:02d}:{minute:02d} UTC',
                        replace_existing=True
                    )
                    job_count += 1
                    logger.info(f"Добавлена задача отправки отчетов в {hour:02d}:{minute:02d} UTC для {len(users)} пользователей")
            
            # Если нет пользователей с настроенными часовыми поясами, используем старую схему
            if job_count == 0:
                self.scheduler.add_job(
                    self._send_daily_reports,
                    CronTrigger(hour=20, minute=0),  # Изменили на 20:00
                    id='daily_reports_fallback',
                    name='Отправка дневных отчетов (fallback)',
                    replace_existing=True
                )
                logger.info("Добавлена fallback задача отправки отчетов в 20:00 UTC")
            
            # Добавляем задачи для напоминаний
            await self._add_reminder_jobs()
            
            self.scheduler.start()
            logger.info(f"Планировщик запущен. Добавлено {job_count} задач отправки отчетов")
            
        except Exception as e:
            logger.error(f"Ошибка запуска планировщика: {e}")
    
    def stop_scheduler(self):
        """Останавливает планировщик"""
        try:
            self.scheduler.shutdown()
            logger.info("Планировщик остановлен")
        except Exception as e:
            logger.error(f"Ошибка остановки планировщика: {e}")
    
    async def _send_daily_reports(self):
        """Отправляет дневные отчеты всем пользователям (fallback)"""
        try:
            await self.report_service.send_daily_reports_to_all_users(self.bot)
        except Exception as e:
            logger.error(f"Ошибка в задаче отправки дневных отчетов: {e}")
    
    async def _send_daily_reports_for_users(self, users):
        """Отправляет дневные отчеты конкретным пользователям"""
        try:
            await self.report_service.send_daily_reports_to_users(self.bot, users)
        except Exception as e:
            logger.error(f"Ошибка в задаче отправки дневных отчетов для пользователей: {e}")
    
    def add_test_job(self):
        """Добавляет тестовую задачу (для отладки)"""
        try:
            self.scheduler.add_job(
                self._send_daily_reports,
                'interval',
                minutes=1,
                id='test_reports',
                name='Тестовая отправка отчетов',
                replace_existing=True
            )
            logger.info("Тестовая задача добавлена")
        except Exception as e:
            logger.error(f"Ошибка добавления тестовой задачи: {e}")
    
    def remove_test_job(self):
        """Удаляет тестовую задачу"""
        try:
            self.scheduler.remove_job('test_reports')
            logger.info("Тестовая задача удалена")
        except Exception as e:
            logger.error(f"Ошибка удаления тестовой задачи: {e}")

    async def _add_reminder_jobs(self):
        """Добавляет задачи для напоминаний"""
        try:
            logger.info("Все напоминания отключены по запросу пользователя")
            
        except Exception as e:
            logger.error(f"Ошибка добавления задач напоминаний: {e}")

    async def _send_water_reminders(self):
        """Отправляет напоминания о воде"""
        try:
            from datetime import datetime
            current_hour = datetime.now().hour
            users = await self.reminder_service.get_users_for_reminder(ReminderType.WATER, current_hour)
            
            for user_id in users:
                await self.reminder_service.send_reminder(self.bot, user_id, ReminderType.WATER)
            
            if users:
                logger.info(f"Напоминания о воде отправлены {len(users)} пользователям")
                
        except Exception as e:
            logger.error(f"Ошибка отправки напоминаний о воде: {e}")

    async def _send_meal_reminders(self):
        """Отправляет напоминания о еде"""
        try:
            from datetime import datetime
            current_hour = datetime.now().hour
            users = await self.reminder_service.get_users_for_reminder(ReminderType.MEAL, current_hour)
            
            for user_id in users:
                await self.reminder_service.send_reminder(self.bot, user_id, ReminderType.MEAL)
            
            if users:
                logger.info(f"Напоминания о еде отправлены {len(users)} пользователям")
                
        except Exception as e:
            logger.error(f"Ошибка отправки напоминаний о еде: {e}")

    async def _send_calorie_reminders(self):
        """Отправляет напоминания о лимите калорий"""
        try:
            from datetime import datetime
            current_hour = datetime.now().hour
            users = await self.reminder_service.get_users_for_reminder(ReminderType.CALORIE_LIMIT, current_hour)
            
            for user_id in users:
                await self.reminder_service.send_reminder(self.bot, user_id, ReminderType.CALORIE_LIMIT)
            
            if users:
                logger.info(f"Напоминания о калориях отправлены {len(users)} пользователям")
                
        except Exception as e:
            logger.error(f"Ошибка отправки напоминаний о калориях: {e}")

    async def _send_motivation_reminders(self):
        """Отправляет мотивационные сообщения"""
        try:
            from datetime import datetime
            current_hour = datetime.now().hour
            users = await self.reminder_service.get_users_for_reminder(ReminderType.MOTIVATION, current_hour)
            
            for user_id in users:
                await self.reminder_service.send_motivational_message(self.bot, user_id)
            
            if users:
                logger.info(f"Мотивационные сообщения отправлены {len(users)} пользователям")
                
        except Exception as e:
            logger.error(f"Ошибка отправки мотивационных сообщений: {e}")





