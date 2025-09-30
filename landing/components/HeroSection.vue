<template>
  <section class="hero">
    <div class="container">
      <!-- Badge -->
      <div class="badge">
        {{ $t('hero.badge') }}
      </div>
      
      <!-- Main Title -->
      <h1 class="hero-title" v-html="$t('hero.title')">
      </h1>
      
      <!-- Subtitle -->
      <p class="hero-subtitle">
        {{ $t('hero.subtitle') }}
      </p>
      
      <!-- CTA Button -->
      <div class="cta-container">
        <a href="https://t.me/caloriesnote_bot" class="cta-button">
          {{ $t('hero.ctaButton') }}
        </a>
      </div>
      
      <!-- Social Proof -->
      <div class="social-proof">
        <div class="stars">
          <span class="star filled">★</span>
          <span class="star filled">★</span>
          <span class="star filled">★</span>
          <span class="star filled">★</span>
          <span class="star half-filled">★</span>
        </div>
        <div class="proof-text">{{ $t('hero.socialProof', { count: userCount }) }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Динамический счетчик пользователей
const userCount = ref(325)

// Анимация при загрузке
onMounted(() => {
  const hero = document.querySelector('.hero')
  if (hero) {
    hero.style.opacity = '0'
    hero.style.transform = 'translateY(30px)'
    hero.style.transition = 'opacity 0.8s ease, transform 0.8s ease'
    
    setTimeout(() => {
      hero.style.opacity = '1'
      hero.style.transform = 'translateY(0)'
    }, 100)
  }

  // Обновление счетчика каждые 10 минут
  setInterval(() => {
    const randomIncrease = Math.floor(Math.random() * 11) // 0-10
    userCount.value += randomIncrease
  }, 10 * 60 * 1000) // 10 минут в миллисекундах
})
</script>

<style scoped>
.hero {
  @apply bg-white py-20 px-4;
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  @apply max-w-4xl mx-auto text-center;
}

.badge {
  @apply inline-block px-4 py-2 rounded-full text-sm mb-8;
  background: #ecfdf5;
  color: #10b981;
  letter-spacing: 0.05em;
  font-weight: 400;
  border: 1px solid #a7f3d0;
}

.hero-title {
  @apply text-5xl text-gray-900 mb-6 leading-tight;
  font-size: clamp(2.5rem, 6vw, 4rem);
  line-height: 1.1;
  font-weight: 400; /* обычный шрифт для всего заголовка */
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.highlight {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 400; /* слово не жирное */
  font-style: italic; /* легкий наклон, как у effortlessly */
}

.hero-subtitle {
  @apply text-xl text-gray-600 mb-12 leading-relaxed max-w-2xl mx-auto;
  font-size: clamp(1.1rem, 2.5vw, 1.25rem);
  font-weight: 400;
}

.cta-container {
  @apply mb-12;
}

.cta-button {
  @apply inline-flex items-center justify-center px-8 py-4 text-lg transition-all duration-200 rounded-full text-white;
  background: #10b981;
  border: 1px solid #059669;
  box-shadow: 0 12px 24px rgba(16, 185, 129, 0.25), 0 2px 8px rgba(0,0,0,0.06);
  font-weight: 500;
}

.cta-button:hover {
  background: #059669;
  border-color: #047857;
  transform: translateY(-1px);
}

.social-proof {
  @apply flex flex-col items-center space-y-3;
}

.stars {
  @apply flex space-x-1;
}

.star {
  @apply text-2xl;
  color: #d1d5db; /* серый цвет для незаполненных звезд */
}

.star.filled {
  color: #fbbf24; /* желтый цвет для заполненных звезд */
}

.star.half-filled {
  background: linear-gradient(90deg, #fbbf24 50%, #d1d5db 50%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.proof-text {
  @apply text-gray-600 font-medium text-base;
}

.user-count {
  @apply font-bold text-gray-900;
  color: #10b981;
}

@media (max-width: 768px) {
  .hero {
    @apply py-16 px-4;
    min-height: 70vh;
  }
  
  .hero-title {
    @apply text-3xl mb-4;
  }
  
  .hero-subtitle {
    @apply text-lg mb-8;
  }
  
  .cta-button {
    @apply px-6 py-3 text-base;
  }
  
  .badge {
    @apply text-xs px-3 py-1;
  }
}
</style>
