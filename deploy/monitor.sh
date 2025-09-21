#!/bin/bash
# Скрипт мониторинга бота

cd /opt/calories-bot

echo "📊 Статус Calories Bot"
echo "======================"

# Статус контейнера
echo "🐳 Docker контейнер:"
sudo docker-compose -f docker-compose.prod.yml ps

# Логи последние 20 строк
echo -e "\n📝 Последние логи:"
sudo docker-compose -f docker-compose.prod.yml logs --tail=20

# Использование ресурсов
echo -e "\n💾 Использование ресурсов:"
sudo docker stats calories-bot --no-stream

# Размер логов
echo -e "\n📁 Размер логов:"
du -sh logs/ 2>/dev/null || echo "Логи не найдены"

# Проверка здоровья
echo -e "\n❤️ Проверка здоровья:"
if sudo docker inspect calories-bot | grep '"Health"' > /dev/null; then
    sudo docker inspect calories-bot | grep -A 10 '"Health"'
else
    echo "Healthcheck не настроен"
fi
