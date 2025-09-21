#!/bin/bash
# Скрипт первоначальной настройки сервера

set -e

echo "🚀 Настройка сервера для Calories Bot..."

# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Устанавливаем Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Устанавливаем Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Устанавливаем Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Создаем директории
echo "📁 Создаем директории..."
sudo mkdir -p /opt/calories-bot/{logs,temp_photos}
sudo chown -R $USER:$USER /opt/calories-bot

# Создаем systemd сервис для автозапуска
echo "⚙️ Настраиваем автозапуск..."
sudo tee /etc/systemd/system/calories-bot.service > /dev/null <<EOF
[Unit]
Description=Calories Bot Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/calories-bot
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable calories-bot.service

echo "✅ Сервер настроен! Не забудьте:"
echo "1. Добавить SSH ключ в GitHub Secrets"
echo "2. Добавить BOT_TOKEN и GEMINI_API_KEY в GitHub Secrets"
echo "3. Скопировать credentials.json в /opt/calories-bot/"
