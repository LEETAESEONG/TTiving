<template>
  <div class="show-list-body">
    <div
      class="show-list-large-box"
      v-for="(movie, index) in movies"
      :key="index"
    >
      <img @click="goMovieDetail(movie.id)" :src="TMDB_URL + movie.poster_path" alt="" class="show-list-img" />
      <div class="show-list-middle-box">
        <div class="show-list-text">
          <h2 class="show-list-title">{{ movie.title }}</h2>
          <h4>평점: {{ movie.vote_average }}</h4>
          <h4>개봉일: {{ movie.release_date }}</h4>
        </div>
        <div class="show-list-overview">
          <p>{{ movie.overview }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      movies: [],
      TMDB_URL: "https://image.tmdb.org/t/p/w500",
    };
  },
  methods: {
    getMovieList() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/movies",
      })
        .then((res) => {
          this.movies = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    goMovieDetail (movieId) {
      const detailPath = "/movieDetail/" + movieId
      this.$router.push(detailPath)
    }
  },
  created() {
    this.getMovieList();
  },
};
</script>

<style>
.show-list-body {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
.show-list-large-box {
  padding: 10px;
  display: inline-flex;
  margin: 10px;
}
.show-list-img {
  cursor: pointer;
  border-radius: 10px;
  height: 450px;
  width: 300px;
  box-shadow: 5px 5px 6px red;
}
.show-list-middle-box {
  display: flex;
  flex-flow: row wrap;
  height: 450px;
  width: 300px;
  padding: 10px;
}

.show-list-text {
  text-align: left;
  width: 280px;
  height: 180px;
  padding: 5px;
}
.show-list-overview {
  width: 280px;
  height: 250px;
  overflow: scroll;
  padding: 5px;
}
.show-list-overview::-webkit-scrollbar {
  display: none; /* 크롬, 사파리, 오페라, 엣지 */
}
.show-list-title {
  font-weight: 400;
  text-shadow:4px 4px 6px red;
}
</style>