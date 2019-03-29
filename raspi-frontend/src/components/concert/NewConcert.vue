<template>
  <div id="newConcert">
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
    $("#newConcert").slideDown(800);
  },
  beforeRouteLeave(from, to, next) {
    next();
  },
  methods: {
    async submit() {
      this.newConcert.date = this.$moment(newConcert.date).format(
        "YYYY-MM-DDTHH:MM"
      );
      if (this.newConcert.id) {
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
      $("#newConcert").slideUp(800, function() {
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
#newConcert {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 2rem;
  padding: 1rem 1.5rem;
  height: 450px;
  width: 495px;
  display: inline-block;
  position: relative;
  border: 3px solid black;
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
div.form-data-row > input {
  display: inline-block;
  margin: 0 0.5rem;
  width: calc(100% - 1rem);
  padding-left: 8px;
  border-radius: 8px;
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
</style>

