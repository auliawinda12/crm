<template>
  <div ref="scrollAreaRef" class="relative overflow-hidden">
    <div
      ref="viewportRef"
      :class="[
        'h-full w-full overflow-auto scroll-smooth',
        orientation === 'both' || orientation === 'horizontal'
          ? '[scrollbar-gutter:stable]'
          : '',
        scrollClass,
      ]"
    >
      <div ref="contentRef" :class="contentClass">
        <slot />
      </div>
    </div>
    <!-- Custom scrollbar for webkit browsers -->
    <div
      v-if="showScrollbar"
      :class="[
        'pointer-events-none absolute right-0 top-0 h-full w-2 transition-opacity',
        'touch-none',
      ]"
    >
      <div
        ref="scrollbarRef"
        :class="[
          'h-full w-full rounded-full opacity-0 transition-opacity duration-150',
          'hover:opacity-50',
          'bg-muted-foreground/20',
        ]"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  scrollClass: {
    type: String,
    default: 'sidebar-scroll',
  },
  contentClass: {
    type: String,
    default: '',
  },
  orientation: {
    type: String,
    default: 'vertical',
    validator: (value) => ['vertical', 'horizontal', 'both'].includes(value),
  },
  showScrollbar: {
    type: Boolean,
    default: false,
  },
})

const scrollAreaRef = ref(null)
const viewportRef = ref(null)
const contentRef = ref(null)
const scrollbarRef = ref(null)

const emit = defineEmits(['scroll'])

let resizeObserver = null

onMounted(() => {
  if (viewportRef.value) {
    viewportRef.value.addEventListener('scroll', handleScroll)

    // Observe content size changes
    if (typeof ResizeObserver !== 'undefined') {
      resizeObserver = new ResizeObserver(() => {
        updateScrollbar()
      })
      resizeObserver.observe(contentRef.value)
    }
  }
})

onUnmounted(() => {
  if (viewportRef.value) {
    viewportRef.value.removeEventListener('scroll', handleScroll)
  }
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})

function handleScroll(event) {
  emit('scroll', event)
  updateScrollbar()
}

function updateScrollbar() {
  if (!props.showScrollbar || !scrollbarRef.value || !viewportRef.value) return

  const viewport = viewportRef.value
  const content = contentRef.value
  const scrollbar = scrollbarRef.value

  const scrollRatio = viewport.scrollTop / (content.scrollHeight - viewport.clientHeight)
  const thumbHeight = (viewport.clientHeight / content.scrollHeight) * 100

  scrollbar.style.height = `${thumbHeight}%`
  scrollbar.style.transform = `translateY(${scrollRatio * (100 - thumbHeight)}%)`
}

// Expose scroll methods
defineExpose({
  scrollTo: (options) => viewportRef.value?.scrollTo(options),
  scrollTop: () => viewportRef.value?.scrollTo({ top: 0, behavior: 'smooth' }),
  scrollBottom: () =>
    viewportRef.value?.scrollTo({
      top: contentRef.value?.scrollHeight || 0,
      behavior: 'smooth',
    }),
})
</script>
