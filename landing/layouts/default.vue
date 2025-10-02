<template>
  <div>
    <!-- Main Content -->
    <main>
      <slot />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <img 
              src="/logo.jpg" 
              alt="Calories Bot" 
              class="brand-icon"
              loading="eager"
            />
            <span class="brand-text">Calories Notebook Bot</span>
          </div>
          <div class="footer-links">
            <a href="https://t.me/caloriesnote_bot" class="footer-link">Telegram Bot</a>
            <NuxtLink to="/privacy" class="footer-link privacy-link">Политика конфиденциальности</NuxtLink>
            <NuxtLink to="/terms" class="footer-link">Условия использования</NuxtLink>
          </div>
        </div>
        <div class="footer-bottom">
          <p class="footer-text">
            Сделано с ❤️ для тех, кто следит за питанием
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// SEO мета-теги для всех страниц
useHead({
  htmlAttrs: {
    lang: 'ru'
  },
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'format-detection', content: 'telephone=no' }
  ],
  link: [
    { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
    { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
    { rel: 'preconnect', href: 'https://t.me' },
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap' },
    
    // Favicons
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
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
    { rel: 'msapplication-TileColor', content: '#ffffff' },
    { rel: 'msapplication-TileImage', content: '/ms-icon-144x144.png' },
    { rel: 'msapplication-config', content: '/browserconfig.xml' },
    
    // Web App Manifest
    { rel: 'manifest', href: '/manifest.json' }
  ]
})

// Плавная прокрутка для якорных ссылок
onMounted(() => {
  // Обработка якорных ссылок
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute('href'))
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        })
      }
    })
  })
})
</script>

<style scoped>
.container {
  @apply max-w-7xl mx-auto px-6;
}

.footer {
  @apply bg-gray-900 text-white py-12;
}

.footer-content {
  @apply flex flex-col md:flex-row items-center justify-between mb-8;
}

.footer-brand {
  @apply flex items-center space-x-2 text-xl font-bold mb-4 md:mb-0;
}

.brand-icon {
  @apply w-8 h-8 rounded-full object-cover;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.footer-links {
  @apply flex space-x-6;
}

.footer-link {
  @apply text-gray-300 hover:text-white transition-colors duration-300;
}

.privacy-link {
  @apply font-semibold text-white border-b border-gray-400 hover:border-white;
}

.footer-bottom {
  @apply text-center pt-8 border-t border-gray-700;
}

.footer-text {
  @apply text-gray-400;
}

@media (max-width: 768px) {
  .footer-content {
    @apply text-center;
  }
  
  .footer-links {
    @apply justify-center mt-4;
  }
}
</style>
