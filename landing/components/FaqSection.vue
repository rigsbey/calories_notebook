<template>
  <section class="faq" aria-labelledby="faq-heading">
    <div class="container">
      <h2 id="faq-heading" class="faq-title">
        Часто задаваемые вопросы
      </h2>
      
      <div class="faq-container">
        <div 
          v-for="(faq, index) in faqs" 
          :key="index" 
          class="faq-item"
          :class="{ 'faq-item--open': openFaq === index }"
          @click="toggleFaq(index)"
        >
          <h3 class="faq-question">
            {{ faq.question }}
            <span class="faq-icon">{{ openFaq === index ? '−' : '+' }}</span>
          </h3>
          <div class="faq-answer" :class="{ 'faq-answer--open': openFaq === index }">
            <p>{{ faq.answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const openFaq = ref(null)

const faqs = [
  {
    question: 'Как работает бот?',
    answer: 'Просто отправьте фото еды в Telegram. ИИ определит продукты, рассчитает калории и БЖУ за 5 секунд. Результат автоматически сохранится в Google Calendar (если подключен).'
  },
  {
    question: 'Насколько точный анализ?',
    answer: 'Точность составляет 85-90% для большинства блюд. Бот использует Google Gemini AI, который обучен на миллионах изображений еды. Для лучших результатов фотографируйте еду сверху при хорошем освещении.'
  },
  {
    question: 'Сколько стоит использование?',
    answer: 'Lite план бесплатный навсегда (5 фото в день). Pro план стоит 399₽/месяц с 7-дневным бесплатным периодом. Годовая подписка - 2999₽ (экономия 1798₽).'
  },
  {
    question: 'Как подключить Google Calendar?',
    answer: 'В боте нажмите "Настройки" → "Подключить календарь". Выполните OAuth авторизацию с минимальными разрешениями. Все анализы будут автоматически сохраняться в календарь.'
  },
  {
    question: 'Сколько фото можно отправить?',
    answer: 'Lite: 5 фото в день. Pro: до 200 фото в месяц. Можно докупать дополнительные анализы за Telegram Stars (99⭐ за 10 анализов).'
  },
  {
    question: 'Можно ли исправить результат?',
    answer: 'Да! Если бот ошибся, просто напишите ему "исправь" и опишите, что не так. Он пересчитает анализ с учетом ваших правок.'
  }
]

const toggleFaq = (index) => {
  openFaq.value = openFaq.value === index ? null : index
}

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

  document.querySelectorAll('.faq-item').forEach(el => {
    el.style.opacity = '0'
    el.style.transform = 'translateY(30px)'
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'
    observer.observe(el)
  })
})
</script>

<style scoped>
.faq {
  @apply bg-white py-20;
}

.container {
  @apply max-w-4xl mx-auto px-6;
}

.faq-title {
  @apply text-4xl mb-10 text-center font-bold text-gray-900;
  font-size: clamp(2rem, 4vw, 2.5rem);
  font-weight: 700;
}

.faq-container {
  @apply space-y-4;
}

.faq-item {
  @apply bg-white p-6 rounded-lg cursor-pointer transition-all duration-200;
  border: 1px solid #e5e7eb;
}

.faq-item:hover {
  border-color: #d1d5db;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.faq-item--open {
  border-color: #10b981;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.faq-question {
  @apply text-lg font-semibold text-gray-900 mb-0 flex justify-between items-center;
  font-weight: 600;
}

.faq-icon {
  @apply text-xl font-bold transition-transform duration-300;
  color: #10b981;
  font-weight: 700;
}

.faq-item--open .faq-icon {
  @apply transform rotate-180;
}

.faq-answer {
  @apply overflow-hidden transition-all duration-300 ease-in-out;
  max-height: 0;
}

.faq-answer--open {
  max-height: 200px;
}

.faq-answer p {
  @apply text-gray-600 leading-relaxed pt-4;
  font-weight: 400;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .faq-title {
    @apply text-3xl;
  }
  
  .faq-question {
    @apply text-base;
  }
  
  .faq-item {
    @apply p-4;
  }
}
</style>
