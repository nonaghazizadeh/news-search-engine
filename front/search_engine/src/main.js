import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import VueSidebarMenuAkahon from "vue-sidebar-menu-akahon";
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.component('vue-sidebar-menu-akahon', VueSidebarMenuAkahon);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
