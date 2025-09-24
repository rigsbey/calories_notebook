#!/bin/bash
# Скрипт для тестирования деплоя локально

set -e

echo "🚀 Тестирование деплоя на сервере..."

# Создаем директории если их нет
ssh german_server "mkdir -p /opt/calories-bot/{logs,temp_photos}"

# Переходим в рабочую директорию
ssh german_server "cd /opt/calories-bot"

# Создаем .env файл с секретами
ssh german_server "cat > /opt/calories-bot/.env << 'EOF'
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
FIREBASE_CREDENTIALS_PATH=caloriesbot-949dd-firebase-adminsdk-fbsvc-4ecc1b1ad9.json
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_OAUTH_REDIRECT_PORT=8000
GOOGLE_OAUTH_REDIRECT_PATH=/oauth2callback
GOOGLE_OAUTH_REDIRECT_BASE=https://api.toxiguard.site
EOF"

# Копируем Firebase credentials
scp caloriesbot-949dd-firebase-adminsdk-fbsvc-4ecc1b1ad9.json german_server:/opt/calories-bot/

# Создаем Google OAuth credentials
ssh german_server "cat > /opt/calories-bot/credentials.json << 'CREDEOF'
{
  \"web\": {
    \"client_id\": \"YOUR_CLIENT_ID_HERE\",
    \"project_id\": \"caloriesbot-949dd\",
    \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",
    \"token_uri\": \"https://oauth2.googleapis.com/token\",
    \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",
    \"client_secret\": \"YOUR_CLIENT_SECRET_HERE\",
    \"redirect_uris\": [
      \"https://api.toxiguard.site/oauth2callback\"
    ],
    \"javascript_origins\": [
      \"https://api.toxiguard.site\"
    ]
  }
}
CREDEOF"

# Создаем docker-compose файл
ssh german_server "cat > /opt/calories-bot/docker-compose.prod.yml << 'DOCKEREOF'
version: '3.8'

services:
  calories-bot:
    image: ghcr.io/rigsbey/calories_notebook:latest
    container_name: calories-bot
    restart: unless-stopped
    environment:
      - BOT_TOKEN=8289791710:AAF7Q6oTSbBHMbqtR1eGMGyQTwlZcXXRYuw
      - GEMINI_API_KEY=AIzaSyB3jK8L9mN2pQ1rS4tU6vW8xY0zA1bC3dE
      - FIREBASE_CREDENTIALS_PATH=caloriesbot-949dd-firebase-adminsdk-fbsvc-4ecc1b1ad9.json
      - GOOGLE_CREDENTIALS_PATH=credentials.json
      - GOOGLE_OAUTH_REDIRECT_PORT=8000
      - GOOGLE_OAUTH_REDIRECT_PATH=/oauth2callback
      - GOOGLE_OAUTH_REDIRECT_BASE=https://api.toxiguard.site
    volumes:
      - /opt/calories-bot/logs:/app/logs
      - /opt/calories-bot/temp_photos:/app/temp_photos
      - /opt/calories-bot/caloriesbot-949dd-firebase-adminsdk-fbsvc-4ecc1b1ad9.json:/app/caloriesbot-949dd-firebase-adminsdk-fbsvc-4ecc1b1ad9.json:ro
      - /opt/calories-bot/credentials.json:/app/credentials.json:ro
    logging:
      driver: \"json-file\"
      options:
        max-size: \"10m\"
        max-file: \"3\"
DOCKEREOF"

# Устанавливаем правильные права
ssh german_server "chmod -R 777 /opt/calories-bot/logs /opt/calories-bot/temp_photos"

# Останавливаем старый контейнер
ssh german_server "cd /opt/calories-bot && docker-compose -f docker-compose.prod.yml down || true"

# Запускаем новый контейнер
ssh german_server "cd /opt/calories-bot && docker-compose -f docker-compose.prod.yml pull && docker-compose -f docker-compose.prod.yml up -d"

# Проверяем статус
ssh german_server "cd /opt/calories-bot && docker-compose -f docker-compose.prod.yml ps"

# Показываем логи
sleep 5
ssh german_server "cd /opt/calories-bot && docker-compose -f docker-compose.prod.yml logs --tail 10"

echo "✅ Деплой завершен!"
