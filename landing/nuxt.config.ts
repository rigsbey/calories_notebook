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
        { name: 'google-site-verification', content: 'cJxB6xaxazRAHUhm1d7MgbgciM8QiVZY0Vg4TIwbhe8' },
        { name: 'theme-color', content: '#667eea' },
        { name: 'msapplication-TileColor', content: '#667eea' }
      ],
          link: [
            { rel: 'canonical', href: 'https://calories.toxiguard.site/' },
            
            // Favicons
            { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
            { rel: 'icon', type: 'image/png', href: '/favicon.png' },
            { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
            { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
            { rel: 'icon', type: 'image/png', sizes: '96x96', href: '/favicon-96x96.png' },
            
            // Apple Touch Icons
            { rel: 'apple-touch-icon', sizes: '57x57', href: '/apple-icon-57x57.png' },
            { rel: 'apple-touch-icon', sizes: '60x60', href: '/apple-icon-60x60.png' },
            { rel: 'apple-touch-icon', sizes: '72x72', href: '/apple-icon-72x72.png' },
            { rel: 'apple-touch-icon', sizes: '76x76', href: '/apple-icon-76x76.png' },
            { rel: 'apple-touch-icon', sizes: '114x114', href: '/apple-icon-114x114.png' },
            { rel: 'apple-touch-icon', sizes: '120x120', href: '/apple-icon-120x120.png' },
            { rel: 'apple-touch-icon', sizes: '144x144', href: '/apple-icon-144x144.png' },
            { rel: 'apple-touch-icon', sizes: '152x152', href: '/apple-icon-152x152.png' },
            { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-icon-180x180.png' },
            { rel: 'apple-touch-icon', href: '/apple-icon.png' },
            { rel: 'apple-touch-icon-precomposed', href: '/apple-icon-precomposed.png' },
            
            // Android Icons
            { rel: 'icon', type: 'image/png', sizes: '36x36', href: '/android-icon-36x36.png' },
            { rel: 'icon', type: 'image/png', sizes: '48x48', href: '/android-icon-48x48.png' },
            { rel: 'icon', type: 'image/png', sizes: '72x72', href: '/android-icon-72x72.png' },
            { rel: 'icon', type: 'image/png', sizes: '96x96', href: '/android-icon-96x96.png' },
            { rel: 'icon', type: 'image/png', sizes: '144x144', href: '/android-icon-144x144.png' },
            { rel: 'icon', type: 'image/png', sizes: '192x192', href: '/android-icon-192x192.png' },
            
            // Microsoft Tiles
            { rel: 'msapplication-TileImage', content: '/ms-icon-144x144.png' },
            { rel: 'msapplication-config', content: '/browserconfig.xml' },
            
            // Web App Manifest
            { rel: 'manifest', href: '/manifest.json' },
            
            // Fonts and external resources
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
  ssr: true,
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
