import { computed, watch, onMounted } from 'vue'
import { useStorage } from '@vueuse/core'

const THEME_KEY = 'crm-theme'
const SYSTEM_THEME_KEY = 'crm-system-theme'

export function useTheme() {
  // Get stored theme or default to 'system'
  const storedTheme = useStorage(THEME_KEY, 'system')

  // Computed to resolve actual theme (dark/light)
  const actualTheme = computed(() => {
    if (storedTheme.value === 'system') {
      return getSystemTheme()
    }
    return storedTheme.value
  })

  // Computed to check if current theme is dark
  const isDark = computed(() => actualTheme.value === 'dark')

  // Computed for theme label (for display purposes)
  const themeLabel = computed(() => {
    if (storedTheme.value === 'system') {
      return `System (${isDark.value ? 'Dark' : 'Light'})`
    }
    return storedTheme.value.charAt(0).toUpperCase() + storedTheme.value.slice(1)
  })

  // Function to get system theme preference
  function getSystemTheme() {
    if (typeof window === 'undefined') return 'light'
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light'
  }

  // Function to set theme
  function setTheme(theme) {
    if (!['light', 'dark', 'system'].includes(theme)) {
      console.warn(`Invalid theme: ${theme}`)
      return
    }
    storedTheme.value = theme
    applyTheme(theme === 'system' ? getSystemTheme() : theme)
  }

  // Function to toggle theme
  function toggleTheme() {
    if (storedTheme.value === 'light') {
      setTheme('dark')
    } else if (storedTheme.value === 'dark') {
      setTheme('system')
    } else {
      // If system, toggle to opposite of current actual theme
      setTheme(isDark.value ? 'light' : 'dark')
    }
  }

  // Function to apply theme to DOM
  function applyTheme(theme) {
    if (typeof window === 'undefined') return

    const root = document.documentElement
    const isDarkMode = theme === 'dark'

    if (isDarkMode) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }

    // Store for potential SSR or other uses
    localStorage.setItem(SYSTEM_THEME_KEY, theme)
  }

  // Listen for system theme changes
  function listenForSystemThemeChange() {
    if (typeof window === 'undefined') return

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

    const handleChange = () => {
      if (storedTheme.value === 'system') {
        applyTheme(getSystemTheme())
      }
    }

    // Modern browsers
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange)
      return () => mediaQuery.removeEventListener('change', handleChange)
    }
    // Older browsers
    else if (mediaQuery.addListener) {
      mediaQuery.addListener(handleChange)
      return () => mediaQuery.removeListener(handleChange)
    }
  }

  // Apply theme on mount
  onMounted(() => {
    applyTheme(actualTheme.value)
    const cleanup = listenForSystemThemeChange()

    // Cleanup on unmount (if component uses cleanup)
    if (cleanup) {
      watch(
        () => null,
        () => cleanup?.()
      )
    }
  })

  return {
    theme: computed(() => storedTheme.value),
    actualTheme,
    isDark,
    themeLabel,
    setTheme,
    toggleTheme,
  }
}

// Singleton instance for global use
let globalThemeInstance = null

export function useGlobalTheme() {
  if (!globalThemeInstance) {
    globalThemeInstance = useTheme()
  }
  return globalThemeInstance
}
