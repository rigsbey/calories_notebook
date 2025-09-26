<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Blog Hero -->
    <section class="blog-hero">
      <div class="container">
        <h1 class="blog-title">Блог о здоровом питании</h1>
        <p class="blog-subtitle">Полезные статьи о подсчете калорий, анализе питания и здоровом образе жизни</p>
      </div>
    </section>

    <!-- Blog Posts -->
    <section class="blog-posts">
      <div class="container">
        <div class="posts-grid">
          <article class="post-card" v-for="post in posts" :key="post.slug">
            <div class="post-image">
              <img :src="post.image" :alt="post.title" />
            </div>
            <div class="post-content">
              <div class="post-meta">
                <span class="post-date">{{ post.date }}</span>
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
  title: 'Блог о здоровом питании | Calories Bot - статьи о подсчете калорий',
  description: 'Полезные статьи о подсчете калорий, анализе питания и здоровом образе жизни. Советы по использованию Telegram-бота для контроля питания.',
  keywords: 'блог о питании, подсчет калорий, здоровое питание, анализ еды, КБЖУ, дневник питания, Telegram бот',
  ogTitle: 'Блог о здоровом питании | Calories Bot',
  ogDescription: 'Полезные статьи о подсчете калорий, анализе питания и здоровом образе жизни.',
  ogImage: 'https://calories.toxiguard.site/blog-og.jpg'
})

// JSON-LD для блога
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Блог Calories Bot",
        "description": "Полезные статьи о подсчете калорий, анализе питания и здоровом образе жизни",
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
    title: 'Подсчет калорий по фото: как работает и зачем нужен Telegram-бот для анализа питания',
    excerpt: 'Контроль питания - основа здорового образа жизни. Но подсчет калорий вручную - скучная рутина. Сегодня всё изменилось: появились Telegram-боты с ИИ...',
    date: '26 сентября 2025',
    category: 'Питание',
    image: '/blog/podschet-kaloriy-po-foto.jpg'
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
