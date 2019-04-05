<template>
  <div style="width: 100%; height: 100%; position: relative">
    <h1 class="page-title">Spectacles</h1>
    <div id="tableContainer">
      <div>
        <!-- <div class="button-bg"></div>
        <div class="button-bar-bg"></div>-->
        <!-- <h2 class="instructions visible-instructions">Ajoutez un concert à votre calendrier</h2> -->
        <button
          id="newConcertBtn"
          v-if="!createEditConcert"
          class="btn btn-primary button"
          @click="createConcert"
        >Nouveau Concert</button>
        <NewConcert
          v-if="createEditConcert"
          :newConcert="newConcert"
          @cancelCreateEdit="cancelCreateEdit"
          @editConcert="editConcert"
          @remove="remove"
          :venues="venues"
          :resource="resource"
          :selected="selected"
        />
        <div class="col-md-12 mx-auto show-concert-container">
          <ShowConcerts
            :concerts="concerts"
            :venues="venues"
            @cancelCreateEdit="cancelCreateEdit"
            @editConcert="editConcert"
            @remove="remove"
            :resource="resource"
          />
        </div>
      </div>
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
      concerts: [],
      selected: ""
    };
  },
  mounted: function() {
    document.getElementById("app").classList.add("concerts");
  },
  beforeRouteLeave: function(from, to, next) {
    document.getElementById("app").classList.remove("concerts");
    next();
  },
  methods: {
    createConcert() {
      this.createEditConcert = !this.createEditVenue;
      this.newConcert = {
        name: "",
        date: this.$moment().format("YYYY-MM-DD HH:MM"),
        description: "",
        venue: "",
        ticket_price: "",
        sellers: []
      };
      this.selected = 0;
    },
    cancelCreateEdit(concert) {
      if (concert) {
        this.concerts.push(concert);
      }
      this.createEditConcert = !this.createEditConcert;
    },
    editConcert(concert) {
      this.newConcert = concert;
      this.selected = this.newConcert.venue;
    },
    async getConcerts() {
      this.resource.get().then(response => {
        this.concerts = response.body;
      });
    },
    async remove(concertArray) {
      if (confirm("Êtes-vous certain?"))
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
@import url("https://fonts.googleapis.com/css?family=Srisakdi");
@import url("https://fonts.googleapis.com/css?family=Sniglet");
@import url("https://fonts.googleapis.com/css?family=Raleway");

h1.page-title {
  margin: 0;
  position: absolute;
  left: 0;
  top: 0;
  width: auto;
  font-family: "Raleway", sans-serif;
  text-align: left;
  padding: 0.6rem 1rem;
  background-color: rgba(0, 0, 0, 0.8);
  box-shadow: 0 0 9px 5px black;
  letter-spacing: 1px;
  font-size: 3rem;
  z-index: 1;
  color: white;
  text-shadow: 2px 2px 5px black;
}

#tableContainer {
  display: table;
  position: relative;
  height: 100%;
  width: 100%;
}

#tableContainer > div {
  display: table-cell;
  vertical-align: middle;
  padding-bottom: 20%;
}

div.venue {
  width: 100%;
  height: calc(100% - 85px);
}

h2.instructions {
  font-family: "Sniglet", cursive;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
  margin-bottom: 2rem;
}

.button {
  font-family: "Sniglet", cursive;
  padding-left: 2rem;
  padding-right: 2rem;
  background-color: rgba(240, 240, 240, 1);
  border-color: rgba(0, 0, 0, 0.8);
  border-width: 2px;
  font-size: 1.5rem;
  color: rgba(0, 0, 0, 0.8);
  z-index: 3;
  position: relative;
}

.button:hover {
  background-color: rgba(240, 240, 240, 1);
  border-color: #42b983;
  color: #42b983;
}

div.show-concert-container {
  position: relative;
  min-height: 100vh;
  padding-top: 6rem;
  padding-left: 0;
}

#newConcertBtn {
  position: absolute;
  right: 3rem;
  top: 1.5rem;
  font-size: 1.2rem;
}
</style>
