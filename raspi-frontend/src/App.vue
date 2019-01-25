<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/sign-up">Sign Up</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#app.sign-up {
  background-image: url("~@/assets/login-bg.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  height: 100vh;
  width: 100vw;
}

#nav {
  padding: 30px;
  box-sizing: border-box;
  height: 85px;
  background-color: rgba(255,255,255,0.8);
  box-shadow: 0px 0px 9px 9px rgba(0,0,0,0.5);
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
