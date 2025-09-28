import asyncio
import logging
import os
import atexit
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from handlers import register_handlers
from config import BOT_TOKEN, TEMP_DIR
from utils import setup_logging, clean_temp_files
from services.scheduler_service import SchedulerService

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)

async def setup_bot_commands(bot: Bot):
    """Настройка команд меню бота"""
    commands = [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="help", description="ℹ️ Помощь по использованию"),
        BotCommand(command="pro", description="🌟 Pro подписка"),
        BotCommand(command="day", description="📊 Итоги дня"),
        BotCommand(command="week", description="📈 Итоги недели (Pro)"),
        BotCommand(command="summary", description="📋 Сводка питания"),
        BotCommand(command="gconnect", description="📅 Подключить Google Calendar"),
        BotCommand(command="gstatus", description="🔍 Статус календаря"),
        BotCommand(command="gdisconnect", description="❌ Отключить календарь"),
    ]
    
    try:
        await bot.set_my_commands(commands)
        logger.info("Команды меню бота настроены успешно")
    except Exception as e:
        logger.error(f"Ошибка настройки команд меню: {e}")

async def main():
    # Проверяем наличие токена
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в переменных окружения!")
        return
    
    # Создаем папку для временных файлов
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Очищаем старые временные файлы при запуске
    clean_temp_files(TEMP_DIR)
    
    # Регистрируем очистку при завершении
    atexit.register(lambda: clean_temp_files(TEMP_DIR))
    
    # Инициализируем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Регистрируем обработчики
    register_handlers(dp)
    
    # Настраиваем команды меню
    await setup_bot_commands(bot)
    
    # Инициализируем планировщик
    scheduler = SchedulerService(bot)
    await scheduler.start_scheduler()
    
    logger.info("🤖 Бот успешно запущен!")
    
    try:
        # Запускаем бота
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        # Останавливаем планировщик
        scheduler.stop_scheduler()
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())
