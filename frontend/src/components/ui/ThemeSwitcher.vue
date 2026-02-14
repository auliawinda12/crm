<template>
  <div :class="['relative', className]">
    <button
      :class="[
        'flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
        'hover:bg-accent hover:text-accent-foreground',
        'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
        isOpen && 'bg-accent',
      ]"
      @click="toggleDropdown"
    >
      <component :is="currentIcon" class="h-4 w-4" />
      <span v-if="showLabel">{{ themeLabel }}</span>
    </button>

    <transition
      enter-active-class="transition-all duration-200 ease-out"
      leave-active-class="transition-all duration-150 ease-in"
      enter-from-class="opacity-0 scale-95 translate-y-1"
      enter-to-class="opacity-100 scale-100 translate-y-0"
      leave-from-class="opacity-100 scale-100 translate-y-0"
      leave-to-class="opacity-0 scale-95 translate-y-1"
    >
      <div
        v-if="isOpen"
        :class="[
          'absolute z-50 mt-2 min-w-[180px] overflow-hidden rounded-lg border bg-popover p-1 shadow-md',
          'animate-in fade-in-0 zoom-in-95 slide-in-from-top-2',
          positionClass,
        ]"
      >
        <button
          v-for="option in themeOptions"
          :key="option.value"
          :class="[
            'relative flex w-full cursor-pointer select-none items-center gap-3 rounded-md px-3 py-2 text-sm outline-none',
            'transition-colors',
            theme === option.value
              ? 'bg-accent text-accent-foreground'
              : 'text-foreground hover:bg-accent/50 hover:text-accent-foreground',
          ]"
          @click="selectTheme(option.value)"
        >
          <component :is="option.icon" class="h-4 w-4 shrink-0" />
          <span class="flex-1 text-left">{{ option.label }}</span>
          <span
            v-if="theme === option.value"
            class="ml-auto flex h-4 w-4 items-center justify-center"
          >
            <svg
              class="h-3.5 w-3.5"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </span>
        </button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
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
  showLabel: {
    type: Boolean,
    default: true,
  },
  position: {
    type: String,
    default: 'bottom',
    validator: (value) => ['top', 'bottom', 'left', 'right'].includes(value),
  },
})

const emit = defineEmits(['change'])

const { theme, setTheme, themeLabel } = useGlobalTheme()

const isOpen = ref(false)

const positionClass = computed(() => {
  const positions = {
    top: 'bottom-full mb-2',
    bottom: 'top-full mt-2',
    left: 'right-0',
    right: 'left-0',
  }
  return positions[props.position] || positions.bottom
})

const themeOptions = [
  { value: 'light', label: 'Light', icon: SunIcon },
  { value: 'dark', label: 'Dark', icon: MoonIcon },
  { value: 'system', label: 'System', icon: MonitorIcon },
]

const currentIcon = computed(() => {
  const option = themeOptions.find((opt) => opt.value === theme.value)
  return option?.icon || MonitorIcon
})

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

function selectTheme(value) {
  setTheme(value)
  isOpen.value = false
  emit('change', value)
}

function closeDropdown() {
  isOpen.value = false
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

function handleClickOutside(event) {
  const target = event.target
  if (target && !target.closest('.relative')) {
    closeDropdown()
  }
}
</script>
