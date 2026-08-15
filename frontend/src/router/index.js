import { createRouter, createWebHistory } from 'vue-router'

import UsersView from '@/views/UsersView.vue'
import SettingsView from '@/views/SettingsView.vue'

const routes = [
  { path: '/', redirect: '/users' },
  { path: '/users', name: 'users', component: UsersView },
  { path: '/settings', name: 'settings', component: SettingsView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
