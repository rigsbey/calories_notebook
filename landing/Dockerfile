# Используем официальный Node.js образ
FROM node:20-alpine AS base

# Устанавливаем зависимости

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и pnpm-lock.yaml
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем исходный код
COPY . .

# Сборка приложения
RUN npm run build

# Продакшн образ
FROM node:20-alpine AS production

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json
COPY package*.json ./

# Устанавливаем только продакшн зависимости
RUN npm install --only=production && npm cache clean --force

# Копируем собранное приложение
COPY --from=base /app/.output ./.output

# Создаем пользователя для безопасности
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nuxt -u 1001

# Меняем владельца файлов
RUN chown -R nuxt:nodejs /app
USER nuxt

# Открываем порт
EXPOSE 3000

# Устанавливаем переменные окружения
ENV NODE_ENV=production
ENV PORT=3000
ENV HOST=0.0.0.0

# Запускаем приложение
CMD ["node", ".output/server/index.mjs"]
