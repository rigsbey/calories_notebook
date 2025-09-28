<template>
  <section class="features" id="features">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Что умеет бот</h2>
        <p class="section-subtitle">Все необходимое для контроля питания в одном Telegram-боте</p>
      </div>

      <div class="features-grid">
        <div 
          class="feature-card" 
          :class="{
            'pro-feature': feature.available === 'pro',
            'lite-feature': feature.available === 'lite',
            'all-feature': feature.available === 'all'
          }"
          v-for="(feature, index) in features" 
          :key="index"
        >
          <div class="feature-icon">{{ feature.icon }}</div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
          <div class="feature-badge" v-if="feature.available === 'pro'">Pro</div>
          <div class="feature-badge lite-badge" v-if="feature.available === 'lite'">Lite</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const features = ref([
  {
    icon: '🤖',
    title: 'ИИ определяет продукты по фото',
    description: 'Любое блюдо — от салата до пиццы. Просто сфотографируй и отправь.',
    available: 'all'
  },
  {
    icon: '⚡',
    title: 'Результат за 5 секунд',
    description: 'Калории, БЖУ и витамины мгновенно. Никакого ручного ввода.',
    available: 'all'
  },
  {
    icon: '📊',
    title: 'Базовый анализ КБЖУ',
    description: 'Калории, белки, жиры и углеводы для каждого блюда.',
    available: 'lite'
  },
  {
    icon: '🍽️',
    title: 'Мульти-тарелка',
    description: 'Анализ нескольких блюд на одном фото. Только в Pro.',
    available: 'pro'
  },
  {
    icon: '🧬',
    title: 'Детальные витамины + советы',
    description: 'Микронутриенты, дефициты и умные рекомендации. Только в Pro.',
    available: 'pro'
  },
  {
    icon: '📅',
    title: 'Синхронизация с Google Calendar',
    description: 'Автосохранение всех анализов в календарь. Только в Pro.',
    available: 'pro'
  },
  {
    icon: '📈',
    title: 'Полные отчеты за неделю',
    description: 'Детальная аналитика и трекинг прогресса. Только в Pro.',
    available: 'pro'
  },
  {
    icon: '📄',
    title: 'Экспорт в PDF/CSV',
    description: 'Скачивай данные для дальнейшего анализа. Только в Pro.',
    available: 'pro'
  },
  {
    icon: '✏️',
    title: 'Исправление результатов',
    description: 'Если что-то не так — просто напиши боту, и он исправит.',
    available: 'all'
  }
])

// Анимация появления элементов
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1'
        entry.target.style.transform = 'translateY(0)'
      }
    })
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  })

  document.querySelectorAll('.feature-card').forEach(el => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(30px)'
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'
    observer.observe(el)
  })
})
</script>

<style scoped>
.features {
  @apply bg-gray-50 py-20;
}

.container {
  @apply max-w-6xl mx-auto px-6;
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
  @apply text-xl text-gray-600 max-w-4xl mx-auto;
  font-weight: 400;
  line-height: 1.6;
}

.features-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8;
}

.feature-card {
  @apply bg-white p-8 rounded-xl transition-all duration-200 relative;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.feature-card.pro-feature {
  border-color: #10b981;
  background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
}

.feature-card.pro-feature:hover {
  box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.1), 0 4px 6px -2px rgba(16, 185, 129, 0.05);
}

.feature-card.lite-feature {
  border-color: #6b7280;
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
}

.feature-card.all-feature {
  border-color: #3b82f6;
  background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
}

.feature-badge {
  @apply absolute top-3 right-3 px-2 py-1 text-xs font-semibold rounded-full;
  background: #10b981;
  color: white;
}

.feature-badge.lite-badge {
  background: #6b7280;
}

.feature-icon {
  @apply text-4xl mb-4;
}

.feature-title {
  @apply text-xl font-semibold text-gray-900 mb-3;
  font-weight: 600;
}

.feature-description {
  @apply text-gray-600 leading-relaxed;
  font-weight: 400;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .section-title {
    @apply text-3xl;
  }
  
  .section-subtitle {
    @apply text-lg;
  }
  
  .feature-card {
    @apply p-6;
  }
  
  .feature-title {
    @apply text-lg;
  }
  
  .feature-description {
    @apply text-sm;
  }
}
</style>
