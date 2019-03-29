<template>
  <div id="showConcert">
    <div v-for="(concert, index) in concerts" class="card" :key="concert.id">
      <div class="card-body">
        <p>{{concert.name}}</p>
        <p>{{concert.date | moment("YYYY-MM-DD HH:MM")}}</p>
        <p>{{concert.description}}</p>
        <div v-for="venue in venues" :key="venue.id">
          <p v-if="venue.id === concert.venue">Salle: {{venue.name}}</p>
        </div>
        <p>Prix: {{concert.ticket_price}}$</p>
        <b-button variant="primary" @click="edit(concert)">Modifier</b-button>
        <b-button variant="danger" @click="remove(concert, index)">Effacer</b-button>
        <b-button variant="success" @click="publish(concert)">Publier</b-button>
        <b-button variant="info" @click="endSale(concert)">Fermer Vente</b-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ShowConcerts",
  props: {
    concerts: Array,
    venues: Array,
    resource: Object
  },
  methods: {
    edit(concert) {
      this.$emit("editConcert", concert);
      this.$emit("cancelCreateEdit");
    },
    remove(concert, index) {
      this.$emit("remove", { concert: concert, index: index });
    },
    publish(concert) {
      this.resource.publish({ id: concert.id }).then(response => {
        if (response.status === 200) {
          //TODO
        }
      });
    },
    endSale(concert) {
      this.resource.endSale({ id: concert.id }).then(response => {
        if (response.status === 200) {
          //TODO
        }
      });
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
