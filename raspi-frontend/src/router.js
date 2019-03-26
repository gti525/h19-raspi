import Vue from "vue";
import Router from "vue-router";
import SignUp from "./views/SignUp.vue";
import Venue from "./views/Venue.vue";
import Concert from "./views/Concert.vue";
import Stats from "./views/Stats.vue";
import Home from "./views/Home.vue";
import Stats2 from "./views/Stats2.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
      props: true
    },
    {
      path: "/signin",
      name: "sign-up",
      component: SignUp,
      props: true
    },
    {
      path: "/venues",
      name: "venue",
      component: Venue,
      beforeEnter: (to, from, next) => {
        if (localStorage.getItem("token")) {
          next();
        } else {
          next({
            name: "sign-up",
            params: { error: "Veuillez vous connecter avant de poursuivre" }
          });
        }
      }
    },
    {
      path: "/concerts",
      name: "concerts",
      component: Concert,
      beforeEnter: (to, from, next) => {
        if (localStorage.getItem("token")) {
          next();
        } else {
          next({
            name: "sign-up",
            params: { error: "Veuillez vous connecter avant de poursuivre" }
          });
        }
      }
    },
    {
      path: "/stats",
      name: "stats",
      component: Stats,
      beforeEnter: (to, from, next) => {
        if (localStorage.getItem("token")) {
          next();
        } else {
          next({
            name: "sign-up",
            params: { error: "Veuillez vous connecter avant de poursuivre" }
          });
        }
      }
    },
    {
      path: "/stats2",
      name: "stats2",
      component: Stats2,
      beforeEnter: (to, from, next) => {
        if (localStorage.getItem("token")) {
          next();
        } else {
          next({
            name: "sign-up",
            params: { error: "Veuillez vous connecter avant de poursuivre" }
          });
        }
      }
    }
  ]
});
