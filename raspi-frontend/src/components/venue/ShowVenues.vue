<template>
  <div id="showVenue">
    <div v-for="venue in venues" class="card" :key="venue.id">
      <div class="card-body">
        <h2>{{venue.name}}</h2>
        <p>adresse: {{venue.address}}</p>
        <p>Capacité: {{venue.capacity}} personnes</p>
        <div v-if="venue.shows.length !== 0">
          <h4>Spectacles à venir:</h4>
          <div v-for="show in venue.shows" :key="show.id">
            <div v-if="!dateHasPassed(show.date)">
              <p>
                {{show.name}}
                <br>
                {{show.date | moment("YYYY-MM-DD HH:MM")}}
              </p>
            </div>
          </div>
        </div>
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
    },
    dateHasPassed(date) {
      let dateConverted = this.$moment(date);
      return this.$moment().isAfter(dateConverted);
    }
  },
  data() {
    return {
      today: new Date()
    };
  }
};
</script>

<style scoped>
.card {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 2rem;
}
</style>