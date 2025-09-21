import os
import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Any

def setup_logging():
    """Настройка системы логирования"""
    # Создаем папку для логов
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Настройка формата логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Настройка логирования в файл
    log_filename = os.path.join(log_dir, f"bot_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # Вывод в консоль
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
    
    for line in lines:
        if 'ВИТАМИНЫ И МИНЕРАЛЫ' in line.upper():
            formatted_lines.append("📊 ВИТАМИНЫ И МИНЕРАЛЫ (% от нормы)")
            formatted_lines.append("")
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
                
                # Форматируем строку с выравниванием
                formatted_line = f"{emoji} {vitamin_name:<13} {bar}   {percentage}%"
                formatted_lines.append(formatted_line)
                continue
        
        # Если вышли из раздела витаминов
        if in_vitamins_section and line.strip() and not line.strip().startswith('-'):
            in_vitamins_section = False
        
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def format_nutrition_info(analysis_text: str) -> str:
    """Форматирование информации о питании для красивого отображения"""
    if not analysis_text:
        return "❌ Не удалось получить информацию о питании"
    
    # Добавляем эмодзи для лучшего восприятия
    formatted = analysis_text
    
    # Заменяем стандартные маркеры на эмодзи
    replacements = {
        'Калории:': '🔥 Калории:',
        'Белки:': '🥩 Белки:',
        'Жиры:': '🥑 Жиры:',
        'Углеводы:': '🍞 Углеводы:',
        'ПРОДУКТЫ:': '🍽️ ПРОДУКТЫ:',
        'ПИЩЕВАЯ ЦЕННОСТЬ': '📊 ПИЩЕВАЯ ЦЕННОСТЬ',
        'ПРИМЕРНЫЙ ВЕС:': '⚖️ ПРИМЕРНЫЙ ВЕС:'
    }
    
    for old, new in replacements.items():
        formatted = formatted.replace(old, new)
    
    # Форматируем раздел витаминов с инфографикой
    formatted = format_vitamins_section(formatted)
    
    return formatted
