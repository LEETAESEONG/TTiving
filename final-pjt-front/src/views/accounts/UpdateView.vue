<template>
<div style="height: 1200px;">
  <b-container
    class="genre-list d-flex flex-wrap justify-content-center"
    style="max-width: 1800px; margin-bottom: 20px;"
  >
    <div v-if="isLoading">로딩중입니다.</div>
      <pick-genre-item
      v-else
        class="m-5"
        v-for="genre in genreList"
        :key="genre.id"
        :genre="genre"
        :id="genre.id"
        :selected="selected_toggle_genres[genre.id]"
        @catch_genre="catch_genre"
      ></pick-genre-item>
      <div style="width:100%; height:300px"></div>
  </b-container>
</div>
  
</template>

<script>
import axios from "axios";
import PickGenreItem from "../../components/accounts/PickGenreItem.vue";

export default {
  components: {
    PickGenreItem,
  },
  data() {
    return {
      isLoading: true,
      genreList: {},
      selected_genres: [],
      selected_toggle_genres: {
        12: false,
        14: false,
        18: false,
        27: false,
        28: false,
        35: false,
        36: false,
        53: false,
        80: false,
        99: false,
        878: false,
        9648: false,
        10402: false,
        10749: false,
        10752: false,
      },
    };
  },
  created() {
    this.getGenre();
    this.getSelectedGenres();
  },
  methods: {
    // 장르를 띄워주는 함수
    getGenre() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/movies/genres/",
      })
        .then((res) => {
          console.log(res.data);
          this.genreList = res.data;
          this.isLoading = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // 선택한 장르를 저장해주는 함수
    getSelectedGenres() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/accounts/picked_genre",
        headers: {
          Authorization: "Bearer " + this.$store.state.token,
        },
      })
        .then((res) => {
          this.selected_genres = res.data.map((item) => item.id);
          this.catch_genre();
          this.$store.dispatch("getSelectedGenres", res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    catch_genre() {
      for (let id of [
        12, 14, 16, 18, 27, 28, 35, 36, 53, 80, 99, 878, 9648, 10402, 10749,
        10752,
      ]) {
        if (this.selected_genres.includes(id)) {
          this.selected_toggle_genres[id] = true;
        } else {
          this.selected_toggle_genres[id] = false;
        }
      }
    },
  },
};
</script>

<style>
.genre-list {
  height: 600px;
}
</style>