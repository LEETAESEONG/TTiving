<template>
  <div
    class="p-2 my-1 rounded"
    style="background-color: white; color: black"
    @click.prevent="wantUpdate"
  >
    <div class="m-auto d-flex w-100 justify-content-between">
      <div class="movieInfo">
        <b-avatar :src="userPic" class="mx-2"></b-avatar>
        <span @click="moveToUser">{{ userName.username }} </span> -
        <span class="mx-2 m-auto" @click.prevent="moveToMovie">{{
          movie.title
        }}</span>
        <b-form-rating
          inline
          no-border
          :value="review.rank"
          variant="warning"
          show-value
          readonly
        ></b-form-rating>
      </div>
      <small class="my-auto px-2"
        ><span> {{ review.created_at.substr(0, 10) }}</span>
        {{ review.created_at.substr(11, 5) }}
      </small>
    </div>
    <div class="d-flex justify-content-between">
      <span class="mx-2 my-auto">{{ review.content }}</span>
      <div>
        <b-button-group class="mx-1">
          <b-button @click="likes" :pressed="like" variant="outline-danger">
            <b-icon icon="hand-thumbs-up"></b-icon>
            <span>{{ like_count }} </span>
          </b-button>
          <b-button
            @click="dislikes"
            :pressed="dislike"
            variant="outline-danger"
          >
            <b-icon icon="hand-thumbs-down"></b-icon>
            <span>{{ dislike_count }} </span>
          </b-button>
        </b-button-group>
        <b-button
          @click.prevent="removeComment"
          variant="danger"
          style="z-index: 1"
          v-if="this.$store.state.myid==this.review.user"
          >삭제</b-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CommentListItem",
  data() {
    return {
      userName: "",
      movie: "",
      like: false,
      dislike: false,
      like_count: 0,
      dislike_count: 0,
      userPic: "",
    };
  },
  props: {
    review: Object,
  },
  methods: {
    getMovieDetail() {
      // id를 사용하여 영화 정보 가져오기
      // 예를 들어 axios를 사용하여 API 요청을 보내고 영화 정보를 가져올 수 있습니다.
      // this.id를 사용하여 API 요청 URL에 해당 id를 전달할 수 있습니다.
      axios({
        method: "GET",
        url: `http://127.0.0.1:8000/movies/${this.review.movie}/`,
      }).then((res) => {
        // console.log(res);
        this.movie = res.data;
      });
    },
    getUserName() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/accounts/userinfo/",
      }).then((res) => {
        this.userName = res.data.username[this.review.user - 1];
        this.userPic = res.data.user[this.review.user - 1].picture;
      });
    },
    removeComment() {
      console.log(this.review.id);
      axios({
        method: "DELETE",
        url:
          "http://127.0.0.1:8000/comments/delete_put/" + this.review.id + "/",
        headers: {
          Authorization: "Bearer " + this.$store.state.token,
        },
      })
        .then((res) => {
          console.log(res.data);
          this.$emit("comments");
        })
        .catch((err) => {
          console.log(err);
        });
    },
    wantUpdate() {
      this.$emit("wantUpdate");
    },
    moveToMovie() {
      console.log(this.movie);
      if (this.$route.path !== `/movieDetail/${this.movie.id}`) {
        this.$router.push(`/movieDetail/${this.movie.id}`);
      }
    },
    moveToUser() {
      console.log(this.review);
      if (this.$route.path !== `/profile/${this.review.user}`) {
        this.$router.push(`/profile/${this.review.user}`);
      }
    },
    likes_or_dislikes() {
      if (this.$store.state.myid) {
        axios({
          method: "GET",
          url: `http://127.0.0.1:8000/comments/likes_or_dislikes/${this.review.id}`,
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
          .then((res) => {

            console.log(res);

            this.like_count = res.data.like_count;
            this.dislike_count = res.data.dislike_count;
            if (res.data.likes_or_dislikes == 1) {
              this.like = true;
            } else if (res.data.likes_or_dislikes == -1) {
              this.dislike = true;
            }
          })
          .catch((err) => console.log(err));
      }
    },
    likes(event) {
      event.stopPropagation();
      if (this.$store.state.myid) {
        axios({
          method: "POST",
          url: `http://127.0.0.1:8000/comments/likes/${this.review.id}/`,
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
          .then((res) => {
            console.log(res);
            this.like_count = res.data.like_count;
            this.dislike_count = res.data.dislike_count;
            if (res.data.likes_or_dislikes == 1) {
              this.like = true;
              this.dislike = false;
            } else if (res.data.likes_or_dislikes == -1) {
              this.dislike = true;
              this.like = false;
            } else {
              this.like = false;
            }
          })
          .catch((err) => console.log(err));
      } else {
        alert("로그인 후 이용가능합니다.");
        this.$router.push("/login");
      }
    },
    dislikes(event) {
      event.stopPropagation();
      if (this.$store.state.myid) {
        axios({
          method: "POST",
          url: `http://127.0.0.1:8000/comments/dislikes/${this.review.id}/`,
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
          .then((res) => {
            this.like_count = res.data.like_count;
            this.dislike_count = res.data.dislike_count;
            if (res.data.likes_or_dislikes == 1) {
              this.like = true;
              this.dislike = false;
            } else if (res.data.likes_or_dislikes == -1) {
              this.dislike = true;
              this.like = false;
            } else {
              this.dislike = false;
            }
          })
          .catch((err) => console.log(err));
      } else {
        alert("로그인 후 이용가능합니다.");
        this.$router.push("/login");
      }
    },
  },
  created() {
    this.getUserName();
    this.getMovieDetail();
  },
  mounted() {
    this.likes_or_dislikes();
  },
};
</script>

<style>
.movieInfo > span {
  cursor: pointer;
}
</style>
