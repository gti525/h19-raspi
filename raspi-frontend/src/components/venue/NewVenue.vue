<template>
  <div id="newVenue">
    <h2>Créer une salle</h2>
    <form id="venueForm" v-on:submit="submit(newVenue)">
      <div class="form-data-row">
        <input v-model="newVenue.name" type="text" name="name" placeholder="nom">
      </div>
      <div class="form-data-row">
        <input v-model="newVenue.address" type="text" name="address" placeholder="adresse">
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
export default {
  name: "NewVenue",
  props: {
    newVenue: Object,
    resource: Object
  },
  methods: {
    submit(form) {
      if (form.id) {
        this.resource.update({ id: form.id }, form).then(
          response => {
            console.log(response);
          },
          error => {
            console.log(error);
          }
        );
      } else {
        this.resource.save({}, form).then(
          response => {
            console.log(response);
          },
          error => {
            console.log(error);
          }
        );
      }
      this.$emit("cancelCreateEdit");
    },
    cancel() {
      this.$emit("cancelCreateEdit");
    }
  }
};
</script>
<style scoped>
#newVenue {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 2rem;
  padding: 1rem 1.5rem;
  height: 420px;
  width: 495px;
  display: inline-block;
  position: relative;
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
