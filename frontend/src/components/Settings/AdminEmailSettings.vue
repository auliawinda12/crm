<template>
  <div class="flex flex-col gap-6 p-8 h-full overflow-y-auto">
    <!-- Header -->
    <div>
      <h2 class="text-2xl font-semibold text-ink-gray-8">
        {{ __('Administrator Email Settings') }}
      </h2>
      <p class="text-base text-ink-gray-5 mt-1">
        {{ __('Change the email address for the Administrator account') }}
      </p>
    </div>

    <!-- Current Email Display -->
    <div class="bg-surface-gray-1 rounded-lg p-5 border border-outline-gray-2">
      <div class="flex items-center justify-between">
        <div>
          <label class="text-sm text-ink-gray-5 block mb-1">
            {{ __('Current Administrator Email') }}
          </label>
          <div class="flex items-center gap-2">
            <span class="text-lg font-medium text-ink-gray-8">
              {{ currentEmail }}
            </span>
            <Badge
              v-if="!editing"
              variant="subtle"
              theme="green"
              :label="__('Active')"
            />
          </div>
        </div>
        <Button
          v-if="!editing"
          :label="__('Change Email')"
          icon-left="edit"
          @click="startEditing"
        />
      </div>
    </div>

    <!-- Edit Form (shown when editing) -->
    <div v-if="editing" class="bg-surface-modal rounded-lg p-5 border border-outline-gray-2">
      <div class="flex flex-col gap-4">
        <!-- New Email Input -->
        <div>
          <FormControl
            v-model="newEmail"
            type="email"
            :label="__('New Email Address')"
            :placeholder="__('Enter new email address')"
            :description="__('The Administrator will use this email to login')"
          />
        </div>

        <!-- Confirm Email Input -->
        <div>
          <FormControl
            v-model="confirmEmail"
            type="email"
            :label="__('Confirm Email Address')"
            :placeholder="__('Confirm new email address')"
          />
        </div>

        <!-- Warning Message -->
        <div class="flex items-start gap-3 bg-yellow-50 border border-yellow-200 rounded-md p-3">
          <WarningIcon class="size-5 text-yellow-600 shrink-0 mt-0.5" />
          <div class="text-sm text-yellow-800">
            <p class="font-medium">{{ __('Important:') }}</p>
            <ul class="list-disc list-inside mt-1 space-y-1">
              <li>{{ __('Make sure the new email is correct before saving') }}</li>
              <li>{{ __('You will need to login with the new email address') }}</li>
              <li>{{ __('All email notifications will be sent to this address') }}</li>
            </ul>
          </div>
        </div>

        <!-- Error Message -->
        <ErrorMessage
          v-if="errorMessage"
          :message="errorMessage"
          class="text-sm"
        />
      </div>
    </div>

    <!-- Action Buttons -->
    <div v-if="editing" class="flex justify-end gap-3 pt-2">
      <Button
        :label="__('Cancel')"
        variant="outline"
        @click="cancelEditing"
      />
      <Button
        :label="__('Save Changes')"
        variant="solid"
        :loading="saving"
        :disabled="!isValid"
        @click="saveEmail"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource, toast, FormControl, Badge } from 'frappe-ui'
import WarningIcon from '~icons/lucide/alert-triangle'

const currentEmail = ref('')
const newEmail = ref('')
const confirmEmail = ref('')
const editing = ref(false)
const saving = ref(false)
const errorMessage = ref('')

const isValid = computed(() => {
  return (
    newEmail.value &&
    confirmEmail.value &&
    newEmail.value === confirmEmail.value &&
    newEmail.value !== currentEmail.value &&
    isValidEmail(newEmail.value)
  )
})

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

function startEditing() {
  editing.value = true
  newEmail.value = ''
  confirmEmail.value = ''
  errorMessage.value = ''
}

function cancelEditing() {
  editing.value = false
  newEmail.value = ''
  confirmEmail.value = ''
  errorMessage.value = ''
}

const updateAdminEmail = createResource({
  url: 'crm.api.update_admin_email',
  makeParams() {
    return {
      new_email: newEmail.value
    }
  },
  onSuccess: () => {
    currentEmail.value = newEmail.value
    editing.value = false
    newEmail.value = ''
    confirmEmail.value = ''
    errorMessage.value = ''
    toast.success(__('Administrator email updated successfully'))
  },
  onError: (error) => {
    errorMessage.value = error.messages?.[0] || error.message || __('Failed to update email')
  }
})

function saveEmail() {
  errorMessage.value = ''

  if (!newEmail.value) {
    errorMessage.value = __('Please enter a new email address')
    return
  }

  if (newEmail.value !== confirmEmail.value) {
    errorMessage.value = __('Email addresses do not match')
    return
  }

  if (newEmail.value === currentEmail.value) {
    errorMessage.value = __('New email must be different from current email')
    return
  }

  if (!isValidEmail(newEmail.value)) {
    errorMessage.value = __('Please enter a valid email address')
    return
  }

  saving.value = true
  updateAdminEmail.submit()
    .finally(() => {
      saving.value = false
    })
}

const getCurrentEmail = createResource({
  url: 'crm.api.get_admin_email',
  onSuccess: (data) => {
    currentEmail.value = data.email
  }
})

onMounted(() => {
  getCurrentEmail.fetch()
})
</script>
