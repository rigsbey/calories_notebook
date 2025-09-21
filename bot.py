import asyncio
import logging
import os
import atexit
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_handlers
from config import BOT_TOKEN, TEMP_DIR
from utils import setup_logging, clean_temp_files

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)

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
    
    logger.info("🤖 Бот успешно запущен!")
    
    try:
        # Запускаем бота
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())
