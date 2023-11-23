<template>
  <img id="player" :src="videoSrc" frameborder="0"/>
</template>

<script>
export default {
  name: "VideoItem",
  props: {
    video: Object,
  },
  created() {
    this.videoSrc = "http://img.youtube.com/vi/" + this.video.key + "/0.jpg";
  },
  data() {
    return {
      videoSrc: "",
    };
  },
  methods : {
  }
};
</script>

<style>

</style>