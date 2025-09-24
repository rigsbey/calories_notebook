#!/usr/bin/env python3

import os
import asyncio
from services.google_calendar import GoogleCalendarService

async def test_html_pages():
    """Тестирует загрузку HTML страниц"""
    print("🧪 Тестирование HTML страниц OAuth callback...")
    
    service = GoogleCalendarService()
    
    # Тестируем загрузку успешной страницы
    try:
        success_html = await service._load_html_template('oauth_callback.html')
        print(f"✅ Страница успеха загружена ({len(success_html)} символов)")
        print(f"   Содержит 'Google Calendar подключен': {'Google Calendar подключен' in success_html}")
    except Exception as e:
        print(f"❌ Ошибка загрузки страницы успеха: {e}")
    
    # Тестируем загрузку страницы ошибки
    try:
        error_html = await service._load_html_template('oauth_error.html')
        print(f"✅ Страница ошибки загружена ({len(error_html)} символов)")
        print(f"   Содержит 'Ошибка подключения': {'Ошибка подключения' in error_html}")
    except Exception as e:
        print(f"❌ Ошибка загрузки страницы ошибки: {e}")
    
    # Проверяем существование файлов
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    success_file = os.path.join(templates_dir, 'oauth_callback.html')
    error_file = os.path.join(templates_dir, 'oauth_error.html')
    
    print(f"\n📁 Проверка файлов:")
    print(f"   oauth_callback.html: {'✅' if os.path.exists(success_file) else '❌'}")
    print(f"   oauth_error.html: {'✅' if os.path.exists(error_file) else '❌'}")
    
    print("\n🎉 Тестирование завершено!")

if __name__ == "__main__":
    asyncio.run(test_html_pages())
