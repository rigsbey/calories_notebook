<template>
  <header class="header">
    <div class="header-container">
      <div class="header-left">
        <div class="logo">
          <img src="/logo.jpg" alt="Calories Bot" class="logo-icon" />
          <span class="logo-text">Calories Bot</span>
        </div>
      </div>
      
      <nav class="header-nav">
        <a href="/#features" class="nav-link">{{ $t('nav.features') }}</a>
        <a href="/#how-it-works" class="nav-link">{{ $t('nav.howItWorks') }}</a>
        <a href="/#pricing" class="nav-link">{{ $t('nav.pricing') }}</a>
        <a href="/blog" class="nav-link">{{ $t('nav.blog') }}</a>
        <a href="/#faq" class="nav-link">{{ $t('nav.faq') }}</a>
        <a href="/privacy" class="nav-link">{{ $t('nav.privacy') }}</a>
      </nav>
      
      <div class="header-right">
        <LanguageSwitcher />
        <a href="https://t.me/caloriesnote_bot" class="btn-start-growing">
          {{ $t('nav.launchBot') }}
        </a>
      </div>

      <!-- Mobile menu button -->
      <button class="mobile-menu-btn" @click="toggleMobileMenu">
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>
    </div>

    <!-- Mobile menu -->
    <div class="mobile-menu" :class="{ 'mobile-menu--open': mobileMenuOpen }">
      <nav class="mobile-nav">
        <a href="/#features" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.features') }}</a>
        <a href="/#how-it-works" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.howItWorks') }}</a>
        <a href="/#pricing" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.pricing') }}</a>
        <a href="/blog" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.blog') }}</a>
        <a href="/#faq" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.faq') }}</a>
        <a href="/privacy" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.privacy') }}</a>
      </nav>
      
      <!-- Language Switcher for Mobile -->
      <div class="mobile-language-section">
        <LanguageSwitcher @language-changed="closeMobileMenu" />
      </div>
      
      <div class="mobile-buttons">
        <a href="https://t.me/caloriesnote_bot" class="btn-start-growing w-full">
          {{ $t('nav.launchBot') }}
        </a>
      </div>
    </div>
  </header>
</template>

<script setup>
import LanguageSwitcher from './ui/LanguageSwitcher.vue'

const mobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

// Close mobile menu when clicking outside
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.header') && mobileMenuOpen.value) {
      mobileMenuOpen.value = false
    }
  })
})
</script>

<style scoped>
.header {
  @apply bg-white border-b border-gray-100 sticky top-0 z-50;
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.95);
}

.header-container {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16;
}

.header-left {
  @apply flex items-center;
}

.logo {
  @apply flex items-center space-x-3;
}

.logo-icon {
  @apply w-8 h-8 rounded-full object-cover;
  border: 1px solid #e5e7eb;
}

.logo-text {
  @apply text-xl text-gray-900;
  font-weight: 500;
}

.header-nav {
  @apply hidden md:flex items-center space-x-8;
}

.nav-link {
  @apply text-gray-600 hover:text-gray-900 transition-colors duration-200;
  font-size: 15px;
  font-weight: 400;
}

.nav-link:hover {
  color: #374151;
}

.header-right {
  @apply hidden md:flex items-center space-x-4;
}

.btn-text {
  @apply text-gray-900 hover:text-gray-700 transition-colors duration-200;
  font-size: 16px;
  font-weight: 400;
  text-decoration: none;
}

.btn-start-growing {
  @apply px-4 py-2 rounded-full text-gray-900 transition-all duration-200;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  font-size: 16px;
  font-weight: 400;
  text-decoration: none;
}

.btn-start-growing:hover {
  background: #e5e7eb;
  border-color: #9ca3af;
}

.mobile-menu-btn {
  @apply md:hidden flex flex-col items-center justify-center w-6 h-6 space-y-1;
}

.hamburger-line {
  @apply w-6 h-0.5 bg-gray-600 transition-all duration-200;
}

.mobile-menu {
  @apply md:hidden bg-white border-t border-gray-100 absolute top-full left-0 right-0 shadow-lg transform transition-all duration-300 opacity-0 -translate-y-2 pointer-events-none;
}

.mobile-menu--open {
  @apply opacity-100 translate-y-0 pointer-events-auto;
}

.mobile-nav {
  @apply flex flex-col py-4;
}

.mobile-nav-link {
  @apply px-6 py-3 text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors duration-200 font-medium;
}

.mobile-language-section {
  @apply px-6 py-4 border-t border-gray-100;
}

.mobile-buttons {
  @apply px-6 pb-6;
}

.w-full {
  width: 100%;
}

.mb-3 {
  margin-bottom: 0.75rem;
}

@media (max-width: 768px) {
  .header-container {
    @apply px-4;
  }
  
  .logo-text {
    @apply text-lg;
  }
}
</style>
