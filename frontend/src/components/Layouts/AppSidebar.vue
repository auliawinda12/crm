<template>
  <aside
    :class="[
      'group/sidebar relative flex h-full flex-col border-r bg-sidebar transition-all duration-300 ease-in-out',
      'glass-effect border-gradient',
      isSidebarCollapsed ? 'w-16' : 'w-64',
    ]"
  >
    <!-- Header / Logo Section -->
    <div class="flex flex-col border-b border-sidebar-border p-3">
      <UserDropdown :isCollapsed="isSidebarCollapsed" />

      <!-- Theme Toggle - Only show when expanded -->
      <transition
        enter-active-class="transition-all duration-200 ease-out"
        leave-active-class="transition-all duration-150 ease-in"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div
          v-if="!isSidebarCollapsed"
          class="mt-2 flex items-center justify-between rounded-lg bg-accent/50 p-2"
        >
          <span class="text-xs font-medium text-accent-foreground/70">Theme</span>
          <ThemeSwitcher
            :show-label="false"
            className="!static !p-0 !bg-transparent"
            @change="handleThemeChange"
          />
        </div>
      </transition>
    </div>

    <!-- Navigation Section -->
    <ScrollArea
      ref="scrollAreaRef"
      scroll-class="sidebar-scroll"
      content-class="flex flex-col gap-1 p-2"
    >
      <!-- Notifications -->
      <SidebarLink
        id="notifications-btn"
        :label="__('Notifications')"
        :icon="NotificationsIcon"
        :isCollapsed="isSidebarCollapsed"
        @click="() => toggleNotificationPanel()"
      >
        <template #right>
          <Badge
            v-if="!isSidebarCollapsed && unreadNotificationsCount"
            :label="unreadNotificationsCount"
            variant="destructive"
            class="ml-auto"
          />
          <div
            v-else-if="unreadNotificationsCount"
            class="absolute -right-1 top-2 z-20 h-2 w-2 rounded-full bg-destructive ring-2 ring-sidebar"
          />
        </template>
      </SidebarLink>

      <Separator orientation="horizontal" class="mx-1.5 my-1" />

      <!-- Navigation Sections -->
      <template v-for="view in allViews" :key="view.label">
        <CollapsibleSection
          :label="view.name"
          :hideLabel="view.hideLabel"
          :opened="view.opened"
        >
          <template #header="{ opened, hide, toggle }">
            <button
              v-if="!hide"
              :class="[
                'flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-sidebar-foreground/70 transition-colors',
                'hover:bg-sidebar-accent hover:text-sidebar-foreground',
                'focus:outline-none focus:ring-2 focus:ring-sidebar-ring',
                isSidebarCollapsed
                  ? 'h-0 w-0 overflow-hidden opacity-0 p-0'
                  : 'opacity-100',
              ]"
              @click="toggle()"
            >
              <ChevronRightIcon
                :class="[
                  'h-4 w-4 shrink-0 transition-transform duration-200',
                  opened && 'rotate-90',
                ]"
              />
              <span>{{ __(view.name) }}</span>
            </button>
          </template>

          <nav class="flex flex-col gap-0.5">
            <SidebarLink
              v-for="link in view.views"
              :key="link.label"
              :icon="link.icon"
              :label="__(link.label)"
              :to="link.to"
              :isCollapsed="isSidebarCollapsed"
            />
          </nav>
        </CollapsibleSection>
      </template>
    </ScrollArea>

    <!-- Footer Section -->
    <div class="flex flex-col border-t border-sidebar-border p-2">
      <!-- Banners -->
      <div class="flex flex-col gap-2 pb-2">
        <SignupBanner
          v-if="isDemoSite"
          :isSidebarCollapsed="isSidebarCollapsed"
          :afterSignup="() => capture('signup_from_demo_site')"
        />
        <TrialBanner
          v-if="isFCSite"
          :isSidebarCollapsed="isSidebarCollapsed"
          :afterUpgrade="() => capture('upgrade_plan_from_trial_banner')"
        />
        <GettingStartedBanner
          v-if="!isOnboardingStepsCompleted"
          :isSidebarCollapsed="isSidebarCollapsed"
        />
      </div>

      <!-- Help & Collapse -->
      <SidebarLink
        v-if="isOnboardingStepsCompleted"
        :label="__('Help')"
        :isCollapsed="isSidebarCollapsed"
        @click="
          () => {
            showHelpModal = minimize ? true : !showHelpModal
            minimize = !showHelpModal
          }
        "
      >
        <template #icon>
          <HelpIcon class="h-4 w-4" />
        </template>
      </SidebarLink>

      <!-- Collapse/Expand Button -->
      <button
        :class="[
          'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-sidebar-foreground/70 transition-all',
          'hover:bg-sidebar-accent hover:text-sidebar-foreground',
          'focus:outline-none focus:ring-2 focus:ring-sidebar-ring',
        ]"
        @click="toggleCollapse"
      >
        <span
          class="grid h-5 w-5 flex-shrink-0 place-items-center"
          :class="{ 'mx-auto': isSidebarCollapsed }"
        >
          <CollapseSidebar
            :class="[
              'h-5 w-5 text-sidebar-foreground/70 transition-transform duration-300',
              isSidebarCollapsed && 'rotate-180',
            ]"
          />
        </span>
        <transition
          enter-active-class="transition-all duration-200 ease-out"
          leave-active-class="transition-all duration-150 ease-in"
          enter-from-class="opacity-0 -translate-x-2"
          enter-to-class="opacity-100 translate-x-0"
          leave-from-class="opacity-100 translate-x-0"
          leave-to-class="opacity-0 -translate-x-2"
        >
          <span v-if="!isSidebarCollapsed">
            {{ isSidebarCollapsed ? __('Expand') : __('Collapse') }}
          </span>
        </transition>
      </button>
    </div>

    <!-- Modals & Components -->
    <Notifications />
    <Settings />
    <HelpModal
      v-if="showHelpModal"
      v-model="showHelpModal"
      v-model:articles="articles"
      :logo="CRMLogo"
      :afterSkip="(step) => capture('onboarding_step_skipped_' + step)"
      :afterSkipAll="() => capture('onboarding_steps_skipped')"
      :afterReset="(step) => capture('onboarding_step_reset_' + step)"
      :afterResetAll="() => capture('onboarding_steps_reset')"
      docsLink="https://docs.frappe.io/crm"
    />
    <IntermediateStepModal
      v-model="showIntermediateModal"
      :currentStep="currentStep"
    />
  </aside>
