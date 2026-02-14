<template>
  <div
    :class="[
      'shrink-0 bg-border',
      orientation === 'horizontal' ? 'h-[1px] w-full' : 'h-full w-[1px]',
      decorative ? 'role-none' : 'role-separator',
      className,
    ]"
    :role="decorative ? 'none' : 'separator'"
    :aria-orientation="orientation"
  />
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  orientation: {
    type: String,
    default: 'horizontal',
    validator: (value) => ['horizontal', 'vertical'].includes(value),
  },
  decorative: {
    type: Boolean,
    default: false,
  },
  className: {
    type: String,
    default: '',
  },
})
</script>
