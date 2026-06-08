import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  const fontSize = ref(100) // Percentual
  const isHighContrast = ref(false)
  const theme = ref('default') // 'default' ou 'alternative'

  const toggleHighContrast = () => {
    isHighContrast.value = !isHighContrast.value
  }

  const increaseFontSize = () => {
    if (fontSize.value < 150) fontSize.value += 10
  }

  const decreaseFontSize = () => {
    if (fontSize.value > 80) fontSize.value -= 10
  }

  const setTheme = (newTheme) => {
    theme.value = newTheme
  }

  // Watchers para aplicar mudanças no DOM
  watch(isHighContrast, (val) => {
    if (val) {
      document.documentElement.classList.add('high-contrast')
    } else {
      document.documentElement.classList.remove('high-contrast')
    }
  }, { immediate: true })

  watch(fontSize, (val) => {
    document.documentElement.style.fontSize = `${val}%`
  }, { immediate: true })

  watch(theme, (val) => {
    document.documentElement.setAttribute('data-theme', val)
  }, { immediate: true })

  return {
    fontSize,
    isHighContrast,
    theme,
    toggleHighContrast,
    increaseFontSize,
    decreaseFontSize,
    setTheme
  }
})
