import Vue from "vue";
import Router from "vue-router";
import SignUp from "./views/SignUp.vue";
import Venue from "./views/Venue.vue";
import Concert from "./views/Concert.vue";
import Stats from "./views/Stats.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "sign-up",
      component: SignUp
    },
    {
      path: "/venues",
      name: "venue",
      component: Venue,
      beforeEnter: (to, from, next) => {
        if (localStorage.getItem("token")) {
          next();
        } else {
          next({ path: "/" });
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
          next({ path: "/" });
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
          next({ path: "/" });
        }
      }
    }
  ]
});
