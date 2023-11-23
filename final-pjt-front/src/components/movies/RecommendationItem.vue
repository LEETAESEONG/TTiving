<template>
  <img v-if="moviePP != null && moviePP != undefined" :src="'https://image.tmdb.org/t/p/w300' + moviePP" alt="" @click="clickSlide" style="cursor: pointer;"/>
</template>

<script>

export default {
  name: "RecommendationItem",
  props: {
    movieId: Number,
    moviePP: String,
  },
  components: {
  },
  data() {
    return {};
  },
  created() {},
  methods: {
    clickSlide() {
      console.log(this.movieId)
       this.$router.push(`/movieDetail/${this.movieId}`);
    }
  },
};
</script>

<style scoped>
img {
  border-radius: 5px;
  height: 450px;
  width: 300px;
  border: 8px solid rgb(60, 45, 145, 0.2)
}
</style>