#!/usr/bin/env python3
"""
Тестирование основных компонентов бота
"""
import os
import sys
import asyncio
from config import BOT_TOKEN, OPENAI_API_KEY

def test_config():
    """Тестирует конфигурацию"""
    print("🔍 Проверка конфигурации...")
    
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN не настроен")
        return False
    else:
        print(f"✅ BOT_TOKEN: {BOT_TOKEN[:10]}...")
    
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY не настроен")
        return False
    else:
        print(f"✅ OPENAI_API_KEY: {OPENAI_API_KEY[:10]}...")
    
    return True

def test_imports():
    """Тестирует импорты"""
    print("\n🔍 Проверка импортов...")
    
    try:
        from services.openai_service import OpenAIService
        print("✅ OpenAI сервис импортирован")
    except Exception as e:
        print(f"❌ Ошибка импорта OpenAI сервиса: {e}")
        return False
    
    try:
        from services.google_calendar import GoogleCalendarService
        print("✅ Google Calendar сервис импортирован")
    except Exception as e:
        print(f"❌ Ошибка импорта Google Calendar сервиса: {e}")
        return False
    
    try:
        import handlers
        print("✅ Обработчики импортированы")
    except Exception as e:
        print(f"❌ Ошибка импорта обработчиков: {e}")
        return False
    
    return True

async def test_openai_service():
    """Тестирует OpenAI сервис"""
    print("\n🔍 Проверка OpenAI сервиса...")
    
    try:
        from services.openai_service import OpenAIService
        service = OpenAIService()
        print("✅ OpenAI сервис инициализирован")
        
        # Проверяем наличие клиента
        if hasattr(service, 'client') and service.client:
            print("✅ OpenAI клиент создан")
        else:
            print("❌ OpenAI клиент не создан")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Ошибка инициализации OpenAI сервиса: {e}")
        return False

def test_directories():
    """Проверяет наличие необходимых директорий"""
    print("\n🔍 Проверка директорий...")
    
    directories = ['temp_photos', 'logs', 'services']
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ Директория {directory} существует")
        else:
            print(f"❌ Директория {directory} не найдена")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ Директория {directory} создана")
            except Exception as e:
                print(f"❌ Не удалось создать директорию {directory}: {e}")
                return False
    
    return True

async def main():
    print("🧪 Тестирование компонентов бота")
    print("=" * 40)
    
    tests = [
        ("Конфигурация", test_config),
        ("Директории", test_directories),
        ("Импорты", test_imports),
        ("OpenAI сервис", test_openai_service),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
            
        except Exception as e:
            print(f"❌ Ошибка в тесте '{name}': {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Бот готов к запуску.")
        print("Запустите: python bot.py")
    else:
        print("⚠️  Некоторые тесты не прошли. Проверьте конфигурацию.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
