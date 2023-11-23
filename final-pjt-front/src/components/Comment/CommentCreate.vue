<template>
  <div class="comment-form rounded my-5 py-3" style="background-color: white">
    <b-form-rating
      class="m-1"
      no-border
      inline
      v-model="rank"
      show-value
      variant="warning"
    ></b-form-rating>
    <b-form-textarea
      class="m-auto"
      style="width: 90%"
      v-model="content"
      placeholder="댓글을 입력해주세요"
      rows="3"
      no-resize
    >
    </b-form-textarea>
    <b-button
      style="width: 90%"
      class="my-1"
      variant="success"
      @click="commentcreate"
      >등록하기</b-button
    >
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CommentCreate",
  props: {
    movie_pk: String,
  },
  data() {
    return {
      rank: null,
      content: "",
    };
  },
  methods: {
    commentcreate() {
      const rank = this.rank;
      const content = this.content;
      axios({
        method: "post",
        url: `http://localhost:8000/comments/${this.movie_pk}/`,
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`,
        },
        data: {
          rank,
          content,
        },
      })
        .then((res) => {
          this.rank = null;
          this.content = "";
          console.log(res.data);
          this.$emit("comments");
        })
        .catch((err) => {
          console.log(err);
          alert('별점과 댓글을 작성해주세요')
        });
    },
  },
};
</script>

<style>
</style>