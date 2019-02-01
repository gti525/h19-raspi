<template>
    <div>
        <div v-for="concert in concerts" class="card" :key="concert.id">
            <div class="card-body">
                <p>{{concert.name}}</p>
                <p>{{concert.date}}</p>
                <p>{{concert.description}}</p>
            </div>
        </div>
    </div>
</template>

<<script>
export default {
    name: "ShowConcerts",
    props: {
        concerts: Array
    }
}
</script>

<style scoped>
.card {
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 2rem;
}
</style>