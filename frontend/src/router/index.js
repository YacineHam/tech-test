import { createRouter, createWebHistory } from 'vue-router'

import UsersView from '@/views/UsersView.vue'
import DocumentsView from '@/views/DocumentsView.vue'
import SettingsView from '@/views/SettingsView.vue'

const routes = [
  { path: '/', redirect: '/users' },
  { path: '/users', name: 'users', component: UsersView },
  { path: '/documents', name: 'documents', component: DocumentsView },
  { path: '/settings', name: 'settings', component: SettingsView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
