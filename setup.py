#!/usr/bin/env python3
"""
Скрипт для первоначальной настройки бота
"""
import os
import sys

def create_env_file():
    """Создает .env файл если его нет"""
    env_path = ".env"
    
    if os.path.exists(env_path):
        print("✅ Файл .env уже существует")
        return True
    
    print("📝 Создание .env файла...")
    
    bot_token = input("Введите Telegram Bot Token (получите у @BotFather): ").strip()
    if not bot_token:
        print("❌ Токен бота обязателен!")
        return False
    
    # OpenAI ключ (не используется, оставляем пустым)
    openai_key = "your_openai_api_key_here"
    
    env_content = f"""# Telegram Bot Token
BOT_TOKEN={bot_token}

# OpenAI API Key
OPENAI_API_KEY={openai_key}

# Google Calendar API credentials file path
GOOGLE_CREDENTIALS_PATH=credentials.json
"""
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Файл .env создан успешно!")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания .env файла: {e}")
        return False

def check_dependencies():
    """Проверяет установленные зависимости"""
    print("🔍 Проверка зависимостей...")
    
    required_packages = [
        'aiogram',
        'python-dotenv',
        'openai',
        'google-api-python-client',
        'Pillow',
        'aiofiles'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("Установите их командой: pip install -r requirements.txt")
        return False
    
    print("✅ Все зависимости установлены!")
    return True

def create_directories():
    """Создает необходимые директории"""
    directories = ['temp_photos', 'logs']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Создана папка: {directory}")

def main():
    print("🚀 Настройка Telegram-бота для анализа питания")
    print("=" * 50)
    
    # Создаем директории
    create_directories()
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    # Создаем .env файл
    if not create_env_file():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Настройка завершена!")
    print("\n📋 Следующие шаги:")
    print("1. Для Google Calendar API:")
    print("   - Создайте проект в Google Cloud Console")
    print("   - Включите Calendar API")
    print("   - Скачайте credentials.json в корень проекта")
    print("\n2. Запустите бота:")
    print("   python bot.py")
    print("\n3. Отправьте боту команду /start для проверки")

if __name__ == "__main__":
    main()
