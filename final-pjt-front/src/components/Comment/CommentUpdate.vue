<template>
  <div>
    <b-form-rating
      class="mb-1"
      show-clear
      inline
      no-border
      v-model="rank"
      variant="warning"
      show-value
    ></b-form-rating>
    <b-form-textarea
      style="width: 90%"
      class="m-auto"
      no-border
      id="textarea-no-resize"
      v-model="content"
      rows="3"
      no-resize
    ></b-form-textarea>
    <b-button @click="commentupdate" style="width: 90%;"
      class="mt-1 mb-2"
      variant="success">수정하기</b-button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CommentUpdate",
  props: {
    review: Object,
  },
  data() {
    return {
      rank: null,
      content: "",
    };
  },
  created() {
    this.content = this.review.content;
    this.rank = this.review.rank;
  },
  methods: {
    commentupdate() {
      const rank = this.rank;
      const content = this.content;
      axios({
        method: "PUT",
        url: `http://localhost:8000/comments/delete_put/${this.review.id}/`,
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`,
        },
        data: {
          rank,
          content,
        },
      })
        .then((res) => {
          this.rank = rank;
          this.content = content;
          console.log(res.data);
          this.$emit("comments");
          this.$emit("wantUpdate");
        })
        .catch((err) => console.log(err));
    },
  },
};
</script>

<style>
</style>