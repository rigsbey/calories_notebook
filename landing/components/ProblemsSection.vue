<template>
  <section class="problems" aria-labelledby="problems-heading">
    <div class="container">
      <h2 id="problems-heading" class="problems-title">
        😤 Проблемы с подсчетом калорий и контролем питания
      </h2>
      <ul class="problem-list">
        <li v-for="(problem, index) in problems" :key="index" class="problem-item">
          <span class="emoji">{{ problem.emoji }}</span>
          {{ problem.text }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
const problems = ref([
  {
    emoji: '🤔',
    text: 'Смотришь на тарелку и понятия не имеешь сколько там калорий?'
  },
  {
    emoji: '📱',
    text: 'Надоело искать каждый продукт в приложениях для подсчета калорий?'
  },
  {
    emoji: '⏰',
    text: 'Тратишь 10 минут на ввод каждого приема пищи вручную?'
  },
  {
    emoji: '🤷‍♀️',
    text: 'Не знаешь какие витамины получаешь с едой?'
  },
  {
    emoji: '📊',
    text: 'Хочешь следить за питанием, но лень ведать дневник еды?'
  }
])

// Анимация появления элементов
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1'
          entry.target.style.transform = 'translateX(0)'
        }, index * 100)
      }
    })
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  })

  document.querySelectorAll('.problem-item').forEach(el => {
    el.style.opacity = '0'
    el.style.transform = 'translateX(-30px)'
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'
    observer.observe(el)
  })
})
</script>

<style scoped>
.problems {
  @apply bg-white rounded-3xl p-12 mb-10 shadow-2xl;
}

.container {
  @apply max-w-4xl mx-auto;
}

.problems-title {
  @apply text-4xl text-red-500 mb-8 text-center font-bold;
  font-size: clamp(2rem, 4vw, 2.5rem);
}

.problem-list {
  @apply list-none space-y-4;
}

.problem-item {
  @apply text-xl p-4 bg-red-50 border-l-4 border-red-500 rounded-lg;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  transition: all 0.3s ease;
}

.problem-item:hover {
  @apply bg-red-100 transform scale-105;
}

.emoji {
  @apply text-2xl mr-3;
  font-size: 1.2em;
}

@media (max-width: 768px) {
  .problems {
    @apply p-8;
  }
  
  .problems-title {
    @apply text-2xl;
  }
  
  .problem-item {
    @apply text-lg p-3;
  }
}
</style>
