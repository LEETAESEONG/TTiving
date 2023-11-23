<template>
  <div class="mb-5">
    <div class="main-container">
      <swiper :options="mainSwiperOption">
        <swiper-slide
          v-for="(movie, index) in randomMovies"
          :key="index"
          style="color: white"
        >
          <div
            class="outer"
            :style="`background-image: linear-gradient(to bottom, rgba(10, 10, 50, 0.42), rgba(10, 10, 20, 0.63)), url('https://image.tmdb.org/t/p/original${movie.backdrop_path}')`"
          >
            <div class="bottomleft">
              <h2>{{ movie.original_title }}</h2>
            </div>
            <div class="bottomRight">
              <button class="detail-btn"><h2>
                <router-link
                :to="`/movieDetail/${movie.id}`"
                style="color: white; text-decoration: none;">
                  자세히보기
                </router-link>
                </h2></button>
            </div>
          </div>
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
    <div
      class="recommend-list"
      v-for="(movies, index) in recommendMovie"
      :key="index"
      v-show="selected"
    >
      <div class="recommend-top">
        <h2
          style="color: aliceblue; padding-bottom: 10px; display: inline-block"
          :style="{ display: selected ? '' : 'none' }"
        >
          {{ recommendName[index] }}
        </h2>
        <router-link class="all_views" :to="`/allMovie/${index}`"
          >전체보기</router-link
        >
        <!-- <div class="swiper-pagination" slot="pagination"></div> -->
      </div>
      <swiper class="swiper" :options="swiperOption">
        <swiper-slide v-for="(movie, movieIndex) in movies" :key="movieIndex">
          <recommendation-item
            v-show="selected"
            :movieId="movie.id"
            :moviePP="movie.poster_path"
          ></recommendation-item>
          <div style="padding-top: 10px">
            <h3 style="vertical-align: bottom">{{ movie.title }}</h3>
            <h5 v-show="index == 0">개봉일 : {{movie.release_date}}</h5>
            <h5 v-show="index == 1">평점 : {{movie.vote_average}}</h5>
          </div>
        </swiper-slide>

        <div
          class="swiper-button-next"
          slot="button-next"
          style="color: white"
        ></div>
      </swiper>
    </div>

    <!-- 선택한 장르가 없을 때 v-show -->
  </div>
</template>

<script>
import RecommendationItem from "@/components/movies/RecommendationItem.vue";
import axios from "axios";
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/css/swiper.css";
import { sampleSize } from "lodash";

export default {
  components: {
    RecommendationItem,
    Swiper,
    SwiperSlide,
  },
  data() {
    return {
      recommendName: {
        0: "지금 상영할 수도 있어요!",
        1: "평점이 높은 걸 보고 싶지 않나요?",
        2: "# 0123 가나다라 ABCD",
      },
      selected: false,
      recommendMovie: [],
      swiperOption: {
        slidesPerView: 5,
        spaceBetween: 30,
        loop: false,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      },
      mainSwiperOption: {
        slidesPerView: 1,
        loop: true,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      },
      randomMovies: [],
      all_movie_ids: [],
    };
  },
  created() {
    this.recommend();
    if (this.$store.state.all_movie_ids.length == 0) {
      this.$store.dispatch("getAllMovieIds");
    }
    this.all_movie_ids = this.$store.state.all_movie_ids;
    this.randomThree();
  },
  methods: {
    recommend() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/movies/normal_recommendation/",
        headers: {
          Authorization: "Bearer " + this.$store.state.token,
        },
      })
        .then((res) => {
          if (res.data[0].length) {
            console.log(res.data[0])
            this.selected = true;
          } else {
            this.selected = false;
          }
          this.recommendMovie = res.data;
          this.$store.dispatch("recommendMovie", res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    randomThree() {
      const API_KEY = process.env.VUE_APP_API_KEY;
      const allMovies = this.all_movie_ids;

      const requests = allMovies.map((oneId) =>
        axios({
          method: "GET",
          url: `https://api.themoviedb.org/3/movie/${oneId}?language=en-US&api_key=${API_KEY}`,
        })
      );
      Promise.all(requests)
        .then((ress) => {
          const haveBackMovies = ress
            .map((res) => res.data)
            .filter((movie) => movie.backdrop_path);

          this.randomMovies = sampleSize(haveBackMovies, 5);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
.recommend-list {
  padding: 20px;
  text-align: left;
  align-items: bottom;
  position: relative;
}
.all_views {
  display: inline-block;
  padding-top: 20px;
  text-decoration: none;
  color: white;
}
.recommend-top {
  display: flex;
  justify-content: space-between;
}
.main-container {
  height: 1000px;
  transform: 0% 0%;
}
.main-text {
  position: absolute;
  transform: 50% 50%;
  display: table;
}
.outer {
  position: relative;
  /* background: url(/images/css_textoverimage.jpg); */
  width: 100%;
  height: 1000px;
  background-size: cover;
}
.bottomleft {
  position: absolute;
  bottom: 0;
  left: 0.5em;
  font-weight: bold;
  color: #fff;
  padding: 50px;
}
.bottomRight {
  position: absolute;
  bottom: 0;
  right: 0.5em;
  padding: 50px;
}
.detail-btn {
  border-radius: 10px;
  background-color:rgba(0, 0, 0, 0.5);
  color: white;
  box-shadow: 6px 6px 6px black;
}
</style>