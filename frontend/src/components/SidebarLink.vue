<template>
  <component
    :is="to ? 'button' : 'div'"
    :class="[
      'group relative flex w-full items-center gap-3 rounded-lg transition-all duration-200',
      'focus:outline-none focus:ring-2 focus:ring-sidebar-ring focus:ring-offset-2 focus:ring-offset-sidebar',
      buttonClasses,
    ]"
    @click="handleClick"
  >
    <!-- Icon Container -->
    <Tooltip
      :text="label"
      placement="right"
      :disabled="!isCollapsed"
    >
      <div
        :class="[
          'flex h-9 w-9 shrink-0 items-center justify-center rounded-md transition-all duration-200',
          iconContainerClasses,
        ]"
      >
        <slot name="icon">
          <Icon
            :icon="icon"
            :class="[
              'h-4 w-4 shrink-0 transition-all duration-200',
              iconClasses,
            ]"
          />
        </slot>
      </div>
    </Tooltip>

    <!-- Label Container -->
    <Tooltip
      :text="label"
      placement="right"
      :disabled="isCollapsed"
      :hoverDelay="1.5"
    >
      <transition
        enter-active-class="transition-all duration-200 ease-out"
        leave-active-class="transition-all duration-150 ease-in"
        enter-from-class="opacity-0 translate-x-[-8px]"
        enter-to-class="opacity-100 translate-x-0"
        leave-from-class="opacity-100 translate-x-0"
        leave-to-class="opacity-0 translate-x-[-8px]"
      >
        <span
          v-if="!isCollapsed"
          :class="[
            'flex-1 truncate text-sm font-medium',
            labelClasses,
          ]"
        >
          {{ label }}
        </span>
      </transition>
    </Tooltip>

    <!-- Right Slot (Badges, etc.) -->
    <transition
      enter-active-class="transition-all duration-200 ease-out"
      leave-active-class="transition-all duration-150 ease-in"
      enter-from-class="opacity-0 translate-x-[8px]"
      enter-to-class="opacity-100 translate-x-0"
      leave-from-class="opacity-100 translate-x-0"
      leave-to-class="opacity-0 translate-x-[8px]"
    >
      <div
        v-if="!isCollapsed && $slots.right"
        class="ml-auto flex shrink-0 items-center"
      >
        <slot name="right" />
      </div>
    </transition>

    <!-- Active Indicator -->
    <transition
      enter-active-class="transition-all duration-200 ease-out"
      leave-active-class="transition-all duration-150 ease-in"
      enter-from-class="scale-0 opacity-0"
      enter-to-class="scale-100 opacity-100"
      leave-from-class="scale-100 opacity-100"
      leave-to-class="scale-0 opacity-0"
    >
      <div
        v-if="isActive"
        :class="[
          'absolute left-0 top-1/2 h-8 w-1 -translate-y-1/2 rounded-r-full',
          'bg-primary shadow-lg shadow-primary/50',
          isCollapsed && 'left-1/2 top-auto -translate-x-1/2 h-1 w-8 rounded-full',
        ]"
      />
    </transition>

    <!-- Hover Glow Effect -->
    <div
      :class="[
        'absolute inset-0 rounded-lg opacity-0 transition-opacity duration-200',
        'bg-gradient-to-r from-primary/0 via-primary/5 to-primary/0',
        'group-hover:opacity-100',
      ]"
    />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Icon from '@/components/Icon.vue'
import { Tooltip } from 'frappe-ui'
import { isMobileView, mobileSidebarOpened } from '@/composables/settings'

const router = useRouter()
const route = useRoute()

const props = defineProps({
  icon: {
    type: [Object, String, Function],
  },
  label: {
    type: String,
    default: '',
  },
  to: {
    type: [Object, String],
    default: '',
  },
  isCollapsed: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

const isActive = computed(() => {
  if (!props.to) return false
  if (route.query.view) {
    return route.query.view == props.to?.query?.view
  }
  return route.name === props.to
})

const buttonClasses = computed(() => {
  const baseClasses = 'cursor-pointer select-none'

  if (isActive.value) {
    return [
      baseClasses,
      'bg-sidebar-accent text-sidebar-accent-foreground',
      'shadow-sm',
    ]
  }

  return [
    baseClasses,
    'text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground',
    'active:bg-sidebar-accent',
  ]
})

const iconContainerClasses = computed(() => {
  if (isActive.value) {
    return 'bg-primary/10 text-primary'
  }
  return 'text-sidebar-foreground/70 group-hover:text-sidebar-foreground'
})

const iconClasses = computed(() => {
  if (isActive.value) {
    return ''
  }
  return 'group-hover:scale-110'
})

const labelClasses = computed(() => {
  return isActive.value ? 'text-sidebar-accent-foreground' : ''
})

function handleClick(event) {
  emit('click', event)

  if (!props.to) return

  if (typeof props.to === 'object') {
    router.push(props.to)
  } else {
    router.push({ name: props.to })
  }

  if (isMobileView.value) {
    mobileSidebarOpened.value = false
  }
}
</script>

<style scoped>
/* Smooth transitions */
.group\/sidebar * {
  transition-property: color, background-color, border-color, transform, opacity;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Icon hover effect */
.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}

/* Ensure proper stacking of elements */
.group\/sidebar > * {
  position: relative;
  z-index: 1;
}

.group\/sidebar > .absolute {
  z-index: 0;
}
</style>
