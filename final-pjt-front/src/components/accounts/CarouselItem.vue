<template>
  <div>
    <b-carousel-slide
      v-for="(path, index) in postersArray"
      :key="index"
      :img-src="path"
    >
    </b-carousel-slide>
  </div>
</template>

<script>
export default {
  name: "CarouselItem",
  data() {
    return {
      postersArray: [],
    };
  },
  props: {
    id: Number,
  },
  created() {
    this.getPosters()
  },
  methods: {
    getPosters() {
      this.postersArray = this.$store.state.posters[this.id];
    },
  },
};
</script>

<style>
</style>