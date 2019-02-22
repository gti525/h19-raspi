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
      component: Venue
    },
    {
      path: "/concerts",
      name: "concerts",
      component: Concert
    },
    {
      path: "/stats",
      name: "stats",
      component: Stats
    }
  ]
});
