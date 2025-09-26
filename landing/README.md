# Calories Landing - SEO-оптимизированный лендинг

Современный лендинг для Telegram-бота анализа питания, построенный на Nuxt.js с максимальной оптимизацией под SEO.

## 🚀 Особенности

- **SEO-оптимизация**: Полная настройка мета-тегов, структурированных данных, sitemap
- **Производительность**: Оптимизация Core Web Vitals, lazy loading, code splitting
- **Адаптивность**: Полностью адаптивный дизайн для всех устройств
- **Доступность**: Соответствие стандартам WCAG 2.1
- **Аналитика**: Интеграция с Google Analytics и отслеживание Web Vitals

## 🛠 Технологии

- **Nuxt.js 3** - Vue.js фреймворк с SSR
- **TypeScript** - Типизация
- **Tailwind CSS** - Utility-first CSS фреймворк
- **@nuxtjs/seo** - SEO модули
- **@nuxt/image** - Оптимизация изображений
- **Docker** - Контейнеризация

## 📦 Установка

```bash
# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev

# Сборка для продакшна
npm run build

# Предварительный просмотр сборки
npm run preview
```

## 🐳 Docker

```bash
# Сборка образа
docker build -t calories-landing .

# Запуск контейнера
docker run -p 3000:3000 calories-landing

# Или через docker-compose
docker-compose up -d
```

## 🚀 Деплой

```bash
# Автоматический деплой на сервер
./deploy.sh
```

## 📊 SEO оптимизация

### Мета-теги
- Динамические title и description
- Open Graph теги для социальных сетей
- Twitter Card теги
- Структурированные данные (JSON-LD)

### Производительность
- Server-Side Rendering (SSR)
- Автоматическая оптимизация изображений
- Lazy loading
- Code splitting
- Preloading критических ресурсов

### Core Web Vitals
- Отслеживание LCP, FID, CLS
- Оптимизация анимаций
- Сжатие ресурсов

## 📁 Структура проекта

```
landing/
├── assets/           # Статические ресурсы
├── components/       # Vue компоненты
├── layouts/          # Макеты страниц
├── middleware/       # Middleware для SEO
├── pages/            # Страницы приложения
├── plugins/          # Плагины
├── public/           # Публичные файлы
├── server/           # Серверные API
├── nuxt.config.ts    # Конфигурация Nuxt
└── package.json      # Зависимости
```

## 🎨 Компоненты

- **HeroSection** - Главная секция с призывом к действию
- **ProblemsSection** - Секция с проблемами пользователей
- **ProductSection** - Описание продукта и функций
- **FaqSection** - Часто задаваемые вопросы
- **InfoSection** - Информационный контент
- **CtaSection** - Финальный призыв к действию

## 🔧 Конфигурация

Основные настройки находятся в `nuxt.config.ts`:

- SEO модули и настройки
- Мета-теги и структурированные данные
- Оптимизация изображений
- Google Analytics
- Sitemap и robots.txt

## 📈 Мониторинг

- Google Analytics для отслеживания трафика
- Core Web Vitals для мониторинга производительности
- Логи контейнера для отладки

## 🤝 Разработка

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License
