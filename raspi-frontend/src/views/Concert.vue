<template>
  <div>
    <h1>Page des spectacles/Concerts</h1>
    <button v-if="!createEditConcert" class="btn btn-primary" @click="createConcert">Nouveau Concert</button>
    <NewConcert v-if="createEditConcert" :newConcert="newConcert" @cancelCreateEdit="cancelCreateEdit" />
    <div class="col-md-6 mx-auto">
      <ShowConcerts :concerts="concerts" />
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
      newConcert: {},
      createEditConcert: false,
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
      ],
      concerts: [
        {
          id: 10,
          name: "Ariana Grande Concert",
          date: new Date(2019, 6, 4, 8),
          description: "Ariana Grande de retour à Montréal bitches"
        },
        {
          id: 12,
          name: "BlackPink In Your Area",
          date: new Date(2029, 8, 14, 8),
          description: "Du kpop à Montréal"
        }
      ]
    };
  },
  methods: {
    mounted() {
      this.concerts[0].venue = this.venues[0];
      this.concerts[1].venue = this.venues[1];
    },
    createConcert() {
      this.createEditConcert = !this.createEditVenue;
      this.newConcert = {
        name: "",
        date: new Date(),
        description: "",
        venue: this.venues[0]
      }
    },
    cancelCreateEdit() {
      this.createEditConcert = !this.createEditConcert;
    },
    editConcert(concert) {
      this.newConcert = concert;
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