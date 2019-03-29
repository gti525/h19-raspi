<template>
<div>
  <div id="newConcertOverlay"></div>
  <div id="newVenue" style="display: none">
    <h2>Créer un Concert</h2>
    <div v-if="errors">
      <div v-for="(value, key) in errors" :key="key">
        <span class="alert alert-danger">{{value}}</span>
      </div>
    </div>
    <form id="venueForm" v-on:submit="submit(newConcert)">
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
      <div class="form-data-row" style="padding-top: 0">
        <input class="date-selector" type="text" placeholder="Date du concert">
      </div>
      <div class="form-data-row" id="roomSelectionContainer">
        <select @change=onVenueChange v-model="selected" required>
          <option disabled value="">Salle de Spectacle</option>
          <option v-for="venue in venues" :key="venue.id" :value="venue.id">{{venue.name}}</option>
        </select>
      </div>
      <div class="form-data-row">
        <input placeholder="Prix du Billet" v-model="newConcert.ticket_price" type="number" name="price">
      </div>
      <div class="control">
        <b-button variant="primary" @click="submit(newConcert)">Soumettre</b-button>
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

export default {
  name: "NewConcert",
  props: {
    newConcert: Object,
    resource: Object,
    venues: Array
  },
  data: () => {
    return {
      selected: '',
      errors: {}
    };
  },
  mounted: function() {
    prepareDatePicker();
    window.newConcert = this.newConcert;
    $("#newVenue").slideDown(400);
    document.getElementById('newConcertOverlay').classList.remove('hidden-overlay');
    document.getElementById('newConcertOverlay').classList.add('visible-overlay');
  },
  beforeRouteLeave(from, to, next) {
    next();
  },
  methods: {
    async submit(form) {
      form.date = this.$moment(form.date).format("YYYY-MM-DDTHH:MM");
      if (form.id) {
        this.resource.update({ id: form.id }, form).then(
          response => {
            console.debug(response);
          },
          error => {
            this.errors = error.body;
          }
        );
        this.$emit("cancelCreateEdit");
      } else {
        this.resource.save({}, form).then(
          response => {
            if (response.status === 201)
              this.$emit("cancelCreateEdit", response.body);
          },
          error => {
            this.errors = error.body;
          }
        );
      }
    },
    cancel() {
      let that = this;
      $("#newVenue").slideUp(400, function() {
        that.$emit("cancelCreateEdit");
      });
      document.getElementById('newConcertOverlay')
        .classList.replace('visible-overlay', 'hidden-overlay');
    },
    onVenueChange() {
      document.querySelector('#roomSelectionContainer > select').classList.add('valid-selection');
    }
  }
};

function prepareDatePicker() {
  let that = this;

  const picker = $("input.date-selector[type=text]").datetimepicker({
    format: "Y-m-d H:i",
    inline: false,
    onChangeDateTime: function(dp, $input) {
      console.log(
        "updating new concert date to: ",
        new Date($input.val()).toString()
      );
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
  background-color: rgba(0,0,0,0.75);
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
  height: 450px;
  width: 495px;
  display: inline-block;
  border: 3px solid black;
  position: absolute;
  z-index: 20;
  left: calc(50% - 247px);
  top: 5rem;
}

#newVenue > h2,
#newVenue > h5 {
  text-align: left;
  padding-left: 0.5rem;
}

#newVenue > h2 {
  margin-top: 0.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
}

#newVenue > h5 {
  margin-bottom: 1rem;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.6);
}

div.form-data-row {
  display: block;
  width: 100%;
  padding: 0.5rem 0 0.3rem 0;
  position: relative;
}

div.form-data-row > input, #roomSelectionContainer > select {
  display: inline-block;
  margin: 0 0.5rem;
  width: calc(100% - 1rem);
  padding-left: 8px;
  border-radius: 5px;
  height: 43.5px;
  border: 1px solid darkgray;
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

div.form-data-row > input:focus, #roomSelectionContainer > select:focus {
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
  padding-top: 18px;
}
</style>

