<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Terms Content -->
    <section class="terms-hero">
      <div class="container">
        <h1 class="terms-title">Условия использования</h1>
        <p class="terms-subtitle">Правила использования Calories Bot</p>
      </div>
    </section>

    <section class="terms-content">
      <div class="container">
        <div class="content-wrapper">
          <div class="terms-section">
            <h2>1. Принятие условий</h2>
            <p>Используя Calories Bot, вы соглашаетесь с данными условиями. Если вы не согласны с какими-либо условиями, пожалуйста, не используйте наш сервис.</p>
          </div>

          <div class="terms-section">
            <h2>2. Описание сервиса</h2>
            <p>Calories Bot - это Telegram-бот для анализа питания, который:</p>
            <ul>
              <li>Анализирует фотографии еды с помощью ИИ</li>
              <li>Предоставляет информацию о калориях и питательных веществах</li>
              <li>Сохраняет анализы в Google Calendar (опционально)</li>
              <li>Предоставляет статистику питания</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>3. Права пользователя</h2>
            <p>Вы имеете право:</p>
            <ul>
              <li>Бесплатно использовать базовые функции бота</li>
              <li>Получать точную информацию о питании</li>
              <li>Управлять своими данными</li>
              <li>Отключить интеграцию с Google Calendar</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>4. Обязанности пользователя</h2>
            <p>При использовании сервиса вы обязуетесь:</p>
            <ul>
              <li>Предоставлять корректную информацию</li>
              <li>Не использовать бота для незаконных целей</li>
              <li>Не нарушать права интеллектуальной собственности</li>
              <li>Соблюдать правила Telegram</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>5. Ограничения ответственности</h2>
            <p>Мы не несем ответственности за:</p>
            <ul>
              <li>Точность анализа фотографий (результаты приблизительные)</li>
              <li>Решения, принятые на основе анализа</li>
              <li>Проблемы с интеграцией Google Calendar</li>
              <li>Временные сбои в работе сервиса</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>6. Интеллектуальная собственность</h2>
            <p>Все права на сервис принадлежат разработчику. Вы не можете:</p>
            <ul>
              <li>Копировать или воспроизводить код</li>
              <li>Создавать производные продукты</li>
              <li>Использовать брендинг без разрешения</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>7. Изменения условий</h2>
            <p>Мы можем изменять эти условия. О существенных изменениях мы уведомим через Telegram-бота.</p>
          </div>

          <div class="terms-section">
            <h2>8. Контакты</h2>
            <p>По вопросам условий использования:</p>
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
  description: 'Условия использования Calories Bot. Правила и ограничения сервиса анализа питания.',
  keywords: 'условия использования, правила, Calories Bot, анализ питания',
  ogTitle: 'Условия использования | Calories Bot',
  ogDescription: 'Правила и ограничения сервиса анализа питания.',
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
