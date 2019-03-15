<template>
  <div id="newVenue" style="display: none">
    <h2>Créer une salle</h2>
    <div v-if="errors">
      <div v-for="(value, key) in errors" :key="key">
        <span class="alert alert-danger">{{key}}: {{value}}</span>
      </div>
    </div>
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
</template>

<script>
import $ from "jquery";

export default {
  name: "NewVenue",
  props: {
    newVenue: Object,
    resource: Object
  },
  data() {
    return {
      street: "",
      city: "",
      postalCode: "",
      errors: {}
    };
  },
  mounted: function() {
    $('#newVenue').slideDown(400);
  },
  methods: {
    async submit(form) {
      form.address = this.street + ", " + this.city + ", " + this.postalCode;
      if (form.id) {
        this.resource.update({ id: form.id }, form).then(
          response => {},
          error => {
            this.errors = error.body;
          }
        );
        this.$emit("cancelCreateEdit");
      } else {
        this.resource.save({}, form).then(
          response => {
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
    $('#newVenue').slideUp(400, function() {
      that.$emit("cancelCreateEdit");
    });
    }
  }
};
</script>
<style scoped>
#newVenue {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 2rem;
  padding: 1rem 1.5rem;
  height: 450px;
  width: 495px;
  display: inline-block;
  position: relative;
  border: 3px solid black;
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
  background-color: #2ECC40;
  border-color: #AAAAAA;
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
