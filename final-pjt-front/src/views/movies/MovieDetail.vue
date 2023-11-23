<template>
  <div class="wrap">
    <div class="bg-blurred rounded" :style="getBackgroundImageStyle"></div>
    <div
      class="overlay d-flex justify-content-between align-items-center px-5 mx-5"
    >
      <div style="width: 30%">
        <div class="d-flex justify-content-between">
          <div>
            <h1 style="display: inline-block; color: white; font-size: 50px">
              {{ movie.title }}
            </h1>
          </div>
          <div class="my-auto">
            <b-button-group>
              <b-button
                @click="likes"
                :pressed="like"
                variant="outline-warning"
              >
                <b-icon icon="emoji-smile"></b-icon>
              </b-button>
              <b-button
                @click="dislikes"
                :pressed="dislike"
                variant="outline-warning"
              >
                <b-icon icon="emoji-frown"></b-icon>
              </b-button>
            </b-button-group>
          </div>
        </div>

        <p class="d-flex">
          <span> 개봉일 : {{ movie.release_date }} </span>
          <span> | </span>
          <span> 평점 : {{ movie.vote_average }} </span>
        </p>

        <br />
        <p class="overview-table">
          {{ movie.overview }}
        </p>
      </div>
      <img class="poster m-4" :src="poster_path" alt="" />
    </div>
    <hr style="width: 80%" class="m-auto" />

    <div>
      <h2 class="mx-5 my-3" style="text-align: left">관련 영상</h2>
      <div v-if="videos == undefined || videos.length == 0" class="my-5">
        관련 영상이 없습니다.
      </div>
      <swiper
        @click-slide="clickSlide"
        :options="swiperOption"
        :slides-per-view="3"
        :space-between="10"
        @swiper="onSwiper"
        @slideChange="onSlideChange"
      >
        <swiper-slide
          style="display: inline-block; width: 600px"
          v-for="video in videos"
          :key="video.id"
        >
          <video-item :video="video"></video-item>
        </swiper-slide>
        <div class="swiper-button-prev" slot="button-prev"></div>
        <div class="swiper-button-next" slot="button-next"></div>
      </swiper>
    </div>

    <hr style="width: 80%" class="m-auto" />
    <!-- 댓글 전체 -->
    <comment-list :movie_pk="id"></comment-list>
    <div style="width: 100%; height: 500px"></div>
  </div>
</template>

<script>
import axios from "axios";
import CommentList from "@/components/Comment/CommentList";
import VideoItem from "../../components/movies/VideoItem.vue";

import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/css/swiper.css";

export default {
  components: {
    CommentList,
    VideoItem,
    Swiper,
    SwiperSlide,
  },
  setup() {
    const onSwiper = (swiper) => {
      console.log(swiper);
    };
    const onSlideChange = () => {
      console.log("slide change");
    };
    return {
      onSwiper,
      onSlideChange,
    };
  },
  data() {
    return {
      id: null,
      movie: {},
      poster_path: "",
      like: null,
      dislike: null,
      videoId: null,
      videos: null,
      playerVars: {
        autoplay: 1,
      },
      swiperOption: {
        slidesPerView: 3,
        spaceBetween: 10,
        loop: false,
        // pagination: {
        //   el: ".swiper-pagination",
        //   clickable: true,
        // },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      },
    };
  },
  computed: {
    getBackgroundImageStyle() {
      return {
        backgroundImage: `url(${this.poster_path})`,
      };
    },
  },
  mounted() {
    this.likes_or_dislikes();
  },
  created() {
    this.id = this.$route.params.id; // 경로에서 id 가져오기
    this.getMovieDetail();
    // this.likes_or_dislikes()
  },
  methods: {
    clickSlide(idx) {
      console.log("play: ", this.videos[idx].key);
      this.$router.push(`/player/${this.videos[idx].key}`);
    },
    getMovieDetail() {
      // id를 사용하여 영화 정보 가져오기
      // 예를 들어 axios를 사용하여 API 요청을 보내고 영화 정보를 가져올 수 있습니다.
      // this.id를 사용하여 API 요청 URL에 해당 id를 전달할 수 있습니다.
      axios({
        method: "GET",
        url: `http://127.0.0.1:8000/movies/${this.id}/`,
      })
        .then((res) => {
          this.movie = res.data;
          this.poster_path =
            "https://image.tmdb.org/t/p/w500" + res.data.poster_path;

          // 예고편 영상 가져오기
          // console.log('test3', this.movie)
          axios({
            method: "GET",
            url: `https://api.themoviedb.org/3/movie/${this.movie.id}/videos?language=ko-KR&api_key=${process.env.VUE_APP_API_KEY}`,
          })
            .then((res) => {
              console.log(res);
              this.videos = res.data.results;
            })
            .catch((err) => console.log("youtube-err", err));
        })
        .catch((err) => {
          console.log(err);
        });
    },
    likes_or_dislikes() {
      if (this.$store.state.myid) {
        axios({
          method: "GET",
          url: `http://127.0.0.1:8000/movies/likes_or_dislikes/${this.id}`,
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
          .then((res) => {
            // console.log(res);
            if (res.data.likes_or_dislikes == 1) {
              this.like = true;
            } else if (res.data.likes_or_dislikes == -1) {
              this.dislike = true;
            }
          })
          .catch((err) => console.log(err));
      }
    },
    likes() {
      console.log(this.$store.state.myid);
      if (this.$store.state.myid) {
        axios({
          method: "POST",
          url: `http://127.0.0.1:8000/movies/likes/${this.id}/`,
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
          .then((res) => {
            if (res.data.likes_or_dislikes == 1) {
              this.like = true;
              this.dislike = false;
            } else if (res.data.likes_or_dislikes == -1) {
              this.dislike = true;
              this.like = false;
            } else {
              this.like = false;
            }
          })
          .catch((err) => console.log(err));
      } else {
        alert("로그인 후 이용가능합니다!");
        this.$router.push("/login");
      }
    },
    dislikes() {
      if (this.$store.state.myid) {
        axios({
          method: "POST",
          url: `http://127.0.0.1:8000/movies/dislikes/${this.id}/`,
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
          .then((res) => {
            if (res.data.likes_or_dislikes == 1) {
              this.like = true;
              this.dislike = false;
            } else if (res.data.likes_or_dislikes == -1) {
              this.dislike = true;
              this.like = false;
            } else {
              this.dislike = false;
            }
          })
          .catch((err) => console.log(err));
      } else {
        alert("로그인 후 이용가능합니다.");
        this.$router.push("/login");
      }
    },
  },
};
</script>

<style>
.wrap {
  position: relative;
  overflow-y: auto;
  color: gainsboro;
}

.poster {
  height: 70%;
  box-shadow: 2px 2px 12px 8px black;
}

.bg-blurred {
  filter: blur(10px);
  -webkit-filter: blur(10px);
  background-repeat: no-repeat;
  background-size: cover;
  height: 600px;
  position: relative;
  z-index: -1;
  opacity: 0.3;
  background-color: gray;
}

.overlay {
  position: absolute; /* 추가: 절대적인 위치 설정 */
  top: 0; /* 추가: 상단 여백 조정 */
  left: 0; /* 추가: 좌측 여백 조정 */
  right: 0; /* 추가: 우측 여백 조정 */
  bottom: 0; /* 추가: 하단 여백 조정 */
  display: flex;
  height: 600px;
}

p > span {
  display: flex;
  margin: 0 5px;
}

.overview-table {
  height: 400px;
  overflow: scroll;
}
.overview-table::-webkit-scrollbar {
  display: none;
}
</style>