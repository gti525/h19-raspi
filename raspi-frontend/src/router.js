import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import SignUp from "./views/SignUp.vue";
import Venue from "./views/Venue.vue";
import Concert from "./views/Concert.vue";
import Stats from "./views/Stats.vue";
import SignUp from "./views/SignUp.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/home",
      name: "home",
      component: Home
    },
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
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue")
    }
  ]
});
