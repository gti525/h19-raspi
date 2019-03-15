<template>
  <div style="width: 100%; height: 100%; position: relative; display: table">
    <h1 class="page-title">Salles de spectacles</h1>
    <div class="venue">
      <button v-if="!createEditVenue" class="btn btn-primary button" @click="createVenue">Nouvelle salle</button>
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
  </div>
</template>

<script>
import NewVenue from "@/components/venue/NewVenue.vue";
import ShowVenue from "@/components/venue/ShowVenues.vue";
import $ from "jquery";

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
  mounted: function() {
    document.getElementById("app").classList.add("salles");
    document.querySelector('button.btn-primary').click();
  },
  beforeRouteLeave: function(from, to, next) {
    document.getElementById("app").classList.remove("salles");
    next();
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
    }
  },
  async created() {
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
  display: table-row;
}

h1.page-title {
  margin: 0;
  position: absolute;
  left: 0;
  top: 0;
  width: auto;
  font-family: 'Raleway', sans-serif;
  text-align: left;
  padding: 0.6rem 1rem;
  background-color: rgba(0,0,0,0.8);
  box-shadow: 0 0 9px 5px black;
  letter-spacing: 1px;
  font-size: 3rem;
  z-index: 1;
  color: white;
  text-shadow: 2px 2px 5px black;
}

.button {
  font-family: 'Sniglet', cursive;
  padding-left: 2rem;
  padding-right: 2rem;
  background-color: rgba(240, 240, 240, 1);
  border-color: rgba(0,0,0,0.8);
  border-width: 2px;
  font-size: 1.2rem;
  color: rgba(0,0,0,0.8);
  z-index: 3;
  position: relative;
}

.button:hover {
  opacity: 0.9;
  background-color: rgba(240, 240, 240, 1);
  border-color: rgba(0,0,0,0.8);
  color: black;
}

</style>
