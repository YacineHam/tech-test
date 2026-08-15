<template>
  <!-- Reusable page header: a title on the left, optional actions on the right
       (passed via the #actions slot, e.g. an "Add" button). Used by every view
       so page layout stays consistent. -->
  <div class="d-flex align-center justify-space-between mb-4">
    <div>
      <h1 class="text-h5 font-weight-bold">{{ title }}</h1>
      <div v-if="subtitle" class="text-body-2 text-medium-emphasis">
        {{ subtitle }}
      </div>
    </div>
    <div>
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>
