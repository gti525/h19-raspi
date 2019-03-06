import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import VueResource from "vue-resource";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(VueResource);
Vue.use(require("vue-moment"));

Vue.http.options.root = "http://localhost:8000";

Vue.http.interceptors.push((request, next) => {
  let token = JSON.parse(localStorage.getItem("token"));
  const removeAuthHeaders = request.url.includes("api");
  if (token) {
    if (removeAuthHeaders) {
      request.headers.delete("Authorization");
    } else {
      Vue.http.post("api/token/verify/", { token: token.access }).then(
        function() {},
        function(err) {
          if (err.status === 401) {
            Vue.http
              .post("api/token/refresh/", { refresh: token.refresh })
              .then(
                function(result) {
                  token.access = result.access;
                },
                function(err) {
                  console.log(err);
                  localStorage.removeItem("token");
                  Vue.router.push({
                    name: "home",
                    params: { error: "vous avez été déconnecté " }
                  });
                }
              );
          }
        }
      );
      request.headers.set("Authorization", token.access);
    }
  }
  console.log(request);
  next(response => console.log(response));
});

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
