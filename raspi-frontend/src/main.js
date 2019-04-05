import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import VueResource from "vue-resource";
import Notifications from "vue-notification";
import Vuelidate from "vuelidate";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(VueResource);
Vue.use(require("vue-moment"));
Vue.use(Notifications);
Vue.use(Vuelidate);

Vue.http.options.root = "https://venue-api.lanets.ca";

Vue.http.interceptors.push((request, next) => {
  var token = JSON.parse(localStorage.getItem("token"));
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
              .then(result => {
                token = {
                  access: result.body.access,
                  refresh: token.refresh
                };
                localStorage.setItem("token", JSON.stringify(token));
              });
          }
        }
      );
      request.headers.set("Authorization", "Bearer " + token.access);
    }
  }
  next(response => {
    if (response.status === 401) {
      Vue.notify({
        group: "foo",
        title: "Erreur!",
        text: "Jeton expiré. Veuillez réessayer à nouveau",
        type: "error"
      });
    }
    /*
    if (response.status !== 200 && response.url.includes("api/token/refresh")) {
      localStorage.removeItem("token");
      Vue.notify({
        group: "foo",
        title: "Erreur!",
        text: "Erreur d'authentification. Vous avez été déconnecté"
      });
      Vue.router.push({
        name: "home"
      });
    }
    if (response.status === 400 && !removeAuthHeaders) {
      Vue.http
        .post("api/token/refresh/", { refresh: token.refresh })
        .then(result => {
          localStorage.setItem(
            "token",
            JSON.stringify({
              access: result.body.access,
              refresh: token.refresh
            })
          );
        })
        .catch(() => {
          localStorage.removeItem("token");
          Vue.notify({
            group: "foo",
            title: "Erreur!",
            text: "Erreur d'authentification. Vous avez été déconnecté"
          });
          Vue.router.push({
            name: "home"
          });
        });
    }
    */
  });
});

Vue.config.productionTip = false;

global.vue = new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
