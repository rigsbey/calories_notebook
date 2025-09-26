#!/bin/bash

# Скрипт деплоя лендинга на сервер
set -e

echo "🚀 Начинаем деплой лендинга..."

# Переменные
SERVER="german_server"
REMOTE_PATH="/opt/calories-landing"
LOCAL_PATH="$(pwd)"

# Проверяем подключение к серверу
echo "📡 Проверяем подключение к серверу..."
ssh $SERVER "echo 'Подключение к серверу успешно'"

# Создаем директорию на сервере
echo "📁 Создаем директорию на сервере..."
ssh $SERVER "mkdir -p $REMOTE_PATH"

# Копируем файлы на сервер
echo "📤 Копируем файлы на сервер..."
rsync -avz --delete \
  --exclude 'node_modules' \
  --exclude '.nuxt' \
  --exclude '.output' \
  --exclude '.git' \
  --exclude '*.log' \
  $LOCAL_PATH/ $SERVER:$REMOTE_PATH/

# Устанавливаем зависимости и собираем на сервере
echo "🔨 Устанавливаем зависимости и собираем проект..."
ssh $SERVER "cd $REMOTE_PATH && npm install && npm run build"

# Останавливаем старый контейнер
echo "🛑 Останавливаем старый контейнер..."
ssh $SERVER "cd $REMOTE_PATH && docker-compose down || true"

# Запускаем новый контейнер
echo "▶️ Запускаем новый контейнер..."
ssh $SERVER "cd $REMOTE_PATH && docker-compose up -d --build"

# Проверяем статус
echo "✅ Проверяем статус контейнера..."
ssh $SERVER "cd $REMOTE_PATH && docker-compose ps"

# Проверяем доступность сайта
echo "🌐 Проверяем доступность сайта..."
sleep 10
if curl -f -s "https://calories.toxiguard.site" > /dev/null; then
    echo "✅ Сайт доступен!"
else
    echo "❌ Сайт недоступен. Проверьте логи:"
    ssh $SERVER "cd $REMOTE_PATH && docker-compose logs"
fi

echo "🎉 Деплой завершен!"
