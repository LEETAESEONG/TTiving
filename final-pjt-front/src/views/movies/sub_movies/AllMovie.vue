<template>
  <div style="padding: 20px">
    <h1 style="color: white;">{{ recommendName[now_content] }}</h1>
    <b-container>
      <b-row>
        <b-col cols="3" v-for="(movie, index) in now_movies" :key="index">
          <div style="padding: 10px">
            <recommendation-item
              :movieId="movie.id"
              :moviePP="movie.poster_path"
            ></recommendation-item>
            <h6 style="padding: 10px">{{ movie.title }}</h6>
            <h5 v-show="now_content == 0">개봉일 : {{movie.release_date}}</h5>
            <h5 v-show="now_content == 1">평점 : {{movie.vote_average}}</h5>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import RecommendationItem from "@/components/movies/RecommendationItem.vue";

export default {
  components: {
    RecommendationItem,
  },
  data() {
    return {
      now_content: null,
      now_movies: [],
      recommendName: {
        0: "지금 상영할 수도 있어요!",
        1: "평점이 높은 걸 보고 싶지 않나요?",
        2: "# 0123 가나다라 ABCD",
      },
    };
  },
  methods: {},
  created() {
    this.now_content = this.$route.params.contentId;
    if (this.now_movies.length == 0) {
      this.now_movies = this.$store.state.recommend_movie_list[this.now_content];
    }
  },
};
</script>

<style>
</style>