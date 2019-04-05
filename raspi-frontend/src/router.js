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
      beforeEnter: (to, from, next) => {
        if (localStorage.getItem("token")) {
          next({
            name: "venue"
          });
        } else {
          next();
        }
      }
    },
    {
      path: "/signin",
      name: "sign-up",
      component: SignUp,
      beforeEnter: (to, from, next) => {
        if (localStorage.getItem("token")) {
          next(
            { name: "venue" },
            Vue.notify({
              group: "foo",
              title: "Erreur",
              text: "Vous êtes déjà connecté",
              type: "error"
            })
          );
        } else {
          next();
        }
      }
    },
    {
      path: "/venues",
      name: "venue",
      component: Venue,
      beforeEnter: (to, from, next) => {
        if (localStorage.getItem("token")) {
          next();
        } else {
          next(
            { name: "sign-up" },
            Vue.notify({
              group: "foo",
              title: "Erreur",
              text: "Veuillez-vous connecter",
              type: "error"
            })
          );
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
          next(
            { name: "sign-up" },
            Vue.notify({
              group: "foo",
              title: "Erreur",
              text: "Veuillez-vous connecter",
              type: "error"
            })
          );
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
          next(
            { name: "sign-up" },
            Vue.notify({
              group: "foo",
              title: "Erreur",
              text: "Veuillez-vous connecter",
              type: "error"
            })
          );
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
          next(
            { name: "sign-up" },
            Vue.notify({
              group: "foo",
              title: "Erreur",
              text: "Veuillez-vous connecter",
              type: "error"
            })
          );
        }
      }
    }
  ]
});
