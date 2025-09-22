import asyncio
import logging
import os
import atexit

# Устанавливаем Gemini API ключ для тестирования ПЕРЕД импортом модулей
os.environ["GEMINI_API_KEY"] = "AIzaSyAfF657E3lChR6whEdf1Rzw8eqJrrSR-qg"

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_handlers
from config import TEMP_DIR
from utils import setup_logging, clean_temp_files

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)

async def main():
    # Устанавливаем тестовый токен
    BOT_TOKEN = "8368637397:AAHeOqbS4KlrYhDiKQNJr8HsHxZcyLBNLYE"
    
    # Проверяем наличие токена
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден!")
        return
    
    # Проверяем наличие Gemini API ключа
    from config import GEMINI_API_KEY
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY не найден в переменных окружения!")
        logger.error("Создайте файл .env на основе env_example.txt и добавьте ваш API ключ")
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
    
    logger.info("🤖 Тестовый бот успешно запущен!")
    
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
