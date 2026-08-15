import { createI18n } from 'vue-i18n'

import en from '@/locales/en.json'
import fr from '@/locales/fr.json'

// Locale files live in src/locales/<lang>.json. To add a language, drop a new
// file there and add it to `messages` below. Components must use t('...') /
// $t('...') for any user-facing string so it is translatable.
const FALLBACK = 'en'

export default createI18n({
  legacy: false, // Composition API: useI18n() in <script setup>
  locale: localStorage.getItem('locale') || FALLBACK,
  fallbackLocale: FALLBACK,
  messages: { en, fr },
})
