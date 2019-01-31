<template>
  <div class="venue">
    <h1>Page des salles de spectacles</h1>
    <button v-if="!createEditVenue" class="btn btn-primary" @click="createVenue">Nouvelle salle</button>
    <NewVenue
      v-if="createEditVenue"
      :newVenue="newForm"
      :ogVenue="ogVenue"
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
      // for testing purposes
      venues: [
        {
          id: 36,
          name: "1st venue",
          address: "123 avenue",
          capacity: 420
        },
        {
          id: 37,
          name: "2nd super venue",
          address: "456 bld",
          capacity: 69
        },
        {
          id: 38,
          name: "3rd amazing place",
          address: "789 street",
          capacity: 1337
        }
      ]
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
      this.createEditVenue = !this.createEditVenue;
    },
    editVenue(venue) {
      this.newForm = venue;
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
