<template>
  <div id="showConcert">
    <div v-for="concert in concerts" class="concert-row" :key="concert.id">
      <div class="concert-cell">
        <div class="space-taker"></div>
      </div>
      <div class="concert-cell">
        <div class="left-aligned">
          <div class="concert-name">{{concert.name}}</div>
          <div class="concert-time">{{concert.date | moment("YYYY-MM-DD HH:MM")}}</div>
        </div>
      </div>
      <div class="concert-cell">
        <div class="concert-venues">{{listVenues(venues, concert)}}</div>
      </div>
      <div class="concert-cell">
        <div class="concert-description">{{concert.description.substring(0, Math.min(30, concert.description.length)) + (concert.description.length > 30 ?"..." :"")}}</div>
      </div>
      <div class="concert-cell">
        <div class="concert-action-btn">
          <span @click="edit(concert)">Modifier</span>&nbsp;|&nbsp;
          <span @click="remove(concert)">Effacer</span>&nbsp;|&nbsp;
          <span @click="publish(concert)">Publier</span>&nbsp;|&nbsp;
          <span @click="endSale(concert)">Fermer Vente</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ShowConcerts",
  props: {
    concerts: Array,
    venues: Array,
    resource: Object
  },
  methods: {
    edit(concert) {
      this.$emit("editConcert", concert);
      this.$emit("cancelCreateEdit");
    },
    remove(concert, index) {
      this.$emit("remove", { concert: concert, index: index });
    },
    publish(concert) {
      this.resource.publish({ id: concert.id }).then(response => {
        if (response.status === 200) {
          //TODO
        }
      });
    },
    listVenues(venues, concert) {
      let venueNames = venues
        .filter(v => v.id === concert.venue)
        .map(v => v.name)
        .join(', ');
      const MAX_STR_LENGTH = 30;
      return venueNames
        .substring(0, Math.min(MAX_STR_LENGTH, venueNames.length)) 
        + (venueNames.length > MAX_STR_LENGTH ?'...' :'');
    },
    endSale(concert) {
      this.resource.endSale({ id: concert.id }).then(response => {
        if (response.status === 200) {
          //TODO
        }
      });
    }
  }
};
</script>

<style scoped>
#showConcert {
  width: 100vw;
  margin-top: 1rem;
  display: table;
}

div.concert-row {
  width: 100vw;
  padding: 1rem;
  display: table-row;
  text-align: left;
}

div.concert-row:nth-child(2n+1) {
  background-color: rgba(0,0,0,0.1);
}

div.concert-row > .concert-cell {
  display: table-cell;
  vertical-align: middle;
  font-family: 'Sniglet';
}

div.concert-row > .concert-cell > .left-aligned {
  display: inline-block;
  text-align: left;
}

div.concert-row > .concert-cell .concert-name {
  padding-top: 0.5rem;
  font-weight: bold;
  font-size: 1.2rem;
}

div.concert-row > .concert-cell .concert-time {
  padding-bottom: 0.5rem;
}

div.concert-row > .concert-cell .concert-description {
  /* font-style: italic; */
}

div.concert-row > .concert-cell .concert-venues {
  text-decoration: underline;
}

div.concert-action-btn > span {
  cursor: pointer;
}

div.concert-action-btn > span:hover {
  text-decoration: underline;
  color: #2ECC40;
}

div.concert-row > .concert-cell > .space-taker {
  width: 2vw;
}

</style>
