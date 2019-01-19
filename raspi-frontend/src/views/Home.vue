<template>
  <div class="home">
    <div class="jumbotron">
      <img alt="Vue logo" src="../assets/logo.png">
      <HelloWorld msg="Gestion de Salles"/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "home",
  components: {
    HelloWorld
  }
};
</script>
