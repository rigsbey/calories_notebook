<template>
  <section class="info-section" aria-labelledby="info-heading">
    <div class="container">
      <h2 id="info-heading" class="info-title">
        📚 Все о правильном подсчете калорий и КБЖУ
      </h2>
      
      <div class="info-content">
        <div 
          v-for="(info, index) in infoBlocks" 
          :key="index" 
          class="info-block"
          :style="{ animationDelay: `${index * 0.2}s` }"
        >
          <h3 class="info-block-title">{{ info.title }}</h3>
          <p class="info-block-text" v-html="info.content"></p>
        </div>
        
        <!-- Example Report -->
        <div class="info-block">
          <h3 class="info-block-title">📊 Пример отчета за день</h3>
          <div class="report-example">
            <div class="report-header">📅 Итоги дня (2025-09-24)</div>
            <div class="report-line">👤 @username</div>
            <div class="report-line">📊 Проанализировано приемов пищи: 10</div>
            <div class="report-line">🔥 Калории: 4580 ккал (из 2200)</div>
            <div class="report-line">🥩 Белки: 160.0 г / 120 г</div>
            <div class="report-line">🥑 Жиры: 262.0 г / 75 г</div>
            <div class="report-line">🌾 Углеводы: 425.0 г / 250 г</div>
            <div class="report-line">💊 Витамины: A(35%), C(60%), K(90%), B12(50%)</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const infoBlocks = ref([
  {
    title: '🎯 Зачем нужен контроль калорий?',
    content: 'Подсчет калорий — основа <strong>здорового питания</strong> и эффективного <strong>похудения</strong>. Наш <strong>бот-диетолог</strong> помогает вести <strong>дневник питания онлайн</strong> без сложных расчетов. Просто фотографируйте еду и получайте точный анализ <strong>калорийности по фото</strong>.'
  },
  {
    title: '⚖️ Что такое КБЖУ и почему это важно?',
    content: '<strong>КБЖУ</strong> — это калории, белки, жиры и углеводы. Правильный <strong>баланс БЖУ</strong> обеспечивает организм энергией и строительными материалами. Наш <strong>калькулятор КБЖУ</strong> автоматически рассчитывает все показатели на основе анализа фото еды.'
  },
  {
    title: '🤖 Как работает ИИ для питания?',
    content: 'Наш <strong>ИИ-бот</strong> использует технологии <strong>распознавания еды по фото</strong> для определения состава блюда. Бот анализирует ингредиенты, рассчитывает <strong>питание и витамины</strong>, а затем сохраняет данные для отслеживания прогресса.'
  },
  {
    title: '📱 Преимущества Telegram-бота для диеты',
    content: 'В отличие от обычных <strong>приложений для похудения</strong>, наш бот работает прямо в Telegram. Не нужно скачивать дополнительные программы — просто отправляйте фото еды и получайте <strong>автоматический подсчет калорий</strong> с сохранением данных.'
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

  document.querySelectorAll('.info-block').forEach(el => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(30px)'
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'
    observer.observe(el)
  })
})
</script>

<style scoped>
.info-section {
  @apply bg-white rounded-3xl p-12 mb-10 shadow-2xl;
}

.container {
  @apply max-w-5xl mx-auto;
}

.info-title {
  @apply text-4xl text-gray-800 mb-10 text-center font-bold;
  font-size: clamp(2rem, 4vw, 2.5rem);
}

.info-content {
  @apply space-y-8;
}

.info-block {
  @apply p-8 bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl border-l-4 border-green-500;
}

.info-block-title {
  @apply text-2xl text-gray-800 mb-4 font-semibold;
}

.info-block-text {
  @apply text-gray-600 leading-relaxed text-lg;
}

.info-block-text strong {
  @apply text-gray-800 font-semibold;
}

.report-example {
  @apply bg-gray-100 p-5 rounded-xl mt-4 font-mono text-sm;
}

.report-header {
  @apply text-gray-800 font-bold mb-2;
}

.report-line {
  @apply mb-2;
}

@media (max-width: 768px) {
  .info-section {
    @apply p-8;
  }
  
  .info-title {
    @apply text-2xl;
  }
  
  .info-block {
    @apply p-6;
  }
  
  .info-block-title {
    @apply text-xl;
  }
  
  .info-block-text {
    @apply text-base;
  }
}
</style>
