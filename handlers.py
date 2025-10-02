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
from services.subscription_service import SubscriptionService
from services.personal_goals_service import PersonalGoalsService
from services.export_service import ExportService
from config import TEMP_DIR
from utils import error_handler, format_nutrition_info, extract_meal_title

logger = logging.getLogger(__name__)

# Состояния для FSM
class FoodAnalysisStates(StatesGroup):
    waiting_for_weight = State()

class PersonalGoalStates(StatesGroup):
    waiting_for_goal_type = State()
    waiting_for_weight = State()
    waiting_for_height = State()
    waiting_for_age = State()
    waiting_for_activity = State()

# Создаем клавиатуру с кнопками
def get_main_keyboard():
    """Создает основную клавиатуру с кнопками"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Итоги дня"), KeyboardButton(text="📈 Итоги недели")],
            [KeyboardButton(text="📸 Анализ еды"), KeyboardButton(text="📅 Календарь")],
            [KeyboardButton(text="🎯 Цели"), KeyboardButton(text="⭐ Pro")],
            [KeyboardButton(text="📊 Статус"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

async def get_calendar_connect_keyboard(user_id: int):
    """Создает клавиатуру с кнопкой подключения Google Calendar"""
    try:
        auth_url = await calendar_service.get_auth_url(user_id)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Подключить Google Calendar", url=auth_url)]
        ])
        return keyboard
    except Exception as e:
        logger.error(f"Ошибка создания кнопки подключения календаря: {e}")
        return None

# Инициализируем сервисы
gemini_service = GeminiService()
calendar_service = GoogleCalendarService()
firebase_service = FirebaseService()
subscription_service = SubscriptionService()
personal_goals_service = PersonalGoalsService()
export_service = ExportService()

# Создаем роутер
router = Router()

# Обработчики команд с высоким приоритетом (должны быть ПЕРЕД FSM обработчиками)
@router.message(Command("cancel"))
@error_handler
async def cancel_handler(message: Message, state: FSMContext):
    """Отмена текущей операции и сброс состояния FSM"""
    await state.clear()
    await message.answer(
        "❌ Операция отменена.\n\n"
        "Вы можете начать заново или использовать команды бота.",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("gdisconnect"))
@error_handler
async def gdisconnect_handler(message: Message, state: FSMContext):
    """Отключение Google Calendar от аккаунта"""
    # Сбрасываем любое активное состояние FSM
    await state.clear()
    
    try:
        # Проверяем, подключен ли календарь
        connected = await calendar_service.ensure_connected(message.from_user.id)
        
        if not connected:
            keyboard = await get_calendar_connect_keyboard(message.from_user.id)
            await message.answer(
                "❌ Google Calendar не подключен.\n\n"
                "Подключите календарь для автоматической записи событий питания:",
                reply_markup=keyboard
            )
            return
        
        # Отключаем календарь
        await calendar_service.disconnect_user(message.from_user.id)
        await message.answer(
            "✅ Google Calendar отключен.\n\n"
            "События питания больше не будут записываться в ваш календарь.",
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Ошибка отключения календаря: {e}")
        await message.answer("❌ Не удалось отключить календарь. Попробуйте позже.")

@router.message(Command("help"))
@error_handler
async def help_handler(message: Message, state: FSMContext):
    """Обработчик команды /help - помощь по использованию"""
    # Сбрасываем любое активное состояние FSM
    await state.clear()
    
    help_text = """
🤖 **Календарь калорий - умный бот для анализа питания**

**📸 Основные функции:**
• Отправьте фото еды для анализа КБЖУ
• Получите информацию о витаминах и минералах
• Автоматическая запись в Google Calendar

**📊 Команды:**
• `/start` - запустить бота
• `/status` - статус подписки
• `/day` - итоги дня
• `/week` - итоги недели (Pro)
• `/summary` - сводка питания
• `/goals` - персональные цели (Pro)
• `/recommendations` - умные рекомендации (Pro)
• `/export` - экспорт отчетов (Pro)
• `/cancel` - отменить текущую операцию

**📅 Календарь:**
• `/gconnect` - подключить Google Calendar
• `/gstatus` - статус календаря
• `/gdisconnect` - отключить календарь

**⭐ Pro функции:**
• Неограниченные фото
• Персональные цели
• Умные рекомендации ИИ
• Экспорт отчетов
• История и аналитика

**🆘 Поддержка:**
Если возникли проблемы, используйте команду `/cancel` для сброса состояния.
    """
    
    await message.answer(help_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@router.message(Command("start"))
@error_handler
async def start_handler(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    # Сбрасываем любое активное состояние FSM
    await state.clear()
    
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
    
    # Получаем информацию о подписке пользователя
    user_subscription = await subscription_service.get_user_subscription(user_id)
    subscription_type = user_subscription.get('type', 'lite') if user_subscription else 'lite'

    # Формируем приветственное сообщение
    welcome_text = f"""
🤖 **Добро пожаловать в Календарь калорий!**

Привет, {first_name}! 👋

Я умный бот для анализа питания, который поможет вам:
• 📸 Анализировать еду по фото
• 📊 Считать калории, белки, жиры, углеводы
• 💊 Показывать витамины и минералы
• 📅 Записывать приемы пищи в Google Calendar

**Ваш статус:** {subscription_type.upper()}

**🚀 Как начать:**
1. Отправьте фото еды
2. Укажите примерный вес
3. Получите подробный анализ!

**💡 Совет:** Используйте команду `/help` для получения полного списка функций.
    """
    
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())
    
    # Определяем лимиты и возможности
    if subscription_type == 'lite':
        limit_text = "📊 **Lite (бесплатно)**: 5 фото в день, базовый анализ КБЖУ"
        upgrade_text = "\n💡 Хотите больше? Попробуйте Pro с мульти-тарелкой, витаминами и экспортом!"
    elif subscription_type in ['trial', 'pro']:
        limit_text = "⭐ **Pro**: До 200 фото в месяц + все возможности!"
        upgrade_text = ""
    else:
        limit_text = "📊 **Lite (бесплатно)**: 5 фото в день, базовый анализ КБЖУ"
        upgrade_text = "\n💡 Хотите больше? Попробуйте Pro с мульти-тарелкой, витаминами и экспортом!"
    
    welcome_text = f"""
