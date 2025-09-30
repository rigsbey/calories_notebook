<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Terms Content -->
    <section class="terms-hero">
      <div class="container">
        <h1 class="terms-title">{{ $t('terms.title') }}</h1>
        <p class="terms-subtitle">{{ $t('terms.subtitle') }}</p>
      </div>
    </section>

    <section class="terms-content">
      <div class="container">
        <div class="content-wrapper">
          <div class="terms-section">
            <h2>{{ $t('terms.sections.acceptance.title') }}</h2>
            <p>{{ $t('terms.sections.acceptance.content') }}</p>
          </div>

          <div class="terms-section">
            <h2>{{ $t('terms.sections.service.title') }}</h2>
            <p>{{ $t('terms.sections.service.content') }}</p>
            <ul>
              <li>{{ $t('terms.service.aiAnalysis') }}</li>
              <li>{{ $t('terms.service.nutritionInfo') }}</li>
              <li>{{ $t('terms.service.calendarSave') }}</li>
              <li>{{ $t('terms.service.statistics') }}</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>{{ $t('terms.userRights.title') }}</h2>
            <p>{{ $t('terms.userRights.description') }}</p>
            <ul>
              <li>{{ $t('terms.userRights.freeUse') }}</li>
              <li>{{ $t('terms.userRights.accurateInfo') }}</li>
              <li>{{ $t('terms.userRights.manageData') }}</li>
              <li>{{ $t('terms.userRights.disableCalendar') }}</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>{{ $t('terms.sections.userObligations.title') }}</h2>
            <p>{{ $t('terms.sections.userObligations.content') }}</p>
            <ul>
              <li>{{ $t('terms.userObligations.correctInfo') }}</li>
              <li>{{ $t('terms.userObligations.noIllegalUse') }}</li>
              <li>{{ $t('terms.userObligations.noViolateIP') }}</li>
              <li>{{ $t('terms.userObligations.followTelegramRules') }}</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>{{ $t('terms.sections.limitation.title') }}</h2>
            <p>{{ $t('terms.sections.limitation.content') }}</p>
            <ul>
              <li>{{ $t('terms.limitation.accuracy') }}</li>
              <li>{{ $t('terms.limitation.decisions') }}</li>
              <li>{{ $t('terms.limitation.calendarIssues') }}</li>
              <li>{{ $t('terms.limitation.serviceOutages') }}</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>{{ $t('terms.sections.intellectualProperty.title') }}</h2>
            <p>{{ $t('terms.sections.intellectualProperty.content') }}</p>
            <ul>
              <li>{{ $t('terms.intellectualProperty.noCopy') }}</li>
              <li>{{ $t('terms.intellectualProperty.noDerivatives') }}</li>
              <li>{{ $t('terms.intellectualProperty.noBranding') }}</li>
            </ul>
          </div>

          <div class="terms-section">
            <h2>{{ $t('terms.sections.modifications.title') }}</h2>
            <p>{{ $t('terms.sections.modifications.content') }}</p>
          </div>

          <div class="terms-section">
            <h2>{{ $t('terms.sections.contact.title') }}</h2>
            <p>{{ $t('terms.sections.contact.content') }}</p>
            <ul>
              <li><strong>Email:</strong> abulkhanov.kamil@gmail.com</li>
              <li><strong>Telegram:</strong> @caloriesnote_bot</li>
            </ul>
          </div>

          <div class="terms-section">
            <p><strong>{{ $t('terms.lastUpdated') }}:</strong> 26 сентября 2025</p>
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
  title: () => `${t('terms.title')} | Calories Bot`,
  description: () => t('terms.subtitle'),
  keywords: 'terms of use, rules, Calories Bot, nutrition analysis',
  ogTitle: () => `${t('terms.title')} | Calories Bot`,
  ogDescription: () => t('terms.subtitle'),
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
