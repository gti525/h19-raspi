<template>
  <div>
    <div id="newConcertOverlay"></div>
    <div id="newVenue" style="display: none">
      <h2>Créer un Concert</h2>
      <form id="venueForm" v-on:submit.prevent="submit()">
        <div class="form-data-row">
          <input
            v-model="newConcert.name"
            type="text"
            name="name"
            autocomplete="off"
            placeholder="Nom du concert"
          >
        </div>
        <div class="form-data-row">
          <textarea
            v-model="newConcert.description"
            type="text"
            name="description"
            placeholder="Description du concert"
          ></textarea>
        </div>
        <div class="form-data-row">
          <input
            class="date-selector"
            type="text"
            placeholder="Date du concert"
            v-bind:value="getConcertDate(newConcert)"
          >
        </div>
        <div class="form-data-row" id="roomSelectionContainer">
          <select @change="onVenueChange" v-model="selected" required>
            <option disabled hidden value>Salle de Spectacle</option>
            <option v-for="venue in venues" :key="venue.id" :value="venue.id">{{venue.name}}</option>
          </select>
        </div>
        <div class="form-data-row">
          <input
            placeholder="Prix du Billet"
            v-model="newConcert.ticket_price"
            type="number"
            name="price"
          >
        </div>
        <div class="form-data-row" id="roomSelectionContainer">
          <div id="equipeCheckContainer" class="form-group">
            <label for="equipe1">Vente 1</label>
            <input type="checkbox" id="equipe1" value="1" v-model="newConcert.sellers">
            <label for="equipe2">Vente 2</label>
            <input type="checkbox" id="equipe2" value="2" v-model="newConcert.sellers">
          </div>
        </div>
        <!-- <span>{{newConcert.date | moment("YYYY-MM-DDTHH:MM")}}</span> -->
        <div class="control">
          <b-button variant="primary" @click="submit()">Soumettre</b-button>
          <b-button variant="danger" @click="cancel()">Cancel</b-button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
import datetimepicker from "jquery-datetimepicker";
// import './../../../node_modules/js-datepicker/dist/datepicker.min.css';
import "./../../../node_modules/jquery-datetimepicker/jquery.datetimepicker.css";
import { required, minLength } from "vuelidate/lib/validators";

export default {
  name: "NewConcert",
  props: {
    newConcert: Object,
    resource: Object,
    venues: Array,
    selected: Number
  },
  data: () => {
    return {};
  },
  validations: {
    newConcert: {
      name: { required, min: minLength(4) },
      description: { required },
      venue: { required },
      ticket_price: { required },
      date: { required }
    },
    name: { required }
  },
  mounted: function() {
    prepareDatePicker();
    window.newConcert = this.newConcert;
    $("#newVenue").slideDown(400);
    document
      .getElementById("newConcertOverlay")
      .classList.remove("hidden-overlay");
    document
      .getElementById("newConcertOverlay")
      .classList.add("visible-overlay");
  },
  beforeRouteLeave(from, to, next) {
    next();
  },
  methods: {
    getConcertDate(concert) {
      return concert.date || moment("YYYY-MM-DDTHH:MM");
    },
    async submit() {
      this.newConcert.date = this.$moment(this.newConcert.date).format(
        "YYYY-MM-DDTHH:MM"
      );
      this.newConcert.venue = this.selected;
      if (this.newConcert.id) {
        this.resource.update({ id: this.newConcert.id }, this.newConcert).then(
          response => {
            if (response.status === 200) {
              this.$notify({
                group: "foo",
                title: "Réussi!",
                text: "Spectacle modifié avec succès!",
                type: "success"
              });
            }
          },
          error => {
            for (const [key, value] of Object.entries(error.body)) {
              this.$notify({
                group: "foo",
                title: "Erreur dans " + key,
                text: value[0],
                type: "warn"
              });
            }
          }
        );
        this.$emit("cancelCreateEdit");
      } else {
        this.resource.save({}, this.newConcert).then(
          response => {
            if (response.status === 201)
              this.$notify({
                group: "foo",
                title: "Réussi!",
                text: "Spectacle créé avec succès",
                type: "success"
              });
            this.$emit("cancelCreateEdit", response.body);
          },
          error => {
            console.log(error);
            for (const [key, value] of Object.entries(error.body)) {
              this.$notify({
                group: "foo",
                title: "Erreur dans " + key,
                text: value[0],
                type: "warn"
              });
            }
          }
        );
      }
    },
    cancel() {
      let that = this;
      $("#newVenue").slideUp(400, function() {
        that.$emit("cancelCreateEdit");
      });
      document
        .getElementById("newConcertOverlay")
        .classList.replace("visible-overlay", "hidden-overlay");
    },
    onVenueChange() {
      document
        .querySelector("#roomSelectionContainer > select")
        .classList.add("valid-selection");
    }
  }
};

