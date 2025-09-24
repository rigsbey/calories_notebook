"""
Дополнительные команды для управления ботом
"""
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import error_handler
from services.report_service import ReportService
from services.google_calendar import GoogleCalendarService

logger = logging.getLogger(__name__)

# Создаем роутер для команд
commands_router = Router()

# Инициализируем сервис отчетов
report_service = ReportService()
calendar_service = GoogleCalendarService()

@commands_router.message(Command("help"))
@error_handler
async def help_handler(message: Message):
    """Обработчик команды /help"""
    help_text = """
🤖 **Помощь по использованию бота**

**Основные команды:**
/start - Запустить бота
/help - Показать эту справку
/info - Информация о боте
/day - Итоги дня (быстрый доступ)
/week - Итоги недели (быстрый доступ)
/summary - Итоги дня
/summary week - Итоги недели

**Как использовать:**
1. 📸 Отправьте фото еды
2. 🔢 Укажите вес в граммах
3. 📊 Получите анализ КБЖУ
4. 📅 Информация сохранится в календаре

**Поддерживаемые форматы:**
• Фото в формате JPG, PNG
• Вес от 1 до 5000 грамм
• Любые блюда и продукты

**Что анализирует бот:**
• Состав блюда
• Калории и КБЖУ
• Витамины и полезные вещества
• Пищевую ценность

Если возникли проблемы, попробуйте отправить фото заново.
    """
    await message.answer(help_text, parse_mode="Markdown")

@commands_router.message(Command("info"))
@error_handler
async def info_handler(message: Message):
    """Обработчик команды /info"""
    info_text = """
ℹ️ **Информация о боте**

**Версия:** 1.0.0
**Технологии:**
• Python 3.8+
• aiogram 3.x
• OpenAI GPT-4 Vision
• Google Calendar API

**Возможности:**
🔍 Анализ состава еды по фото
📊 Расчет калорий и КБЖУ
💊 Определение витаминов
📅 Сохранение в Google Calendar
🤖 Интеллектуальные ответы

**Безопасность:**
• Фото удаляются после обработки
• Данные не сохраняются на сервере
• Используются официальные API

Бот создан для помощи в контроле питания и здорового образа жизни! 💪
    """
    await message.answer(info_text, parse_mode="Markdown")

@commands_router.message(Command("day"))
@error_handler
async def day_handler(message: Message):
    """Обработчик команды /day - быстрый доступ к дневному отчету"""
    try:
        await message.answer("📊 Генерирую отчет за день...")
        report = await report_service.generate_daily_report(message.from_user.id)
        await message.answer(report)
        
    except Exception as e:
        logger.error(f"Ошибка генерации дневного отчета: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.")

@commands_router.message(Command("week"))
@error_handler
async def week_handler(message: Message):
    """Обработчик команды /week - быстрый доступ к недельному отчету"""
    try:
        await message.answer("📊 Генерирую отчет за неделю...")
        report = await report_service.generate_weekly_report(message.from_user.id)
        await message.answer(report)
        
    except Exception as e:
        logger.error(f"Ошибка генерации недельного отчета: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.")

@commands_router.message(Command("summary"))
@error_handler
async def summary_handler(message: Message):
    """Обработчик команды /summary"""
    try:
        # Проверяем аргументы команды
        command_args = message.text.split()
        
        if len(command_args) > 1 and command_args[1].lower() == 'week':
            # Недельный отчет
            await message.answer("📊 Генерирую отчет за неделю...")
            report = await report_service.generate_weekly_report(message.from_user.id)
        else:
            # Дневной отчет
            await message.answer("📊 Генерирую отчет за день...")
            report = await report_service.generate_daily_report(message.from_user.id)
        
        await message.answer(report)
        
    except Exception as e:
        logger.error(f"Ошибка генерации отчета: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.")

@commands_router.message(lambda message: message.text and message.text.lower() in ['итоги дня', 'итоги недели', 'отчет'])
@error_handler
async def text_summary_handler(message: Message):
    """Обработчик текстовых запросов отчетов"""
    try:
        text = message.text.lower()
        
        if 'недели' in text or 'неделя' in text:
            await message.answer("📊 Генерирую отчет за неделю...")
            report = await report_service.generate_weekly_report(message.from_user.id)
        else:
            await message.answer("📊 Генерирую отчет за день...")
            report = await report_service.generate_daily_report(message.from_user.id)
        
        await message.answer(report)
        
    except Exception as e:
        logger.error(f"Ошибка генерации отчета по тексту: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.")
