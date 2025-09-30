<template>
  <section class="pricing" id="pricing">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Выберите свой тарифный план</h2>
        <p class="section-subtitle">Начните с бесплатного Lite или получите все функции Pro</p>
      </div>

      <div class="pricing-grid">
        <!-- Lite Plan -->
        <div class="pricing-card lite-card">
          <div class="pricing-badge">Правильный текст</div>
          <div class="pricing-plan">
            <h3 class="plan-name">Правильный текст</h3>
            <div class="plan-price">
              <span class="price">Правильный текст</span>
              <span class="period">Правильный текст</span>
            </div>
            <p class="plan-description">Правильный текст</p>
            
            <div class="plan-features">
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item disabled">
                <span class="feature-check">✗</span>
                Правильный текст
              </div>
              <div class="feature-item disabled">
                <span class="feature-check">✗</span>
                Правильный текст
              </div>
            </div>
          </div>
          
          <a 
            href="https://t.me/caloriesnote_bot" 
            class="cta-button lite-button"
            @click="trackClick('lite')"
          >
            Правильный текст
          </a>
        </div>

        <!-- Pro Plan -->
        <div class="pricing-card pro-card">
          <div class="pricing-badge pro-badge">Правильный текст</div>
          <div class="pricing-plan">
            <h3 class="plan-name">Правильный текст</h3>
            <div class="plan-price">
              <span class="price">{{ getPrice('pro') }}{{ getCurrencySymbol() }}</span>
              <span class="period">Правильный текст</span>
            </div>
            <div class="plan-savings">
              Правильный текст
            </div>
            <p class="plan-description">Правильный текст</p>
            
            <div class="plan-features">
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
            </div>
          </div>
          
          <a 
            href="https://t.me/caloriesnote_bot?start=pro" 
            class="cta-button pro-button"
            @click="trackClick('pro')"
          >
            Правильный текст
          </a>
        </div>

        <!-- Annual Plan -->
        <div class="pricing-card annual-card">
          <div class="pricing-badge annual-badge">Правильный текст</div>
          <div class="pricing-plan">
            <h3 class="plan-name">Правильный текст</h3>
            <div class="plan-price">
              <span class="price">Правильный текст</span>
              <span class="period">Правильный текст</span>
            </div>
            <div class="plan-savings">
              Правильный текст
            </div>
            <p class="plan-description">Правильный текст</p>
            
            <div class="plan-features">
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
              <div class="feature-item">
                <span class="feature-check">✓</span>
                Правильный текст
              </div>
            </div>
          </div>
          
          <a 
            href="https://t.me/caloriesnote_bot?start=pro_annual" 
            class="cta-button annual-button"
            @click="trackClick('annual')"
          >
            Правильный текст
          </a>
        </div>
      </div>

      <!-- Additional Features -->
      <div class="additional-features">
        <h3 class="features-title">Правильный текст</h3>
        <div class="stars-features">
          <div class="star-feature">
            <span class="star-icon">💫</span>
            <span class="star-text">Правильный текст</span>
          </div>
          <div class="star-feature">
            <span class="star-icon">🍽️</span>
            <span class="star-text">Правильный текст</span>
          </div>
          <div class="star-feature">
            <span class="star-icon">📄</span>
            <span class="star-text">Правильный текст</span>
          </div>
        </div>
        <p class="stars-note">
          Правильный текст
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useCurrency } from '~/composables/useCurrency'

const { formatPrice, getPriceForLocale, currentCurrency } = useCurrency()

const trackClick = (plan) => {
  // Отправка события в аналитику
  if (process.client && window.gtag) {
    window.gtag('event', 'pricing_click', {
      event_category: 'conversion',
      event_label: plan,
      value: plan === 'lite' ? 0 : plan === 'pro' ? 399 : 2990
    })
  }
  console.log(`Pricing button clicked: ${plan}`)
}

// Функции для работы с ценами
const getPrice = (plan) => {
  const { locale } = useI18n()
  
  if (plan === 'pro') {
    return locale.value === 'en' ? '9' : '399'
  } else if (plan === 'annual') {
    return locale.value === 'en' ? '60' : '2990'
  }
  
  return '0'
}

// Функция для получения символа валюты
const getCurrencySymbol = () => {
  return currentCurrency.value.symbol
}

const formatCurrency = (price) => {
  return formatPrice(price)
}

// Анимация появления
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1'
          entry.target.style.transform = 'translateY(0)'
        }, index * 100)
      }
    })
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  })

  document.querySelectorAll('.pricing-card').forEach(el => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(30px)'
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'
    observer.observe(el)
  })
})
</script>

