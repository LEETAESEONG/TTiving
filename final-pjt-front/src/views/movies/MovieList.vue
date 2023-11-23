<template>
  <div>
    <router-link class="all_view" to="/showMovieList"><h2 style="margin-right: 20px;">전체보기</h2></router-link>
    <swiper :options="swiperOption" class="swiper" style="padding-top: 20px; padding-bottom: 20px;">
      <swiper-slide v-for="(poster_path, index) in posterPathes" :key="index">
        <router-link :to="`/movieDetail/${poster_path[1]}`">
          <b-img class="poster-box" :src="poster_path[0]"></b-img>
        </router-link>
      </swiper-slide>
      <div
        class="swiper-button-prev"
        slot="button-prev"
        style="color: white"
      ></div>
      <div
        class="swiper-button-next"
        slot="button-next"
        style="color: white"
      ></div>
    </swiper>
  </div>
</template>

<script>
import axios from "axios";
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/css/swiper.css";

const TMDB_URL = "https://image.tmdb.org/t/p/w500";

export default {
  components: {
    Swiper,
    SwiperSlide,
  },
  data() {
    return {
      posterPathes: [],
      swiperOption: {
        slidesPerView: 3,
        loop: true,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      },
    };
  },
  methods: {
    getMovieList() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/movies",
      })
        .then((res) => {
          this.posterPathes = res.data.map((item) => [
            TMDB_URL + item.poster_path,
            item.id,
          ]);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.getMovieList();
  },
};
</script>

<style scoped>
.poster-box {
  border-radius: 20px;
  box-shadow: 12px 12px 6px 6px gray;
  height: 749px;
}
.all_view {
  text-decoration: none;
  color: white;
  position: relative;
  text-align: right;
}
</style>
