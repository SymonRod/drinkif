import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'

require('@/assets/main.scss');
require('@/assets/js/modal.js'); 

createApp(App).use(store).use(i18n).use(router).mount('#app')
