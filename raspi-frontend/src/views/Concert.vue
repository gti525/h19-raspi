<template>
  <div style="width: 100%; height: 100%; position: relative">
    <img id="imgSalle" src="~@/assets/login-bg.jpg"/>
    <img id="imgGuit" src="~@/assets/guit-bg.jpg"/>
    <div id="imgSalleOverlay"></div>
    <h1 class="page-title">Spectacles</h1>
    <div id="tableContainer">
      <div>
        <div class="button-bg"></div>
        <div class="button-bar-bg"></div>
        <button v-if="!createEditConcert" class="btn btn-primary button" @click="createConcert">Nouveau Concert</button>
        <NewConcert
          v-if="createEditConcert"
          :newConcert="newConcert"
          @cancelCreateEdit="cancelCreateEdit"
          :resource="resource"
          :venues="venues"
        />
        <div class="col-md-6 mx-auto button">
          <ShowConcerts
            :concerts="concerts"
            :venues="venues"
            @cancelCreateEdit="cancelCreateEdit"
            @editConcert="editConcert"
            @remove="remove"
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
      concerts: []
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
@import url('https://fonts.googleapis.com/css?family=Srisakdi');
@import url('https://fonts.googleapis.com/css?family=Sniglet');
@import url('https://fonts.googleapis.com/css?family=Raleway');

#imgGuit {
  width: 100vw;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
  -webkit-clip-path: polygon(-20% 50%, 100% -40%, 100% 40%, 10% 120%);
  clip-path: polygon(0% 0%, 100% 0%, 100% 50%, 0% 50%);
}

img#imgSalle {
  width: 100vw;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
  -webkit-clip-path: polygon(-20% 50%, 100% -40%, 100% 40%, 10% 120%);
  clip-path: polygon(0% 50%, 100% 50%, 100% 100%, 0% 100%);
}

#imgSalleOverlay {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 0.5;
  background-color: rgba(0,0,0,0.6);
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

#tableContainer {
  display: table;
  position: relative;
  height: 100%;
  width: 100%;
}

#tableContainer > div {
  display: table-cell;
  vertical-align: middle;
}

div.button-bg {
  width: 10rem;
  height: 10rem;
  border-radius: 5rem;
  background-color: rgba(0,0,0,0.8);
  box-shadow: 0px 0px 5px 1px rgba(250,250,250,1);
  position: absolute;
  top: calc(50% - 5rem);
  left: calc(50% - 5rem);
  z-index: 2;
}

div.button-bar-bg {
  width: 100%;
  height: 1.2rem;
  background-color: rgba(0,0,0,0.8);
  box-shadow: 0px 0px 5px 1px rgba(250,250,250,1);
  position: absolute;
  top: calc(50% - 0.6rem);
  left: 0;
  z-index: 2;
}

div.venue {
  width: 100%;
  height: calc(100% - 85px);
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
