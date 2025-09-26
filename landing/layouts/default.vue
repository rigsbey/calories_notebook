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
            <img src="/logo.jpg" alt="Calories Bot" class="brand-icon" />
            <span class="brand-text">Calories Notebook Bot</span>
          </div>
          <div class="footer-links">
            <a href="https://t.me/caloriesnote_bot" class="footer-link">Telegram Bot</a>
            <NuxtLink to="/privacy" class="footer-link">Конфиденциальность</NuxtLink>
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
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap' }
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
