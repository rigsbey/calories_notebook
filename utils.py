import os
import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Any

def setup_logging():
    """Настройка системы логирования"""
    # Настройка формата логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Настройка логирования только в консоль (без файла)
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler()  # Только вывод в консоль
        ]
    )
    
    # Отключаем избыточное логирование некоторых библиотек
    logging.getLogger('aiogram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)

def error_handler(func: Callable) -> Callable:
    """Декоратор для обработки ошибок в обработчиках"""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(func.__module__)
            logger.error(f"Ошибка в функции {func.__name__}: {e}", exc_info=True)
            
            # Если есть message в аргументах, отправляем пользователю сообщение об ошибке
            for arg in args:
                if hasattr(arg, 'answer'):  # Это объект Message
                    await arg.answer(
                        "❌ Произошла ошибка. Попробуйте позже или обратитесь к администратору."
                    )
                    break
    return wrapper

def clean_temp_files(directory: str, max_age_hours: int = 24):
    """Очистка старых временных файлов"""
    logger = logging.getLogger(__name__)
    
    if not os.path.exists(directory):
        return
    
    current_time = datetime.now().timestamp()
    cleaned_count = 0
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getctime(file_path)
                if file_age > max_age_hours * 3600:  # Конвертируем часы в секунды
                    os.remove(file_path)
                    cleaned_count += 1
        
        if cleaned_count > 0:
            logger.info(f"Очищено {cleaned_count} старых временных файлов")
            
    except Exception as e:
        logger.error(f"Ошибка при очистке временных файлов: {e}")

def create_vitamin_bar(percentage: int) -> str:
    """Создает цветной прогресс-бар для витамина"""
    if percentage <= 0:
        return "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜"
    elif percentage >= 100:
        return "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩"
    
    # Рассчитываем количество заполненных блоков (максимум 10 блоков)
    filled_blocks = int((percentage / 100) * 10)
    empty_blocks = 10 - filled_blocks
    
    return "🟩" * filled_blocks + "⬜" * empty_blocks

def get_vitamin_emoji(vitamin_name: str) -> str:
    """Возвращает эмодзи для витамина или минерала"""
    vitamin_emojis = {
        'витамин c': '🍊',
        'витамин a': '🥕', 
        'витамин k': '🌿',
        'витамин e': '🌰',
        'витамин d': '☀️',
        'витамин b12': '🥩',
        'витамин b6': '🐟',
        'фолиевая кислота': '🥬',
        'калий': '🍌',
        'кальций': '🥛',
        'магний': '🌰',
        'железо': '🥩',
        'цинк': '🦪',
        'фосфор': '🐟',
        'натрий': '🧂',
        'марганец': '🌱'
    }
    
    vitamin_lower = vitamin_name.lower()
    for key, emoji in vitamin_emojis.items():
        if key in vitamin_lower:
            return emoji
    
    return '💊'  # По умолчанию

def format_vitamins_section(text: str) -> str:
    """Форматирует раздел витаминов с инфографикой"""
    lines = text.split('\n')
    formatted_lines = []
    
    in_vitamins_section = False
    vitamin_lines = []  # Собираем все строки витаминов для обработки
    
    for line in lines:
        if 'ВИТАМИНЫ И МИНЕРАЛЫ' in line.upper():
            formatted_lines.append("📊 ВИТАМИНЫ И МИНЕРАЛЫ (% от нормы)")
            formatted_lines.append("")  # Пустая строка для отступа
            in_vitamins_section = True
            continue
        
        if in_vitamins_section and line.strip().startswith('-'):
            # Парсим строку витамина
            import re
            match = re.search(r'- ([^:]+):\s*(\d+)%', line)
            if match:
                vitamin_name = match.group(1).strip()
                percentage = int(match.group(2))
                
                emoji = get_vitamin_emoji(vitamin_name)
                bar = create_vitamin_bar(percentage)
                
                # Сохраняем данные витамина для последующего форматирования
                vitamin_lines.append((emoji, vitamin_name, bar, percentage))
                continue
        
        # Если вышли из раздела витаминов
        if in_vitamins_section and line.strip() and not line.strip().startswith('-'):
            # Форматируем все витамины в моноширинном блоке с эмодзи
            if vitamin_lines:
                formatted_lines.append("```")
                for emoji, name, bar, percent in vitamin_lines:
                    # Форматируем витамины в одну строку для мобильных устройств
                    formatted_lines.append(f"{emoji} {name}: {bar} {percent}%")
                formatted_lines.append("```")
                formatted_lines.append("")
                vitamin_lines = []
            
            in_vitamins_section = False
        
        formatted_lines.append(line)
    
    # Если файл закончился в разделе витаминов
    if vitamin_lines:
        formatted_lines.append("```")
        for emoji, name, bar, percent in vitamin_lines:
            # Форматируем витамины в одну строку для мобильных устройств
            formatted_lines.append(f"{emoji} {name}: {bar} {percent}%")
        formatted_lines.append("```")
    
    return '\n'.join(formatted_lines)

def format_nutrition_info(analysis_text: str) -> str:
    """Форматирование информации о питании для красивого отображения"""
    if not analysis_text:
        return "❌ Не удалось получить информацию о питании"
    
    # Добавляем эмодзи для лучшего восприятия
    formatted = analysis_text
    
    # Заменяем стандартные маркеры на эмодзи и добавляем отступы
    replacements = {
        'Калории:': '🔥 Калории:',
        'Белки:': '🥩 Белки:',
        'Жиры:': '🥑 Жиры:',
        'Углеводы:': '🍞 Углеводы:',
        'ПРОДУКТЫ:': '🍽️ ПРОДУКТЫ:',
        'ПИЩЕВАЯ ЦЕННОСТЬ': '\n📊 ПИЩЕВАЯ ЦЕННОСТЬ',  # Добавляем отступ сверху
        'ПРИМЕРНЫЙ ВЕС:': '⚖️ ПРИМЕРНЫЙ ВЕС:'
    }
    
    for old, new in replacements.items():
        formatted = formatted.replace(old, new)
    
    # Форматируем раздел витаминов с инфографикой
    formatted = format_vitamins_section(formatted)
    
    return formatted

def extract_meal_title(analysis_text: str) -> str:
    """Извлекает краткое название блюда из текста анализа."""
    try:
        text = analysis_text or ""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if not lines:
            return "Прием пищи"
        
        # Ищем раздел продуктов
        for i, line in enumerate(lines):
            if 'ПРОДУКТЫ' in line.upper():
                # Берем следующую строку после "ПРОДУКТЫ"
                if i + 1 < len(lines):
                    products_line = lines[i + 1]
                    # Извлекаем основные продукты из описания
                    products = _extract_main_products(products_line)
                    if products:
                        return products
                break
        
        # Если не нашли продукты, ищем в первой строке
        first_line = lines[0]
        if len(first_line) > 10:  # Не слишком короткая строка
            return _extract_main_products(first_line) or "Прием пищи"
        
        return "Прием пищи"
    except Exception:
        return "Прием пищи"

def _extract_main_products(text: str) -> str:
    """Извлекает основные продукты из текста."""
    text = text.lower()
    
    # Словарь основных продуктов
    products = {
        'крекеры': 'Крекеры',
        'хлеб': 'Хлеб', 
        'салат': 'Салат',
        'суп': 'Суп',
        'паста': 'Паста',
        'макароны': 'Макароны',
        'рис': 'Рис',
        'картофель': 'Картофель',
        'курица': 'Курица',
        'мясо': 'Мясо',
        'рыба': 'Рыба',
        'яйца': 'Яйца',
        'сыр': 'Сыр',
        'йогурт': 'Йогурт',
        'творог': 'Творог',
        'фрукты': 'Фрукты',
        'овощи': 'Овощи',
        'каша': 'Каша',
        'омлет': 'Омлет',
        'бутерброд': 'Бутерброд',
        'пицца': 'Пицца',
        'бургер': 'Бургер',
        'сэндвич': 'Сэндвич',
        'мамалыга': 'Мамалыга',
        'помидоры': 'Помидоры',
        'масло': 'Масло',
        'петрушка': 'Петрушка'
    }
    
    # Ищем основные продукты
    found_products = []
    for key, value in products.items():
        if key in text:
            found_products.append(value)
    
    if found_products:
        # Возвращаем до 2 основных продуктов
        return ', '.join(found_products[:2])
    
    # Если не нашли конкретные продукты, берем первые слова (но не технические)
    words = text.split()
    # Фильтруем технические слова
    filtered_words = []
    skip_words = {
        'примерный', 'вес', 'г', 'на', 'фото', 'не', 'знаю', 'граммовку', 'анализ', 'завершен',
        'обновленный', 'анализ', 'продукты', 'пищевая', 'ценность', 'витамины', 'минералы',
        'нормы', 'калории', 'белки', 'жиры', 'углеводы', 'приготовленная', 'воде', 'возможно',
        'небольшим', 'количеством', 'масла', 'подсолнечное', 'кукурузное', 'мамалыга', 'кукурузная',
        'каша', 'каши', 'пюре', 'нута', 'хумус', 'ломтика', 'помидора', 'помидоров', 'веточка',
        'петрушки', 'украшения', 'полито', 'маслом', 'скорее', 'всего', 'оливковым'
    }
    
    for word in words[:6]:  # Берем до 6 слов
        clean_word = word.strip('.,!?()[]{}":;').lower()
        if (clean_word and 
            clean_word not in skip_words and 
            len(clean_word) > 2 and 
            not clean_word.isdigit() and  # Исключаем числа
            not clean_word.endswith('г')):  # Исключаем "250г"
            filtered_words.append(clean_word.title())
    
    if filtered_words:
        return ' '.join(filtered_words[:3])  # Максимум 3 слова
    
    return None
