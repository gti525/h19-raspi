<template>
  <div class="venue">
    <h1>Page des salles de spectacles</h1>
    <button v-if="!createEditVenue" class="btn btn-primary" @click="createVenue">Nouvelle salle</button>
    <NewVenue v-if="createEditVenue" :newVenue="newForm" @cancelCreateEdit="cancelCreateEdit"/>
  </div>
</template>

<script>
import NewVenue from "@/components/venue/NewVenue.vue";

export default {
  name: "venue",
  components: {
    NewVenue
  },
  data: () => {
    return {
      newForm: {},
      createEditVenue: false
    };
  },
  methods: {
    createVenue() {
      this.createEditVenue = !this.createEditVenue;
      this.newForm = {
        name: "",
        address: "",
        capacity: 0
      };
    },
    cancelCreateEdit() {
      this.createEditVenue = false;
    }
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Acme");

div.venue {
  width: 100%;
  height: calc(100% - 85px);
}

h1 {
  color: white;
}
</style>
