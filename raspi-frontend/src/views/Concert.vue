<template>
  <div>
    <h1>Page des spectacles/Concerts</h1>
  </div>
</template>

<script>
export default {
  name: "concert",
  components: {},
  data: () => {
    return {
      newConcert: {},
      createEditConcert: false,
      venues: [
        {
          id: 36,
          name: "1st venue",
          address: "123 avenue",
          capacity: 420
        },
        {
          id: 37,
          name: "2nd super venue",
          address: "456 bld",
          capacity: 69
        },
        {
          id: 38,
          name: "3rd amazing place",
          address: "789 street",
          capacity: 1337
        }
      ],
      concerts: [
        {
          id: 10,
          name: "Ariana Grande Concert",
          date: new Date(2019, 6, 4, 8),
          description: "Ariana Grande de retour à Montréal bitches",
          venue: 36
        },
        {
          id: 10,
          name: "BlackPink In Your Area",
          date: new Date(2029, 8, 14, 8),
          description: "Ariana Grande de retour à Montréal bitches",
          venue: 36
        },
        {}
      ]
    };
  }
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Acme");

div.venue {
  width: 100%;
  height: calc(100% - 85px);
}

h1 {
  color: white;
}
</style>