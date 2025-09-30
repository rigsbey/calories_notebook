<template>
  <div>
    <!-- Header -->
    <HeaderSection />
    
    <!-- Blog Hero -->
    <section class="blog-hero">
      <div class="container">
        <h1 class="blog-title">{{ $t('blog.title') }}</h1>
        <p class="blog-subtitle">{{ $t('blog.subtitle') }}</p>
      </div>
    </section>

    <!-- Blog Posts -->
    <section class="blog-posts">
      <div class="container">
        <div class="posts-grid">
          <article class="post-card" v-for="post in posts" :key="post.slug">
            <div class="post-image">
              <img :src="post.image" :alt="$t(`blog.posts.${post.slug}.title`)" />
            </div>
            <div class="post-content">
              <div class="post-meta">
                <span class="post-date">{{ $t('blog.publishedOn') }} {{ post.date }}</span>
                <span class="post-category">{{ $t(`blog.posts.${post.slug}.category`) }}</span>
              </div>
              <h2 class="post-title">
                <NuxtLink :to="`/blog/${post.slug}`">{{ $t(`blog.posts.${post.slug}.title`) }}</NuxtLink>
              </h2>
              <p class="post-excerpt">{{ $t(`blog.posts.${post.slug}.excerpt`) }}</p>
              <div class="post-footer">
                <NuxtLink :to="`/blog/${post.slug}`" class="read-more">
                  {{ $t('blog.readMore') }} →
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
const { t } = useI18n()
useSeoMeta({
  title: () => `${t('blog.title')} | Calories Bot`,
  description: () => t('blog.subtitle'),
  keywords: 'nutrition blog, calorie counting, healthy eating, food analysis, macros, nutrition diary, Telegram bot',
  ogTitle: () => `${t('blog.title')} | Calories Bot`,
  ogDescription: () => t('blog.subtitle'),
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
        "name": t('blog.title'),
        "description": t('blog.subtitle'),
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
    date: '26 сентября 2025',
    image: '/blog/podschet-kaloriy-po-foto.jpg'
  },
  {
    slug: 'avtomaticheskiy-dnevnik-pitaniya',
    date: '28 сентября 2025',
    image: '/blog/avtomaticheskiy-dnevnik-pitaniya.jpg'
  },
  {
    slug: 'ii-v-pitanii-kak-iskusstvennyy-intellekt-menyaet-zdorove',
    date: '28 сентября 2025',
    image: '/blog/ii-v-pitanii.jpg'
  },
  {
    slug: 'pochemu-vazhno-sledit-za-kaloriyami-nauka-zdorove-prakticheskie-vyvody',
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
