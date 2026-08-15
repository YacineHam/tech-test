<template>
  <div>
    <PageHeader :title="t('documents.title')" :subtitle="t('documents.subtitle')" />

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
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import api from '@/api/client'
import DataTable from '@/components/common/DataTable.vue'
import PageHeader from '@/components/common/PageHeader.vue'

const { t, locale } = useI18n()

const MEDIA_URL = `${api.defaults.baseURL}/media`

const STATUS_COLORS = { processing: 'warning', ready: 'success', failed: 'error' }

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

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/api/documents')
    documents.value = data
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
