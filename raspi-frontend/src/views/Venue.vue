<template>
  <div class="venue">
    <h1>Salles de spectacles</h1>
    <button v-if="!createEditVenue" class="btn btn-primary" @click="createVenue">Nouvelle salle</button>
    <NewVenue
      v-if="createEditVenue"
      :newVenue="newForm"
      :resource="resource"
      @cancelCreateEdit="cancelCreateEdit"
    />
    <div class="col-md-6 mx-auto">
      <ShowVenue :venues="venues" @cancelCreateEdit="cancelCreateEdit" @editVenue="editVenue"/>
    </div>
  </div>
</template>

<script>
import NewVenue from "@/components/venue/NewVenue.vue";
import ShowVenue from "@/components/venue/ShowVenues.vue";

export default {
  name: "venue",
  components: {
    NewVenue,
    ShowVenue
  },
  data: () => {
    return {
      newForm: {},
      createEditVenue: false,
      venues: [],
      resource: {}
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
    cancelCreateEdit(venue) {
      if (venue) {
        this.venues.push(venue);
      }
      this.createEditVenue = !this.createEditVenue;
    },
    editVenue(venue) {
      this.newForm = venue;
    },
    async refreshToken() {
      var token = JSON.parse(localStorage.getItem("token"));
      await this.$http
        .post("api/token/refresh/", { refresh: token.refresh })
        .then(
          res => {
            token.access = res.body.access;
            localStorage.setItem("token", JSON.stringify(token));
          },
          error => {
            console.log(error);
          }
        );
    }
  },
  async created() {
    await this.refreshToken();
    this.resource = this.$resource("venues/{id}");
    this.resource.get().then(response => {
      this.venues = response.body;
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
