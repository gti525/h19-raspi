<template>
  <div id="newVenue">
    <h2>Créer un Concert</h2>
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
      <div class="form-data-row">
        <input class="date-selector" type="text" placeholder="Date du concert">
      </div>
      <div class="form-data-row" id="roomSelectionContainer">
        <label id="roomLabel" class="label">Salle</label>
        <select v-model="newConcert.venue" required>
          <option v-for="venue in venues" :key="venue.id" :value="venue.id">{{venue.name}}</option>
        </select>
      </div>
      <div class="form-data-row">
        <label class="label">Prix du Billet</label>
        <input v-model="newConcert.ticket_price" type="number" name="price">
      </div>
      <div class="control">
        <b-button variant="primary" @click="submit()">Soumettre</b-button>
        <b-button variant="danger" @click="cancel()">Cancel</b-button>
      </div>
    </form>
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
    venues: Array
  },
  data: () => {
    return {
      errors: {}
    };
  },
  validations: {
    newConcert: {
      name: { required, min: minLength(4) },
      description: { required },
      venue: { required },
      ticket_price: { required },
      date: { required }
    }
  },
  mounted: function() {
    prepareDatePicker();
    window.newConcert = this.newConcert;
    document
      .querySelector("h2.instructions")
      .classList.replace("visible-instructions", "hidden-instructions");
    setTimeout(function() {
      // allowing 100 ms delay for h2.instructions to start disappearing
      $("#newVenue").slideDown(800);
    }, 100);
  },
  beforeRouteLeave(from, to, next) {
    next();
  },
  methods: {
    async submit() {
      newConcert.date = this.$moment(newConcert.date).format(
        "YYYY-MM-DDTHH:MM"
      );
      if (newConcert.id) {
        this.resource.update({ id: newConcert.id }, newConcert).then(
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
        this.resource.save({}, newConcert).then(
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
      $("#newVenue").slideUp(800, function() {
        document
          .querySelector("h2.instructions")
          .classList.replace("hidden-instructions", "visible-instructions");
        that.$emit("cancelCreateEdit");
      });
    }
  }
};

function prepareDatePicker() {
  let that = this;

  const picker = $("input.date-selector[type=text]").datetimepicker({
    format: "Y-m-d H:i",
    inline: false,
    onChangeDateTime: function(dp, $input) {
      window.newConcert.date = new Date($input.val()).toString();
    }
  });
}
</script>

<style scoped>
#newVenue {
  background-color: rgba(240, 240, 240, 1);
  border-radius: 2rem;
  padding: 1rem 1.5rem;
  height: 375px;
  width: 495px;
  display: inline-block;
  position: absolute;
  top: calc(40% - 187.5px);
  left: calc(50% - 247.5px);
  z-index: 10;
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

div.form-data-row > input {
  display: inline-block;
  margin: 0 0.5rem;
  width: calc(100% - 1rem);
  padding-left: 8px;
  border-radius: 5px;
  height: 43.5px;
  border: 1px solid darkgray;
}

div.form-data-row > input.invalid-form-data {
  border: 1px solid #ff4136 !important;
}

div.form-data-row > input:focus {
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

#roomLabel {
  margin-right: 1rem;
}

#roomLabel + select {
  min-width: 6rem;
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

#roomSelectionContainer {
  margin: 0.3rem 0px 0.5rem 0;
  text-align: left;
  padding-left: 0.8rem;
}

div.control {
  text-align: left;
  padding-left: 0.8rem;
}
</style>

