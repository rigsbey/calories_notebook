"""
Дополнительные команды для управления ботом
"""
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils import error_handler

logger = logging.getLogger(__name__)

# Создаем роутер для команд
commands_router = Router()

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
