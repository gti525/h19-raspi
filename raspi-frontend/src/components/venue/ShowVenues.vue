<template>
  <div id="showVenue">
    <div v-for="venue in venues" class="card" :key="venue.id">
      <div class="card-body">
        <p>{{venue.name}}</p>
        <p>{{venue.address}}</p>
        <p>Capacité: {{venue.capacity}} personnes</p>
        <b-button variant="primary" @click="edit(venue)">Modifier</b-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ShowVenues",
  props: {
    venues: Array
  },
  methods: {
    edit(venue) {
      this.$emit("editVenue", venue);
      this.$emit("cancelCreateEdit");
    }
  }
};
</script>

<style scoped>
.card {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 2rem;
}
</style>