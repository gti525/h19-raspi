<template>
    <div id="newVenue">
        <h2>Créer un Concert</h2>
        <form id="venueForm" v-on:submit="submit(newConcert)">
            <div class="form-data-row">
                <input v-model="newConcert.name" type="text" name="name" placeholder="nom du Concert">
            </div>
            <div class="form-data-row">
                <textarea v-model="newConcert.description" type="text" name="description" placeholder="description du concert" />
            </div>
            <div class="form-data-row">
                <input v-model="newConcert.date" type="date">
            </div>
        </form>
    </div>
</template>

<script>
export default {
    name: "NewConcert",
    props: {
        newConcert: Object,
    },
    methods: {
        submit(form){
            console.log(form);
            this.$emit("cancelCreateEdit");
        }
    }
}
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