</template>

<script setup>
import { ref, computed, markRaw, onMounted } from 'vue'
import { useStorage } from '@vueuse/core'
import router from '@/router'
import { useGlobalTheme } from '@/composables/theme'
import ScrollArea from '@/components/ui/ScrollArea.vue'
import Separator from '@/components/ui/Separator.vue'
import Badge from '@/components/ui/Badge.vue'
import ThemeSwitcher from '@/components/ui/ThemeSwitcher.vue'
import CollapsibleSection from '@/components/CollapsibleSection.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import UserDropdown from '@/components/UserDropdown.vue'
import Notifications from '@/components/Notifications.vue'
import Settings from '@/components/Settings/Settings.vue'
import CRMLogo from '@/components/Icons/CRMLogo.vue'
import HelpIcon from '@/components/Icons/HelpIcon.vue'
import CollapseSidebar from '@/components/Icons/CollapseSidebar.vue'
import NotificationsIcon from '@/components/Icons/NotificationsIcon.vue'
import {
  SignupBanner,
  TrialBanner,
  HelpModal,
  GettingStartedBanner,
  useOnboarding,
  showHelpModal,
  minimize,
  IntermediateStepModal,
  useTelemetry,
} from 'frappe-ui/frappe'
import { viewsStore } from '@/stores/views'
import { notificationsStore, unreadNotificationsCount } from '@/stores/notifications'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/users'
import { showSettings, activeSettingsPage } from '@/composables/settings'
import { showChangePasswordModal } from '@/composables/modals'
import { FeatherIcon, call } from 'frappe-ui'

