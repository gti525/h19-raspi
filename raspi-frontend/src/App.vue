<template>
  <div id="app">
    <div id="nav">
      <router-link to="/venues" v-if="isLoggedIn()">Salles</router-link>
      <span v-if="isLoggedIn()">|</span>
      <router-link to="/concerts" v-if="isLoggedIn()">Spectacles</router-link>
      <span v-if="isLoggedIn()">|</span>
      <router-link to="/stats" v-if="isLoggedIn()">Stats</router-link>
      <span v-if="isLoggedIn()">|</span>
      <b-button variant="link" @click="logout()" v-if="isLoggedIn()" style="color:red">Déconnexion</b-button>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
  methods: {
    isLoggedIn() {
      return localStorage.getItem("token") !== null;
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push({ path: "/" });
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-image: url("~@/assets/login-bg.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  height: 100vh;
  width: 100vw;
}

#app.sign-up {
  background-repeat: no-repeat;
  background-size: cover;
  height: 100vh;
  width: 100vw;
}

#app.stats {
  background-image: url("~@/assets/stats-bg.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  height: 100vh;
  width: 100vw;
}

#nav {
  padding: 30px;
  box-sizing: border-box;
  height: 85px;
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0px 0px 9px 9px rgba(0, 0, 0, 0.5);
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 0 1rem;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
