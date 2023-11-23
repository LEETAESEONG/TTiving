<template>
  <youtube :video-id="videoId" width="80%" :player-vars="playerVars"
          height="100%"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%">

  </youtube>
</template>

<script>
export default {
  name: "VideoPlayer",
  data(){
    return{
        videoId : '',
        playerVars : {
            autoplay : 1
        }
    }
  },
  created() {
    this.videoId = this.$route.params.videoId;
  }
};
</script>

<style>
</style>