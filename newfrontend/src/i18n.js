import { createI18n } from 'vue-i18n'

import * as it from './locales/it.json' 
import * as en from './locales/en.json' 

//console.log(it)


var messages = {
  'it-IT': it.default,
  'en-US': en.default
}

/**
 * Load locale messages
 *
 * The loaded `JSON` locale messages is pre-compiled by `@intlify/vue-i18n-loader`, which is integrated into `vue-cli-plugin-i18n`.
 * See: https://github.com/intlify/vue-i18n-loader#rocket-i18n-resource-pre-compilation
 */
// function loadLocaleMessages() {
//   const locales = require.context('./locales', true, /[A-Za-z0-9-_,\s]+\.json$/i)
//   console.log('locales', locales);
//   const messages = {}
//   locales.keys().forEach(key => {
//     console.log(key);
//     const matched = key.match(/([A-Za-z0-9-_]+)\./i)
//     if (matched && matched.length > 1) {
//       const locale = matched[1]
//       messages[locale] = locales(key).default
//     }
//   })
//   return messages
// }

//console.log(messages)

export default createI18n({
  globalInjection: true,
  legacy: false,
  locale: 'it-IT',
  fallbackLocale: 'it-IT',
  messages: messages
})