🍽️ Добро пожаловать в бот анализа питания!

{limit_text}

Отправьте фото вашей еды, и я:
• Определю состав блюда
• Рассчитаю КБЖУ и калории
• Укажу витамины и полезные вещества (Pro)
• Сохраню информацию в Google Calendar (Pro)

📅 Подключите Google Calendar через кнопку "📅 Календарь" для автоматического сохранения всех анализов!

{upgrade_text}

Используйте кнопки ниже для быстрого доступа к функциям!
    """
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode='Markdown')

@router.message(F.photo)
@error_handler
async def photo_handler(message: Message, state: FSMContext):
    """Обработчик фото еды"""
    try:
        user_id = message.from_user.id
        
        # Проверяем лимиты подписки
        can_analyze, limit_message = await subscription_service.can_analyze_photo(user_id)
        if not can_analyze:
            # Получаем информацию о текущем использовании
            subscription = await subscription_service.get_user_subscription(user_id)
            daily_count = subscription.get('daily_photo_count', 0)
            
            # Показываем пейволл с более дружелюбным сообщением
            from handlers_payments import show_paywall
            await show_paywall(
                message,
                title="📸 Дневной лимит исчерпан",
                description=f"😊 Вы уже проанализировали {daily_count} фото сегодня!\n\n⏰ Лимит сбросится завтра в 00:00\n\n🌟 **Pro** снимет все ограничения:",
                features=[
                    "• До 200 фото в месяц",
                    "• Мульти-тарелка (несколько блюд)",
                    "• Детальные витамины и советы", 
                    "• Экспорт в PDF/CSV",
                    "• Google Calendar интеграция"
                ]
            )
            return
        
        # Сохраняем/обновляем информацию о пользователе
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
        
        # Проверяем доступность мульти-тарелки
        can_multi_dish, multi_message = await subscription_service.can_use_feature(user_id, "multi_dish")
        
        # Создаем клавиатуру с кнопками
        keyboard_buttons = [[InlineKeyboardButton(text="❓ Не знаю граммовку", callback_data="unknown_weight")]]
        
        if can_multi_dish:
            keyboard_buttons.append([InlineKeyboardButton(text="🍽️ Несколько блюд на фото", callback_data="multi_dish")])
        else:
            keyboard_buttons.append([InlineKeyboardButton(text="🌟 Мульти-тарелка (Pro)", callback_data="multi_dish_paywall")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await message.answer(
            "📸 Фото получено!\n\n"
            "Теперь укажите вес еды в граммах (например: 250)\n"
            "Или выберите опцию ниже:",
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

@router.callback_query(F.data == "multi_dish_paywall")
@error_handler
async def multi_dish_paywall_handler(callback: CallbackQuery):
    """Обработчик пейволла для мульти-тарелки"""
    await callback.answer()
    
    from handlers_payments import show_paywall
    await show_paywall(
        callback.message,
        title="🍽️ Мульти-тарелка доступна в Pro",
        description="Анализируйте несколько блюд на одном фото:",
        features=[
            "• Определение каждого блюда отдельно",
            "• КБЖУ для каждого продукта",
            "• Общий подсчет питательности",
            "• + все остальные функции Pro",
            "• 7 дней бесплатно для новых пользователей"
        ]
    )

@router.callback_query(F.data == "multi_dish")
@error_handler
async def multi_dish_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик анализа мульти-тарелки (только для Pro)"""
    await callback.answer()
    
    # Проверяем доступность функции
    can_use, message = await subscription_service.can_use_feature(callback.from_user.id, "multi_dish")
    if not can_use:
        from handlers_payments import show_paywall
        await show_paywall(
            callback.message,
            title="🍽️ Мульти-тарелка недоступна",
            description=message,
            features=[
                "• Анализ нескольких блюд одновременно",
                "• Детальный КБЖУ каждого продукта",
                "• Общая питательная ценность"
            ]
        )
        return
    
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
    await callback.message.answer("🔍 Анализирую фото с несколькими блюдами...")
    
    # Увеличиваем счетчик анализов
    await subscription_service.increment_photo_count(callback.from_user.id)
    
    # Анализируем через специальный метод для мульти-тарелки
    # TODO: Добавить специальный метод в gemini_service для мульти-тарелки
    analysis_result = await gemini_service.analyze_food_auto_weight(photo_path)
    
    # Сохраняем анализ
    user_id = callback.from_user.id
    analysis_storage.store_analysis(
        user_id=user_id,
        analysis_text=analysis_result,
        image_path=photo_path,
        weight=None,
        is_multi_dish=True
    )
    
    # Сохраняем в Firebase
    analysis_data = {
        'analysis_text': analysis_result,
        'weight': 'multi_dish',
        'user_id': str(user_id),
        'is_multi_dish': True
    }
    await firebase_service.save_analysis(user_id, analysis_data)
    
    # Форматируем ответ
    formatted_response = format_nutrition_info(analysis_result)
    final_response = f"🍽️ **Мульти-тарелка анализ:**\n\n{formatted_response}"
    
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
        "✅ **Мульти-анализ завершен!**\n\n"
        "🍽️ Проанализированы все блюда на фото\n"
        "💬 Исправления: просто напишите текстом\n"
        "📸 Или отправьте новое фото",
        parse_mode="Markdown"
    )
    
    # Проверяем статус календаря и добавляем уведомление
    # Проверяем статус подключения календаря
    try:
        connected = await calendar_service.ensure_connected(callback.from_user.id)
        if connected:
            calendar_status = "\n✅ **Анализ сохранен в Google Calendar!**"
            await callback.message.answer(
                f"✅ Анализ завершен!{calendar_status}\n\n"
                "💬 Если нужно что-то исправить, просто напишите текстом:\n"
                "• \"На фото не руккола, а листья салата\"\n"
                "• \"Вес не 450г, а 300г\"\n"
                "• \"Добавь туда еще помидоры\"\n\n"
                "📸 Или отправьте новое фото для следующего анализа.",
                parse_mode="Markdown"
            )
        else:
            calendar_status = "\n📅 **Подключите Google Calendar** для автоматического сохранения анализов"
            keyboard = await get_calendar_connect_keyboard(callback.from_user.id)
            await callback.message.answer(
                f"✅ Анализ завершен!{calendar_status}\n\n"
                "💬 Если нужно что-то исправить, просто напишите текстом:\n"
                "• \"На фото не руккола, а листья салата\"\n"
                "• \"Вес не 450г, а 300г\"\n"
                "• \"Добавь туда еще помидоры\"\n\n"
                "📸 Или отправьте новое фото для следующего анализа.",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
    except Exception as e:
        logger.warning(f"Не удалось проверить статус календаря: {e}")
        calendar_status = "\n📅 **Подключите Google Calendar** для автоматического сохранения анализов"
        keyboard = await get_calendar_connect_keyboard(callback.from_user.id)
        await callback.message.answer(
            f"✅ Анализ завершен!{calendar_status}\n\n"
            "💬 Если нужно что-то исправить, просто напишите текстом:\n"
            "• \"На фото не руккола, а листья салата\"\n"
            "• \"Вес не 450г, а 300г\"\n"
            "• \"Добавь туда еще помидоры\"\n\n"
            "📸 Или отправьте новое фото для следующего анализа.",
            parse_mode="Markdown",
            reply_markup=keyboard
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
        
        # Увеличиваем счетчик анализов
        await subscription_service.increment_photo_count(message.from_user.id)
        
        # Анализируем еду через Gemini
        analysis_result = await gemini_service.analyze_food(photo_path, weight)
        
        # Получаем информацию о подписке для адаптации ответа
        subscription = await subscription_service.get_user_subscription(message.from_user.id)
        subscription_type = subscription['type']
        
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
                'user_id': str(user_id),
                'subscription_type': subscription_type
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
        try:
            connected = await calendar_service.ensure_connected(message.from_user.id)
            if connected:
                calendar_status = "\n✅ **Анализ сохранен в Google Calendar!**"
                    # Адаптивное сообщение в зависимости от подписки
                if subscription_type == "lite":
                    # Показываем счетчик и рекламу Pro
                    daily_count = subscription['daily_photo_count']
                    remaining = 5 - daily_count
                    
                    pro_teaser = ""
                    if remaining <= 2:
                        pro_teaser = f"\n\n🌟 **Осталось {remaining} анализов сегодня**\n" \
                                   "• Pro: до 200 фото/мес + мульти-тарелка\n" \
                                   "• Команда /pro для подробностей"
                    elif daily_count == 1:
                        # Показываем "вау-эффект" после первого анализа
                        pro_teaser = "\n\n✨ **Понравился анализ?**\n" \
                                   "🌟 В Pro: детальные витамины, экспорт, календарь\n" \
                                   "🚀 Первые 7 дней бесплатно: /pro"
                    elif daily_count == 0:
                        # Мотивация для первого анализа
                        pro_teaser = "\n\n🎯 **Начните путь к здоровому питанию!**\n" \
                                   "📸 Анализируйте еду и следите за прогрессом"
                    
                    await message.answer(
                        f"✅ Анализ завершен!{calendar_status}{pro_teaser}\n\n"
                        "💬 Если нужно что-то исправить, просто напишите текстом:\n"
                        "• \"На фото не руккола, а листья салата\"\n"
                        "• \"Вес не 450г, а 300г\"\n\n"
                        "📸 Или отправьте новое фото для анализа.",
                        parse_mode="Markdown"
                    )
                else:
                    # Pro/Trial пользователи
                    await message.answer(
                        f"✅ Анализ завершен!{calendar_status}\n\n"
                        "💬 Если нужно что-то исправить, просто напишите текстом:\n"
                        "• \"На фото не руккола, а листья салата\"\n"
                        "• \"Вес не 450г, а 300г\"\n"
                        "• \"Добавь туда еще помидоры\"\n\n"
                        "📸 Или отправьте новое фото для следующего анализа.",
                        parse_mode="Markdown"
                    )
            else:
                calendar_status = "\n📅 **Подключите Google Calendar** для автоматического сохранения анализов"
                keyboard = await get_calendar_connect_keyboard(message.from_user.id)
                
                # Адаптивное сообщение в зависимости от подписки
                if subscription_type == "lite":
                    # Показываем счетчик и рекламу Pro
                    daily_count = subscription['daily_photo_count']
                    remaining = 5 - daily_count
                    
                    pro_teaser = ""
                    if remaining <= 2:
                        pro_teaser = f"\n\n🌟 **Осталось {remaining} анализов сегодня**\n" \
                                   "• Pro: до 200 фото/мес + мульти-тарелка\n" \
                                   "• Команда /pro для подробностей"
                    elif daily_count == 1:
                        # Показываем "вау-эффект" после первого анализа
                        pro_teaser = "\n\n✨ **Понравился анализ?**\n" \
                                   "🌟 В Pro: детальные витамины, экспорт, календарь\n" \
                                   "🚀 Первые 7 дней бесплатно: /pro"
                    
                    await message.answer(
                        f"✅ Анализ завершен!{calendar_status}{pro_teaser}\n\n"
                        "💬 Если нужно что-то исправить, просто напишите текстом:\n"
                        "• \"На фото не руккола, а листья салата\"\n"
                        "• \"Вес не 450г, а 300г\"\n\n"
                        "📸 Или отправьте новое фото для анализа.",
                        parse_mode="Markdown",
                        reply_markup=keyboard
                    )
                else:
                    # Pro/Trial пользователи
                    await message.answer(
                        f"✅ Анализ завершен!{calendar_status}\n\n"
                        "💬 Если нужно что-то исправить, просто напишите текстом:\n"
                        "• \"На фото не руккола, а листья салата\"\n"
                        "• \"Вес не 450г, а 300г\"\n"
                        "• \"Добавь туда еще помидоры\"\n\n"
                        "📸 Или отправьте новое фото для следующего анализа.",
                        parse_mode="Markdown",
                        reply_markup=keyboard
                    )
        except Exception as e:
            logger.warning(f"Не удалось проверить статус календаря: {e}")
            calendar_status = "\n📅 **Подключите Google Calendar** для автоматического сохранения анализов"
            keyboard = await get_calendar_connect_keyboard(message.from_user.id)
            
            # Адаптивное сообщение в зависимости от подписки
            if subscription_type == "lite":
                # Показываем счетчик и рекламу Pro
                daily_count = subscription['daily_photo_count']
                remaining = 5 - daily_count
                
                pro_teaser = ""
                if remaining <= 2:
                    pro_teaser = f"\n\n🌟 **Осталось {remaining} анализов сегодня**\n" \
                               "• Pro: до 200 фото/мес + мульти-тарелка\n" \
                               "• Команда /pro для подробностей"
                elif daily_count == 1:
                    # Показываем "вау-эффект" после первого анализа
                    pro_teaser = "\n\n✨ **Понравился анализ?**\n" \
                               "🌟 В Pro: детальные витамины, экспорт, календарь\n" \
                               "🚀 Первые 7 дней бесплатно: /pro"
                
                await message.answer(
                    f"✅ Анализ завершен!{calendar_status}{pro_teaser}\n\n"
                    "💬 Если нужно что-то исправить, просто напишите текстом:\n"
                    "• \"На фото не руккола, а листья салата\"\n"
                    "• \"Вес не 450г, а 300г\"\n\n"
                    "📸 Или отправьте новое фото для анализа.",
                    parse_mode="Markdown",
                    reply_markup=keyboard
                )
            else:
                # Pro/Trial пользователи
                await message.answer(
                    f"✅ Анализ завершен!{calendar_status}\n\n"
                    "💬 Если нужно что-то исправить, просто напишите текстом:\n"
                    "• \"На фото не руккола, а листья салата\"\n"
                    "• \"Вес не 450г, а 300г\"\n"
                    "• \"Добавь туда еще помидоры\"\n\n"
                    "📸 Или отправьте новое фото для следующего анализа.",
                    parse_mode="Markdown",
                    reply_markup=keyboard
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
    # Проверяем доступность полных отчетов
    subscription = await subscription_service.get_user_subscription(message.from_user.id)
    
    if subscription['type'] == 'lite':
        from handlers_payments import show_paywall
        await show_paywall(
            message,
            title="📈 Полные отчеты в Pro",
            description="Lite: только краткий отчет за день\n\n🌟 **Pro** открывает:",
            features=[
                "• Подробные отчеты за неделю",
                "• Анализ трендов питания",
                "• Рекомендации по улучшению",
                "• Экспорт в PDF/CSV",
                "• История без ограничений"
            ]
        )
        return
    
    from services.report_service import ReportService
    report_service = ReportService()
    
    try:
        await message.answer("📊 Генерирую полный отчет за неделю...")
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
    # Проверяем доступность календарной интеграции
    subscription = await subscription_service.get_user_subscription(message.from_user.id)
    
    if subscription['type'] == 'lite':
        from handlers_payments import show_paywall
        await show_paywall(
            message,
            title="📅 Google Calendar в Pro",
            description="Автосохранение всех анализов в календарь\n\n🌟 **Pro** подключает:",
            features=[
                "• Автосохранение каждого анализа",
                "• Создание календаря питания",
                "• Напоминания о приемах пищи",
                "• Синхронизация на всех устройствах",
                "• Долгосрочная история питания"
            ]
        )
        return
    
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
            # Получаем ссылку для авторизации
            try:
                auth_url = await calendar_service.get_auth_url(message.from_user.id)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔗 Подключить Google Calendar", url=auth_url)]
                ])
                
                await message.answer(
                    "📅 **Подключение Google Calendar**\n\n"
                    "🔗 Для автоматического сохранения анализов еды в календарь нажмите кнопку ниже:\n\n"
                    "✅ После подключения все анализы будут сохраняться автоматически!",
                    parse_mode="Markdown",
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.error(f"Ошибка получения ссылки авторизации: {e}")
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

@router.message(F.text == "⭐ Pro")
@error_handler
async def pro_button(message: Message):
    """Обработчик кнопки 'Pro'"""
    # Используем тот же обработчик, что и для команды /pro
    await pro_handler(message)

@router.message(F.text == "📊 Статус")
@error_handler
async def status_button(message: Message):
    """Обработчик кнопки 'Статус'"""
    # Используем тот же обработчик, что и для команды /status
    await status_handler(message)

@router.message(F.text == "ℹ️ Помощь")
@error_handler
async def help_button(message: Message):
    """Обработчик кнопки 'Помощь'"""
    help_text = """
🤖 **Помощь по использованию бота**

**Основные команды:**
/start - Запустить бота
/help - Показать эту справку
/status - Мой статус подписки
/pro - Информация о Pro подписке
/day - Итоги дня (быстрый доступ)
/week - Итоги недели (Pro)
/summary - Итоги дня
/summary week - Итоги недели (Pro)
/goals - Персональные цели (Pro)
/recommendations - Умные рекомендации (Pro)
📅 - Подключить Google Calendar (Pro)
/gstatus - Статус Google Calendar
/gdisconnect - Отключить Google Calendar

**Тарифные планы:**
📊 **Lite (бесплатно)**: 5 фото в день, базовый анализ КБЖУ
⭐ **Pro (399₽/мес)**: 200 фото в месяц, мульти-тарелка, витамины, экспорт, персональные цели
💎 **Pro Год (2990₽)**: Все функции Pro со скидкой 50%

**Как использовать:**
1. 📸 Отправьте фото еды
2. 🔢 Укажите вес в граммах
3. 📊 Получите анализ КБЖУ
4. 🎯 Установите персональную цель (Pro)
5. 🤖 Получайте умные рекомендации (Pro)
6. 📅 Информация сохранится в календаре (Pro)

**Поддерживаемые форматы:**
• Фото в формате JPG, PNG
• Вес от 1 до 5000 грамм
• Любые блюда и продукты

**Что анализирует бот:**
• Состав блюда
• Калории и КБЖУ
• Витамины и полезные вещества (Pro)
• Пищевую ценность
• Персональные рекомендации (Pro)

Если возникли проблемы, попробуйте отправить фото заново.
    """
    await message.answer(help_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@router.message(F.text == "🎯 Цели")
@error_handler
async def goals_button(message: Message):
    """Обработчик кнопки 'Цели'"""
    await goals_handler(message)

@router.message(Command("goals"))
@error_handler
async def goals_handler(message: Message):
    """Обработчик команды /goals - персональные цели"""
    user_id = message.from_user.id
    
    # Проверяем доступность функции
    can_use, message_text = await personal_goals_service.can_use_personal_goals(user_id)
    if not can_use:
        from handlers_payments import show_paywall
        await show_paywall(
            message,
            title="🎯 Персональные цели в Pro",
            description="Установите цель и получайте умные рекомендации!\n\n🌟 **Pro** добавляет:",
            features=[
                "• Персональные цели (похудение, набор массы, поддержание)",
                "• Расчет дневной нормы калорий",
                "• Умные рекомендации ИИ",
                "• Отслеживание прогресса",
                "• Советы по БЖУ под вашу цель"
            ]
        )
        return
    
    # Получаем текущую цель
    goal = await personal_goals_service.get_user_goal(user_id)
    
    if goal:
        # Показываем текущую цель
        goal_type_names = {
            "weight_loss": "📉 Похудение",
            "weight_gain": "📈 Набор веса", 
            "maintenance": "⚖️ Поддержание веса",
            "muscle_gain": "💪 Набор мышц",
            "health_improvement": "🏥 Улучшение здоровья"
        }
        
        goal_name = goal_type_names.get(goal['goal_type'], goal['goal_type'])
        daily_calories = goal.get('daily_calories', 2000)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Мой прогресс", callback_data="show_goal_progress")],
            [InlineKeyboardButton(text="🤖 Получить рекомендации", callback_data="get_recommendations")],
            [InlineKeyboardButton(text="✏️ Изменить цель", callback_data="change_goal")],
            [InlineKeyboardButton(text="❌ Удалить цель", callback_data="delete_goal")]
        ])
        
        await message.answer(
            f"🎯 **Ваша персональная цель**\n\n"
            f"**Тип цели:** {goal_name}\n"
            f"**Дневная норма калорий:** {daily_calories} ккал\n"
            f"**Текущий вес:** {goal.get('current_weight', 'не указан')} кг\n"
            f"**Целевой вес:** {goal.get('target_weight', 'не указан')} кг\n"
            f"**Установлена:** {goal.get('goal_set_at', {}).strftime('%d.%m.%Y') if goal.get('goal_set_at') else 'неизвестно'}\n\n"
            f"💡 Используйте кнопки ниже для управления целью!",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        # Предлагаем установить цель
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📉 Похудение", callback_data="set_goal_weight_loss")],
            [InlineKeyboardButton(text="📈 Набор веса", callback_data="set_goal_weight_gain")],
            [InlineKeyboardButton(text="⚖️ Поддержание", callback_data="set_goal_maintenance")],
            [InlineKeyboardButton(text="💪 Набор мышц", callback_data="set_goal_muscle_gain")],
            [InlineKeyboardButton(text="🏥 Улучшение здоровья", callback_data="set_goal_health_improvement")]
        ])
        
        await message.answer(
            "🎯 **Персональные цели**\n\n"
            "Установите персональную цель для получения умных рекомендаций!\n\n"
            "**Что вы получите:**\n"
            "• Расчет дневной нормы калорий\n"
            "• Персональные рекомендации ИИ\n"
            "• Советы по БЖУ под вашу цель\n"
            "• Отслеживание прогресса\n\n"
            "Выберите вашу цель:",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

@router.callback_query(F.data.startswith("set_goal_"))
@error_handler
async def set_goal_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик установки цели"""
    await callback.answer()
    
    goal_type = callback.data.replace("set_goal_", "")
    
    # Сохраняем тип цели в состоянии
    await state.update_data(goal_type=goal_type)
    await state.set_state(PersonalGoalStates.waiting_for_weight)
    
    await callback.message.edit_text(
        "🎯 **Установка персональной цели**\n\n"
        f"**Выбранная цель:** {goal_type}\n\n"
        "Теперь укажите ваш текущий вес в килограммах (например: 70):",
        parse_mode="Markdown"
    )

@router.message(PersonalGoalStates.waiting_for_weight)
@error_handler
async def goal_weight_handler(message: Message, state: FSMContext):
    """Обработчик веса для цели"""
    try:
        weight = float(message.text.strip())
        if weight <= 0 or weight > 300:
            await message.answer("❌ Пожалуйста, введите корректный вес от 1 до 300 кг")
            return
        
        await state.update_data(current_weight=weight)
        await state.set_state(PersonalGoalStates.waiting_for_height)
        
        await message.answer(
            "✅ Вес сохранен!\n\n"
            "Теперь укажите ваш рост в сантиметрах (например: 175):"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите вес числом (например: 70)")

@router.message(PersonalGoalStates.waiting_for_height)
@error_handler
async def goal_height_handler(message: Message, state: FSMContext):
    """Обработчик роста для цели"""
    try:
        height = float(message.text.strip())
        if height <= 0 or height > 250:
            await message.answer("❌ Пожалуйста, введите корректный рост от 1 до 250 см")
            return
        
        await state.update_data(height=height)
        await state.set_state(PersonalGoalStates.waiting_for_age)
        
        await message.answer(
            "✅ Рост сохранен!\n\n"
            "Теперь укажите ваш возраст в годах (например: 25):"
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите рост числом (например: 175)")

@router.message(PersonalGoalStates.waiting_for_age)
@error_handler
async def goal_age_handler(message: Message, state: FSMContext):
    """Обработчик возраста для цели"""
    try:
        age = int(message.text.strip())
        if age <= 0 or age > 120:
            await message.answer("❌ Пожалуйста, введите корректный возраст от 1 до 120 лет")
            return
        
        await state.update_data(age=age)
        await state.set_state(PersonalGoalStates.waiting_for_activity)
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛋️ Малоподвижный", callback_data="activity_sedentary")],
            [InlineKeyboardButton(text="🚶 Легкая активность", callback_data="activity_light")],
            [InlineKeyboardButton(text="🏃 Умеренная активность", callback_data="activity_moderate")],
            [InlineKeyboardButton(text="💪 Высокая активность", callback_data="activity_active")],
            [InlineKeyboardButton(text="🔥 Очень высокая", callback_data="activity_very_active")]
        ])
        
        await message.answer(
            "✅ Возраст сохранен!\n\n"
            "Выберите ваш уровень физической активности:",
            reply_markup=keyboard
        )
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите возраст числом (например: 25)")

@router.callback_query(F.data.startswith("activity_"))
@error_handler
async def goal_activity_handler(callback: CallbackQuery, state: FSMContext):
    """Обработчик уровня активности"""
    await callback.answer()
    
    activity_map = {
        "activity_sedentary": "sedentary",
        "activity_light": "light", 
        "activity_moderate": "moderate",
        "activity_active": "active",
        "activity_very_active": "very_active"
    }
    
    activity_level = activity_map[callback.data]
    
    # Получаем все данные из состояния
    data = await state.get_data()
    
    # Устанавливаем цель
    success = await personal_goals_service.set_user_goal(
        user_id=callback.from_user.id,
        goal_type=data['goal_type'],
        current_weight=data['current_weight'],
        height=data['height'],
        age=data['age'],
        activity_level=activity_level
    )
    
    if success:
        goal = await personal_goals_service.get_user_goal(callback.from_user.id)
        daily_calories = goal.get('daily_calories', 2000)
        
        await callback.message.edit_text(
            f"🎉 **Цель установлена!**\n\n"
            f"✅ Персональная цель настроена\n"
            f"📊 Дневная норма калорий: {daily_calories} ккал\n\n"
            f"🤖 Теперь вы будете получать умные рекомендации!\n"
            f"📸 Анализируйте еду и следите за прогрессом!",
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            "❌ **Ошибка установки цели**\n\n"
            "Попробуйте установить цель заново через команду /goals"
        )
    
    await state.clear()

@router.message(Command("recommendations"))
@error_handler
async def recommendations_handler(message: Message):
    """Обработчик команды /recommendations - умные рекомендации"""
    user_id = message.from_user.id
    
    # Проверяем доступность функции
    can_use, message_text = await personal_goals_service.can_use_personal_goals(user_id)
    if not can_use:
        from handlers_payments import show_paywall
        await show_paywall(
            message,
            title="🤖 Умные рекомендации в Pro",
            description="Получайте персональные советы по питанию!\n\n🌟 **Pro** включает:",
            features=[
                "• Анализ вашего питания",
                "• Рекомендации под вашу цель",
                "• Советы по БЖУ",
                "• Мотивационные сообщения"
            ]
        )
        return
    
    # Получаем дневное питание
    today = datetime.now().strftime('%Y-%m-%d')
    analyses = await firebase_service.get_daily_analyses(user_id, today)
    
    if not analyses:
        await message.answer(
            "📊 **Нет данных за сегодня**\n\n"
            "Проанализируйте хотя бы одно блюдо, чтобы получить рекомендации!",
            parse_mode="Markdown"
        )
        return
    
    # Агрегируем питание за день
    daily_nutrition = await firebase_service.aggregate_daily_nutrition(analyses)
    
    # Генерируем рекомендации
    await message.answer("🤖 Генерирую персональные рекомендации...")
    recommendations = await personal_goals_service.generate_smart_recommendations(
        user_id, daily_nutrition
    )
    
    await message.answer(recommendations, parse_mode="Markdown")

@router.message(Command("export"))
@error_handler
async def export_handler(message: Message):
    """Обработчик команды /export - экспорт отчетов"""
    user_id = message.from_user.id
    
    # Проверяем доступность функции
    can_export, message_text = await export_service.can_use_export(user_id)
    if not can_export:
        from handlers_payments import show_paywall
        await show_paywall(
            message,
            title="📊 Экспорт отчетов в Pro",
            description="Сохраняйте и делитесь отчетами!\n\n🌟 **Pro** включает:",
            features=[
                "• Экспорт в CSV (таблица данных)",
                "• Красивые PDF отчеты",
                "• Ссылки для шаринга с врачом/тренером",
                "• Отчеты за любой период"
            ]
        )
        return
    
    # Получаем варианты экспорта
    export_options = await export_service.get_export_options(user_id)
    
    if not export_options["available"]:
        await message.answer(f"❌ {export_options['message']}")
        return
    
    # Создаем клавиатуру с вариантами экспорта
    keyboard_buttons = []
    for option in export_options["options"]:
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"{option['icon']} {option['name']}",
                callback_data=f"export_{option['type']}"
            )
        ])
    
    keyboard_buttons.append([
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_export")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer(
        "📊 **Экспорт отчетов**\n\n"
        "Выберите формат экспорта:\n\n"
        "📊 **CSV** - таблица с данными для Excel\n"
        "📄 **PDF** - красивый отчет с графиками\n"
        "🔗 **Поделиться** - ссылка для отправки врачу/тренеру",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("export_"))
@error_handler
async def export_callback_handler(callback: CallbackQuery):
    """Обработчик экспорта через callback"""
    await callback.answer()
    
    export_type = callback.data.replace("export_", "")
    user_id = callback.from_user.id
    
    if export_type == "csv":
        await callback.message.edit_text("📊 Генерирую CSV файл...")
        
        csv_data = await export_service.generate_csv_report(user_id, 7)
        
        if csv_data:
            # Отправляем CSV файл
            from aiogram.types import BufferedInputFile
            
            csv_content = csv_data.getvalue()
            csv_file = BufferedInputFile(
                csv_content.encode('utf-8'),
                filename=f"nutrition_report_{datetime.now().strftime('%Y%m%d')}.csv"
            )
            
            await callback.message.answer_document(
                document=csv_file,
                caption="📊 **CSV отчет готов!**\n\n"
                       "Файл содержит все ваши анализы за последние 7 дней.\n"
                       "Можете открыть в Excel или Google Sheets.",
                parse_mode="Markdown"
            )
        else:
            await callback.message.edit_text(
                "❌ **Ошибка генерации CSV**\n\n"
                "Не удалось создать отчет. Попробуйте позже."
            )
    
    elif export_type == "pdf":
        await callback.message.edit_text("📄 Генерирую PDF отчет...")
        
        pdf_data = await export_service.generate_pdf_report(user_id, 7)
        
        if pdf_data:
            # Отправляем PDF файл
            from aiogram.types import BufferedInputFile
            
            pdf_file = BufferedInputFile(
                pdf_data,
                filename=f"nutrition_report_{datetime.now().strftime('%Y%m%d')}.html"
            )
            
            await callback.message.answer_document(
                document=pdf_file,
                caption="📄 **PDF отчет готов!**\n\n"
                       "Красивый отчет с вашими данными за последние 7 дней.\n"
                       "Можете сохранить или отправить врачу/тренеру.",
                parse_mode="Markdown"
            )
        else:
            await callback.message.edit_text(
                "❌ **Ошибка генерации PDF**\n\n"
                "Не удалось создать отчет. Попробуйте позже."
            )
    
    elif export_type == "share":
        await callback.message.edit_text("🔗 Создаю ссылку для шаринга...")
        
        share_link = await export_service.generate_shareable_link(user_id, "weekly")
        
        if share_link:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔗 Открыть отчет", url=share_link)],
                [InlineKeyboardButton(text="📤 Поделиться", callback_data="share_report")]
            ])
            
            await callback.message.edit_text(
                f"🔗 **Ссылка для шаринга готова!**\n\n"
                f"**Ссылка:** {share_link}\n\n"
                f"📤 Можете отправить эту ссылку:\n"
                f"• Врачу для консультации\n"
                f"• Тренеру для анализа питания\n"
                f"• Нутрициологу для рекомендаций\n\n"
                f"💡 Ссылка действительна 30 дней",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            await callback.message.edit_text(
                "❌ **Ошибка создания ссылки**\n\n"
                "Не удалось создать ссылку для шаринга. Попробуйте позже."
            )

@router.callback_query(F.data == "cancel_export")
@error_handler
async def cancel_export_handler(callback: CallbackQuery):
    """Отмена экспорта"""
    await callback.answer()
    
    await callback.message.edit_text(
        "❌ **Экспорт отменен**\n\n"
        "Можете вернуться к экспорту через команду /export",
        parse_mode="Markdown"
    )

@router.message(Command("status"))
@error_handler
async def status_handler(message: Message):
    """Обработчик команды /status - показать статус подписки"""
    user_id = message.from_user.id
    
    # Получаем информацию о подписке
    user_subscription = await subscription_service.get_user_subscription(user_id)
    subscription_type = user_subscription.get('type', 'lite') if user_subscription else 'lite'
    
    # Проверяем, использовал ли пользователь уже пробный период
    user_data = await firebase_service.get_user_info(user_id)
    trial_used = user_data.get('trial_used', False) if user_data else False
    
    # Получаем статистику использования
    if subscription_type == 'lite':
        daily_count = await subscription_service.get_daily_photo_count(user_id)
        remaining_daily = 5 - daily_count
        
        status_text = f"""
📊 **Ваш статус подписки**

🎯 **Текущий план:** Lite (бесплатно)
⏳ **Осталось сегодня:** {remaining_daily} анализов
📅 **Сброс лимита:** завтра в 00:00

**Доступные функции:**
✅ Базовый анализ КБЖУ
✅ Краткий дневной отчет
✅ История 7 дней
✅ Исправление результатов

**Ограничения:**
❌ Мульти-тарелка
❌ Детальные витамины
❌ Экспорт в PDF/CSV
❌ Google Calendar интеграция
❌ Недельные отчеты

💡 **Хотите больше?** Используйте команду /pro
        """
        
        # Добавляем кнопки для апгрейда
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        keyboard_buttons = []
        
        # Добавляем кнопку пробного периода только если пользователь его еще не использовал
        if not trial_used:
            keyboard_buttons.append([InlineKeyboardButton(text="⭐ Попробовать Pro бесплатно", callback_data="start_pro_trial")])
        
        keyboard_buttons.extend([
            [InlineKeyboardButton(text="💎 Купить Pro (399₽/мес)", callback_data="buy_pro_monthly")],
            [InlineKeyboardButton(text="🏆 Pro Год (2990₽, -50%)", callback_data="buy_pro_annual")]
        ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
    elif subscription_type == 'trial':
        end_date = user_subscription.get('end_date')
        daily_count = await subscription_service.get_daily_photo_count(user_id)
        monthly_count = await subscription_service.get_monthly_photo_count(user_id)
        
        status_text = f"""
⭐ **Ваш статус подписки**

🎯 **Текущий план:** Pro Trial (7 дней бесплатно)
📅 **Истекает:** {end_date.strftime('%d.%m.%Y %H:%M') if end_date else 'Неизвестно'}
📊 **Использовано в месяце:** {monthly_count}/200 анализов

**Доступные функции:**
✅ До 200 фото в месяц
✅ Мульти-тарелка
✅ Детальные витамины + советы
✅ Google Calendar интеграция
✅ Экспорт в PDF/CSV
✅ Недельные отчеты
✅ Приоритетная очередь

🚀 **Продлите подписку** для продолжения после триала!
        """
        
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Продлить Pro (399₽/мес)", callback_data="buy_pro_monthly")],
            [InlineKeyboardButton(text="🏆 Pro Год (2990₽, -50%)", callback_data="buy_pro_annual")]
        ])
        
    elif subscription_type == 'pro':
        end_date = user_subscription.get('end_date')
        daily_count = await subscription_service.get_daily_photo_count(user_id)
        monthly_count = await subscription_service.get_monthly_photo_count(user_id)
        
        status_text = f"""
⭐ **Ваш статус подписки**

🎯 **Текущий план:** Pro
📅 **Активен до:** {end_date.strftime('%d.%m.%Y %H:%M') if end_date else 'Бессрочно'}
📊 **Использовано в месяце:** {monthly_count}/200 анализов

**Доступные функции:**
✅ До 200 фото в месяц
✅ Мульти-тарелка
✅ Детальные витамины + советы
✅ Google Calendar интеграция
✅ Экспорт в PDF/CSV
✅ Недельные отчеты
✅ Приоритетная очередь

🎉 **Вы используете все возможности Pro!**
        """
        
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💎 Продлить Pro (399₽/мес)", callback_data="buy_pro_monthly")],
            [InlineKeyboardButton(text="🏆 Перейти на Pro Год (-50%)", callback_data="buy_pro_annual")]
        ])
    
    else:
        status_text = """
❓ **Статус подписки неизвестен**

Попробуйте использовать команду /start для инициализации.
        """
        keyboard = None
    
    await message.answer(status_text, parse_mode="Markdown", reply_markup=keyboard)

@router.message(Command("pro"))
@error_handler
async def pro_handler(message: Message):
    """Обработчик команды /pro - информация о Pro подписке"""
    user_id = message.from_user.id
    
    # Проверяем статус подписки пользователя
    subscription = await subscription_service.get_user_subscription(user_id)
    subscription_type = subscription.get('type', 'lite') if subscription else 'lite'
    
    # Проверяем, использовал ли пользователь уже пробный период
    user_data = await firebase_service.get_user_info(user_id)
    trial_used = user_data.get('trial_used', False) if user_data else False
    
    pro_text = """
⭐ **Pro подписка - все возможности бота**

🎯 **Что входит в Pro:**
✅ До 200 фото в месяц (vs 5 в день в Lite)
✅ Мульти-тарелка (несколько блюд на фото)
✅ Детальные витамины и микронутриенты
✅ Умные советы по питанию
✅ Полные отчеты за неделю
✅ Экспорт в PDF и CSV
✅ Google Calendar интеграция
✅ Приоритетная очередь обработки
✅ Неограниченная история

💰 **Тарифы:**
💎 **Pro Месяц:** 399₽/месяц
🏆 **Pro Год:** 2990₽/год (скидка 50%!)
    """
    
    # Добавляем информацию о пробном периоде только если пользователь его еще не использовал
    if subscription_type != 'trial' and not trial_used:
        pro_text += "⭐ **Пробный период:** 7 дней бесплатно\n\n"
    
    pro_text += "🚀 **Попробуйте прямо сейчас!**"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    # Формируем клавиатуру в зависимости от статуса пользователя
    keyboard_buttons = []
    
    # Добавляем кнопку пробного периода только если пользователь его еще не использовал
    if subscription_type != 'trial' and not trial_used:
        keyboard_buttons.append([InlineKeyboardButton(text="⭐ 7 дней Pro бесплатно", callback_data="start_pro_trial")])
    
    keyboard_buttons.extend([
        [InlineKeyboardButton(text="💎 Pro Месяц (399₽)", callback_data="buy_pro_monthly")],
        [InlineKeyboardButton(text="🏆 Pro Год (2990₽, -50%)", callback_data="buy_pro_annual")],
        [InlineKeyboardButton(text="📊 Мой статус", callback_data="show_status")]
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await message.answer(pro_text, parse_mode="Markdown", reply_markup=keyboard)

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
    # Проверяем доступность полных отчетов
    subscription = await subscription_service.get_user_subscription(message.from_user.id)
    
    if subscription['type'] == 'lite':
        from handlers_payments import show_paywall
        await show_paywall(
            message,
            title="📈 Команда /week доступна в Pro",
            description="В Lite доступны только дневные отчеты\n\n🌟 **Pro** разблокирует:",
            features=[
                "• Команды /week и /summary week",
                "• Детальная аналитика за период",
                "• Трекинг прогресса",
                "• Экспорт данных"
            ]
        )
        return
    
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
    
    # Проверяем доступность недельных отчетов
    if 'week' in command_args:
        subscription = await subscription_service.get_user_subscription(message.from_user.id)
        if subscription['type'] == 'lite':
            from handlers_payments import show_paywall
            await show_paywall(
                message,
                title="📊 /summary week в Pro",
                description="В Lite: только /summary (день)\n\n🌟 **Pro** добавляет:",
                features=[
                    "• /summary week - недельная сводка",
                    "• Детальная аналитика трендов",
                    "• Сравнение с предыдущими периодами",
                    "• Рекомендации по питанию"
                ]
            )
            return
    
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
        
        # Создаем кнопку с ссылкой
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Подключить Google Calendar", url=auth_url)]
        ])
        
        await message.answer(
            "📅 **Подключение Google Calendar**\n\n"
            "🔗 Нажмите кнопку ниже для авторизации в Google и предоставления доступа к календарю:\n\n"
            "✅ После подключения все анализы еды будут автоматически сохраняться в ваш календарь!",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
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
            keyboard = await get_calendar_connect_keyboard(message.from_user.id)
            await message.answer(
                "⚠️ **Google Calendar не подключен**\n\n"
                "🔗 Нажмите кнопку ниже для подключения календаря:",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
    except Exception as e:
        logger.error(f"Ошибка статуса авторизации: {e}")
        await message.answer("❌ Не удалось получить статус. Попробуйте позже.")

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
    # Получаем информацию о подписке для показа лимитов
    user_subscription = await subscription_service.get_user_subscription(user_id)
    subscription_type = user_subscription.get('type', 'lite') if user_subscription else 'lite'
    
    # Определяем информацию о лимитах
    if subscription_type == 'lite':
        # Получаем количество использованных анализов за день
        daily_count = await subscription_service.get_daily_photo_count(user_id)
        remaining = 5 - daily_count
        if remaining > 0:
            limit_info = f"📊 **Lite**: Осталось {remaining} анализов сегодня (из 5)"
        else:
            limit_info = f"📊 **Lite**: Лимит исчерпан ({daily_count}/5 фото)\n⏰ Сбросится завтра в 00:00"
    elif subscription_type in ['trial', 'pro']:
        # Получаем количество использованных анализов за месяц
        monthly_count = await subscription_service.get_monthly_photo_count(user_id)
        remaining = 200 - monthly_count
        limit_info = f"⭐ **Pro**: Осталось {remaining} анализов в месяце (из 200)"
    else:
        limit_info = "📊 **Lite**: 5 фото в день бесплатно"
    
    # Создаем клавиатуру если лимит исчерпан
    keyboard = None
    if subscription_type == 'lite':
        daily_count = await subscription_service.get_daily_photo_count(user_id)
        if daily_count >= 5:
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🌟 Обновиться до Pro", callback_data="show_paywall")]
            ])
    
    await message.answer(
        f"📸 Пожалуйста, отправьте фото еды для анализа!\n\n"
        f"{limit_info}\n\n"
        "💡 После анализа вы сможете исправить результат текстовыми сообщениями:\n"
        "• \"На фото не руккола, а шпинат\"\n"
        "• \"Вес не 300г, а 250г\"\n"
        "• \"Добавь туда морковь\"",
        reply_markup=keyboard
    )

def register_handlers(dp):
    """Регистрирует все обработчики"""
    from commands import commands_router
    from handlers_payments import payments_router
    dp.include_router(router)
    dp.include_router(payments_router)
    dp.include_router(commands_router)
