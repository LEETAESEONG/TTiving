<template>
  <b-card-group columns class="d-flex flex-wrap justify-content-center">
    <b-card style="width:200px; cursor:pointer;"
      v-for="(movie, index) in movies"
      :key="index"
      class="m-3 rounded"
      @click="move(movie.id)"
      img-top
      :img-src="'https://image.tmdb.org/t/p/w500' + movie.poster_path"
    >
      <b-card-text style="color: black">{{ movie.title }} </b-card-text>
    </b-card>
  </b-card-group>
</template>

<script>
// import LikeMovieItem from './LikeMovieItem.vue';
export default {
  name: "UserLikeMovies",
  props: {
    movies: Array,
  },
  components: {
    // LikeMovieItem
  },
  methods: {
    move(id) {
      this.$router.push(`/movieDetail/${id}`);
    },
  },
};
</script>

<style>
.card img {
  border-radius: 10px;
  padding: 3px;
}
</style>