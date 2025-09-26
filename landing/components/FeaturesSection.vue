<template>
  <section class="features" id="features">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Что умеет бот</h2>
        <p class="section-subtitle">Все необходимое для контроля питания в одном Telegram-боте</p>
      </div>

      <div class="features-grid">
        <div class="feature-card" v-for="(feature, index) in features" :key="index">
          <div class="feature-icon">{{ feature.icon }}</div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
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
    description: 'Любое блюдо — от салата до пиццы. Просто сфотографируй и отправь.'
  },
  {
    icon: '⚡',
    title: 'Результат за 5 секунд',
    description: 'Калории, БЖУ и витамины мгновенно. Никакого ручного ввода.'
  },
  {
    icon: '📊',
    title: 'Калории + БЖУ + витамины',
    description: 'Полная информация о питательной ценности каждого блюда.'
  },
  {
    icon: '📅',
    title: 'Синхронизация с Google Calendar',
    description: 'Все данные автоматически сохраняются в твой календарь.'
  },
  {
    icon: '✏️',
    title: 'Можно вручную уточнить',
    description: 'Если что-то не так — просто напиши боту, и он исправит.'
  },
  {
    icon: '📈',
    title: 'Отчеты дня и недели',
    description: 'Смотри статистику по дням и неделям для контроля прогресса.'
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
  @apply bg-white p-8 rounded-xl transition-all duration-200;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
