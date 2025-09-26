<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Privacy Policy Content -->
    <section class="privacy-hero">
      <div class="container">
        <h1 class="privacy-title">Политика конфиденциальности</h1>
        <p class="privacy-subtitle">Как мы защищаем ваши данные</p>
      </div>
    </section>

    <section class="privacy-content">
      <div class="container">
        <div class="content-wrapper">
          <div class="privacy-section">
            <h2>1. Сбор информации</h2>
            <p>Calories Bot собирает минимально необходимую информацию для предоставления услуг:</p>
            <ul>
              <li><strong>Telegram ID</strong> - для идентификации пользователя</li>
              <li><strong>Фотографии еды</strong> - для анализа питания (обрабатываются автоматически и не сохраняются)</li>
              <li><strong>Данные Google Calendar</strong> - только при вашем согласии для сохранения анализов</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>2. Использование данных</h2>
            <p>Мы используем ваши данные исключительно для:</p>
            <ul>
              <li>Анализа фотографий еды с помощью ИИ</li>
              <li>Предоставления информации о калориях и питательных веществах</li>
              <li>Сохранения анализов в Google Calendar (по вашему запросу)</li>
              <li>Улучшения качества сервиса</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>3. Защита данных</h2>
            <p>Мы принимаем все необходимые меры для защиты ваших данных:</p>
            <ul>
              <li>Шифрование данных при передаче</li>
              <li>Безопасное хранение в Firebase</li>
              <li>Ограниченный доступ к данным</li>
              <li>Регулярные проверки безопасности</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>4. Google Calendar интеграция</h2>
            <p>При подключении Google Calendar:</p>
            <ul>
              <li>Мы создаем отдельный календарь "Календарь питания"</li>
              <li>Сохраняем только анализы питания</li>
              <li>Не имеем доступа к другим календарям</li>
              <li>Можете отключить интеграцию в любое время</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>5. Ваши права</h2>
            <p>Вы имеете право:</p>
            <ul>
              <li>Получить копию ваших данных</li>
              <li>Исправить неточную информацию</li>
              <li>Удалить ваши данные</li>
              <li>Отозвать согласие на обработку</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>6. Контакты</h2>
            <p>По вопросам конфиденциальности обращайтесь:</p>
            <ul>
              <li><strong>Email:</strong> abulkhanov.kamil@gmail.com</li>
              <li><strong>Telegram:</strong> @caloriesnote_bot</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>7. Изменения в политике</h2>
            <p>Мы можем обновлять эту политику. О существенных изменениях мы уведомим через Telegram-бота.</p>
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
  title: 'Политика конфиденциальности | Calories Bot',
  description: 'Политика конфиденциальности Calories Bot. Как мы защищаем ваши данные при анализе питания.',
  keywords: 'политика конфиденциальности, защита данных, Calories Bot, анализ питания',
  ogTitle: 'Политика конфиденциальности | Calories Bot',
  ogDescription: 'Как мы защищаем ваши данные при анализе питания.',
  robots: 'index, follow'
})
</script>

<style scoped>
.privacy-hero {
  @apply bg-gradient-to-br from-blue-50 to-indigo-100 py-16;
}

.container {
  @apply max-w-4xl mx-auto px-6;
}

.privacy-title {
  @apply text-4xl font-bold text-gray-900 text-center mb-4;
  font-size: clamp(2rem, 5vw, 3rem);
}

.privacy-subtitle {
  @apply text-xl text-gray-600 text-center;
}

.privacy-content {
  @apply py-16 bg-white;
}

.content-wrapper {
  @apply max-w-3xl mx-auto;
}

.privacy-section {
  @apply mb-8;
}

.privacy-section h2 {
  @apply text-2xl font-bold text-gray-900 mb-4;
}

.privacy-section p {
  @apply text-gray-700 mb-4 leading-relaxed;
}

.privacy-section ul {
  @apply list-disc list-inside space-y-2 mb-4;
}

.privacy-section li {
  @apply text-gray-700;
}

@media (max-width: 768px) {
  .privacy-hero {
    @apply py-12;
  }
  
  .privacy-title {
    @apply text-3xl;
  }
  
  .privacy-subtitle {
    @apply text-lg;
  }
}
</style>
