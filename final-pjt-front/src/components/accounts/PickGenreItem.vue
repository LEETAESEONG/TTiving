<template>
  <b-card class="clickGenre" @click.prevent="pickGenre" :id="genre.id" :style="{'background': selected ? selectedGradient : noneSelectedGradient, 'color' : selected ? 'white': 'black'}">

      <span>{{ genre.name }}</span>
    <span v-show="selected">  (선택 장르✅)</span>
    <b-carousel
      img-width="200"
      class="mt-3"
      style="max-height: 300px; min-width: 150px; max-width: 200px"
    >
      <carousel-item :id="genre.id"></carousel-item>
    </b-carousel>
  </b-card>
</template>

<script>
import CarouselItem from "./CarouselItem.vue";
import axios from "axios";

export default {
  name: "PickGenreItem",
  props: {
    genre: Object,
    selected: Boolean,
  },
  components: {
    CarouselItem,
  },
  data() {
    return {
      noneSelectedGradient: "linear-gradient(rgba(255, 255, 255, 1) 0%, rgba(251, 251, 251, 0.1) 100%), linear-gradient(90deg, #84d2ff, #8d5acd)",
      selectedGradient: "linear-gradient(147deg, #923cb5 0%, #000000 74%)"

    };
  },
  methods: {
    getPoster() {
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/movies/poster/",
        data: { id: this.genre.id },
      })
        .then((res) => {
          const genreId = this.genre.id
          const genrePosterPath = res.data
          this.$store.dispatch("getPoster", { genreId, genrePosterPath })
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // myid() {
    //   console.log(this.genre.id);
    //   const myFound = document.getElementById(this.genre.id);
    //   console.log(myFound);
    // },
    pickGenre() {
      axios({
        method: "GET",
        url: `http://127.0.0.1:8000/accounts/${this.genre.id}/pick_genre/`,
        headers: {
          Authorization: "Bearer " + this.$store.state.token,
        },
      })
        .then((res) => {
          this.$store.dispatch("getBestMovie");
          console.log(res.data);
          this.$emit("catch_genre")
          // 임시조치
          location.reload()
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.getPoster();
  },
};
</script>

<style>
.my {
  color: blueviolet;
}
.clickGenre {
  cursor: pointer;
}
</style>