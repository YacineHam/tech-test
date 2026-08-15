import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Brand palette taken from the reciTAL design system (suite-ui). Use these theme
// tokens in templates (color="primary", text-success, ...) rather than raw hex,
// so a future palette change is a one-line edit here.
export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#502BFF',
          'primary-lighten1': '#9985FF',
          'primary-lighten2': '#CCC2FF',
          'primary-darken1': '#0000CA',
          'primary-darken2': '#14007A',
          'primary-darken3': '#07002D',
          secondary: '#0F64FF',
          'secondary-lighten1': '#6D91FF',
          success: '#2EC96E',
          warning: '#F5B941',
          error: '#F11A34',
          surface: '#FFFFFF',
          background: '#F4F5F9',
        },
      },
    },
  },
  defaults: {
    VCard: { rounded: 'lg' },
  },
})
