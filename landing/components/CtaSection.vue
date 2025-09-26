<template>
  <section class="cta" aria-labelledby="cta-heading">
    <div class="container">
      <div class="cta-content">
        <h2 id="cta-heading" class="cta-title">
          Всегда бесплатно. Никаких подписок
        </h2>
        <p class="cta-subtitle">
          Просто запусти бота и начни считать калории прямо сейчас
        </p>
        
        <div class="pricing-card">
          <div class="pricing-badge">Бесплатно навсегда</div>
          <div class="pricing-plan">
            <h3 class="plan-name">Calories Bot</h3>
            <div class="plan-price">
              <div class="price-main">
                <span class="price">0₽</span>
                <span class="period">/навсегда</span>
              </div>
            </div>
            <p class="plan-description">Для всех, кто хочет легко считать калории по фото</p>
            
            <div class="plan-features">
              <div class="feature-item">
                <span class="feature-check">✓</span>
                ИИ-анализ любых фото еды
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Калории, БЖУ и витамины
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Сохранение в Google Calendar
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Отчеты по дням и неделям
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Можно исправлять результаты
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Работает в Telegram
              </div>
            </div>
            
            <a 
              href="https://t.me/caloriesnote_bot" 
              class="cta-button"
              @click="trackClick"
            >
              🚀 Запустить бота бесплатно
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const trackClick = () => {
  // Отправка события в аналитику
  if (process.client && window.gtag) {
    window.gtag('event', 'cta_click', {
      event_category: 'engagement',
      event_label: 'telegram_bot_button'
    })
  }
  console.log('CTA button clicked')
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
}

.pricing-card {
  @apply relative bg-white rounded-2xl p-8 max-w-md mx-auto;
  border: 2px solid #10b981;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.pricing-badge {
  @apply absolute -top-3 left-1/2 transform -translate-x-1/2 text-white px-4 py-1 rounded-full text-sm font-medium;
  background: #10b981;
  font-weight: 500;
}

.pricing-plan {
  @apply text-center;
}

.plan-name {
  @apply text-2xl font-bold text-gray-900 mb-4;
  font-weight: 700;
}

.plan-price {
  @apply mb-4;
}

.price-small {
  @apply block text-sm text-gray-500 mb-1;
  font-weight: 400;
}

.price-main {
  @apply flex items-baseline justify-center;
}

.price {
  @apply text-4xl font-bold text-gray-900;
  font-weight: 700;
}

.period {
  @apply text-gray-600 ml-2;
  font-weight: 400;
}

.plan-description {
  @apply text-gray-600 mb-8;
  font-weight: 400;
  line-height: 1.6;
}

.plan-features {
  @apply space-y-3 mb-8;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
}

.feature-item {
  @apply text-gray-700 flex items-start;
  font-weight: 400;
  line-height: 1.5;
}

.feature-check {
  @apply text-green-500 mr-3 mt-0.5 flex-shrink-0;
  font-weight: 600;
}

.cta-button {
  @apply w-full text-white px-8 py-5 text-lg font-medium rounded-lg transition-all duration-200;
  background: #10b981;
  border: none;
  font-weight: 500;
  min-height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cta-button:hover {
  background: #059669;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .cta-title {
    @apply text-3xl;
  }
  
  .cta-subtitle {
    @apply text-lg;
  }
  
  .pricing-card {
    @apply p-6;
  }
  
  .price {
    @apply text-3xl;
  }
}
</style>
