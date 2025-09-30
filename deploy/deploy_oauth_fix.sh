#!/bin/bash
# Скрипт для деплоя исправлений OAuth scopes

set -e

echo "🚀 Деплой исправлений OAuth scopes на сервер..."

# Проверяем подключение к серверу
if ! ssh -o ConnectTimeout=10 german_server "echo 'Connected to server'"; then
    echo "❌ Не удается подключиться к серверу german_server"
    echo "Проверьте SSH конфигурацию в ~/.ssh/config"
    exit 1
fi

echo "📁 Создаем директории и копируем обновленные файлы на сервер..."

# Создаем необходимые директории на сервере
ssh german_server "mkdir -p /opt/calories-bot/{services,templates}"

# Копируем обновленные файлы бота
scp services/google_calendar.py german_server:/opt/calories-bot/services/
scp templates/oauth_callback.html german_server:/opt/calories-bot/templates/

echo "📝 Обновляем лендинг с новой политикой конфиденциальности..."

# Сначала собираем лендинг локально
cd landing
npm run build
cd ..

# Копируем обновленные файлы лендинга
scp landing/.output/public/privacy/index.html german_server:/opt/calories-bot/privacy/
scp landing/.output/public/index.html german_server:/opt/calories-bot/landing.html

echo "🐳 Перезапускаем контейнеры с обновленным кодом..."

# Перезапускаем основной бот
ssh german_server << 'EOF'
cd /opt/calories-bot

# Останавливаем старый контейнер
docker-compose -f docker-compose.prod.yml down || true

# Запускаем новый контейнер с обновленным кодом
docker-compose -f docker-compose.prod.yml up -d

# Проверяем статус
docker-compose -f docker-compose.prod.yml ps
EOF

# Перезапускаем лендинг
ssh german_server << 'EOF'
cd /opt/calories-bot

# Останавливаем старый контейнер лендинга
docker-compose -f docker-compose.landing.yml down 2>/dev/null || true

# Запускаем новый
docker-compose -f docker-compose.landing.yml up -d

# Проверяем статус
docker ps | grep calories-landing
EOF

echo "⏳ Ждем запуска сервисов..."
sleep 10

echo "🔍 Проверяем статус сервисов..."

# Проверяем логи бота
ssh german_server "cd /opt/calories-bot && docker-compose -f docker-compose.prod.yml logs --tail 20"

echo ""
echo "✅ Деплой исправлений OAuth завершен!"
echo ""
echo "📋 Что было обновлено:"
echo "   • OAuth scopes: убран избыточный 'calendar' scope"
echo "   • Остался только 'calendar.events' для создания событий"
echo "   • Обновлена политика конфиденциальности"
echo "   • Обновлен лендинг с информацией о безопасности"
echo ""
echo "🌐 Проверьте работу:"
echo "   • Бот: https://t.me/caloriesnote_bot"
echo "   • Лендинг: https://calories.toxiguard.site"
echo "   • OAuth callback: https://api.toxiguard.site/oauth2callback"
echo ""
echo "🧪 Для тестирования OAuth:"
echo "   1. Отправьте /calendar в бота"
echo "   2. Проверьте, что запрашивается только создание событий"
echo "   3. Убедитесь, что нет доступа к просмотру календарей"
