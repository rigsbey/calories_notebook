<template>
  <main class="product" aria-labelledby="product-heading">
    <div class="container">
      <h2 id="product-heading" class="product-title">
        ✅ ИИ-бот для анализа питания и автоматического подсчета калорий
      </h2>
      
      <!-- Demo Section -->
      <div class="demo">
        <h3 class="demo-title">Как работает бот-диетолог для подсчета КБЖУ по фото:</h3>
        <div class="demo-steps">
          <div 
            v-for="(step, index) in demoSteps" 
            :key="index" 
            class="demo-step"
            :style="{ animationDelay: `${index * 0.2}s` }"
          >
            <div class="step-number">{{ index + 1 }}</div>
            <h4 class="step-title">{{ step.title }}</h4>
            <p class="step-description">{{ step.description }}</p>
          </div>
        </div>
      </div>

      <!-- Features Grid -->
      <div class="features">
        <div 
          v-for="(feature, index) in features" 
          :key="index" 
          class="feature"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <span class="feature-icon">{{ feature.icon }}</span>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
      </div>

      <!-- Real Example -->
      <div class="real-example">
        <h3 class="example-title">🔥 Реальный пример работы бота:</h3>
        <div class="example-content">
          <div class="example-header">🍽️ Ваш прием пищи (автоопределение веса):</div>
          
          <div class="example-item">
            <strong>🍽️ ПРОДУКТЫ:</strong> Кусок запеченного лосося, порция вареного белого риса, жареная брокколи и шпинат.
          </div>
          
          <div class="example-item">
            <strong>⚖️ ПРИМЕРНЫЙ ВЕС:</strong> 400 г (лосось - 150 г, рис - 150 г, овощи - 100 г)
          </div>
          
          <div class="example-item">
            <strong>📊 ПИЩЕВАЯ ЦЕННОСТЬ:</strong><br>
            • 🔥 Калории: 550 ккал<br>
            • 🥩 Белки: 35 г<br>
            • 🥑 Жиры: 25 г<br>
            • 🍞 Углеводы: 45 г
          </div>
          
          <div class="example-item">
            <strong>📊 ВИТАМИНЫ И МИНЕРАЛЫ:</strong><br>
            🥕 Витамин A: 🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ 35%<br>
            🍊 Витамин C: 🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ 60%<br>
            🌿 Витамин K: 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ 90%<br>
            🥩 Витамин B12: 🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜ 50%
          </div>
          
          <div class="example-success">
            ✅ Анализ завершен!
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
const demoSteps = ref([
  {
    title: '📸 Сфотографировал еду',
    description: 'Любое блюдо, любой ракурс'
  },
  {
    title: '⚖️ Указал вес',
    description: 'Или нажал "не знаю"'
  },
  {
    title: '📊 Получил анализ',
    description: 'КБЖУ, калории, витамины'
  },
  {
    title: '📊 Получил отчет',
    description: 'Детальная статистика по питанию'
  }
])

const features = ref([
  {
    icon: '🤖',
    title: 'ИИ-анализ фото',
    description: 'Определяет состав блюда по фотографии с точностью диетолога'
  },
  {
    icon: '⚡',
    title: '5 секунд',
    description: 'От фото до результата. Быстрее чем найти продукт в базе'
  },
  {
    icon: '📊',
    title: 'Полный анализ',
    description: 'Калории, белки, жиры, углеводы, витамины и микроэлементы'
  },
  {
    icon: '✏️',
    title: 'Коррекция',
    description: 'Исправь анализ текстом: "Это не руккола, а шпинат"'
  },
  {
    icon: '📈',
    title: 'Отчеты',
    description: 'Итоги дня и недели по питанию одной командой'
  }
])

// Анимация появления элементов
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in')
      }
    })
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  })

  document.querySelectorAll('.demo-step, .feature').forEach(el => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(30px)'
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'
    observer.observe(el)
  })
})
</script>

<style scoped>
.product {
  @apply bg-white rounded-3xl p-12 mb-10 shadow-2xl;
}

.container {
  @apply max-w-6xl mx-auto;
}

.product-title {
  @apply text-4xl text-green-500 mb-8 text-center font-bold;
  font-size: clamp(2rem, 4vw, 2.5rem);
}

.demo {
  @apply bg-gray-50 rounded-2xl p-8 my-10;
}

.demo-title {
  @apply text-2xl mb-8 text-center text-gray-800 font-semibold;
}

.demo-steps {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8;
}

.demo-step {
  @apply text-center p-6 bg-white rounded-xl border-2 border-gray-200 transition-all duration-300;
}

.demo-step:hover {
  @apply border-blue-400 transform -translate-y-2 shadow-lg;
}

.step-number {
  @apply w-10 h-10 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold mx-auto mb-4;
}

.step-title {
  @apply text-lg font-semibold mb-2 text-gray-800;
}

.step-description {
  @apply text-gray-600 text-sm;
}

.features {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 my-10;
}

.feature {
  @apply text-center p-8 bg-gray-50 rounded-2xl border-2 border-gray-200 transition-all duration-300;
}

.feature:hover {
  @apply border-blue-400 transform -translate-y-2 shadow-lg;
}

.feature-icon {
  @apply text-5xl mb-6 block;
}

.feature-title {
  @apply text-xl font-semibold mb-4 text-gray-800;
}

.feature-description {
  @apply text-gray-600;
}

.real-example {
  @apply bg-green-50 p-8 rounded-2xl my-10 text-center;
}

.example-title {
  @apply text-2xl text-green-800 mb-6 font-semibold;
}

.example-content {
  @apply bg-white p-6 rounded-xl text-left max-w-2xl mx-auto font-mono text-sm shadow-lg;
}

.example-header {
  @apply text-gray-800 font-bold mb-4;
}

.example-item {
  @apply mb-3;
}

.example-success {
  @apply text-green-600 font-bold text-center p-3 bg-green-100 rounded-lg mt-4;
}

.animate-in {
  @apply opacity-100 transform-none;
}

@media (max-width: 768px) {
  .product {
    @apply p-8;
  }
  
  .demo-steps {
    @apply grid-cols-1;
  }
  
  .features {
    @apply grid-cols-1;
  }
}
</style>
