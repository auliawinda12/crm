<template>
  <div
    :class="[
      'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
      variantClasses,
      className,
    ]"
  >
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (value) =>
      ['default', 'secondary', 'destructive', 'outline', 'ghost', 'accent'].includes(
        value
      ),
  },
  className: {
    type: String,
    default: '',
  },
})

const variantClasses = computed(() => {
  const variants = {
    default: 'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
    secondary: 'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
    destructive:
      'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
    outline: 'text-foreground',
    ghost: 'border-transparent bg-transparent text-foreground hover:bg-accent hover:text-accent-foreground',
    accent: 'border-transparent bg-accent text-accent-foreground hover:bg-accent/80',
  }
  return variants[props.variant] || variants.default
})
</script>
