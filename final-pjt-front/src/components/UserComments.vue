<template>
  <div>
    <comment-list-item v-for="comment in comments" :key="comment.id" :review="comment"></comment-list-item>
  </div>
</template>

<script>
import CommentListItem from './Comment/CommentListItem.vue';
export default {
  name: "UserComments",
  components : {
    CommentListItem
  },
  props : {
    comments : Array
  }
};
</script>

<style>
</style>