import os
import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.gemini_service import GeminiService
from services.google_calendar import GoogleCalendarService
from services.analysis_storage import analysis_storage
from services.firebase_service import FirebaseService
from services.timezone_service import TimezoneService
from config import TEMP_DIR
from utils import error_handler, format_nutrition_info, extract_meal_title

logger = logging.getLogger(__name__)

# Состояния для FSM
class FoodAnalysisStates(StatesGroup):
    waiting_for_weight = State()

class TimezoneStates(StatesGroup):
    waiting_for_timezone = State()

# Создаем клавиатуру с кнопками
def get_main_keyboard():
    """Создает основную клавиатуру с кнопками"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Итоги дня"), KeyboardButton(text="📈 Итоги недели")],
            [KeyboardButton(text="📸 Анализ еды"), KeyboardButton(text="📅 Календарь")],
            [KeyboardButton(text="🌍 Часовой пояс"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

# Инициализируем сервисы
gemini_service = GeminiService()
calendar_service = GoogleCalendarService()
firebase_service = FirebaseService()
timezone_service = TimezoneService()

# Создаем роутер
router = Router()

@router.message(Command("start"))
@error_handler
async def start_handler(message: Message):
    """Обработчик команды /start"""
    # Сохраняем/обновляем информацию о пользователе
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    await firebase_service.create_or_update_user(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )
    
    welcome_text = """
🍽️ Добро пожаловать в бот анализа питания!

Отправьте фото вашей еды, и я:
• Определю состав блюда
• Рассчитаю КБЖУ и калории
• Укажу витамины и полезные вещества
• Сохраню информацию в Google Calendar

📅 Подключите Google Calendar через кнопку "📅 Календарь" для автоматического сохранения всех анализов!

