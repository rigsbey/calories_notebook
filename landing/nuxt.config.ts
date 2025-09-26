// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  // Модули
  modules: [
    '@nuxtjs/tailwindcss'
  ],

  // Tailwind CSS конфигурация
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: 'tailwind.config.js'
  },

  // App конфигурация
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'Telegram-бот для анализа питания | Подсчет калорий по фото | @caloriesnote_bot',
      meta: [
        { name: 'description', content: '🤖 Telegram-бот для анализа питания. Отправь фото еды - получи точный расчет КБЖУ, калорий и витаминов за 5 секунд. Автоматическое сохранение в Google Calendar. Бесплатно!' },
        { name: 'keywords', content: 'telegram бот, анализ питания, подсчет калорий, КБЖУ, фото еды, диета, похудение, здоровое питание, калории, белки, жиры, углеводы, витамины' },
        { name: 'author', content: 'Calories Notebook Bot' },
        { name: 'robots', content: 'index, follow' },
        { name: 'googlebot', content: 'index, follow' },
        { name: 'theme-color', content: '#667eea' },
        { name: 'msapplication-TileColor', content: '#667eea' }
      ],
          link: [
            { rel: 'canonical', href: 'https://calories.toxiguard.site/' },
            { rel: 'icon', type: 'image/png', href: '/favicon.png' },
            { rel: 'apple-touch-icon', href: '/favicon.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap' },
        { rel: 'preconnect', href: 'https://t.me' },
        { rel: 'dns-prefetch', href: 'https://t.me' }
      ]
    }
  },

  // CSS конфигурация
  css: ['~/assets/css/main.css'],

  // Рендеринг
  ssr: false,
  nitro: {
    preset: 'static'
  },

  // Runtime конфигурация
  runtimeConfig: {
    public: {
      siteUrl: 'https://calories.toxiguard.site',
      telegramBot: '@caloriesnote_bot'
    }
  }
})