// Chevron icon
const ChevronRightIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="m9 18 6-6-6-6"/>
    </svg>
  `,
}

// Stores & Composables
const { getPinnedViews, getPublicViews } = viewsStore()
const { toggle: toggleNotificationPanel } = notificationsStore()
const { capture } = useTelemetry()
const { theme } = useGlobalTheme()

// State
const isSidebarCollapsed = useStorage('isSidebarCollapsed', false)
const isFCSite = ref(window.is_fc_site)
const isDemoSite = ref(window.is_demo_site)
const scrollAreaRef = ref(null)

// Onboarding
const { user } = sessionStore()
const { users, isManager } = usersStore()
const { isOnboardingStepsCompleted, setUp } = useOnboarding('frappecrm')

// Navigation links
import LucideLayoutDashboard from '~icons/lucide/layout-dashboard'
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
import DealsIcon from '@/components/Icons/DealsIcon.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import CalendarIcon from '@/components/Icons/CalendarIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import PinIcon from '@/components/Icons/PinIcon.vue'
import SquareAsterisk from '@/components/Icons/SquareAsterisk.vue'
import InviteIcon from '@/components/Icons/InviteIcon.vue'
import ConvertIcon from '@/components/Icons/ConvertIcon.vue'
import CommentIcon from '@/components/Icons/CommentIcon.vue'
import EmailIcon from '@/components/Icons/EmailIcon.vue'
import StepsIcon from '@/components/Icons/StepsIcon.vue'

const links = [
  { label: 'Dashboard', icon: LucideLayoutDashboard, to: 'Dashboard' },
  { label: 'Leads', icon: LeadsIcon, to: 'Leads' },
  { label: 'Deals', icon: DealsIcon, to: 'Deals' },
  { label: 'Contacts', icon: ContactsIcon, to: 'Contacts' },
  { label: 'Organizations', icon: OrganizationsIcon, to: 'Organizations' },
  { label: 'Notes', icon: NoteIcon, to: 'Notes' },
  { label: 'Tasks', icon: TaskIcon, to: 'Tasks' },
  { label: 'Calendar', icon: CalendarIcon, to: 'Calendar' },
  { label: 'Call Logs', icon: PhoneIcon, to: 'Call Logs' },
]

// Views computation
const allViews = computed(() => {
  let _views = [
    {
      name: 'All Views',
      hideLabel: true,
      opened: true,
      views: links.filter((link) => {
        if (link.condition) {
          return link.condition()
        }
        return true
      }),
    },
  ]

  if (getPublicViews().length) {
    _views.push({
      name: 'Public views',
      opened: true,
      views: parseView(getPublicViews()),
    })
  }

  if (getPinnedViews().length) {
    _views.push({
      name: 'Pinned views',
      opened: true,
      views: parseView(getPinnedViews()),
    })
  }

  return _views
})

function parseView(views) {
  return views.map((view) => ({
    label: view.label,
    icon: getIcon(view.route_name, view.icon),
    to: {
      name: view.route_name,
      params: { viewType: view.type || 'list' },
      query: { view: view.name },
    },
  }))
}

function getIcon(routeName, icon) {
  if (icon) return icon

  const iconMap = {
    Leads: LeadsIcon,
    Deals: DealsIcon,
    Contacts: ContactsIcon,
    Organizations: OrganizationsIcon,
    Notes: NoteIcon,
    'Call Logs': PhoneIcon,
  }

  return iconMap[routeName] || PinIcon
}

// Theme handling
function handleThemeChange(newTheme) {
  console.log('Theme changed to:', newTheme)
}

// Toggle collapse
function toggleCollapse() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
  // Scroll to top after expand
  if (!isSidebarCollapsed.value && scrollAreaRef.value) {
    setTimeout(() => {
      scrollAreaRef.value.scrollTop?.()
    }, 300)
  }
}

// Onboarding steps (kept from original)
const showIntermediateModal = ref(false)
const currentStep = ref({})

const steps = [
  {
    name: 'setup_your_password',
    title: __('Setup your password'),
    icon: markRaw(SquareAsterisk),
    completed: false,
    onClick: () => {
      minimize.value = true
      showChangePasswordModal.value = true
    },
  },
  {
    name: 'create_first_lead',
    title: __('Create your first lead'),
    icon: markRaw(LeadsIcon),
    completed: false,
    onClick: () => {
      minimize.value = true
      router.push({ name: 'Leads' })
    },
  },
  {
    name: 'invite_your_team',
    title: __('Invite your team'),
    icon: markRaw(InviteIcon),
    completed: false,
    onClick: () => {
      minimize.value = true
      showSettings.value = true
      activeSettingsPage.value = 'Invite User'
    },
    condition: () => isManager(),
  },
  {
    name: 'convert_lead_to_deal',
    title: __('Convert lead to deal'),
    icon: markRaw(ConvertIcon),
    completed: false,
    dependsOn: 'create_first_lead',
    onClick: async () => {
      minimize.value = true
      currentStep.value = {
        title: __('Convert lead to deal'),
        buttonLabel: __('Convert'),
        videoURL: '/assets/crm/videos/convertToDeal.mov',
        onClick: async () => {
          showIntermediateModal.value = false
          currentStep.value = {}
          let lead = await getFirstLead()
          if (lead) {
            router.push({ name: 'Lead', params: { leadId: lead } })
          } else {
            router.push({ name: 'Leads' })
          }
        },
      }
      showIntermediateModal.value = true
    },
  },
  {
    name: 'create_first_task',
    title: __('Create your first task'),
    icon: markRaw(TaskIcon),
    completed: false,
    onClick: async () => {
      minimize.value = true
      let deal = await getFirstDeal()
      if (deal) {
        router.push({
          name: 'Deal',
          params: { dealId: deal },
          hash: '#tasks',
        })
      } else {
        router.push({ name: 'Tasks' })
      }
    },
  },
  {
    name: 'create_first_note',
    title: __('Create your first note'),
    icon: markRaw(NoteIcon),
    completed: false,
    onClick: async () => {
      minimize.value = true
      let deal = await getFirstDeal()
      if (deal) {
        router.push({
          name: 'Deal',
          params: { dealId: deal },
          hash: '#notes',
        })
      } else {
        router.push({ name: 'Notes' })
      }
    },
  },
  {
    name: 'add_first_comment',
    title: __('Add your first comment'),
    icon: markRaw(CommentIcon),
    completed: false,
    dependsOn: 'create_first_lead',
    onClick: async () => {
      minimize.value = true
      let deal = await getFirstDeal()
      if (deal) {
        router.push({
          name: 'Deal',
          params: { dealId: deal },
          hash: '#comments',
        })
      } else {
        router.push({ name: 'Leads' })
      }
    },
  },
  {
    name: 'send_first_email',
    title: __('Send email'),
    icon: markRaw(EmailIcon),
    completed: false,
    dependsOn: 'create_first_lead',
    onClick: async () => {
      minimize.value = true
      let deal = await getFirstDeal()
      if (deal) {
        router.push({
          name: 'Deal',
          params: { dealId: deal },
          hash: '#emails',
        })
      } else {
        router.push({ name: 'Leads' })
      }
    },
  },
  {
    name: 'change_deal_status',
    title: __('Change deal status'),
    icon: markRaw(StepsIcon),
    completed: false,
    dependsOn: 'convert_lead_to_deal',
    onClick: async () => {
      minimize.value = true
      currentStep.value = {
        title: __('Change deal status'),
        buttonLabel: __('Change'),
        videoURL: '/assets/crm/videos/changeDealStatus.mov',
        onClick: async () => {
          showIntermediateModal.value = false
          currentStep.value = {}
          let deal = await getFirstDeal()
          if (deal) {
            router.push({
              name: 'Deal',
              params: { dealId: deal },
              hash: '#activity',
            })
          } else {
            router.push({ name: 'Leads' })
          }
        },
      }
      showIntermediateModal.value = true
    },
  },
]

async function getFirstLead() {
  let firstLead = localStorage.getItem('firstLead' + user)
  if (firstLead) return firstLead
  return await call('crm.api.onboarding.get_first_lead')
}

async function getFirstDeal() {
  let firstDeal = localStorage.getItem('firstDeal' + user)
  if (firstDeal) return firstDeal
  return await call('crm.api.onboarding.get_first_deal')
}

// Help center articles
const articles = ref([
  {
    title: __('Introduction'),
    opened: false,
    subArticles: [
      { name: 'introduction', title: __('Introduction') },
      { name: 'setting-up', title: __('Setting up') },
    ],
  },
  {
    title: __('Settings'),
    opened: false,
    subArticles: [
      { name: 'profile', title: __('Profile') },
      { name: 'custom-branding', title: __('Custom branding') },
      { name: 'home-actions', title: __('Home actions') },
      { name: 'invite-users', title: __('Invite users') },
    ],
  },
  {
    title: __('Masters'),
    opened: false,
    subArticles: [
      { name: 'lead', title: __('Lead') },
      { name: 'deal', title: __('Deal') },
      { name: 'contact', title: __('Contact') },
      { name: 'organization', title: __('Organization') },
      { name: 'note', title: __('Note') },
      { name: 'task', title: __('Task') },
      { name: 'call-log', title: __('Call log') },
      { name: 'email-template', title: __('Email template') },
    ],
  },
  {
    title: __('Capturing leads'),
    opened: false,
    subArticles: [{ name: 'web-form', title: __('Web form') }],
  },
  {
    title: __('Views'),
    opened: false,
    subArticles: [
      { name: 'view', title: __('Saved view') },
      { name: 'public-view', title: __('Public view') },
      { name: 'pinned-view', title: __('Pinned view') },
    ],
  },
  {
    title: __('Other features'),
    opened: false,
    subArticles: [
      { name: 'email-communication', title: __('Email communication') },
      { name: 'comment', title: __('Comment') },
      { name: 'data', title: __('Data') },
      { name: 'service-level-agreement', title: __('Service level agreement') },
      { name: 'assignment-rule', title: __('Assignment rule') },
      { name: 'notification', title: __('Notification') },
    ],
  },
  {
    title: __('Customization'),
    opened: false,
    subArticles: [
      { name: 'custom-fields', title: __('Custom fields') },
      { name: 'custom-actions', title: __('Custom actions') },
      { name: 'custom-statuses', title: __('Custom statuses') },
      { name: 'custom-list-actions', title: __('Custom list actions') },
      { name: 'quick-entry-layout', title: __('Quick entry layout') },
    ],
  },
  {
    title: __('Integration'),
    opened: false,
    subArticles: [
      { name: 'twilio', title: __('Twilio') },
      { name: 'exotel', title: __('Exotel') },
      { name: 'whatsapp', title: __('WhatsApp') },
      { name: 'erpnext', title: __('ERPNext') },
    ],
  },
  {
    title: __('Frappe CRM mobile'),
    opened: false,
    subArticles: [
      { name: 'mobile-app-installation', title: __('Mobile app installation') },
    ],
  },
])

onMounted(async () => {
  await users.promise
  const filteredSteps = steps.filter((step) => {
    if (step.condition) {
      return step.condition()
    }
    return true
  })
  setUp(filteredSteps)
})
</script>

<style scoped>
/* Smooth transitions for collapse/expand */
.group/sidebar {
  transition-property: width, transform, opacity;
}

/* Custom scrollbar for sidebar */
:deep(.sidebar-scroll) {
  scrollbar-width: thin;
  scrollbar-color: hsl(var(--muted-foreground) / 0.2) transparent;
}

:deep(.sidebar-scroll)::-webkit-scrollbar {
  width: 4px;
}

:deep(.sidebar-scroll)::-webkit-scrollbar-track {
  background: transparent;
}

:deep(.sidebar-scroll)::-webkit-scrollbar-thumb {
  background: hsl(var(--muted-foreground) / 0.2);
  border-radius: 9999px;
}

:deep(.sidebar-scroll)::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--muted-foreground) / 0.3);
}

/* Ensure icons scale properly in collapsed state */
.sidebar-link-icon {
  transition: all 0.2s ease;
}

/* Tooltip positioning fix */
.tooltip {
  pointer-events: none;
}
</style>
