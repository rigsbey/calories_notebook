# Используем официальный Node.js образ
FROM node:20-alpine AS base

# Устанавливаем pnpm для более быстрой установки пакетов
RUN npm install -g pnpm

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и pnpm-lock.yaml
COPY package*.json ./
COPY pnpm-lock.yaml* ./

# Устанавливаем зависимости
RUN pnpm install --frozen-lockfile

# Копируем исходный код
COPY . .

# Сборка приложения
RUN pnpm run build

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
