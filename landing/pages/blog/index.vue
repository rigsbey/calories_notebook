<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Blog Hero -->
    <section class="blog-hero">
      <div class="container">
        <h1 class="blog-title">Блог о питании и здоровье</h1>
        <p class="blog-subtitle">Полезные статьи о правильном питании, подсчете калорий и здоровом образе жизни</p>
      </div>
    </section>

    <!-- Blog Posts -->
    <section class="blog-posts">
      <div class="container">
        <div class="posts-grid">
          <article class="post-card" v-for="post in posts" :key="post.slug">
            <div class="post-image">
              <img 
                :src="post.image" 
                :alt="post.title" 
                loading="lazy"
                class="w-full h-48 object-cover rounded-lg"
              />
            </div>
            <div class="post-content">
              <div class="post-meta">
                <span class="post-date">Опубликовано {{ post.date }}</span>
                <span class="post-category">{{ post.category }}</span>
              </div>
              <h2 class="post-title">
                <NuxtLink :to="`/blog/${post.slug}`">{{ post.title }}</NuxtLink>
              </h2>
              <p class="post-excerpt">{{ post.excerpt }}</p>
              <div class="post-footer">
                <NuxtLink :to="`/blog/${post.slug}`" class="read-more">
                  Читать далее →
                </NuxtLink>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// SEO мета-теги для блога
useSeoMeta({
  title: 'Блог о питании и здоровье | Calories Bot',
  description: 'Полезные статьи о правильном питании, подсчете калорий и здоровом образе жизни. ИИ-анализ еды и автоматический дневник питания.',
  ogTitle: 'Блог о питании и здоровье | Calories Bot',
  ogDescription: 'Полезные статьи о правильном питании, подсчете калорий и здоровом образе жизни',
  ogImage: 'https://calories.toxiguard.site/blog-og.jpg',
  ogUrl: 'https://calories.toxiguard.site/blog',
  robots: 'index, follow',
  author: 'Calories Bot'
})

// Canonical URL и JSON-LD для блога
useHead({
  link: [
    { rel: 'canonical', href: 'https://calories.toxiguard.site/blog' }
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Блог о питании и здоровье",
        "description": "Полезные статьи о правильном питании, подсчете калорий и здоровом образе жизни",
        "url": "https://calories.toxiguard.site/blog",
        "publisher": {
          "@type": "Organization",
          "name": "Calories Bot",
          "url": "https://calories.toxiguard.site"
        }
      })
    }
  ]
})

// Список статей
const posts = ref([
  {
    slug: 'podschet-kaloriy-po-foto-telegram-bot',
    title: 'Подсчет калорий по фото: как Telegram-бот меняет правила игры',
    excerpt: 'Узнайте, как ИИ-анализ фотографий еды помогает точно считать калории и контролировать питание',
    category: 'Питание',
    date: '26 сентября 2025',
    image: '/blog/podschet-kaloriy-po-foto.jpg'
  },
  {
    slug: 'avtomaticheskiy-dnevnik-pitaniya',
    title: 'Автоматический дневник питания: будущее уже здесь',
    excerpt: 'Как технологии упрощают ведение дневника питания и помогают достичь целей в здоровье',
    category: 'Технологии',
    date: '28 сентября 2025',
    image: '/blog/avtomaticheskiy-dnevnik-pitaniya.jpg'
  },
  {
    slug: 'ii-v-pitanii-kak-iskusstvennyy-intellekt-menyaet-zdorove',
    title: 'ИИ в питании: как искусственный интеллект меняет здоровье',
    excerpt: 'Революция в области питания: как машинное обучение помогает принимать правильные решения',
    category: 'ИИ и здоровье',
    date: '28 сентября 2025',
    image: '/blog/ii-v-pitanii.jpg'
  },
  {
    slug: 'pochemu-vazhno-sledit-za-kaloriyami-nauka-zdorove-prakticheskie-vyvody',
    title: 'Почему важно следить за калориями: наука, здоровье, практические выводы',
    excerpt: 'Научные исследования о важности подсчета калорий и практические советы для здорового питания',
    category: 'Наука',
    date: '28 сентября 2025',
    image: '/blog/pochemu-vazhno-sledit-za-kaloriyami.jpg'
  }
])
</script>

<style scoped>
.blog-hero {
  @apply bg-gradient-to-br from-emerald-50 to-green-100 py-16;
}

.container {
  @apply max-w-6xl mx-auto px-6;
}

.blog-title {
  @apply text-4xl font-bold text-gray-900 text-center mb-4;
  font-size: clamp(2rem, 5vw, 3rem);
}

.blog-subtitle {
  @apply text-xl text-gray-600 text-center max-w-3xl mx-auto;
}

.blog-posts {
  @apply py-16 bg-white;
}

.posts-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8;
}

.post-card {
  @apply bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1;
  border: 1px solid #e5e7eb;
}

.post-image {
  @apply h-48 overflow-hidden;
}

.post-image img {
  @apply w-full h-full object-cover;
}

.post-content {
  @apply p-6;
}

.post-meta {
  @apply flex items-center space-x-4 mb-3;
}

.post-date {
  @apply text-sm text-gray-500;
}

.post-category {
  @apply text-sm px-3 py-1 rounded-full;
  background: #ecfdf5;
  color: #10b981;
  font-weight: 500;
}

.post-title {
  @apply text-xl font-bold text-gray-900 mb-3;
}

.post-title a {
  @apply text-gray-900 hover:text-emerald-600 transition-colors duration-200;
}

.post-excerpt {
  @apply text-gray-600 mb-4 leading-relaxed;
}

.read-more {
  @apply text-emerald-600 font-medium hover:text-emerald-700 transition-colors duration-200;
}

@media (max-width: 768px) {
  .blog-hero {
    @apply py-12;
  }
  
  .blog-title {
    @apply text-3xl;
  }
  
  .blog-subtitle {
    @apply text-lg;
  }
  
  .posts-grid {
    @apply grid-cols-1 gap-6;
  }
}
</style>
