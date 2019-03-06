<template>
  <div>
    <h1>Spectacles</h1>
    <button v-if="!createEditConcert" class="btn btn-primary" @click="createConcert">Nouveau Concert</button>
    <NewConcert
      v-if="createEditConcert"
      :newConcert="newConcert"
      @cancelCreateEdit="cancelCreateEdit"
      :resource="resource"
      :venues="venues"
    />
    <div class="col-md-6 mx-auto">
      <ShowConcerts
        :concerts="concerts"
        :venues="venues"
        @cancelCreateEdit="cancelCreateEdit"
        @editConcert="editConcert"
        @remove="remove"
      />
    </div>
  </div>
</template>

<script>
import ShowConcerts from "@/components/concert/ShowConcerts.vue";
import NewConcert from "@/components/concert/NewConcert.vue";

export default {
  name: "concert",
  components: {
    NewConcert,
    ShowConcerts
  },
  data: () => {
    return {
      resource: {},
      newConcert: {},
      createEditConcert: false,
      venues: [],
      concerts: []
    };
  },
  methods: {
    createConcert() {
      this.createEditConcert = !this.createEditVenue;
      this.newConcert = {
        name: "",
        date: new Date(),
        description: "",
        venue: this.venues[0]
      };
    },
    cancelCreateEdit(concert) {
      if (concert) {
        this.concerts.push(concert);
      }
      this.createEditConcert = !this.createEditConcert;
    },
    editConcert(concert) {
      this.newConcert = concert;
    },
    async remove(concertArray) {
      await this.refreshToken();
      this.resource.remove({ id: concertArray.concert.id }).then(response => {
        if (response.status === "204") {
          this.$delete(this.concerts, concertArray.index);
        }
      });
    }
  },
  async created() {
    this.resource = this.$resource("shows/{id}");
    this.$http.get("venues/").then(response => {
      this.venues = response.body;
    });
    this.resource.get().then(response => {
      this.concerts = response.body;
    });
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
