// plugins/vuetify.js
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const dark = {
  dark: true,
  colors: {
    primary: "#00bad3",
    secondary: "#424242",
  },
}

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    components,
    directives,
    theme: {
      defaultTheme: 'dark',
      themes: {
        dark,
      }
    },
  })
  nuxtApp.vueApp.use(vuetify)
})
