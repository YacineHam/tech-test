<template>
  <v-navigation-drawer
    permanent
    color="primary-darken3"
    theme="dark"
    width="240"
  >
    <div class="px-5 py-6">
      <div class="text-h6 font-weight-bold">reciTAL</div>
      <div class="text-caption" style="color: #ffffff88">{{ t('app.subtitle') }}</div>
    </div>

    <v-list nav density="comfortable" class="px-3">
      <!-- Add a new section by appending to NAV_ITEMS below — give it a labelKey
           that exists in the locale files (src/locales/*.json). -->
      <v-list-item
        v-for="item in NAV_ITEMS"
        :key="item.to"
        :to="item.to"
        :prepend-icon="item.icon"
        :title="t(item.labelKey)"
        rounded="lg"
        class="nav-item"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Single source of truth for the menu. Each entry maps to a route in
// src/router/index.js and a translation key in the locale files.
const NAV_ITEMS = [
  { labelKey: 'nav.users', icon: 'mdi-account-group', to: '/users' },
  { labelKey: 'nav.settings', icon: 'mdi-cog', to: '/settings' },
]
</script>

<style scoped>
/* Inactive items: white text on the dark navy drawer.
   Active item: lavender pill with dark navy text — the reciTAL (suite-ui) look. */
.nav-item {
  color: #ffffffcc;
  margin-bottom: 4px;
}

.nav-item.v-list-item--active {
  background-color: rgb(var(--v-theme-primary-lighten2)) !important;
  color: rgb(var(--v-theme-primary-darken3)) !important;
}
</style>
