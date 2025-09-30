<template>
  <section class="cta" aria-labelledby="cta-heading">
    <div class="container">
      <div class="cta-content">
        <h2 id="cta-heading" class="cta-title">
          Готов начать контролировать питание?
        </h2>
        <p class="cta-subtitle">
          Запусти бота прямо сейчас и получи первый анализ за 5 секунд
        </p>
        
        <div class="cta-buttons">
          <a 
            href="https://t.me/caloriesnote_bot" 
            class="cta-button primary"
            @click="trackClick('start_free')"
          >
            🚀 Попробовать бесплатно
          </a>
          
          <a 
            href="https://t.me/caloriesnote_bot?start=pro" 
            class="cta-button secondary"
            @click="trackClick('start_pro')"
          >
            ⭐ 7 дней Pro бесплатно
          </a>
        </div>
        
        <div class="cta-features">
          <div class="cta-feature">
            <span class="feature-icon">⚡</span>
            <span class="feature-text">Результат за 5 секунд</span>
          </div>
          <div class="cta-feature">
            <span class="feature-icon">📱</span>
            <span class="feature-text">Работает в Telegram</span>
          </div>
          <div class="cta-feature">
            <span class="feature-icon">🔒</span>
            <span class="feature-text">Безопасно и конфиденциально</span>
          </div>
        </div>
        
        <div class="cta-legal">
          <p class="legal-text">
            Используя сервис, вы соглашаетесь с нашими условиями использования и политикой конфиденциальности
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const trackClick = (action) => {
  // Отправка события в аналитику
  if (process.client && window.gtag) {
    window.gtag('event', 'cta_click', {
      event_category: 'engagement',
      event_label: action
    })
  }
  console.log(`CTA button clicked: ${action}`)
}

// Анимация появления
onMounted(() => {
  const cta = document.querySelector('.cta')
  if (cta) {
    cta.style.opacity = '0'
    cta.style.transform = 'translateY(30px)'
    cta.style.transition = 'opacity 0.8s ease, transform 0.8s ease'
    
    setTimeout(() => {
      cta.style.opacity = '1'
      cta.style.transform = 'translateY(0)'
    }, 200)
  }
})
</script>

<style scoped>
.cta {
  @apply bg-white py-20;
}

.container {
  @apply max-w-4xl mx-auto px-6;
}

.cta-content {
  @apply text-center;
}

.cta-title {
  @apply text-4xl font-bold text-gray-900 mb-4;
  font-size: clamp(2rem, 5vw, 2.5rem);
  font-weight: 700;
}

.cta-subtitle {
  @apply text-xl text-gray-600 mb-12;
  font-weight: 400;
  line-height: 1.6;
}

.cta-buttons {
  @apply flex flex-col sm:flex-row gap-4 justify-center items-center mb-12;
}

.cta-button {
  @apply px-8 py-4 text-lg font-medium rounded-lg transition-all duration-200;
  border: none;
  font-weight: 500;
  min-height: 56px;
  min-width: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.cta-button.primary {
  @apply text-white;
  background: #10b981;
}

.cta-button.primary:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
}

.cta-button.secondary {
  @apply text-gray-700 bg-gray-100 border-2 border-gray-200;
}

.cta-button.secondary:hover {
  @apply bg-gray-200 border-gray-300;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.cta-features {
  @apply flex flex-col sm:flex-row gap-8 justify-center items-center;
}

.cta-feature {
  @apply flex items-center space-x-3;
}

.feature-icon {
  @apply text-2xl;
}

.feature-text {
  @apply text-gray-600 font-medium;
}

.cta-legal {
  @apply mt-8 pt-6 border-t border-gray-200;
}

.legal-text {
  @apply text-sm text-gray-500 leading-relaxed;
}

.legal-link {
  @apply text-blue-600 hover:text-blue-800 underline transition-colors duration-200;
}

@media (max-width: 768px) {
  .cta-title {
    @apply text-3xl;
  }
  
  .cta-subtitle {
    @apply text-lg mb-8;
  }
  
  .cta-buttons {
    @apply mb-8;
  }
  
  .cta-button {
    @apply w-full text-base py-4;
    min-width: auto;
  }
  
  .cta-features {
    @apply flex-col gap-4;
  }
  
  .feature-icon {
    @apply text-xl;
  }
  
  .feature-text {
    @apply text-sm;
  }
}

@media (max-width: 640px) {
  .cta-buttons {
    @apply flex-col;
  }
}
</style>
