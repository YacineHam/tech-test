<template>
  <v-app>
    <SideBar />
    <v-main class="bg-background">
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import SideBar from '@/components/SideBar.vue'
</script>
