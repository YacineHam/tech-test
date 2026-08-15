<template>
  <div>
    <PageHeader :title="t('users.title')" :subtitle="t('users.subtitle')" />

    <DataTable :headers="headers" :items="users" :loading="loading">
      <template #item.role="{ item }">
        <v-chip :color="roleColor(item.role)" size="small" label>
          {{ item.role }}
        </v-chip>
      </template>
      <template #item.created_at="{ item }">
        {{ formatDate(item.created_at) }}
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

// Headers are computed so the column titles re-translate when the language
// changes. Dates are formatted using the active locale too.
const headers = computed(() => [
  { title: t('users.headers.id'), key: 'id' },
  { title: t('users.headers.name'), key: 'name' },
  { title: t('users.headers.email'), key: 'email' },
  { title: t('users.headers.role'), key: 'role' },
  { title: t('users.headers.created'), key: 'created_at' },
])

const users = ref([])
const loading = ref(false)

const ROLE_COLORS = { Admin: 'primary', Reviewer: 'secondary', Viewer: 'grey' }
function roleColor(role) {
  return ROLE_COLORS[role] || 'grey'
}

function formatDate(value) {
  return new Date(value).toLocaleDateString(locale.value)
}

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/api/users')
    users.value = data
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
