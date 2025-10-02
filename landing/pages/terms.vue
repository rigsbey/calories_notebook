<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Terms Content -->
    <section class="terms-hero">
      <div class="container">
        <h1 class="terms-title">Условия использования</h1>
        <p class="terms-subtitle">Правила использования сервиса Calories Bot</p>
      </div>
    </section>

    <section class="terms-content">
      <div class="container">
        <div class="content-wrapper">
          <div class="terms-section">
            <h2>Принятие условий</h2>
            <p>Используя наш сервис, вы соглашаетесь с данными условиями использования.</p>
          </div>

          <div class="terms-section">
            <h2>Описание сервиса</h2>
            <p>Calories Bot предоставляет следующие услуги:</p>
            <ul>
              <li>Анализ фотографий еды с помощью ИИ</li>
              <li>Предоставление информации о питании и калориях</li>
              <li>Статистика и отчеты о питании</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>Права пользователей</h2>
            <p>Пользователи имеют следующие права:</p>
            <ul>
              <li>Бесплатное использование базовых функций</li>
              <li>Получение точной информации о питании</li>
              <li>Управление своими данными</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>Обязанности пользователей</h2>
            <p>Пользователи обязуются:</p>
            <ul>
              <li>Предоставлять корректную информацию</li>
              <li>Не использовать сервис в незаконных целях</li>
              <li>Не нарушать права интеллектуальной собственности</li>
              <li>Соблюдать правила Telegram</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>Ограничения ответственности</h2>
            <p>Мы не несем ответственности за:</p>
            <ul>
              <li>Точность анализа питания (результаты носят рекомендательный характер)</li>
              <li>Решения, принятые на основе наших рекомендаций</li>
              <li>Временные сбои в работе сервиса</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>Интеллектуальная собственность</h2>
            <p>Все права на сервис принадлежат нам. Запрещается:</p>
            <ul>
              <li>Копировать или воспроизводить сервис</li>
              <li>Создавать производные продукты</li>
              <li>Использовать наши торговые марки</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>Изменения условий</h2>
            <p>Мы можем изменять данные условия. О существенных изменениях уведомим заранее.</p>
          </div>

          <div class="terms-section">
            <h2>Контакты</h2>
            <p>По вопросам использования сервиса обращайтесь:</p>
            <ul>
              <li><strong>Email:</strong> abulkhanov.kamil@gmail.com</li>
              <li><strong>Telegram:</strong> @caloriesnote_bot</li>
            </ul>
          </div>

          <div class="terms-section">
            <p><strong>Последнее обновление:</strong> 26 сентября 2025</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// SEO мета-теги
useSeoMeta({
  title: 'Условия использования | Calories Bot',
  description: 'Правила использования сервиса Calories Bot',
  keywords: 'terms of use, rules, Calories Bot, nutrition analysis',
  ogTitle: 'Условия использования | Calories Bot',
  ogDescription: 'Правила использования сервиса Calories Bot',
  robots: 'index, follow'
})
</script>

<style scoped>
.terms-hero {
  @apply bg-gradient-to-br from-green-50 to-emerald-100 py-16;
}

.container {
  @apply max-w-4xl mx-auto px-6;
}

.terms-title {
  @apply text-4xl font-bold text-gray-900 text-center mb-4;
  font-size: clamp(2rem, 5vw, 3rem);
}

.terms-subtitle {
  @apply text-xl text-gray-600 text-center;
}

.terms-content {
  @apply py-16 bg-white;
}

.content-wrapper {
  @apply max-w-3xl mx-auto;
}

.terms-section {
  @apply mb-8;
}

.terms-section h2 {
  @apply text-2xl font-bold text-gray-900 mb-4;
}

.terms-section p {
  @apply text-gray-700 mb-4 leading-relaxed;
}

.terms-section ul {
  @apply list-disc list-inside space-y-2 mb-4;
}

.terms-section li {
  @apply text-gray-700;
}

@media (max-width: 768px) {
  .terms-hero {
    @apply py-12;
  }
  
  .terms-title {
    @apply text-3xl;
  }
  
  .terms-subtitle {
    @apply text-lg;
  }
}
</style>
