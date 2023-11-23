<template>
  <div style="width: 100%; padding-top: 10px; padding-bottom: 10px">
    <best-movie-item
      class="large-box"
      v-for="(rankedMovie, index) in rankedMovies"
      :key="rankedMovie.movie.id"
      :rankedMovie="rankedMovie"
      :rank="index"
      :id="'box' + index"
    ></best-movie-item>
  </div>
</template>

<script>
import BestMovieItem from "@/components/movies/BestMovieItem.vue";

export default {
  components: {
    BestMovieItem,
  },
  mounted() {
    const options = {
      threshold: 0.7, // 화면에 보이는 비율이 50% 이상이면 적용
    };
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = 1;
        } else {
          entry.target.style.opacity = 0;
        }
      });
    }, options);

    observer.observe(document.getElementById("box0"))
    observer.observe(document.getElementById("box1"))
    observer.observe(document.getElementById("box2"))
    observer.observe(document.getElementById("box3"))
    observer.observe(document.getElementById("box4"))
    observer.observe(document.getElementById("box5"))
    observer.observe(document.getElementById("box6"))
    observer.observe(document.getElementById("box7"))
    observer.observe(document.getElementById("box8"))
    observer.observe(document.getElementById("box9"))

  },
  data() {
    return {
      rankedMovies: [],
    };
  },
  created() {
    this.getRankedMovie();
    this.rankedMovies = this.$store.state.bestMovies;
  },
  methods: {
    getRankedMovie() {
      this.$store.dispatch("getBestMovie");
    },
  },
};
</script>

<style scoped>
.large-box {
  opacity: 0;
  transition: all 0.7s;
}
</style>
