import os
import logging
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.gemini_service import GeminiService
from services.google_calendar import GoogleCalendarService
from services.analysis_storage import analysis_storage
from services.firebase_service import FirebaseService
from config import TEMP_DIR
from utils import error_handler, format_nutrition_info

logger = logging.getLogger(__name__)

# Состояния для FSM
class FoodAnalysisStates(StatesGroup):
    waiting_for_weight = State()

# Создаем клавиатуру с кнопками
def get_main_keyboard():
    """Создает основную клавиатуру с кнопками"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Итоги дня"), KeyboardButton(text="📈 Итоги недели")],
            [KeyboardButton(text="📸 Анализ еды"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

# Инициализируем сервисы
gemini_service = GeminiService()
calendar_service = GoogleCalendarService()
firebase_service = FirebaseService()

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

Используйте кнопки ниже для быстрого доступа к функциям!
    """
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

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
    
    # Сохраняем анализ для возможности редактирования
    user_id = callback.from_user.id if callback.from_user else None
    if user_id is not None:
        analysis_storage.store_analysis(
            user_id=user_id,
            analysis_text=analysis_result,
            image_path=photo_path,
            weight=None  # Автоопределение веса
        )
    
    # Сохраняем в Firebase
    user_id = callback.from_user.id
    if user_id is not None:
        analysis_data = {
            'analysis_text': analysis_result,
            'weight': 'auto',
            'user_id': str(user_id)
        }
        await firebase_service.save_analysis(user_id, analysis_data)
    
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
            "✅ Анализ завершен! \n\n"
            "💬 Если нужно что-то исправить, просто напишите текстом:\n"
            "• \"На фото не руккола, а листья салата\"\n"
            "• \"Вес не 450г, а 300г\"\n"
            "• \"Добавь туда еще помидоры\"\n\n"
            "📸 Или отправьте новое фото для следующего анализа."
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
        
        # Сохраняем анализ для возможности редактирования
        user_id = message.from_user.id if message.from_user else None
        if user_id is not None:
            analysis_storage.store_analysis(
                user_id=user_id,
                analysis_text=analysis_result,
                image_path=photo_path,
                weight=weight
            )
        
        # Сохраняем в Firebase
        user_id = message.from_user.id
        if user_id is not None:
            analysis_data = {
                'analysis_text': analysis_result,
                'weight': str(weight),
                'user_id': str(user_id)
            }
            await firebase_service.save_analysis(user_id, analysis_data)
        
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
            "✅ Анализ завершен!\n\n"
            "💬 Если нужно что-то исправить, просто напишите текстом:\n"
            "• \"На фото не руккола, а листья салата\"\n"
            "• \"Вес не 450г, а 300г\"\n"
            "• \"Добавь туда еще помидоры\"\n\n"
            "📸 Или отправьте новое фото для следующего анализа."
        )
        
    except Exception as e:
        logger.error(f"Ошибка при анализе веса: {e}")
        await message.answer(
            "❌ Произошла ошибка при анализе. "
            "Попробуйте отправить фото заново."
        )
        await state.clear()

# Обработчики кнопок (должны быть ПЕРЕД общим обработчиком текста)
@router.message(F.text == "📊 Итоги дня")
@error_handler
async def daily_summary_button(message: Message):
    """Обработчик кнопки 'Итоги дня'"""
    from services.report_service import ReportService
    report_service = ReportService()
    
    try:
        await message.answer("📊 Генерирую отчет за день...")
        report = await report_service.generate_daily_report(message.from_user.id)
        await message.answer(report)
    except Exception as e:
        logger.error(f"Ошибка генерации дневного отчета: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.")

@router.message(F.text == "📈 Итоги недели")
@error_handler
async def weekly_summary_button(message: Message):
    """Обработчик кнопки 'Итоги недели'"""
    from services.report_service import ReportService
    report_service = ReportService()
    
    try:
        await message.answer("📊 Генерирую отчет за неделю...")
        report = await report_service.generate_weekly_report(message.from_user.id)
        await message.answer(report)
    except Exception as e:
        logger.error(f"Ошибка генерации недельного отчета: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.")

@router.message(F.text == "📸 Анализ еды")
@error_handler
async def food_analysis_button(message: Message):
    """Обработчик кнопки 'Анализ еды'"""
    await message.answer(
        "📸 Отправьте фото еды для анализа!\n\n"
        "Я проанализирую состав, рассчитаю КБЖУ и определю витамины.",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "ℹ️ Помощь")
@error_handler
async def help_button(message: Message):
    """Обработчик кнопки 'Помощь'"""
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
    await message.answer(help_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@router.message(F.text)
@error_handler
async def text_handler(message: Message):
    """Обработчик текстовых сообщений (коррекции анализа)"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли у пользователя недавний анализ для редактирования
    if analysis_storage.has_recent_analysis(user_id):
        # Получаем последний анализ
        last_analysis = analysis_storage.get_last_analysis(user_id)
        
        if last_analysis:
            await message.answer("🔄 Исправляю анализ с учетом ваших замечаний...")
            
            # Исправляем анализ через Gemini
            corrected_analysis = await gemini_service.correct_analysis(
                original_analysis=last_analysis['analysis_text'],
                user_correction=message.text
            )
            
            # Обновляем сохраненный анализ
            analysis_storage.update_analysis(user_id, corrected_analysis)
            
            # Форматируем и отправляем исправленный анализ
            formatted_response = format_nutrition_info(corrected_analysis)
            weight_info = f" ({last_analysis['weight']} г)" if last_analysis['weight'] else " (автоопределение веса)"
            final_response = f"🔄 Исправленный анализ{weight_info}:\n\n{formatted_response}"
            
            # Отправляем без Markdown чтобы избежать ошибок парсинга
            await message.answer(final_response)
            
            await message.answer(
                "✅ Анализ исправлен!\n\n"
                "💬 Нужны еще исправления? Просто напишите что изменить.\n"
                "📸 Или отправьте новое фото для анализа."
            )
            return
    
    # Если нет недавнего анализа, предлагаем отправить фото
    await message.answer(
        "📸 Пожалуйста, отправьте фото еды для анализа!\n\n"
        "💡 После анализа вы сможете исправить результат текстовыми сообщениями:\n"
        "• \"На фото не руккола, а шпинат\"\n"
        "• \"Вес не 300г, а 250г\"\n"
        "• \"Добавь туда морковь\""
    )


def register_handlers(dp):
    """Регистрирует все обработчики"""
    from commands import commands_router
    dp.include_router(router)
    dp.include_router(commands_router)
