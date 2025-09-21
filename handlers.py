import os
import logging
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.gemini_service import GeminiService
from services.google_calendar import GoogleCalendarService
from config import TEMP_DIR
from utils import error_handler, format_nutrition_info

logger = logging.getLogger(__name__)

# Состояния для FSM
class FoodAnalysisStates(StatesGroup):
    waiting_for_weight = State()

# Инициализируем сервисы
gemini_service = GeminiService()
calendar_service = GoogleCalendarService()

# Создаем роутер
router = Router()

@router.message(Command("start"))
@error_handler
async def start_handler(message: Message):
    """Обработчик команды /start"""
    welcome_text = """
🍽️ Добро пожаловать в бот анализа питания!

Отправьте фото вашей еды, и я:
• Определю состав блюда
• Рассчитаю КБЖУ и калории
• Укажу витамины и полезные вещества
• Сохраню информацию в Google Calendar

Просто отправьте фото еды!
    """
    await message.answer(welcome_text)

@router.message(F.photo)
@error_handler
async def photo_handler(message: Message, state: FSMContext):
    """Обработчик фото еды"""
    try:
        # Получаем файл с максимальным разрешением
        photo = message.photo[-1]
        
        # Скачиваем фото
        file_info = await message.bot.get_file(photo.file_id)
        file_extension = file_info.file_path.split('.')[-1]
        file_path = os.path.join(TEMP_DIR, f"food_{message.from_user.id}_{photo.file_id}.{file_extension}")
        
        await message.bot.download_file(file_info.file_path, file_path)
        
        # Сохраняем путь к файлу в состоянии
        await state.update_data(photo_path=file_path)
        await state.set_state(FoodAnalysisStates.waiting_for_weight)
        
        # Создаем кнопку "Не знаю"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❓ Не знаю граммовку", callback_data="unknown_weight")]
        ])
        
        await message.answer(
            "📸 Фото получено!\n\n"
            "Теперь укажите вес еды в граммах (например: 250)\n"
            "Или нажмите кнопку, если не знаете точный вес:",
            reply_markup=keyboard
        )
        
    except Exception as e:
        logger.error(f"Ошибка при обработке фото: {e}")
        await message.answer(
            "❌ Произошла ошибка при обработке фото. "
            "Попробуйте отправить фото еще раз."
        )

@router.callback_query(F.data == "unknown_weight")
@error_handler
async def unknown_weight_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Не знаю граммовку'"""
    await callback.answer()
    
    # Получаем данные из состояния
    data = await state.get_data()
    photo_path = data.get('photo_path')
    
    if not photo_path or not os.path.exists(photo_path):
        await callback.message.answer(
            "❌ Фото не найдено. Пожалуйста, отправьте фото еды заново."
        )
        await state.clear()
        return
    
    # Показываем индикатор загрузки
    await callback.message.answer("🔍 Анализирую фото еды и определяю примерный вес...")
    
    # Анализируем еду через Gemini без указания конкретного веса
    analysis_result = await gemini_service.analyze_food_auto_weight(photo_path)
    
    # Форматируем ответ
    formatted_response = format_nutrition_info(analysis_result)
    final_response = f"🍽️ **Ваш прием пищи (автоопределение веса):**\n\n{formatted_response}"
    
    # Отправляем результат пользователю
    try:
        await callback.message.answer(final_response, parse_mode="Markdown")
    except Exception as e:
        logger.warning(f"Ошибка отправки с Markdown: {e}")
        await callback.message.answer(final_response)
    
    # Удаляем временный файл
    try:
        os.remove(photo_path)
    except Exception as e:
        logger.warning(f"Не удалось удалить временный файл: {e}")
    
    # Очищаем состояние
    await state.clear()
    
    await callback.message.answer(
        "✅ Анализ завершен! Отправьте новое фото для следующего анализа."
    )

@router.message(FoodAnalysisStates.waiting_for_weight)
@error_handler
async def weight_handler(message: Message, state: FSMContext):
    """Обработчик веса еды"""
    try:
        # Проверяем, что введено число
        try:
            weight = int(message.text.strip())
            if weight <= 0 or weight > 5000:
                await message.answer(
                    "❌ Пожалуйста, введите корректный вес от 1 до 5000 грамм"
                )
                return
        except ValueError:
            await message.answer(
                "❌ Пожалуйста, введите вес в граммах числом (например: 250)"
            )
            return
        
        # Получаем данные из состояния
        data = await state.get_data()
        photo_path = data.get('photo_path')
        
        if not photo_path or not os.path.exists(photo_path):
            await message.answer(
                "❌ Фото не найдено. Пожалуйста, отправьте фото еды заново."
            )
            await state.clear()
            return
        
        # Показываем индикатор загрузки
        await message.answer("🔍 Анализирую фото еды...")
        
        # Анализируем еду через Gemini
        analysis_result = await gemini_service.analyze_food(photo_path, weight)
        
        # Форматируем ответ
        formatted_response = format_nutrition_info(analysis_result)
        final_response = f"🍽️ **Ваш прием пищи ({weight} г):**\n\n{formatted_response}"
        
        # Отправляем результат пользователю (без Markdown чтобы избежать ошибок парсинга)
        try:
            await message.answer(final_response, parse_mode="Markdown")
        except Exception as e:
            logger.warning(f"Ошибка отправки с Markdown: {e}")
            # Отправляем без форматирования если есть проблемы с Markdown
            await message.answer(final_response)
        
        # Google Calendar отключен по запросу пользователя
        # await message.answer("📅 Google Calendar отключен")
        
        # Удаляем временный файл
        try:
            os.remove(photo_path)
        except Exception as e:
            logger.warning(f"Не удалось удалить временный файл: {e}")
        
        # Очищаем состояние
        await state.clear()
        
        await message.answer(
            "\n✅ Анализ завершен! Отправьте новое фото для следующего анализа."
        )
        
    except Exception as e:
        logger.error(f"Ошибка при анализе веса: {e}")
        await message.answer(
            "❌ Произошла ошибка при анализе. "
            "Попробуйте отправить фото заново."
        )
        await state.clear()

@router.message(F.text)
@error_handler
async def text_handler(message: Message):
    """Обработчик обычных текстовых сообщений"""
    await message.answer(
        "📸 Пожалуйста, отправьте фото еды для анализа!\n\n"
        "Я умею анализировать только изображения блюд."
    )

def register_handlers(dp):
    """Регистрирует все обработчики"""
    from commands import commands_router
    dp.include_router(router)
    dp.include_router(commands_router)
