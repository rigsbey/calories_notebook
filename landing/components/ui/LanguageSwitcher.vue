<template>
  <div class="language-switcher">
    <button 
      @click="toggleDropdown"
      class="language-button"
      :class="{ 'active': isOpen }"
    >
      <span class="current-lang">{{ currentLanguage.name }}</span>
      <svg 
        class="dropdown-icon" 
        :class="{ 'rotated': isOpen }"
        width="12" 
        height="8" 
        viewBox="0 0 12 8" 
        fill="none"
      >
        <path 
          d="M1 1.5L6 6.5L11 1.5" 
          stroke="currentColor" 
          stroke-width="1.5" 
          stroke-linecap="round" 
          stroke-linejoin="round"
        />
      </svg>
    </button>
    
    <div 
      v-if="isOpen" 
      class="language-dropdown"
      @click.stop
      :style="{ display: isOpen ? 'block' : 'none' }"
    >
      <button 
        v-for="locale in availableLocales" 
        :key="locale.code"
        @click="switchLanguage(locale.code)"
        class="language-option"
        :class="{ 'active': locale.code === currentLocale }"
      >
        <span class="flag">{{ getFlag(locale.code) }}</span>
        <span class="name">{{ locale.name }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
const { locale, locales, setLocale } = useI18n()

const isOpen = ref(false)

const currentLocale = computed(() => locale.value)
const availableLocales = computed(() => locales.value)
const currentLanguage = computed(() => 
  availableLocales.value.find(l => l.code === currentLocale.value) || availableLocales.value[0]
)

const getFlag = (code) => {
  const flags = {
    'ru': '🇷🇺',
    'en': '🇺🇸'
  }
  return flags[code] || '🌐'
}

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const emit = defineEmits(['language-changed'])

const switchLanguage = async (newLocale) => {
  try {
    await setLocale(newLocale)
    isOpen.value = false
    emit('language-changed')
    // Обновляем страницу для применения изменений
    await navigateTo(useRoute().path, { replace: true })
  } catch (error) {
    console.error('Error switching locale:', error)
  }
}

// Закрытие при клике вне компонента
let clickHandler = null

onMounted(() => {
  clickHandler = (e) => {
    if (!e.target.closest('.language-switcher')) {
      isOpen.value = false
    }
  }
  document.addEventListener('click', clickHandler)
})

onUnmounted(() => {
  if (clickHandler) {
    document.removeEventListener('click', clickHandler)
  }
})
</script>

<style scoped>
.language-switcher {
  position: relative;
}

.language-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  background-color: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  transition: all 0.2s;
  cursor: pointer;
}

.language-button:hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.language-button.active {
  border-color: #9ca3af;
  background-color: #f9fafb;
}

.current-lang {
  font-weight: 500;
}

.dropdown-icon {
  transition: transform 0.2s;
}

.dropdown-icon.rotated {
  transform: rotate(180deg);
}

.language-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  z-index: 9999;
  min-width: 140px;
}

.language-option {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 8px 12px;
  font-size: 14px;
  color: #374151;
  background: none;
  border: none;
  cursor: pointer;
  transition: background-color 0.15s;
}

.language-option:hover {
  background-color: #f9fafb;
}

.language-option:first-child {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.language-option:last-child {
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.language-option.active {
  background-color: #f3f4f6;
  color: #111827;
  font-weight: 500;
}

.flag {
  font-size: 16px;
}

.name {
  font-weight: 500;
}

@media (max-width: 768px) {
  .language-button {
    padding: 10px 16px;
    font-size: 16px;
    width: 100%;
    justify-content: center;
    border-radius: 12px;
    background-color: #f8fafc;
    border-color: #e2e8f0;
  }
  
  .language-button:hover {
    background-color: #f1f5f9;
    border-color: #cbd5e1;
  }
  
  .language-dropdown {
    right: 0;
    left: auto;
    min-width: 100%;
    top: 100%;
    margin-top: 8px;
    border-radius: 12px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }
  
  .language-option {
    padding: 12px 16px;
    font-size: 16px;
  }
}
</style>
