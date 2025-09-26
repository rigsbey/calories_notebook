#!/bin/bash
# Скрипт настройки Cloudflare Tunnel для лендинга

set -e

echo "🌐 Настройка Cloudflare Tunnel для лендинга..."

# Создаем туннель для лендинга
echo "📡 Создаем новый туннель..."
TUNNEL_NAME="calories-landing-tunnel"

ssh german_server << EOF
# Создаем туннель
cloudflared tunnel create $TUNNEL_NAME

# Создаем конфиг файл
cat > /root/.cloudflared/config.yml << 'CONFIG'
tunnel: $TUNNEL_NAME
credentials-file: /root/.cloudflared/$TUNNEL_NAME.json

ingress:
  - hostname: caloriesnotebook.com
    service: http://localhost:80
  - hostname: www.caloriesnotebook.com
    service: http://localhost:80
  - service: http_status:404
CONFIG

echo "✅ Туннель создан: $TUNNEL_NAME"
echo "📝 Теперь нужно:"
echo "1. Настроить DNS записи в Cloudflare Dashboard"
echo "2. Запустить туннель: cloudflared tunnel run $TUNNEL_NAME"
EOF

echo "🔧 Следующие шаги:"
echo "1. Зайдите в Cloudflare Dashboard"
echo "2. Добавьте CNAME записи:"
echo "   - caloriesnotebook.com -> dde88031-3172-488c-8caa-ee0617ff849b.cfargotunnel.com"
echo "   - www.caloriesnotebook.com -> dde88031-3172-488c-8caa-ee0617ff849b.cfargotunnel.com"
echo "3. Запустите туннель: ssh german_server 'cloudflared tunnel run calories-landing-tunnel'"
