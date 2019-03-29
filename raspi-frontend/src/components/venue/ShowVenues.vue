<template>
  <div id="showVenue">
    <div v-for="venue in venues" class="venue-row" :key="venue.id">
      <div class="venue-cell">
        <div class="space-taker"></div>
      </div>
      <div class="venue-cell">
        <div class="left-aligned">
          <div class="venue-name">{{venue.name}}</div>
          <div class="venue-address">{{venue.address}}</div>
        </div>
      </div>
      <div class="venue-cell">
        <div class="venue-capacity">Capacité: {{venue.capacity}} personnes</div>
      </div>
      <div class="venue-cell">
        <div class="venue-show">Spectacles:
          <span class="show-trigger upcoming-show">{{countUpcomingShows(venue)}} à venir</span>,
          <span class="show-trigger passed-show">{{venue.shows.length - countUpcomingShows(venue)}} passés</span>
        </div>
      </div>
      <div class="venue-cell">
        <div class="venue-edit-btn" @click="edit(venue)">&#x1F589;&nbsp;<span>[Modifier]</span></div>
      </div>
      <!-- <div v-if="venue.shows.length !== 0">
        <h4>Spectacles:</h4>
        <div v-for="show in ordered(venue.shows)" :key="show.id">
          <div>
            <p>
              {{show.name}}&nbsp;
              <span class="passed-event" v-if="hasDatePassed(show.date)">passé</span>
              <span class="upcoming-event" v-if="!hasDatePassed(show.date)">à venir</span>
              <br>
              {{show.date | moment("YYYY-MM-DD HH:MM")}}
            </p>
          </div>
        </div>
      </div>
      <b-button variant="primary" @click="edit(venue)">Modifier</b-button> -->
    </div>
  </div>
</template>

<script>
export default {
  name: "ShowVenues",
  props: {
    venues: Array
  },
  methods: {
    edit(venue) {
      this.$emit("editVenue", venue);
      this.$emit("cancelCreateEdit");
    },
    hasDatePassed(date) {
      let dateConverted = this.$moment(date);
      return this.$moment().isAfter(dateConverted);
    },
    /**
     * Returns sorted shows (upcoming first, closer to the current date first).
     * Passed shows will only be returned if there are less then 5 upcoming 
     * shows to returned.
     */
    ordered(showsRef) {
      let shows = showsRef.slice(); // must use shallow copy or Vue warns of possible infinite loop
      shows.forEach(s => s.hasDatePassed = this.hasDatePassed(s.date));
      return shows.sort((s1, s2) => s1.hasDatePassed !== s2.hasDatePassed 
        ?(s1.hasDatePassed ?1 :-1)
        :((this.$moment(s2.date)._d.getTime() - this.$moment(s1.date)._d.getTime())
          *(s1.hasDatePassed ?1:-1)))
        .filter((s, idx) => idx < 5 || !s.hasDatePassed);
    },
    countUpcomingShows(venue) {
      return venue.shows.filter(s => !this.hasDatePassed(s.date)).length;
    }
  },
  data() {
    return {
      today: new Date()
    };
  }
}; // TODO if time allows add no-data placeholder
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Sniglet");

span.passed-event {
  color: lightcoral;
  font-size: 0.8rem;
}

span.upcoming-event {
  color: #2ECC40;
  font-size: 0.8rem;
}

#showVenue {
  width: 100vw;
  margin-top: 1rem;
  display: table;
}

div.venue-row {
  width: 100vw;
  padding: 1rem;
  display: table-row;
  text-align: left;
}

div.venue-row:nth-child(2n+1) {
  background-color: rgba(0,0,0,0.1);
}

div.venue-row > .venue-cell {
  display: table-cell;
  vertical-align: middle;
  font-family: 'Sniglet';
}

div.venue-row > .venue-cell > .left-aligned {
  display: inline-block;
  text-align: left;
}

div.venue-row > .venue-cell .venue-name {
  padding-top: 0.5rem;
  font-weight: bold;
  font-size: 1.2rem;
}

div.venue-row > .venue-cell .venue-address {
  padding-bottom: 0.5rem;
}

div.venue-row > .venue-cell > .space-taker {
  width: 2vw;
}

div.venue-edit-btn {
  padding: 0.5rem 0;
  font-size: 1.2rem;
  cursor: pointer;
}

div.venue-edit-btn > span {
  font-size: 0.85rem;
  vertical-align: text-bottom;
}

div.venue-edit-btn:hover {
  color: #2ECC40;
}

span.show-trigger {
  cursor: pointer;
}

span.show-trigger.upcoming-show:hover {
  color: #2ECC40;
}

span.show-trigger.passed-show:hover {
  color: lightcoral;
}

</style>