import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import VueResource from "vue-resource";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(VueResource);

Vue.http.options.root = "http://localhost:8000";
Vue.http.interceptors.push((request, next) => {
  console.log(request);
  next(response => {
    console.log(response);
  });
});
Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
