<template>
  <Dropdown :options="dropdownItems" v-bind="$attrs">
    <template #default="{ open }">
      <button
        :class="[
          'flex h-auto min-h-12 w-full items-center gap-3 rounded-lg px-2 py-2.5 transition-all duration-200',
          'hover:bg-sidebar-accent hover:text-sidebar-foreground',
          'focus:outline-none focus:ring-2 focus:ring-sidebar-ring',
          open ? 'bg-sidebar-accent shadow-sm' : '',
        ]"
      >
        <!-- Logo/Brand -->
        <div
          :class="[
            'flex shrink-0 items-center justify-center rounded-md transition-all duration-200',
            isCollapsed ? 'h-10 w-10' : 'h-8 w-8',
          ]"
        >
          <BrandLogo v-model="brand" :class="['h-full w-full flex-shrink-0']" />
        </div>

        <!-- User Info -->
        <transition
          enter-active-class="transition-all duration-200 ease-out"
          leave-active-class="transition-all duration-150 ease-in"
          enter-from-class="opacity-0 -translate-x-2"
          enter-to-class="opacity-100 translate-x-0"
          leave-from-class="opacity-100 translate-x-0"
          leave-to-class="opacity-0 -translate-x-2"
        >
          <div
            v-if="!isCollapsed"
            class="flex flex-1 flex-col items-start text-left"
          >
            <span
              :class="[
                'text-sm font-semibold leading-tight',
                'text-sidebar-foreground',
              ]"
            >
              {{ __(brand.name || 'CRM') }}
            </span>
            <span
              :class="[
                'mt-0.5 text-xs font-medium leading-tight',
                'text-sidebar-foreground/60',
              ]"
            >
              {{ user.full_name }}
            </span>
          </div>
        </transition>

        <!-- Chevron Indicator -->
        <transition
          enter-active-class="transition-all duration-200 ease-out"
          leave-active-class="transition-all duration-150 ease-in"
          enter-from-class="opacity-0 scale-75"
          enter-to-class="opacity-100 scale-100"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-75"
        >
          <div
            v-if="!isCollapsed"
            class="flex shrink-0 items-center justify-center"
          >
            <ChevronDownIcon
              :class="[
                'h-4 w-4 text-sidebar-foreground/50 transition-transform duration-200',
                open && 'rotate-180',
              ]"
            />
          </div>
        </transition>
      </button>
    </template>
  </Dropdown>
</template>

<script setup>
import { computed, h, markRaw } from 'vue'
import BrandLogo from '@/components/BrandLogo.vue'
import FrappeCloudIcon from '@/components/Icons/FrappeCloudIcon.vue'
import Apps from '@/components/Apps.vue'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/users'
import { getSettings } from '@/stores/settings'
import { showSettings, isMobileView } from '@/composables/settings'
import { showAboutModal } from '@/composables/modals'
import { confirmLoginToFrappeCloud } from '@/composables/frappecloud'
import { Dropdown, useTheme } from 'frappe-ui'

// Chevron down icon component
const ChevronDownIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="m6 9 6 6 6-6"/>
    </svg>
  `,
}

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false,
  },
})

const { settings, brand } = getSettings()
const { logout } = sessionStore()
const { getUser } = usersStore()
const { currentTheme, toggleTheme } = useTheme()

const user = computed(() => getUser() || {})

const dropdownItems = computed(() => {
  if (!settings.value?.dropdown_items) return []

  const items = settings.value.dropdown_items

  const _dropdownItems = [
    {
      group: 'Dropdown Items',
      hideLabel: true,
      items: [],
    },
  ]

  items.forEach((item) => {
    if (item.hidden) return
    if (item.type !== 'Separator') {
      _dropdownItems[_dropdownItems.length - 1].items.push(
        dropdownItemObj(item),
      )
    } else {
      _dropdownItems.push({
        group: '',
        hideLabel: true,
        items: [],
      })
    }
  })

  return _dropdownItems
})

function dropdownItemObj(item) {
  const _item = JSON.parse(JSON.stringify(item))
  let icon = _item.icon || 'external-link'
  if (typeof icon === 'string' && icon.startsWith('<svg')) {
    icon = markRaw(h('div', { innerHTML: icon }))
  }
  _item.icon = icon

  if (_item.is_standard) {
    return getStandardItem(_item)
  }

  return {
    icon: _item.icon,
    label: __(_item.label),
    onClick: () =>
      window.open(_item.route, _item.open_in_new_window ? '_blank' : ''),
  }
}

function getStandardItem(item) {
  switch (item.name1) {
    case 'app_selector':
      return {
        component: markRaw(Apps),
      }
    case 'toggle_theme':
      return {
        icon: currentTheme.value === 'dark' ? 'sun' : item.icon,
        label: __(item.label),
        onClick: toggleTheme,
      }
    case 'settings':
      return {
        icon: item.icon,
        label: __(item.label),
        onClick: () => (showSettings.value = true),
        condition: () => !isMobileView.value,
      }
    case 'login_to_fc':
      return {
        icon: h(FrappeCloudIcon),
        label: __(item.label),
        onClick: () => confirmLoginToFrappeCloud(),
        condition: () => !isMobileView.value && window.is_fc_site,
      }
    case 'about':
      return {
        icon: item.icon,
        label: __(item.label),
        onClick: () => (showAboutModal.value = true),
      }
    case 'logout':
      return {
        icon: item.icon,
        label: __(item.label),
        onClick: () => logout.submit(),
      }
  }
}
</script>

<style scoped>
/* Smooth transitions */
button {
  transition-property: color, background-color, transform, opacity, box-shadow;
}
</style>
