<template>
<div>
  <div id="newVenueOverlay"></div>
  <div id="newVenue" style="display: none">
    <h2>Créer une salle</h2>
    <form id="venueForm" v-on:submit="submit(newVenue)">
      <div class="form-data-row">
        <input v-model="newVenue.name" type="text" name="name" placeholder="nom">
      </div>
      <div class="form-data-row multiple-data">
        <input v-model="street" type="text" name="address" placeholder="adresse">
      </div>
      <div class="form-data-row">
        <input v-model="city" type="text" name="ville" placeholder="ville">
      </div>
      <div class="form-data-row">
        <input v-model="postalCode" type="text" name="postalCode" placeholder="code postal">
      </div>
      <div class="form-data-row">
        <label class="label">Capacité</label>
        <input v-model="newVenue.capacity" type="number" name="capacity">
      </div>
      <div class="control">
        <b-button variant="primary" @click="submit(newVenue)">Soumettre</b-button>
        <b-button variant="danger" @click="cancel()">Cancel</b-button>
      </div>
    </form>
  </div>
</div>
</template>

<script>
import $ from "jquery";
import { required, minLength, between } from "vuelidate/lib/validators";

export default {
  name: "NewVenue",
  props: {
    newVenue: Object,
    resource: Object
  },
  data() {
    return {
      street: this.newVenue.address.split(",")[0] || "",
      city: this.newVenue.address.split(",")[1] || "",
      postalCode: this.newVenue.address.split(",")[2] || "",
      errors: {}
    };
  },
  validation: {
    street: {
      required,
      minLength: minLength(4)
    },
    city: {
      required,
      minLength: minLength(2)
    },
    postalCode: {
      required,
      minLength: minLength(6)
    }
  },
  mounted: function() {
    window.initialVenue = Object.assign({}, this.newVenue);
    $('#newVenue').slideDown(400);
    document.getElementById('newVenueOverlay').classList.remove('hidden-overlay');
    document.getElementById('newVenueOverlay').classList.add('visible-overlay');
  },
  methods: {
    async submit(form) {
      form.address = this.street + ", " + this.city + ", " + this.postalCode;
      if (form.id) {
        this.resource.update({ id: form.id }, form).then(
          response => {
            if (response.status === 200) {
              this.$notify({
                group: "foo",
                title: "Réussi!",
                text: "Salle modifiée avec succès!",
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
        this.resource.save({}, form).then(
          response => {
            this.$notify({
              group: "foo",
              title: "Réussi!",
              text: "Salle créée avec succès",
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
    resetValues() {
      for(let prop in window.initialVenue) {
        this.newVenue[prop] = window.initialVenue[prop];
      }
    },
    cancel() {
      this.resetValues();
      let that = this;
      $('#newVenue').slideUp(400, function() {
        that.$emit("cancelCreateEdit");
      });
      document.getElementById('newVenueOverlay')
        .classList.replace('visible-overlay', 'hidden-overlay');
    }
  },
  watch: {}
};
</script>
<style scoped>
#newVenueOverlay {
  position: absolute;
  z-index: 19;
  height: 100%;
  width: 100%;
  background-color: rgba(0,0,0,0.75);
}

#newVenueOverlay.visible-overlay {
  animation: fade-in;
  animation-duration: 0.5s;
}

#newVenueOverlay.hidden-overlay {
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
