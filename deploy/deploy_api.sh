#!/bin/bash

echo "🚀 Деплой API сервера на сервер..."

# Копируем файлы API сервера
echo "📁 Копируем файлы API сервера на сервер..."
scp nginx-api.conf german_server:/opt/calories-bot/
scp docker-compose.api.yml german_server:/opt/calories-bot/

echo "🐳 Запускаем API nginx контейнер на сервере..."

# Запускаем API nginx контейнер
ssh german_server << 'EOF'
cd /opt/calories-bot

# Останавливаем старый контейнер если есть
docker-compose -f docker-compose.api.yml down || true

# Запускаем новый контейнер
docker-compose -f docker-compose.api.yml up -d

# Проверяем статус
docker-compose -f docker-compose.api.yml ps

echo "✅ API сервер развернут!"
echo "🌐 Доступен по адресу: http://api.toxiguard.site:8080"
echo "📝 OAuth callback: http://api.toxiguard.site:8080/oauth2callback"
EOF

echo "✅ Деплой API сервера завершен!"
