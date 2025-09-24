import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from services.report_service import ReportService

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.report_service = ReportService()
    
    def start_scheduler(self):
        """Запускает планировщик"""
        try:
            # Добавляем задачу отправки дневных отчетов в 21:00
            self.scheduler.add_job(
                self._send_daily_reports,
                CronTrigger(hour=21, minute=0),
                id='daily_reports',
                name='Отправка дневных отчетов',
                replace_existing=True
            )
            
            self.scheduler.start()
            logger.info("Планировщик запущен. Дневные отчеты будут отправляться в 21:00")
            
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
        """Отправляет дневные отчеты всем пользователям"""
        try:
            await self.report_service.send_daily_reports_to_all_users(self.bot)
        except Exception as e:
            logger.error(f"Ошибка в задаче отправки дневных отчетов: {e}")
    
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


