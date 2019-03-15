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
        <b-button variant="link" @click="logout()" style="color:red">Déconnexion</b-button>
      </div>
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
  position: relative;
  overflow-x: hidden;
  overflow-y: auto;
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
  background: rgba(0,0,0,0.1);
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
