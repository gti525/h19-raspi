<template>
  <div id="app">
    <div id="nav">
      <div v-if="!isLoggedIn()">
        <router-link to="/">Home</router-link>
        <span>|</span>
        <router-link to="/signin">Connexion</router-link>
      </div>
      <div v-if="isLoggedIn()">
        <router-link to="/venues">Salles</router-link>
        <span>|</span>
        <router-link to="/concerts">Spectacles</router-link>
        <span>|</span>
        <router-link to="/stats">Stats</router-link>
        <span>|</span>
        <router-link to="/stats2">Stats2</router-link>
        <span>|</span>
        <b-button variant="link" @click="logout()" id="logoutBtn">Déconnexion</b-button>
      </div>
    </div>

    <router-view/>
    <footer>
      <!-- Copyright -->
      <div class="footer-copyright text-center py-3">
        © 2019 Copyright:
        <a href="https://www.facebook.com/eric.boivin.75">GTI525</a>
      </div>
      <!-- Copyright -->
    </footer>
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
  position: relative;
  overflow-x: hidden;
  overflow-y: auto;
}

footer {
  position: fixed;
  bottom: 0;
  width: 100vw;
  background-color: rgba(255, 255, 255, 1);
  z-index: 1000;
  color: #797676;
  font-weight: bold;
  box-shadow: 0px 0px 4px 4px rgba(0, 0, 0, 0.5);
}

#logoutBtn {
  padding: 0;
  margin: 0 1rem;
  display: inline;
  color: #ff4136;
  font-weight: bold;
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

#app.salles, #app.concerts {
  background: rgb(250,250,250);
}

#nav {
  padding: 30px;
  box-sizing: border-box;
  height: 85px;
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0px 0px 9px 9px rgba(0, 0, 0, 0.5);
  z-index: 2;
  position: relative;
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
