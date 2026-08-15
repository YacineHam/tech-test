<template>
  <div>
    <PageHeader :title="t('settings.title')" :subtitle="t('settings.subtitle')" />

    <v-card elevation="1" max-width="480">
      <v-card-text>
        <div class="text-subtitle-1 font-weight-medium mb-1">
          {{ t('settings.language') }}
        </div>
        <div class="text-body-2 text-medium-emphasis mb-4">
          {{ t('settings.languageHint') }}
        </div>

        <v-select
          :model-value="locale"
          :items="LANGUAGES"
          item-title="label"
          item-value="value"
          variant="outlined"
          density="comfortable"
          hide-details
          @update:model-value="setLocale"
        />
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

// Languages offered in the switcher. Labels are shown in their own language on
// purpose, the way most apps present a language picker.
const LANGUAGES = [
  { label: 'English', value: 'en' },
  { label: 'Français', value: 'fr' },
]

function setLocale(value) {
  locale.value = value
  localStorage.setItem('locale', value) // survive a page reload
}
</script>
