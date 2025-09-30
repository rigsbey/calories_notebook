<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Article -->
    <article class="article">
      <div class="container">
        <!-- Article Header -->
        <header class="article-header">
          <div class="article-meta">
            <span class="article-date">{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.date') }}</span>
            <span class="article-category">{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.category') }}</span>
          </div>
          <h1 class="article-title">
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.title') }}
          </h1>
          <p class="article-excerpt">
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.excerpt') }}
          </p>
        </header>

        <!-- Article Content -->
        <div class="article-content prose-content">
          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.introduction.title') }}</h2>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.introduction.paragraph1') }}
          </p>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.introduction.paragraph2') }}
          </p>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.introduction.paragraph3') }}
          </p>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.whyImportant.title') }}</h2>
          
          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.whyImportant.weightControl.title') }}</h3>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.whyImportant.weightControl.content') }}
          </p>

          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.whyImportant.macroBalance.title') }}</h3>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.whyImportant.macroBalance.content') }}
          </p>

          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.whyImportant.vitamins.title') }}</h3>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.whyImportant.vitamins.content') }}
          </p>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.difficulties.title') }}</h2>
          <ul>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.difficulties.item1') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.difficulties.item2') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.difficulties.item3') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.difficulties.item4') }}</li>
          </ul>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.howItWorks.title') }}</h2>
          <p>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.howItWorks.description') }}</p>
          <ul>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.howItWorks.item1') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.howItWorks.item2') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.howItWorks.item3') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.howItWorks.item4') }}</li>
          </ul>

          <div class="article-image">
            <img src="/blog/podschet-kaloriy-po-foto.jpg" :alt="$t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.image.alt')" />
            <p class="image-caption">{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.image.caption') }}</p>
          </div>

          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.caloriesBot.title') }}</h3>
          <ol>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.caloriesBot.step1') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.caloriesBot.step2') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.caloriesBot.step3') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.caloriesBot.step4') }}</li>
          </ol>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.title') }}</h2>
          <ul>
            <li><strong>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.fast.title') }}:</strong> {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.fast.content') }}</li>
            <li><strong>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.convenient.title') }}:</strong> {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.convenient.content') }}</li>
            <li><strong>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.accurate.title') }}:</strong> {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.accurate.content') }}</li>
            <li><strong>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.automatic.title') }}:</strong> {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.automatic.content') }}</li>
            <li><strong>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.flexible.title') }}:</strong> {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.advantages.flexible.content') }}</li>
          </ul>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.targetAudience.title') }}</h2>
          <ul>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.targetAudience.item1') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.targetAudience.item2') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.targetAudience.item3') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.targetAudience.item4') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.targetAudience.item5') }}</li>
          </ul>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.longTerm.title') }}</h2>
          
          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.longTerm.diary.title') }}</h3>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.longTerm.diary.content') }}
          </p>

          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.longTerm.calendar.title') }}</h3>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.longTerm.calendar.content') }}
          </p>

          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.longTerm.reports.title') }}</h3>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.longTerm.reports.content') }}
          </p>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.scientific.title') }}</h2>
          <p>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.scientific.description') }}</p>
          <ul>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.scientific.item1') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.scientific.item2') }}</li>
            <li>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.scientific.item3') }}</li>
          </ul>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.title') }}</h2>
          
          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.q1.title') }}</h3>
          <p>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.q1.answer') }}</p>

          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.q2.title') }}</h3>
          <p>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.q2.answer') }}</p>

          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.q3.title') }}</h3>
          <p>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.q3.answer') }}</p>

          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.q4.title') }}</h3>
          <p>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.faq.q4.answer') }}</p>

          <h2>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.conclusion.title') }}</h2>
          <p>
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.conclusion.text') }}
            <a href="https://t.me/caloriesnote_bot" class="cta-link">{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.conclusion.link') }}</a> 
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.conclusion.ending') }}
          </p>
        </div>

        <!-- CTA Section -->
        <div class="article-cta">
          <h3>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.cta.title') }}</h3>
          <p>{{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.cta.description') }}</p>
          <a href="https://t.me/caloriesnote_bot" class="cta-button">
            {{ $t('blog.posts.podschet-kaloriy-po-foto-telegram-bot.content.cta.button') }}
          </a>
        </div>
      </div>
    </article>
  </div>
</template>

<script setup>
// SEO мета-теги для статьи
useSeoMeta({
  title: 'Подсчет калорий по фото: как работает Telegram-бот для анализа питания | Calories Bot',
  description: 'Узнайте, как работает подсчет калорий по фото в Telegram-боте. Преимущества автоматического анализа питания, точность ИИ и интеграция с Google Calendar.',
  keywords: 'подсчет калорий по фото, Telegram бот анализ питания, КБЖУ по фото, дневник питания, анализ еды, похудение, здоровое питание, ИИ анализ еды',
  ogTitle: 'Подсчет калорий по фото: как работает Telegram-бот для анализа питания',
  ogDescription: 'Узнайте, как работает подсчет калорий по фото в Telegram-боте. Преимущества автоматического анализа питания.',
  ogImage: 'https://calories.toxiguard.site/blog/podschet-kaloriy-po-foto.jpg',
  twitterCard: 'summary_large_image',
  twitterTitle: 'Подсчет калорий по фото: как работает Telegram-бот для анализа питания',
  twitterDescription: 'Узнайте, как работает подсчет калорий по фото в Telegram-боте. Преимущества автоматического анализа питания.'
})

// JSON-LD для статьи
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Подсчет калорий по фото: как работает и зачем нужен Telegram-бот для анализа питания",
        "description": "Узнайте, как работает подсчет калорий по фото в Telegram-боте. Преимущества автоматического анализа питания, точность ИИ и интеграция с Google Calendar.",
        "image": "https://calories.toxiguard.site/blog/podschet-kaloriy-po-foto.jpg",
        "author": {
          "@type": "Organization",
          "name": "Calories Bot"
        },
        "publisher": {
          "@type": "Organization",
          "name": "Calories Bot",
          "url": "https://calories.toxiguard.site"
        },
        "datePublished": "2025-09-26",
        "dateModified": "2025-09-26",
        "mainEntityOfPage": {
          "@type": "WebPage",
          "@id": "https://calories.toxiguard.site/blog/podschet-kaloriy-po-foto-telegram-bot"
        }
      })
    }
  ]
})
</script>