function prepareDatePicker() {
  let that = this;

  const picker = $("input.date-selector[type=text]").datetimepicker({
    format: "YYYY-MM-DDTHH:MM",
    inline: false,
    onChangeDateTime: function(dp, $input) {
      window.newConcert.date = new Date($input.val()).toString();
    }
  });
}
</script>

<style scoped>
#newConcertOverlay {
  position: absolute;
  z-index: 19;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.75);
}

#newConcertOverlay.visible-overlay {
  animation: fade-in;
  animation-duration: 0.5s;
}

#newConcertOverlay.hidden-overlay {
  animation: fade-out;
  animation-duration: 0.5s;
}

@keyframes fade-in {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes fade-out {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

#newVenue {
  background-color: rgba(250, 250, 250, 1);
  border-radius: 2rem;
  padding: 1rem 1.5rem;
  height: 475px;
  width: 495px;
  display: inline-block;
  border: 3px solid black;
  position: absolute;
  z-index: 20;
  left: calc(50% - 247px);
  top: 5rem;
}

#newConcert > h2,
#newConcert > h5 {
  text-align: left;
  padding-left: 0.5rem;
}

#newConcert > h2 {
  margin-top: 0.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
}

#newConcert > h5 {
  margin-bottom: 1rem;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.6);
}

button.btn {
  margin-top: 0.5rem;
}

button.btn.btn-primary {
  margin-right: 1rem;
  background-color: #2ecc40;
  border-color: #aaaaaa;
}

button.btn.btn-primary + button {
  background-color: rgb(108, 117, 125);
  border-color: darkgray;
}

div.form-data-row {
  display: block;
  width: 100%;
  padding: 0.5rem 0 0.3rem 0;
  position: relative;
}

div.form-data-row > input,
#roomSelectionContainer > select {
  display: inline-block;
  margin: 0 0.5rem;
  width: calc(100% - 1rem);
  padding-left: 8px;
  border-radius: 8px;
  height: 43.5px;
  border: 1px solid darkgray;
}

#roomSelectionContainer > select {
  background-color: white;
}

#roomSelectionContainer > select:not(.valid-selection) {
  color: gray;
}

#roomSelectionContainer > select > option:not(:first-child) {
  color: black;
}

div.form-data-row > input.invalid-form-data {
  border: 1px solid #ff4136 !important;
}

div.form-data-row > input:focus,
#roomSelectionContainer > select:focus {
  outline: none; /* so no rectangle around rounded edges */
  border: 1px solid #0074d9;
}

textarea {
  width: calc(100% - 1rem);
  border-radius: 5px;
  padding-left: 0.5rem;
  padding-top: 0.3rem;
  resize: none;
}

textarea:focus {
  outline: none;
  border-color: rgb(77, 144, 254);
}

button.btn.btn-primary {
  margin-right: 1rem;
  background-color: #2ecc40;
  border-color: #aaaaaa;
}

button.btn.btn-primary + button {
  background-color: rgb(108, 117, 125);
  border-color: darkgray;
}

div.control {
  text-align: left;
  padding-left: 0.8rem;
}

#equipeCheckContainer {
  margin-bottom: 0;
}

#equipeCheckContainer > * {
  cursor: pointer;
}

#equipeCheckContainer label {
  margin: 0.2rem 0.5rem;
}

#equipeCheckContainer input:first-of-type {
  margin-right: 0.5rem;
}
</style>

