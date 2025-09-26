#!/bin/bash
# Скрипт деплоя лендинга на сервер

set -e

echo "🚀 Деплой лендинга на сервер..."

# Проверяем подключение к серверу
if ! ssh -o ConnectTimeout=10 german_server "echo 'Connected to server'"; then
    echo "❌ Не удается подключиться к серверу german_server"
    echo "Проверьте SSH конфигурацию в ~/.ssh/config"
    exit 1
fi

echo "📁 Копируем файлы лендинга на сервер..."

# Копируем файлы нового лендинга из .output/public
scp landing/.output/public/index.html german_server:/opt/calories-bot/landing.html
scp landing/.output/public/robots.txt german_server:/opt/calories-bot/robots.txt
scp -r landing/.output/public/_nuxt german_server:/opt/calories-bot/
scp -r landing/.output/public/images german_server:/opt/calories-bot/
scp -r landing/.output/public/blog german_server:/opt/calories-bot/
scp landing/.output/public/favicon.ico german_server:/opt/calories-bot/
scp landing/.output/public/favicon.png german_server:/opt/calories-bot/
scp landing/.output/public/logo.jpg german_server:/opt/calories-bot/
scp sitemap.xml german_server:/opt/calories-bot/
scp nginx.conf german_server:/opt/calories-bot/
scp docker-compose.landing.yml german_server:/opt/calories-bot/

echo "🐳 Запускаем nginx контейнер на сервере..."

# Запускаем nginx контейнер
ssh german_server << 'EOF'
cd /opt/calories-bot

# Останавливаем старый контейнер если есть
docker-compose -f docker-compose.landing.yml down 2>/dev/null || true

# Запускаем новый
docker-compose -f docker-compose.landing.yml up -d

# Проверяем статус
docker ps | grep calories-landing
EOF

echo "✅ Лендинг развернут!"
echo "🌐 Доступен по адресу: http://your-server-ip"
echo "📝 Для настройки домена и SSL:"
echo "   1. Настройте DNS на IP сервера"
echo "   2. Добавьте SSL сертификаты в папку ssl/"
echo "   3. Перезапустите контейнер"