<style scoped>
.article {
  @apply bg-white py-16;
}

.container {
  @apply max-w-4xl mx-auto px-6;
}

.article-header {
  @apply mb-12 text-center;
}

.article-meta {
  @apply flex items-center justify-center space-x-4 mb-6;
}

.article-date {
  @apply text-gray-500;
}

.article-category {
  @apply px-3 py-1 rounded-full text-sm font-medium;
  background: #ecfdf5;
  color: #10b981;
}

.article-title {
  @apply text-4xl font-bold text-gray-900 mb-6 leading-tight;
  font-size: clamp(2rem, 5vw, 3rem);
}

.article-excerpt {
  @apply text-xl text-gray-600 leading-relaxed max-w-3xl mx-auto;
}

.article-content {
  @apply max-w-none;
}

.article-content h2 {
  @apply text-3xl font-bold text-gray-900 mt-12 mb-6;
}

.article-content h3 {
  @apply text-2xl font-semibold text-gray-900 mt-8 mb-4;
}

.article-image {
  @apply my-8 text-center;
}

.article-image img {
  @apply rounded-lg shadow-lg max-w-full h-auto;
  border: 1px solid #e5e7eb;
}

.image-caption {
  @apply text-sm text-gray-600 mt-3 italic;
}

.article-content p {
  @apply text-gray-700 leading-relaxed mb-6;
}

.article-content ul,
.article-content ol {
  @apply mb-6 pl-6;
}

.article-content li {
  @apply text-gray-700 leading-relaxed mb-2;
}

.article-content strong {
  @apply font-semibold text-gray-900;
}

.cta-link {
  @apply text-emerald-600 font-medium hover:text-emerald-700 transition-colors duration-200;
}

.article-cta {
  @apply bg-gradient-to-r from-emerald-50 to-green-50 rounded-2xl p-8 mt-16 text-center;
  border: 1px solid #a7f3d0;
}

.article-cta h3 {
  @apply text-2xl font-bold text-gray-900 mb-4;
}

.article-cta p {
  @apply text-gray-600 mb-6;
}

.cta-button {
  @apply inline-flex items-center justify-center px-8 py-4 text-lg font-medium text-white rounded-lg transition-all duration-200;
  background: #10b981;
  border: none;
}

.cta-button:hover {
  background: #059669;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .article {
    @apply py-12;
  }
  
  .article-title {
    @apply text-3xl;
  }
  
  .article-excerpt {
    @apply text-lg;
  }
  
  .article-content h2 {
    @apply text-2xl;
  }
  
  .article-content h3 {
    @apply text-xl;
  }
}
</style>
