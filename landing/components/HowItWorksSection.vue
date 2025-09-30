<template>
  <section class="how-it-works" id="how-it-works">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Как это работает</h2>
        <p class="section-subtitle">Всего 3 простых шага до точного подсчета калорий</p>
      </div>

      <div class="steps">
        <div class="step" v-for="(step, index) in steps" :key="index">
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-content">
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-description">{{ step.description }}</p>
            <div class="step-demo">
              <div class="demo-screenshot" v-if="step.screenshot">
                <img :src="step.screenshot" :alt="step.title" class="screenshot-image" />
              </div>
              <div class="demo-placeholder" v-else>
                {{ step.demoText }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const steps = [
  {
    title: '📸 Сфотографируй еду',
    description: 'Любое блюдо — от салата до пиццы. Просто отправь фото в Telegram.',
    demoText: '📸 Фото загружено',
    screenshot: '/images/step1-photo.jpg'
  },
  {
    title: '⚡ Получи анализ',
    description: 'Калории, БЖУ и витамины за 5 секунд. Никакого ручного ввода.',
    demoText: '⚡ Анализ готов',
    screenshot: '/images/step2-analysis.jpg'
  },
  {
    title: '📅 Сохрани в календарь',
    description: 'Результат автоматически попадает в Google Calendar.',
    demoText: '📅 Сохранено',
    screenshot: '/images/step3-calendar.jpg'
  }
]

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

  document.querySelectorAll('.step').forEach(el => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(30px)'
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'
    observer.observe(el)
  })
})
</script>

<style scoped>
.how-it-works {
  @apply bg-white py-20;
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
  @apply text-xl text-gray-600 max-w-3xl mx-auto;
  font-weight: 400;
}

.steps {
  @apply grid grid-cols-1 md:grid-cols-3 gap-10;
}

.step {
  @apply flex flex-col items-center text-center space-y-5;
}

.step-number {
  @apply w-12 h-12 text-white rounded-full flex items-center justify-center text-xl font-bold flex-shrink-0;
  background: #10b981;
  font-weight: 700;
}

.step-content {
  @apply w-full;
}

.step-title {
  @apply text-2xl font-bold text-gray-900 mb-4;
  font-weight: 600;
}

.step-description {
  @apply text-lg text-gray-600 mb-5;
  font-weight: 400;
  line-height: 1.5;
}

.step-demo {
  @apply bg-gray-50 rounded-lg p-5;
  border: 1px solid #e5e7eb;
  width: 100%;
  height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.demo-placeholder {
  @apply text-gray-500 text-center py-4 font-medium;
}

.demo-screenshot {
  @apply rounded-lg overflow-hidden;
  border: 1px solid #e5e7eb;
}

.screenshot-image {
  @apply w-full h-auto;
  max-height: 280px;
  min-height: 200px;
  object-fit: contain;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .steps {
    @apply grid-cols-1 gap-6;
  }
  
  .step {
    @apply space-y-3;
  }
  
  .section-title {
    @apply text-3xl;
  }
  
  .section-subtitle {
    @apply text-lg;
  }
  
  .step-title {
    @apply text-lg;
  }
  
  .step-description {
    @apply text-sm;
  }
  
  .step-demo {
    height: 250px;
  }
  
  .screenshot-image {
    max-height: 220px;
    min-height: 150px;
  }
}
</style>
