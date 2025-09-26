<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Hero Section -->
    <HeroSection />
    
    <!-- How It Works Section -->
    <HowItWorksSection />
    
    <!-- Features Section -->
    <div id="features">
      <FeaturesSection />
    </div>
    
    <!-- CTA Section (Pricing) -->
    <div id="pricing">
      <CtaSection />
    </div>
    
    <!-- FAQ Section -->
    <div id="faq">
      <FaqSection />
    </div>
  </div>
</template>

<script setup>
// SEO мета-теги для главной страницы
useSeoMeta({
  title: 'Calories Bot - ИИ-бот для анализа питания | Подсчет калорий по фото | @caloriesnote_bot',
  ogTitle: 'Calories Bot - ИИ-бот для анализа питания | Подсчет калорий по фото',
  description: '🤖 ИИ-бот для анализа питания. Сфотографируй еду - получи точный расчет КБЖУ, калорий и витаминов за 5 секунд. Автоматическое сохранение в Google Calendar. Бесплатно!',
  ogDescription: 'Сфотографируй еду - получи точный анализ КБЖУ, калорий и витаминов за 5 секунд. Автоматическое сохранение в Google Calendar.',
  ogImage: 'https://calories.toxiguard.site/og-image.jpg',
  ogImageAlt: 'Calories Bot - ИИ-анализ питания по фото',
  twitterCard: 'summary_large_image',
  twitterImage: 'https://calories.toxiguard.site/og-image.jpg',
  twitterTitle: 'Calories Bot - ИИ-бот для анализа питания | Подсчет калорий по фото',
  twitterDescription: 'Сфотографируй еду - получи точный анализ КБЖУ, калорий и витаминов за 5 секунд. Автоматическое сохранение в Google Calendar.',
  keywords: 'telegram бот, анализ питания, подсчет калорий, КБЖУ, фото еды, диета, похудение, здоровое питание, калории, белки, жиры, углеводы, витамины, ИИ',
  author: 'Calories Bot',
  robots: 'index, follow',
  googlebot: 'index, follow'
})

// JSON-LD структурированные данные
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Calories Notebook Bot",
        "description": "Telegram-бот для анализа питания по фотографии еды",
        "url": "https://t.me/caloriesnote_bot",
        "applicationCategory": "HealthApplication",
        "operatingSystem": "Telegram",
        "offers": {
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "RUB"
        },
        "featureList": [
          "Анализ фото еды",
          "Расчет КБЖУ и калорий",
          "Определение витаминов",
          "Сохранение в Google Calendar",
          "Отчеты по питанию"
        ]
      })
    }
  ]
})
</script>
