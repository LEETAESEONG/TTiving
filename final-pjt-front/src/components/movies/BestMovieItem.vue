<template>
  <div style="padding-bottom: 10px">
    <div class="d-flex ranking-table">
      <img
        v-if="haveBackDrop"
        class="ranking-backdrop"
        :src="backdrop_path"
        alt=""
      />
      <div v-else class="no-have-back-drop"></div>
      <div class="ranking-text my-auto">
        <h1 class="rank">{{ rank + 1 }}</h1>
        <h1 class="text-shadow">
          {{ rankedMovie.movie.title }}
        </h1>
        <h1 class="text-shadow">
          TTIVING SCORE : {{ rankedMovie.getPoint * 10 }}
        </h1>
      </div>
      <div
        :id="`item${rank}`"
        class="ranking-item my-auto"
        @mouseenter="showTag(rank)"
        @mouseleave="hideTag(rank)"
      >
        <h3 class="gauge-text">
          평점 : {{ rankedMovie.voteAverage * 10 }} / 100
        </h3>
        <div class="gauge-item">
          <div class="gaugebar">
            <div
              class="linebar"
              :style="{ width: rankedMovie.voteAverage * 10 + '%' }"
              :class="[
                rank < 3 ? ['first', 'second', 'third'][rank] : 'normal',
              ]"
            ></div>
          </div>
        </div>
        <div class="gauge-item">
          <h3 class="gauge-text">
            좋아요 점수 : {{ rankedMovie.likesCounts * 10 }} / 100
          </h3>
          <div class="gaugebar">
            <div
              class="linebar"
              :style="{ width: rankedMovie.likesCounts * 10 + '%' }"
              :class="[
                rank < 3 ? ['first', 'second', 'third'][rank] : 'normal',
              ]"
            ></div>
          </div>
        </div>
        <div class="gauge-item">
          <h3 class="gauge-text">
            별점 평균 : {{ rankedMovie.rankAverage * 10 }} / 100
          </h3>
          <div class="gaugebar">
            <div
              class="linebar"
              :style="{ width: rankedMovie.rankAverage * 10 + '%' }"
              :class="[
                rank < 3 ? ['first', 'second', 'third'][rank] : 'normal',
              ]"
            ></div>
          </div>
        </div>

        <div class="gauge-item">
          <h3 class="gauge-text">
            리뷰 점수 : {{ rankedMovie.reviewsCounts * 10 }} / 100
          </h3>
          <div class="gaugebar">
            <div
              class="linebar"
              :style="{ width: rankedMovie.reviewsCounts * 10 + '%' }"
              :class="[
                rank < 3 ? ['first', 'second', 'third'][rank] : 'normal',
              ]"
            ></div>
          </div>
        </div>

        <div class="gauge-item">
          <h3 class="gauge-text">
            장르 순위 : {{ rankedMovie.genreRank * 10 }} / 100
          </h3>
          <div class="gaugebar">
            <div
              class="linebar"
              :style="{ width: rankedMovie.genreRank * 10 + '%' }"
              :class="[
                rank < 3 ? ['first', 'second', 'third'][rank] : 'normal',
              ]"
            ></div>
          </div>
        </div>
      </div>

      <div class="img-box">
        <img
          class="ranking-img"
          :src="
            'https://image.tmdb.org/t/p/w500' + rankedMovie.movie.poster_path
          "
          alt=""
        />
        <div class="ranking-btn-box">
          <button class="detail-btn">
            <h2>
              <router-link
                :to="`/movieDetail/${rankedMovie.movie.id}`"
                style="color: white; text-decoration: none"
              >
                영화 바로가기
              </router-link>
            </h2>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const API_KEY = process.env.VUE_APP_API_KEY;

export default {
  name: "BestMovieItem",
  props: {
    rankedMovie: Object,
    rank: Number,
  },
  methods: {
    showTag(rank) {
      const thisId = "item" + rank;
      const sTag = document.getElementById(thisId);
      sTag.style.opacity = "1";
    },
    hideTag(rank) {
      const thisId = "item" + rank;
      const sTag = document.getElementById(thisId);
      sTag.style.opacity = "0";
    },
  },
  data() {
    return {
      flag: true,
      haveBackDrop: false,
      backdrop_path: "https://image.tmdb.org/t/p/original",
    };
  },
  created() {
    if (
      this.flag &&
      this.backdrop_path === "https://image.tmdb.org/t/p/original"
    ) {
      axios({
        method: "GET",
        url: `https://api.themoviedb.org/3/movie/${this.rankedMovie.movie.id}?language=en-US&api_key=${API_KEY}`,
      })
        .then((res) => {
          this.backdrop_path += res.data.backdrop_path;
          this.flag = false;
          if (res.data.backdrop_path) {
            this.haveBackDrop = true;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
};
</script>

<style>
.gaugebar {
  border: 1px solid black;
  width: 400px;
  height: 50px;
  background-color: white;
  margin: 10px;
  border-radius: 10px;
  display: inline-block;
}
.linebar {
  height: 100%;
  border-radius: 10px;
}
.ranking-item {
  width: 40%;
  align-items: center;
  opacity: 0;
  cursor: pointer;
}
.ranking-table {
  width: 100%;
  justify-content: space-between;

  padding-bottom: 20px;
  vertical-align: middle;
  position: relative;
}
.ranking-img {
  width: 80%;
  border-radius: 20px;
  box-shadow: 12px 6px 6px 2px rgb(0, 0, 0);
}
.ranking-text {
  width: 30%;
}
.first {
  background-color: gold;
}
.second {
  background-color: silver;
}
.third {
  background-color: #cd7f32;
}
.normal {
  background-color: darkseagreen;
}
.ranking-backdrop {
  width: 100%;
  height: 120%;
  position: absolute;
  z-index: -9999;
  object-fit: cover;
}
.rank {
  color: white;
  font-size: 25em;
  font-weight: bold;
  text-shadow: 10px 10px 4px rgb(90, 90, 90), 20px 20px 4px black;
}
.img-box {
  width: 30%;
  padding: 10px;
  padding-top: 50px;
}
.ranking-btn-box {
  padding: 20px;
  right: 0.5em;
}
.text-shadow {
  font-weight: bold;
  text-shadow: 3px 3px 2px gray, 6px 6px 2px black;
}
.gauge-text {
  font-weight: bold;
  text-shadow: 2px 2px 2px gray, 4px 4px 2px black;
}
.no-have-back-drop {
  width: 100%;
  height: 120%;
  position: absolute;
  z-index: -9999;
  object-fit: cover;
  background: linear-gradient(
      217deg,
      rgba(255, 0, 0, 0.8),
      rgba(255, 0, 0, 0) 70.71%
    ),
    linear-gradient(127deg, rgba(0, 255, 0, 0.8), rgba(0, 255, 0, 0) 70.71%),
    linear-gradient(336deg, rgba(0, 0, 255, 0.8), rgba(0, 0, 255, 0) 70.71%);
}
</style>