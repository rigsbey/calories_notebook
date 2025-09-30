<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Privacy Policy Content -->
    <section class="privacy-hero">
      <div class="container">
        <h1 class="privacy-title">Политика конфиденциальности</h1>
        <p class="privacy-subtitle">Как мы собираем, используем и защищаем ваши данные</p>
      </div>
    </section>

    <section class="privacy-content">
      <div class="container">
        <div class="content-wrapper">
          <div class="privacy-section">
            <h2>Сбор данных</h2>
            <p>Мы собираем только необходимые данные для предоставления наших услуг:</p>
            <ul>
              <li><strong>Telegram ID</strong> - для идентификации пользователя и связи с ботом</li>
              <li><strong>Фотографии еды</strong> - для анализа питания и расчета калорий</li>
              <li><strong>Данные Google Calendar</strong> - для сохранения информации о питании (только при вашем согласии)</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>Использование данных</h2>
            <p>Ваши данные используются исключительно для:</p>
            <ul>
              <li>Анализа фотографий еды с помощью ИИ</li>
              <li>Предоставления информации о питании и калориях</li>
              <li>Сохранения данных в Google Calendar (при согласии)</li>
              <li>Улучшения качества сервиса</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>Безопасность данных</h2>
            <p>Мы обеспечиваем максимальную защиту ваших данных:</p>
            <ul>
              <li>Все данные передаются по зашифрованному соединению</li>
              <li>Данные хранятся в защищенной базе Firebase</li>
              <li>Доступ к данным имеют только авторизованные сотрудники</li>
              <li>Регулярные проверки безопасности системы</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>Интеграция с Google Calendar</h2>
            <p>При подключении Google Calendar мы запрашиваем минимальные разрешения:</p>
            <ul>
              <li><strong>Создание событий</strong> - для сохранения информации о питании</li>
              <li>Создается отдельный календарь "Calories Bot"</li>
              <li>Сохраняется только информация о питании</li>
              <li><strong>Нет доступа к другим календарям</strong></li>
              <li><strong>Не читаем существующие события</strong></li>
              <li>Вы можете отключить интеграцию в любой момент</li>
            </ul>
            <p><strong>Запрашиваемые разрешения:</strong> создание событий в календаре</p>
          </div>

          <div class="privacy-section">
            <h2>Права пользователей</h2>
            <p>Вы имеете следующие права в отношении ваших данных:</p>
            <ul>
              <li>Получить копию всех ваших данных</li>
              <li>Исправить неточную информацию</li>
              <li>Удалить ваши данные</li>
              <li>Отозвать согласие на обработку</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>Контакты</h2>
            <p>По вопросам обработки данных обращайтесь:</p>
            <ul>
              <li><strong>Email:</strong> abulkhanov.kamil@gmail.com</li>
              <li><strong>Telegram:</strong> @caloriesnote_bot</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>Изменения в политике</h2>
            <p>Мы можем обновлять эту политику. О существенных изменениях уведомим заранее.</p>
            <p><strong>Последнее обновление:</strong> 30 сентября 2025</p>
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
  description: 'Как мы собираем, используем и защищаем ваши данные',
  keywords: 'privacy policy, data protection, Calories Bot, nutrition analysis',
  ogTitle: 'Политика конфиденциальности | Calories Bot',
  ogDescription: 'Как мы собираем, используем и защищаем ваши данные',
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
