<template>
  <div id="showConcert">
    <div v-for="concert in concerts" class="concert-row" :key="concert.id">
      <div class="concert-cell">
        <div class="space-taker"></div>
      </div>
      <div class="concert-cell">
        <div class="left-aligned">
          <div class="concert-name">{{concert.name}}&nbsp;&nbsp;<span>{{concert.ticket_price}}$/billet</span></div>
          <div class="concert-time">{{getConcertDate(concert)}}</div>
          <span class="concert-venues">Vendeurs:</span>&nbsp;
          <span
            class="concert-sellers"
            v-for="seller in concert.sellers"
            :key="seller"
          >Vente #{{seller}} &nbsp;</span>
          <span class="concert-sellers" v-if="concert.sellers.length == 0">Info non disponible</span>
        </div>
      </div>
      <div class="concert-cell">
        <div class="concert-venues">{{listVenues(venues, concert)}}</div>
      </div>
      <div class="concert-cell">
        <div
          class="concert-description"
        >{{concert.description.substring(0, Math.min(30, concert.description.length)) + (concert.description.length > 30 ?"..." :"")}}</div>
      </div>
      <div class="concert-cell">
        <div class="concert-action-btn">
          <span @click="edit(concert)">Modifier</span>&nbsp;|&nbsp;
          <span @click="remove(concert)">Effacer</span>
          <span v-if="!isCurrentlyPublished(concert)">&nbsp;|&nbsp;</span>
          <span v-if="!isCurrentlyPublished(concert)" @click="publish(concert)">Publier</span>
          <span v-if="!isSalesOver(concert)">&nbsp;|&nbsp;</span>
          <span v-if="!isSalesOver(concert)" @click="endSale(concert)">Fermer Vente</span>
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
    getConcertDate(concert) {
      return this.$moment(concert.date || new Date()).format("YYYY-MM-DD HH:mm");
    },
    edit(concert) {
      this.$emit("editConcert", concert);
      this.$emit("cancelCreateEdit");
    },
    remove(concert, index) {
      this.$emit("remove", { concert: concert, index: index });
    },
    publish(concert) {
      let confirmationMessage = "Publier au site de vente ";
      if (concert.sellers.length == 1) {
        confirmationMessage += concert.sellers[0];
      } else {
        confirmationMessage += "1 et 2";
      }
      if (confirm(confirmationMessage));
      this.$http
        .post("shows/" + concert.id + "/publish")
        .then(() => {
          this.$notify({
            group: "foo",
            title: "Réussi!",
            text: "Spectacle publié avec succès!",
            type: "success"
          });
          this.$emit("getConcerts");
        })
        .catch(err => {
          this.$notify({
            group: "foo",
            title: "Erreur!",
            text: err.body,
            type: "error"
          });
        });
    },
    listVenues(venues, concert) {
      let venueNames = venues
        .filter(v => v.id === concert.venue)
        .map(v => v.name)
        .join(", ");
      const MAX_STR_LENGTH = 30;
      return (
        venueNames.substring(0, Math.min(MAX_STR_LENGTH, venueNames.length)) +
        (venueNames.length > MAX_STR_LENGTH ? "..." : "")
      );
    },
    endSale(concert) {
      this.$http
        .post("shows/" + concert.id + "/endsale")
        .then(() => {
          this.$notify({
            group: "foo",
            title: "Réussi!",
            text: "Spectacle fermé avec succès!",
            type: "success"
          });
          this.$emit("getConcerts");
        })
        .catch(err => {
          this.$notify({
            group: "foo",
            title: "Erreur!",
            text: err.body,
            type: "error"
          });
        });
    },
    isSalesOver(concert) {
      let isOver = false;
      concert.publications.forEach(element => {
        if (element.status == "Vente terminée") {
          isOver = true;
        }
      });
      console.log(concert.name + " sales: " + isOver);
      return isOver;
    },
    isCurrentlyPublished(concert) {
      let isPublished = false;
      concert.publications.forEach(publication => {
        if (publication.status == "En vente") {
          isPublished = true;
        }
      });
      console.log(concert.name + " publised: " + isPublished);
      return isPublished;
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

div.concert-row:nth-child(2n + 1) {
  background-color: rgba(0, 0, 0, 0.1);
}

div.concert-row > .concert-cell {
  display: table-cell;
  vertical-align: middle;
  font-family: "Sniglet";
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

div.concert-row > .concert-cell .concert-name > span {
  font-weight: normal;
  font-size: 0.9rem;
}

div.concert-row > .concert-cell .concert-time {
  padding-bottom: 0.5rem;
}

div.concert-row > .concert-cell .concert-venues {
  text-decoration: underline;
}

div.concer-row > .concert-cell .concert-sellers {
  display: inline-block;
  display: flex;
}

div.concert-action-btn > span {
  cursor: pointer;
}

div.concert-action-btn > span:hover {
  text-decoration: underline;
  color: #2ecc40;
}

div.concert-row > .concert-cell > .space-taker {
  width: 2vw;
}
</style>
