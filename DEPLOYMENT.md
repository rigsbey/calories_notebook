# 🚀 Деплой Calories Bot

## Автоматический деплой через GitHub Actions

### 1. Настройка сервера

Подключитесь к серверу и выполните:

```bash
# Скачайте скрипт настройки
curl -o setup-server.sh https://raw.githubusercontent.com/USERNAME/REPO/main/deploy/setup-server.sh
chmod +x setup-server.sh

# Запустите настройку
./setup-server.sh
```

### 2. Настройка GitHub Secrets

В настройках репозитория GitHub добавьте следующие секреты:

- `HOST` - IP адрес или домен сервера
- `USERNAME` - имя пользователя SSH (обычно `root` или `ubuntu`)
- `SSH_KEY` - приватный SSH ключ для подключения к серверу
- `BOT_TOKEN` - токен Telegram бота
- `GEMINI_API_KEY` - ключ API Google Gemini

### 3. Копирование файлов на сервер

```bash
# Скопируйте credentials.json если используете Google Calendar
scp credentials.json myserver:/opt/calories-bot/
```

### 4. Первый деплой

Сделайте push в ветку `main` - GitHub Actions автоматически:
1. Соберет Docker образ
2. Отправит его в GitHub Container Registry
3. Задеплоит на сервер
4. Запустит бота

## Управление ботом на сервере

### Проверка статуса
```bash
cd /opt/calories-bot
sudo docker-compose -f docker-compose.prod.yml ps
```

### Просмотр логов
```bash
sudo docker-compose -f docker-compose.prod.yml logs -f
```

### Перезапуск
```bash
sudo docker-compose -f docker-compose.prod.yml restart
```

### Мониторинг
```bash
# Скачайте скрипт мониторинга
curl -o monitor.sh https://raw.githubusercontent.com/USERNAME/REPO/main/deploy/monitor.sh
chmod +x monitor.sh
./monitor.sh
```

## Структура деплоя

```
/opt/calories-bot/
├── docker-compose.prod.yml  # Конфигурация Docker Compose
├── .env                     # Переменные окружения
├── credentials.json         # Google Calendar credentials (если нужен)
├── logs/                    # Логи приложения
└── temp_photos/            # Временные файлы фотографий
```

## Автозапуск

Бот настроен на автоматический запуск при перезагрузке сервера через systemd сервис `calories-bot.service`.

### Управление сервисом
```bash
sudo systemctl status calories-bot
sudo systemctl start calories-bot
sudo systemctl stop calories-bot
sudo systemctl restart calories-bot
```

## Troubleshooting

### Проблемы с правами доступа
```bash
sudo chown -R $USER:$USER /opt/calories-bot
```

### Очистка Docker
```bash
sudo docker system prune -a
```

### Проверка здоровья контейнера
```bash
sudo docker inspect calories-bot | grep -A 10 '"Health"'
```
