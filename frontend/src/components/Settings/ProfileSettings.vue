<template>
  <div class="flex h-full flex-col gap-6 p-8 text-ink-gray-8">
    <div class="flex-1 flex flex-col gap-6 mt-2 overflow-y-auto">
      <div v-if="profile" class="flex w-full items-center justify-between">
        <FileUploader
          @success="(file) => updateImage(file.file_url)"
          :validateFile="validateIsImageFile"
        >
          <template #default="{ openFileSelector, error: _error }">
            <div class="flex items-center gap-4">
              <div class="group relative !size-[66px]">
                <Avatar
                  class="!size-16"
                  :image="profile.user_image"
                  :label="profile.full_name"
                />
                <component
                  :is="profile.user_image ? Dropdown : 'div'"
                  v-bind="
                    profile.user_image
                      ? {
                          options: [
                            {
                              icon: 'upload',
                              label: profile.user_image
                                ? __('Change image')
                                : __('Upload image'),
                              onClick: openFileSelector,
                            },
                            {
                              icon: 'trash-2',
                              label: __('Remove image'),
                              onClick: () => updateImage(),
                            },
                          ],
                        }
                      : { onClick: openFileSelector }
                  "
                  class="!absolute bottom-0 left-0 right-0"
                >
                  <div
                    class="z-1 absolute bottom-0.5 left-0 right-0.5 flex h-9 cursor-pointer items-center justify-center rounded-b-full bg-black bg-opacity-40 pt-3 opacity-0 duration-300 ease-in-out group-hover:opacity-100"
                    style="
                      -webkit-clip-path: inset(12px 0 0 0);
                      clip-path: inset(12px 0 0 0);
                    "
                  >
                    <CameraIcon class="size-4 cursor-pointer text-white" />
                  </div>
                </component>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-2xl font-semibold text-ink-gray-8">
                  {{ profile.full_name }}
                </span>
                <span class="text-base text-ink-gray-7">
                  {{ profile.email }}
                </span>
                <ErrorMessage :message="__(_error)" />
              </div>
            </div>
          </template>
        </FileUploader>
        <Button
          :label="__('Change password')"
          icon-left="lock"
          @click="showChangePasswordModal = true"
        />
        <ChangePasswordModal
          v-if="showChangePasswordModal"
          v-model="showChangePasswordModal"
        />
      </div>
      <div class="flex flex-col gap-4">
        <div class="flex justify-between gap-4">
          <FormControl
            class="w-full"
            :label="__('First name')"
            v-model="profile.first_name"
          />
          <FormControl
            class="w-full"
            :label="__('Last name')"
            v-model="profile.last_name"
          />
        </div>
      </div>
      <div
        v-if="isAdministrator"
        class="flex flex-col gap-4 rounded-lg border border-outline-gray-2 bg-surface-gray-1 p-5"
      >
        <div class="flex items-start justify-between gap-4">
          <div>
            <h3 class="text-lg font-semibold text-ink-gray-8">
              {{ __('Administrator Email Settings') }}
            </h3>
            <p class="text-sm text-ink-gray-5 mt-1">
              {{
                __('Change the email address for the Administrator account')
              }}
            </p>
          </div>
          <Button
            v-if="!editingAdminEmail"
            :label="__('Change Email')"
            icon-left="edit"
            @click="startEditingAdminEmail"
          />
        </div>

        <div class="rounded-md border border-outline-gray-2 bg-surface-modal p-4">
          <label class="text-sm text-ink-gray-5">
            {{ __('Current Administrator Email') }}
          </label>
          <div class="mt-1 flex items-center gap-2">
            <span class="text-base font-medium text-ink-gray-8">
              {{ currentAdminEmail || __('Not set') }}
            </span>
            <Badge
              v-if="!editingAdminEmail && currentAdminEmail"
              variant="subtle"
              theme="green"
              :label="__('Active')"
            />
          </div>
        </div>

        <div v-if="editingAdminEmail" class="flex flex-col gap-4">
          <FormControl
            v-model="newAdminEmail"
            type="email"
            :label="__('New Email Address')"
            :placeholder="__('Enter new email address')"
            :description="__('The Administrator will use this email to login')"
          />
          <FormControl
            v-model="confirmAdminEmail"
            type="email"
            :label="__('Confirm Email Address')"
            :placeholder="__('Confirm new email address')"
          />
          <ErrorMessage :message="adminEmailError" />

          <div class="flex justify-end gap-3">
            <Button
              :label="__('Cancel')"
              variant="outline"
              @click="cancelEditingAdminEmail"
            />
            <Button
              :label="__('Save Changes')"
              variant="solid"
              :loading="updateAdminEmail.loading"
              :disabled="!isAdminEmailFormValid"
              @click="saveAdminEmail"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="flex justify-between items-center">
      <div>
        <ErrorMessage :message="error" />
      </div>
      <Button
        variant="solid"
        :label="__('Update')"
        :disabled="!dirty"
        :loading="setUser.loading"
        @click="setUser.submit()"
      />
    </div>
  </div>
