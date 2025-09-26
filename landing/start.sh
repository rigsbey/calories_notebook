#!/bin/bash

# Скрипт для запуска лендинга
set -e

echo "🚀 Запускаем лендинг Calories Bot..."

# Проверяем наличие node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 Устанавливаем зависимости..."
    npm install
fi

# Проверяем режим запуска
if [ "$1" = "dev" ]; then
    echo "🔧 Запускаем в режиме разработки..."
    npm run dev
elif [ "$1" = "build" ]; then
    echo "🔨 Собираем проект..."
    npm run build
    echo "✅ Сборка завершена!"
elif [ "$1" = "preview" ]; then
    echo "👀 Запускаем предварительный просмотр..."
    npm run preview
else
    echo "🔧 Запускаем в режиме разработки..."
    echo "Доступные команды:"
    echo "  ./start.sh dev     - режим разработки"
    echo "  ./start.sh build   - сборка проекта"
    echo "  ./start.sh preview - предварительный просмотр"
    echo ""
    npm run dev
fi
