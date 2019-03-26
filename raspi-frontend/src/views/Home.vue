<template>
  <div id="home">
    <span v-if="error" class="alert alert-danger">{{error}}</span>
    <div id="welcomeMsgContainer">
      <div>
        <h1>BIENVENUE SUR LE SITE DE
          <br>GESTION DE SALLES ET DE SPECTACLES
        </h1>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "home",
  props: {
    error: String
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Acme");

#welcomeMsgContainer {
  display: table;
  position: relative;
  width: 100vw;
  height: 100%;
}

#welcomeMsgContainer > div {
  display: table-cell;
  vertical-align: middle;
  height: 30rem;
}

#welcomeMsgContainer h1 {
  color: #fafafa;
  background-color: rgba(0,0,0,0.55);
  padding: 3rem 0;
  font-family: "Acme", sans-serif;
  text-shadow: 2px 2px 5px black;
}

div.side-panel {
  display: table-cell;
  vertical-align: middle;
  width: 50%;
  background-color: rgba(0, 0, 0, 0.3);
}

div.side-panel > div {
  display: block;
  width: 100%;
  padding: 0 2rem;
}

div.side-panel.left-panel h1 {
  font-size: 3rem !important;
  margin-bottom: 0;
  margin-top: -10px;
}

div.side-panel.left-panel {
  color: #fafafa;
  font-family: "Acme", sans-serif;
  text-shadow: 2px 2px 5px black;
  background-image: url("~@/assets/logo.png");
  background-position: center;
  background-repeat: no-repeat;
  background-size: 300px 260px;
}

div.sign-up {
  display: table;
  position: relative;
  height: 100%;
  width: 100%;
}

#home {
  width: 100%;
  height: calc(100% - 85px);
}
</style>
