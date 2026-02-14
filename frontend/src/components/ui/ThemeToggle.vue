<template>
  <button
    :class="[
      'relative inline-flex h-9 w-9 items-center justify-center rounded-lg',
      'transition-all duration-200 ease-in-out',
      'hover:bg-accent hover:text-accent-foreground',
      'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
      'disabled:pointer-events-none disabled:opacity-50',
      className,
    ]"
    :aria-label="ariaLabel"
    @click="handleToggle"
  >
    <transition
      :name="transition"
      mode="out-in"
      enter-active-class="transition-all duration-200"
      leave-active-class="transition-all duration-200"
      enter-from-class="scale-75 opacity-0"
      enter-to-class="scale-100 opacity-100"
      leave-from-class="scale-100 opacity-100"
      leave-to-class="scale-75 opacity-0"
    >
      <component
        :is="iconComponent"
        :class="['h-[1.15rem] w-[1.15rem]', iconClass]"
      />
    </transition>
    <span class="sr-only">{{ ariaLabel }}</span>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useGlobalTheme } from '@/composables/theme'

// Icon components
const SunIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="4"/>
      <path d="M12 2v2"/>
      <path d="M12 20v2"/>
      <path d="m4.93 4.93 1.41 1.41"/>
      <path d="m17.66 17.66 1.41 1.41"/>
      <path d="M2 12h2"/>
      <path d="M20 12h2"/>
      <path d="m6.34 17.66-1.41 1.41"/>
      <path d="m19.07 4.93-1.41 1.41"/>
    </svg>
  `,
}

const MoonIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
    </svg>
  `,
}

const MonitorIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect width="20" height="14" x="2" y="3" rx="2"/>
      <line x1="8" x2="16" y1="21" y2="21"/>
      <line x1="12" x2="12" y1="17" y2="21"/>
    </svg>
  `,
}

const props = defineProps({
  className: {
    type: String,
    default: '',
  },
  iconClass: {
    type: String,
    default: '',
  },
  showLabel: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['change'])

const { theme, toggleTheme, isDark } = useGlobalTheme()

const ariaLabel = computed(() => {
  if (theme.value === 'system') {
    return `Switch theme (currently: ${isDark.value ? 'dark' : 'light'})`
  }
  return `Switch theme (currently: ${theme.value})`
})

const iconComponent = computed(() => {
  if (theme.value === 'light') return SunIcon
  if (theme.value === 'dark') return MoonIcon
  return MonitorIcon
})

function handleToggle() {
  toggleTheme()
  emit('change', theme.value)
}
</script>