</template>
<script setup>
import ChangePasswordModal from '@/components/Modals/ChangePasswordModal.vue'
import CameraIcon from '@/components/Icons/CameraIcon.vue'
import { usersStore } from '@/stores/users'
import { validateIsImageFile } from '@/utils'
import {
  Dropdown,
  FileUploader,
  Avatar,
  Badge,
  createResource,
  toast,
} from 'frappe-ui'
import { ref, computed, onMounted } from 'vue'

const { getUser, users } = usersStore()

const user = computed(() => getUser() || {})

const profile = ref({})
const error = ref('')
const showChangePasswordModal = ref(false)
const currentAdminEmail = ref('')
const newAdminEmail = ref('')
const confirmAdminEmail = ref('')
const editingAdminEmail = ref(false)
const adminEmailError = ref('')

const isAdministrator = computed(() => user.value.name === 'Administrator')

const dirty = computed(() => {
  return (
    profile.value.first_name !== user.value.first_name ||
    profile.value.last_name !== user.value.last_name
  )
})

const isAdminEmailFormValid = computed(() => {
  return (
    newAdminEmail.value &&
    confirmAdminEmail.value &&
    newAdminEmail.value === confirmAdminEmail.value &&
    newAdminEmail.value !== currentAdminEmail.value &&
    isValidEmail(newAdminEmail.value)
  )
})

const setUser = createResource({
  url: 'frappe.client.set_value',
  makeParams() {
    return {
      doctype: 'User',
      name: user.value.name,
      fieldname: {
        first_name: profile.value.first_name,
        last_name: profile.value.last_name,
        user_image: profile.value.user_image,
      },
    }
  },
  onSuccess: () => {
    error.value = ''
    toast.success(__('Profile updated successfully'))
    users.reload()
  },
  onError: (err) => {
    error.value = err.messages[0] || __('Failed to update profile')
  },
})

const getCurrentAdminEmail = createResource({
  url: 'crm.api.get_admin_email',
  onSuccess: (data) => {
    currentAdminEmail.value = data?.email || ''
    profile.value.email = data?.email || profile.value.email
  },
})

const updateAdminEmail = createResource({
  url: 'crm.api.update_admin_email',
  makeParams() {
    return {
      new_email: newAdminEmail.value,
    }
  },
  onSuccess: () => {
    currentAdminEmail.value = newAdminEmail.value
    profile.value.email = newAdminEmail.value
    editingAdminEmail.value = false
    newAdminEmail.value = ''
    confirmAdminEmail.value = ''
    adminEmailError.value = ''
    toast.success(__('Administrator email updated successfully'))
    users.reload()
  },
  onError: (err) => {
    adminEmailError.value =
      err.messages?.[0] || err.message || __('Failed to update email')
  },
})

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

function startEditingAdminEmail() {
  editingAdminEmail.value = true
  newAdminEmail.value = ''
  confirmAdminEmail.value = ''
  adminEmailError.value = ''
}

function cancelEditingAdminEmail() {
  editingAdminEmail.value = false
  newAdminEmail.value = ''
  confirmAdminEmail.value = ''
  adminEmailError.value = ''
}

function saveAdminEmail() {
  adminEmailError.value = ''

  if (!newAdminEmail.value) {
    adminEmailError.value = __('Please enter a new email address')
    return
  }

  if (newAdminEmail.value !== confirmAdminEmail.value) {
    adminEmailError.value = __('Email addresses do not match')
    return
  }

  if (newAdminEmail.value === currentAdminEmail.value) {
    adminEmailError.value = __('New email must be different from current email')
    return
  }

  if (!isValidEmail(newAdminEmail.value)) {
    adminEmailError.value = __('Please enter a valid email address')
    return
  }

  updateAdminEmail.submit()
}

function updateImage(fileUrl = '') {
  profile.value.user_image = fileUrl
  setUser.submit()
}

onMounted(() => {
  profile.value = { ...user.value }
  if (isAdministrator.value) {
    currentAdminEmail.value = user.value.email || ''
    getCurrentAdminEmail.fetch()
  }
})
</script>
