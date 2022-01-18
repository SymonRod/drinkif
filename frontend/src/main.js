import './plugins/axios'
import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
//import './registerServiceWorker'
import LoadScript from "vue-plugin-load-script";
import i18n from './i18n'

require('@/assets/main.scss');
require('@/assets/js/modal.js'); 
require('../node_modules/@fortawesome/fontawesome-free/js/all.js');
require('../node_modules/material-design-icons/iconfont/material-icons.css');

createApp(App).use(i18n).use(router).use(store).use(LoadScript).mount('#app')
