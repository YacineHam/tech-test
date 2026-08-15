<template>
  <div>
    <PageHeader :title="t('documents.title')" :subtitle="t('documents.subtitle')">
      <template #actions>
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          :loading="uploading"
          @click="fileInput.click()"
        >
          {{ t('documents.upload') }}
        </v-btn>
        <input
          ref="fileInput"
          type="file"
          accept="application/pdf"
          class="d-none"
          @change="onFileSelected"
        />
      </template>
    </PageHeader>

    <v-alert
      v-if="uploadError"
      type="error"
      density="compact"
      closable
      class="mb-4"
      @click:close="uploadError = false"
    >
      {{ t('documents.uploadError') }}
    </v-alert>

    <DataTable :headers="headers" :items="documents" :loading="loading">
      <template #item.thumbnail_path="{ item }">
        <v-img
          v-if="item.thumbnail_path"
          :src="`${MEDIA_URL}/${item.thumbnail_path}`"
          width="48"
          height="48"
          cover
          rounded
          class="my-2"
        />
        <v-icon v-else icon="mdi-file-pdf-box" size="32" color="grey" />
      </template>
      <template #item.number_of_pages="{ item }">
        {{ item.number_of_pages ?? '—' }}
      </template>
      <template #item.size_bytes="{ item }">
        {{ formatSize(item.size_bytes) }}
      </template>
      <template #item.uploaded_at="{ item }">
        {{ formatDate(item.uploaded_at) }}
      </template>
      <template #item.status="{ item }">
        <v-chip :color="STATUS_COLORS[item.status]" size="small" label>
          {{ t(`documents.status.${item.status}`) }}
        </v-chip>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import api from '@/api/client'
import DataTable from '@/components/common/DataTable.vue'
import PageHeader from '@/components/common/PageHeader.vue'

const { t, locale } = useI18n()

const MEDIA_URL = `${api.defaults.baseURL}/media`

const STATUS_COLORS = { processing: 'warning', ready: 'success', failed: 'error' }

const POLL_INTERVAL_MS = 2000

const headers = computed(() => [
  { title: t('documents.headers.thumbnail'), key: 'thumbnail_path', sortable: false },
  { title: t('documents.headers.name'), key: 'name' },
  { title: t('documents.headers.pages'), key: 'number_of_pages' },
  { title: t('documents.headers.size'), key: 'size_bytes' },
  { title: t('documents.headers.uploaded'), key: 'uploaded_at' },
  { title: t('documents.headers.status'), key: 'status' },
])

const documents = ref([])
const loading = ref(false)
const uploading = ref(false)
const uploadError = ref(false)
const fileInput = ref(null)

let pollTimer = null

function formatDate(value) {
  return new Date(value).toLocaleDateString(locale.value)
}

function formatSize(bytes) {
  const format = (value) =>
    value.toLocaleString(locale.value, { maximumFractionDigits: 1 })
  if (bytes < 1024) return `${format(bytes)} ${t('documents.units.b')}`
  if (bytes < 1024 * 1024) return `${format(bytes / 1024)} ${t('documents.units.kb')}`
  return `${format(bytes / (1024 * 1024))} ${t('documents.units.mb')}`
}

async function load({ silent = false } = {}) {
  if (!silent) loading.value = true
  try {
    const { data } = await api.get('/api/documents')
    documents.value = data
    syncPolling()
  } finally {
    if (!silent) loading.value = false
  }
}

function syncPolling() {
  const processing = documents.value.some((doc) => doc.status === 'processing')
  if (processing && !pollTimer) {
    pollTimer = setInterval(() => load({ silent: true }), POLL_INTERVAL_MS)
  } else if (!processing && pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

async function onFileSelected(event) {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  uploading.value = true
  uploadError.value = false
  try {
    await api.post('/api/documents', formData)
    await load()
  } catch {
    uploadError.value = true
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}

onMounted(load)
onUnmounted(() => clearInterval(pollTimer))
</script>
