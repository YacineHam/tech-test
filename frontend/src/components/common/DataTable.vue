<template>
  <!--
    Reusable table. Wraps Vuetify's v-data-table with the project's card styling,
    a built-in search field and sensible defaults.

    Props:
      - headers : column definitions ([{ title, key }, ...])
      - items   : array of rows
      - loading : show the loading bar

    Any named slot you pass (e.g. #item.price) is forwarded straight to
    v-data-table, so callers can customise individual cells without re-styling
    the whole table.
  -->
  <v-card elevation="1">
    <v-card-text>
      <v-text-field
        v-model="search"
        prepend-inner-icon="mdi-magnify"
        :label="t('common.search')"
        density="compact"
        variant="outlined"
        hide-details
        single-line
        clearable
        class="mb-4"
        style="max-width: 320px"
      />

      <v-data-table
        class="data-table"
        :headers="headers"
        :items="items"
        :loading="loading"
        :search="search"
        :items-per-page="10"
        hover
      >
        <!-- Forward every slot the caller provides to v-data-table. -->
        <template v-for="(_, name) in $slots" #[name]="slotProps">
          <slot :name="name" v-bind="slotProps" />
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

defineProps({
  headers: { type: Array, required: true },
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})

const { t } = useI18n()
const search = ref('')
</script>

<style scoped>
/* Match the reciTAL (suite-ui) table look: tall, medium-weight headers on a
   white background and roomy rows. */
.data-table {
  border-radius: 4px;
}

.data-table :deep(.v-data-table__th) {
  height: 54px !important;
  font-size: 16px !important;
  font-weight: 500 !important;
  background-color: rgb(var(--v-theme-surface)) !important;
}

.data-table :deep(.v-data-table__tr) {
  height: 52px !important;
  transition: background-color 0.2s ease;
}
</style>
