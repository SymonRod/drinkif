import './plugins/axios'
import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import './registerServiceWorker'
import LoadScript from "vue-plugin-load-script";
import i18n from './i18n'


require('@/assets/main.scss');

require('@/assets/js/modal.js');



createApp(App).use(i18n).use(router).use(store).use(LoadScript).mount('#app')