Используйте кнопки ниже для быстрого доступа к функциям!
    """
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@router.message(F.photo)
@error_handler
async def photo_handler(message: Message, state: FSMContext):
    """Обработчик фото еды"""
    try:
        # Сохраняем/обновляем информацию о пользователе
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        
        await firebase_service.create_or_update_user(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        
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
            analysis_id = await firebase_service.save_analysis(user_id, analysis_data)
    
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
    
    # Пытаемся создать событие в Google Calendar (если подключен)
    event_id = None
    try:
        if calendar_service:
            title = extract_meal_title(analysis_result)
            success = await calendar_service.create_meal_event(
                user_id=user_id,
                title=title,
                description=formatted_response,
                event_time=callback.message.date
            )
            if success:
                # Получаем ID события из последнего созданного события
                # (это упрощенный подход, в реальности лучше возвращать ID из create_meal_event)
                event_id = "latest"  # Временное решение
    except Exception as e:
        logger.warning(f"Не удалось создать событие в календаре: {e}")

    # Очищаем состояние
    await state.clear()
    
    # Проверяем статус календаря и добавляем уведомление
    calendar_status = ""
    try:
        connected = await calendar_service.ensure_connected(callback.from_user.id)
        if connected:
            calendar_status = "\n✅ **Анализ сохранен в Google Calendar!**"
        else:
            calendar_status = "\n📅 **Подключите Google Calendar** (/gconnect) для автоматического сохранения анализов"
    except Exception as e:
        logger.warning(f"Не удалось проверить статус календаря: {e}")
        calendar_status = "\n📅 **Подключите Google Calendar** (/gconnect) для автоматического сохранения анализов"
    
    await callback.message.answer(
            f"✅ Анализ завершен!{calendar_status}\n\n"
            "💬 Если нужно что-то исправить, просто напишите текстом:\n"
            "• \"На фото не руккола, а листья салата\"\n"
            "• \"Вес не 450г, а 300г\"\n"
            "• \"Добавь туда еще помидоры\"\n\n"
            "📸 Или отправьте новое фото для следующего анализа.",
            parse_mode="Markdown"
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
        
        # Пытаемся создать событие в Google Calendar (если подключен)
        try:
            if calendar_service:
                title = extract_meal_title(analysis_result)
                await calendar_service.create_meal_event(
                    user_id=user_id,
                    title=title,
                    description=formatted_response,
                    event_time=callback.message.date
                )
        except Exception as e:
            logger.warning(f"Не удалось создать событие в календаре: {e}")

        # Удаляем временный файл
        try:
            os.remove(photo_path)
        except Exception as e:
            logger.warning(f"Не удалось удалить временный файл: {e}")
        
        # Очищаем состояние
        await state.clear()
        
        # Проверяем статус календаря и добавляем уведомление
        calendar_status = ""
        try:
            connected = await calendar_service.ensure_connected(message.from_user.id)
            if connected:
                calendar_status = "\n✅ **Анализ сохранен в Google Calendar!**"
            else:
                calendar_status = "\n📅 **Подключите Google Calendar** (/gconnect) для автоматического сохранения анализов"
        except Exception as e:
            logger.warning(f"Не удалось проверить статус календаря: {e}")
            calendar_status = "\n📅 **Подключите Google Calendar** (/gconnect) для автоматического сохранения анализов"
        
        await message.answer(
            f"✅ Анализ завершен!{calendar_status}\n\n"
            "💬 Если нужно что-то исправить, просто напишите текстом:\n"
            "• \"На фото не руккола, а листья салата\"\n"
            "• \"Вес не 450г, а 300г\"\n"
            "• \"Добавь туда еще помидоры\"\n\n"
            "📸 Или отправьте новое фото для следующего анализа.",
            parse_mode="Markdown"
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

@router.message(F.text == "📅 Календарь")
@error_handler
async def calendar_button(message: Message):
    """Обработчик кнопки 'Календарь'"""
    try:
        # Проверяем статус подключения календаря
        connected = await calendar_service.ensure_connected(message.from_user.id)
        
        if connected:
            await message.answer(
                "✅ **Google Calendar подключен!**\n\n"
                "📅 Все анализы еды автоматически сохраняются в ваш календарь питания.\n"
                "🔗 События создаются с подробной информацией о составе и КБЖУ.\n\n"
                "💡 **Команды:**\n"
                "• `/gstatus` - проверить статус\n"
                "• `/gdisconnect` - отключить календарь",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer(
                "📅 **Подключение Google Calendar**\n\n"
                "🔗 Для автоматического сохранения анализов еды в календарь:\n\n"
                "1. Нажмите /gconnect для подключения\n"
                "2. Авторизуйтесь в Google\n"
                "3. Разрешите доступ к календарю\n\n"
                "✅ После подключения все анализы будут сохраняться автоматически!",
                reply_markup=get_main_keyboard()
            )
    except Exception as e:
        logger.error(f"Ошибка при проверке статуса календаря: {e}")
        await message.answer(
            "❌ Не удалось проверить статус календаря. Попробуйте позже.",
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
/gconnect - Подключить Google Calendar
/gstatus - Статус Google Calendar
/gdisconnect - Отключить Google Calendar

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

# Обработчики команд должны быть ПЕРЕД общим обработчиком текста
@router.message(Command("day"))
@error_handler
async def day_command_handler(message: Message):
    """Обработчик команды /day - быстрый доступ к итогам дня"""
    from services.report_service import ReportService
    report_service = ReportService()
    
    try:
        await message.answer("📊 Генерирую отчет за день...")
        report = await report_service.generate_daily_report(message.from_user.id)
        await message.answer(report, reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error(f"Ошибка генерации дневного отчета: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.", reply_markup=get_main_keyboard())

@router.message(Command("week"))
@error_handler
async def week_command_handler(message: Message):
    """Обработчик команды /week - быстрый доступ к итогам недели"""
    from services.report_service import ReportService
    report_service = ReportService()
    
    try:
        await message.answer("📊 Генерирую отчет за неделю...")
        report = await report_service.generate_weekly_report(message.from_user.id)
        await message.answer(report, reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error(f"Ошибка генерации недельного отчета: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.", reply_markup=get_main_keyboard())

@router.message(Command("summary"))
@error_handler
async def summary_command_handler(message: Message):
    """Обработчик команды /summary - сводка питания"""
    # Получаем аргументы команды
    command_args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    from services.report_service import ReportService
    report_service = ReportService()
    
    try:
        if 'week' in command_args:
            await message.answer("📊 Генерирую отчет за неделю...")
            report = await report_service.generate_weekly_report(message.from_user.id)
        else:
            await message.answer("📊 Генерирую отчет за день...")
            report = await report_service.generate_daily_report(message.from_user.id)
        
        await message.answer(report, reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error(f"Ошибка генерации отчета: {e}")
        await message.answer("❌ Ошибка при генерации отчета. Попробуйте позже.", reply_markup=get_main_keyboard())

@router.message(Command("gconnect"))
@error_handler
async def gconnect_handler(message: Message):
    """Старт авторизации в Google Calendar"""
    try:
        auth_url = await calendar_service.get_auth_url(message.from_user.id)
        await message.answer(
            "Для подключения Google Calendar перейдите по ссылке и дайте доступ:",
        )
        await message.answer(auth_url)
    except Exception as e:
        logger.error(f"Ошибка запуска авторизации: {e}")
        await message.answer("❌ Не удалось начать авторизацию. Попробуйте позже.")

@router.message(Command("gstatus"))
@error_handler
async def gstatus_handler(message: Message):
    """Проверка статуса подключения Google Calendar"""
    try:
        connected = await calendar_service.ensure_connected(message.from_user.id)
        if connected:
            await message.answer("✅ Google Calendar подключен. События будут записываться в ваш календарь питания.")
        else:
            await message.answer("⚠️ Google Calendar не подключен. Отправьте /gconnect для подключения.")
    except Exception as e:
        logger.error(f"Ошибка статуса авторизации: {e}")
        await message.answer("❌ Не удалось получить статус. Попробуйте позже.")

@router.message(Command("gdisconnect"))
@error_handler
async def gdisconnect_handler(message: Message):
    """Отключение Google Calendar от аккаунта"""
    try:
        # Проверяем, подключен ли календарь
        connected = await calendar_service.ensure_connected(message.from_user.id)
        
        if not connected:
            await message.answer(
                "ℹ️ Google Calendar не подключен.\n\n"
                "Если хотите подключить календарь, используйте команду /gconnect"
            )
            return
        
        # Отключаем календарь
        success = await calendar_service.disconnect_calendar(message.from_user.id)
        
        if success:
            await message.answer(
                "✅ **Google Calendar отключен!**\n\n"
                "📅 Календарь больше не будет синхронизироваться с вашими анализами еды.\n"
                "🔗 Если захотите подключить снова, используйте команду /gconnect",
                parse_mode="Markdown"
            )
        else:
            await message.answer(
                "❌ Не удалось отключить Google Calendar. Попробуйте позже."
            )
    except Exception as e:
        logger.error(f"Ошибка отключения календаря: {e}")
        await message.answer("❌ Произошла ошибка при отключении календаря. Попробуйте позже.")

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
            
            # Пытаемся обновить событие в Google Calendar
            try:
                if calendar_service:
                    title = extract_meal_title(corrected_analysis)
                    # Для упрощения ищем последнее событие пользователя за сегодня
                    # В реальности лучше хранить event_id в analysis_storage
                    await calendar_service.update_latest_meal_event(
                        user_id=user_id,
                        title=title,
                        description=formatted_response
                    )
            except Exception as e:
                logger.warning(f"Не удалось обновить событие в календаре: {e}")
            
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


@router.message(F.text == "🌍 Часовой пояс")
@error_handler
async def timezone_handler(message: Message, state: FSMContext):
    """Обработчик настройки часового пояса"""
    timezones = timezone_service.get_common_timezones()
    
    # Создаем клавиатуру с часовыми поясами
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    # Добавляем по 2 часовых пояса в ряд
    for i in range(0, len(timezones), 2):
        row = []
        for j in range(2):
            if i + j < len(timezones):
                tz = timezones[i + j]
                tz_name = timezone_service.format_timezone_name(tz)
                row.append(InlineKeyboardButton(
                    text=tz_name,
                    callback_data=f"timezone_{tz}"
                ))
        keyboard.inline_keyboard.append(row)
    
    await message.answer(
        "🌍 Выберите ваш часовой пояс:\n\n"
        "Это поможет боту отправлять вам уведомления в 20:00 по вашему местному времени.",
        reply_markup=keyboard
    )
    await state.set_state(TimezoneStates.waiting_for_timezone)

@router.callback_query(F.data.startswith("timezone_"))
@error_handler
async def timezone_callback(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора часового пояса"""
    timezone = callback.data.replace("timezone_", "")
    user_id = callback.from_user.id
    
    # Сохраняем часовой пояс пользователя
    await firebase_service.create_or_update_user(
        user_id=user_id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name,
        timezone=timezone
    )
    
    tz_name = timezone_service.format_timezone_name(timezone)
    await callback.message.edit_text(
        f"✅ Часовой пояс установлен: {tz_name}\n\n"
        f"Теперь вы будете получать уведомления в 20:00 по вашему местному времени."
    )
    await state.clear()

def register_handlers(dp):
    """Регистрирует все обработчики"""
    from commands import commands_router
    dp.include_router(router)
    dp.include_router(commands_router)
