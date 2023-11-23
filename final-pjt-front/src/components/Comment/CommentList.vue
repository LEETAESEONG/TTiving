<template>
  <b-container>
    <comment-create :movie_pk="movie_pk" @comments="comments"></comment-create>
    <b-list-group
      class="my-3"
      style="background-color: white"
      v-for="review in commentsList"
      :key="review.id"
    >
      <comment-list-item
        :review="review"
        @comments="comments"
        @wantUpdate="wantUpdate(review.id)"
      ></comment-list-item>
      <comment-update
        :review="review"
        :id="review.id"
        @comments="comments"
        @wantUpdate="wantUpdate(review.id)"
        class="d-none"
      ></comment-update>
    </b-list-group>
  </b-container>
</template>

<script>
import CommentCreate from "./CommentCreate.vue";
import CommentListItem from "./CommentListItem.vue";
import CommentUpdate from "./CommentUpdate.vue";
import axios from "axios";

export default {
  components: { CommentCreate, CommentListItem, CommentUpdate },
  name: "CommentList",
  props: {
    movie_pk: String,
  },
  data() {
    return {
      commentsList: {},
    };
  },
  component: {
    CommentCreate,
    CommentListItem,
  },
  methods: {
    comments() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/comments/" + this.movie_pk + "/",
      })
        .then((res) => {
          this.commentsList = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    wantUpdate(reviewId) {
      const updateForm = document.getElementById(reviewId);
      updateForm.classList.toggle("d-none");
    },
  },
  mounted() {
    this.comments();
  },
};
</script>

<style>
.d-none {
  display: none;
}
</style>