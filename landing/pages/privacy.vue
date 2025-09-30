<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Privacy Policy Content -->
    <section class="privacy-hero">
      <div class="container">
        <h1 class="privacy-title">{{ $t('privacy.title') }}</h1>
        <p class="privacy-subtitle">{{ $t('privacy.subtitle') }}</p>
      </div>
    </section>

    <section class="privacy-content">
      <div class="container">
        <div class="content-wrapper">
          <div class="privacy-section">
            <h2>{{ $t('privacy.sections.dataCollection.title') }}</h2>
            <p>{{ $t('privacy.sections.dataCollection.content') }}</p>
            <ul>
              <li><strong>Telegram ID</strong> - {{ $t('privacy.dataCollection.telegramId') }}</li>
              <li><strong>{{ $t('privacy.dataCollection.photos') }}</strong> - {{ $t('privacy.dataCollection.photosDesc') }}</li>
              <li><strong>{{ $t('privacy.dataCollection.googleCalendar') }}</strong> - {{ $t('privacy.dataCollection.googleCalendarDesc') }}</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>{{ $t('privacy.sections.dataUsage.title') }}</h2>
            <p>{{ $t('privacy.sections.dataUsage.content') }}</p>
            <ul>
              <li>{{ $t('privacy.dataUsage.aiAnalysis') }}</li>
              <li>{{ $t('privacy.dataUsage.nutritionInfo') }}</li>
              <li>{{ $t('privacy.dataUsage.calendarSave') }}</li>
              <li>{{ $t('privacy.dataUsage.serviceImprovement') }}</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>{{ $t('privacy.sections.dataSecurity.title') }}</h2>
            <p>{{ $t('privacy.sections.dataSecurity.content') }}</p>
            <ul>
              <li>{{ $t('privacy.dataSecurity.encryption') }}</li>
              <li>{{ $t('privacy.dataSecurity.firebase') }}</li>
              <li>{{ $t('privacy.dataSecurity.limitedAccess') }}</li>
              <li>{{ $t('privacy.dataSecurity.securityChecks') }}</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>{{ $t('privacy.googleCalendar.title') }}</h2>
            <p>{{ $t('privacy.googleCalendar.description') }}</p>
            <ul>
              <li><strong>{{ $t('privacy.googleCalendar.createEvents') }}</strong> - {{ $t('privacy.googleCalendar.createEventsDesc') }}</li>
              <li>{{ $t('privacy.googleCalendar.separateCalendar') }}</li>
              <li>{{ $t('privacy.googleCalendar.saveOnlyNutrition') }}</li>
              <li><strong>{{ $t('privacy.googleCalendar.noAccessOther') }}</strong></li>
              <li><strong>{{ $t('privacy.googleCalendar.noReadExisting') }}</strong></li>
              <li>{{ $t('privacy.googleCalendar.canDisable') }}</li>
            </ul>
            <p><strong>{{ $t('privacy.googleCalendar.requestedPermissions') }}:</strong> {{ $t('privacy.googleCalendar.permissionsDesc') }}</p>
          </div>

          <div class="privacy-section">
            <h2>{{ $t('privacy.sections.userRights.title') }}</h2>
            <p>{{ $t('privacy.sections.userRights.content') }}</p>
            <ul>
              <li>{{ $t('privacy.userRights.getCopy') }}</li>
              <li>{{ $t('privacy.userRights.correctInfo') }}</li>
              <li>{{ $t('privacy.userRights.deleteData') }}</li>
              <li>{{ $t('privacy.userRights.withdrawConsent') }}</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>{{ $t('privacy.sections.contact.title') }}</h2>
            <p>{{ $t('privacy.sections.contact.content') }}</p>
            <ul>
              <li><strong>Email:</strong> abulkhanov.kamil@gmail.com</li>
              <li><strong>Telegram:</strong> @caloriesnote_bot</li>
            </ul>
          </div>

          <div class="privacy-section">
            <h2>{{ $t('privacy.sections.changes.title') }}</h2>
            <p>{{ $t('privacy.sections.changes.content') }}</p>
            <p><strong>{{ $t('privacy.lastUpdated') }}:</strong> 30 сентября 2025</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// SEO мета-теги
const { t } = useI18n()
useSeoMeta({
  title: () => `${t('privacy.title')} | Calories Bot`,
  description: () => t('privacy.subtitle'),
  keywords: 'privacy policy, data protection, Calories Bot, nutrition analysis',
  ogTitle: () => `${t('privacy.title')} | Calories Bot`,
  ogDescription: () => t('privacy.subtitle'),
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