<style scoped>
.pricing {
  @apply bg-gray-50 py-20;
}

.container {
  @apply max-w-7xl mx-auto px-6;
}

.section-header {
  @apply text-center mb-16;
}

.section-title {
  @apply text-4xl font-bold text-gray-900 mb-4;
  font-size: clamp(2rem, 5vw, 2.5rem);
  font-weight: 700;
}

.section-subtitle {
  @apply text-xl text-gray-600;
  font-weight: 400;
}

.pricing-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16;
}

.pricing-card {
  @apply relative bg-white rounded-2xl p-8 transition-all duration-200 flex flex-col;
  border: 2px solid #e5e7eb;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  height: 100%;
}

.pricing-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.pro-card {
  border-color: #10b981;
  box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.1), 0 4px 6px -2px rgba(16, 185, 129, 0.05);
  transform: scale(1.05);
}

.pro-card:hover {
  transform: scale(1.05) translateY(-4px);
}

.pricing-badge {
  @apply absolute -top-3 left-1/2 transform -translate-x-1/2 text-white px-4 py-1 rounded-full text-sm font-medium;
  background: #6b7280;
  font-weight: 500;
}

.pro-badge {
  background: #10b981;
}

.annual-badge {
  background: #f59e0b;
}

.pricing-plan {
  @apply text-center flex-grow;
}

.plan-name {
  @apply text-2xl font-bold text-gray-900 mb-4;
  font-weight: 700;
}

.plan-price {
  @apply mb-2;
  display: flex;
  align-items: baseline;
  justify-content: center;
}

.price {
  @apply text-4xl font-bold text-gray-900;
  font-weight: 700;
}

.period {
  @apply text-gray-600 ml-2;
  font-weight: 400;
}

.plan-savings {
  @apply text-sm text-green-600 font-medium mb-4;
}

.plan-description {
  @apply text-gray-600 mb-8;
  font-weight: 400;
  line-height: 1.6;
}

.plan-features {
  @apply space-y-3 mb-8;
}

.feature-item {
  @apply text-gray-700 flex items-start text-sm;
  font-weight: 400;
  line-height: 1.5;
}

.feature-item.disabled {
  @apply text-gray-400;
}

.feature-check {
  @apply mr-3 mt-0.5 flex-shrink-0;
  font-weight: 600;
}

.feature-item .feature-check {
  @apply text-green-500;
}

.feature-item.disabled .feature-check {
  @apply text-red-400;
}

.cta-button {
  @apply w-full text-white px-8 py-4 text-base font-medium rounded-lg transition-all duration-200;
  border: none;
  font-weight: 500;
  min-height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: auto;
}

.lite-button {
  @apply bg-gray-600;
}

.lite-button:hover {
  @apply bg-gray-700;
  transform: translateY(-1px);
}

.pro-button {
  background: #10b981;
}

.pro-button:hover {
  background: #059669;
  transform: translateY(-1px);
}

.annual-button {
  background: #f59e0b;
}

.annual-button:hover {
  background: #d97706;
  transform: translateY(-1px);
}

.additional-features {
  @apply bg-white rounded-2xl p-8 text-center;
  border: 1px solid #e5e7eb;
}

.features-title {
  @apply text-xl font-semibold text-gray-900 mb-6;
  font-weight: 600;
}

.stars-features {
  @apply flex flex-wrap justify-center gap-6 mb-4;
}

.star-feature {
  @apply flex items-center space-x-2 text-gray-700;
}

.star-icon {
  @apply text-lg;
}

.star-text {
  @apply font-medium;
}

.stars-note {
  @apply text-sm text-gray-500 max-w-2xl mx-auto;
  font-weight: 400;
  line-height: 1.5;
}

@media (max-width: 1024px) {
  .pricing-grid {
    @apply grid-cols-1 md:grid-cols-2;
  }
  
  .pro-card {
    transform: none;
  }
  
  .pro-card:hover {
    transform: translateY(-4px);
  }
}

@media (max-width: 768px) {
  .section-title {
    @apply text-3xl;
  }
  
  .section-subtitle {
    @apply text-lg;
  }
  
  .pricing-grid {
    @apply grid-cols-1 gap-6;
  }
  
  .pricing-card {
    @apply p-6;
  }
  
  .price {
    @apply text-3xl;
  }
  
  .stars-features {
    @apply flex-col gap-3;
  }
}
</style>
