<template>
  <div class="profile">
    <b-container class="d-flex rounded p-3 shadow mb-2">
      <div style="width: 50%; display: inline-block">
        <div @click="showModal" ref="btnShow" style="cursor: pointer">
          <b-avatar
            style="object-fit: cover; border: none"
            :src="user_picture"
            size="10rem"
            class="mb-4"
          ></b-avatar>
        </div>
        <h1 style="color: white">{{ person.username }}</h1>
      </div>
      <div v-if="isloggedin" style="width: 50%; display: inline-block">
        <div class="my-3 person_status">
          <span v-b-modal.followings-modal
            >팔로우 {{ followings.length }}
          </span>
          <span v-b-modal.followers-modal>팔로워 {{ followers.length }} </span>
        </div>
        <div v-if="id == this.$store.state.myid">
          <b-button class="my-2" style="background-color:purple; border:none;"
            ><router-link class="fav-movies" to="/update" 
              >선호하는 장르</router-link
            ></b-button
          ><br />
          <b-button class="quit my-2" @click="showCPF" variant="primary" style="border:none;"
            >비밀번호 변경</b-button
          ><br />
          <b-button v-b-modal.delete-modal class="quit" variant="danger" style="border:none;"
            >회원 탈퇴하기</b-button
          >
        </div>
        <div v-else-if="this.$store.state.myid">
          <b-button
            v-if="status_follow"
            class="bg-primary border"
            @click="followToggle"
            >언팔로우</b-button
          >
          <b-button v-else class="bg-primary quit" @click="followToggle"
            >팔로우</b-button
          >
        </div>
      </div>
      <div v-else>
        <div>로그인 후 프로필 조회가 가능합니다.</div>
        <router-link to="/login" style="color: white"
          >로그인하러 가기</router-link
        >
      </div>
    </b-container>

    <!-- 사용자의 영화 관련 정보 -->
    <b-container>
      <div class="tab mb-4">
        <span
          @click="likeClick"
          :class="{ active: like }"
          style="cursor: pointer"
          >좋아요</span
        >
        <span
          @click="dislikeClick"
          :class="{ active: dislike }"
          style="cursor: pointer"
          >싫어요</span
        >
        <span
          @click="commentClick"
          :class="{ active: comment }"
          style="cursor: pointer"
          >댓글 목록</span
        >
      </div>

      <!-- 비밀번호 변경하기 -->
      <change-password-item v-show="wantShow" @completeCPF="completeCPF"></change-password-item>
      <hr />
      <div v-if="like">
        <user-like-movies
          class="p-3 shadow mb-5"
          :movies="like_movies"
        ></user-like-movies>
      </div>
      <div v-else-if="dislike">
        <user-like-movies
          class="p-3 shadow mb-5"
          :movies="dislike_movies"
        ></user-like-movies>
      </div>
      <div v-else-if="comment">
        <user-comments :comments="comments"></user-comments>
      </div>
    </b-container>

    <!-- =========================   모달    ========================= -->
    <!-- 팔로잉 모달 -->
    <b-modal
      scrollable
      centered
      id="followings-modal"
      :hide-footer="true"
      title="팔로잉"
    >
      <div v-if="followings.length === 0">팔로잉이 없습니다.</div>
      <div v-else>
        <h5
          class="mx-3 my-2"
          v-for="following in followings"
          :key="following.id"
          @click="toUserDetail(following.id)"
          style="cursor: pointer"
        >
          <b-avatar :src="following.picture"></b-avatar>
          {{ following.username }}
        </h5>
      </div>
    </b-modal>

    <!-- 팔로워 모달 -->
    <b-modal
      scrollable
      centered
      id="followers-modal"
      :hide-footer="true"
      title="팔로워"
    >
      <div v-if="followers.length === 0">팔로워가 없습니다.</div>
      <div v-else>
        <h5
          class="mx-3 my-2"
          v-for="follower in followers"
          :key="follower.id"
          @click="toUserDetail(follower.id)"
          style="cursor: pointer"
        >
          <b-avatar :src="follower.picture"></b-avatar>

          {{ follower.username }}
        </h5>
      </div>
    </b-modal>

    <!-- 탈퇴하기 모달 -->
    <b-modal id="delete-modal" hide-footer hide-header>
      <div class="d-block text-center">
        <h3>정말로 탈퇴하시겠습니까?</h3>
      </div>
      <b-button
        id="btnhide"
        class="mt-3 w-100"
        variant="outline-warning"
        @click="hideModal"
        >취소</b-button
      >
      <b-button class="mt-2 w-100" variant="outline-danger" @click="delete_user"
        >탈퇴하기</b-button
      >
    </b-modal>
    
  <!-- 캐릭터 모달 -->
  <b-modal scrollable centered id="chracter-modal" @ok="handleOk">
    <div
      class="d-flex"
      style="
        height: 60px;
        overflow-x: scroll;
        overflow: hiddlen;
        white-space: nowrap;
      "
    >
      <div
        :class="movie == moviename ? 'pushed' : ''"
        @click="changeMovieName(movie)"
        class="rounded-pill p-2 m-1"
        style="
          background-color: darkseagreen;
          color: white;
          font-weight: bolder;
        "
        v-for="movie in movielist"
        :key="movie"
      >
        #{{ movie }}
      </div>
    </div>
    <div class="d-flex flex-wrap">
      <img
        v-for="pic in pictures"
        :key="pic._id"
        class="m-2 rounded"
        :class="pic.imageUrl == user_picture ? 'pushed' : ''"
        @click="changeCharacter(pic.imageUrl)"
        :src="pic.imageUrl"
        alt=""
      />
    </div>
  </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import UserLikeMovies from "../../components/UserLikeMovies.vue";
import UserComments from "../../components/UserComments.vue";
import ChangePasswordItem from "@/components/accounts/ChangePasswordItem.vue"

export default {
  name: "ProfileView",
  components: {
    UserLikeMovies,
    UserComments,
    ChangePasswordItem
  },
  data() {
    return {
      wantShow: false,
      like: true,
      dislike: false,
      comment: false,
      id: '',
      comments: null,
      like_movies: null,
      person: "",
      follow_status: null,
      followings: [],
      followers: [],
      pictures: [],
      moviename: "",
      movielist: [
        "Zootopia",
        "Frozen",
        "Tangled",
        "Beauty and the Beast",
        "The Little Mermaid",
        "Aladdin",
        "The Lion King",
        "Bambi",
      ],
      user_picture: null,
      tmp_pic: null,
    };
  },
  computed: {
    status_follow() {
      return this.follow_status;
    },
    imgSrc() {
      return this.$store.getters.Pic;
    },
    isloggedin() {
      return this.$store.state.myid;
    },
  },
  methods: {
    showCPF () {
      this.wantShow = !this.wantShow
    },
    completeCPF () {
      this.wantShow = false
    },
    hideModal() {
      this.$root.$emit("bv::hide::modal", "delete-modal", "#btnhide");
    },
    delete_user() {
      axios({
        method: "DELETE",
        url: `http://localhost:8000/accounts/delete/`,
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`,
        },
      })
        .then((res) => {
          console.log(res);
          alert(res.data.message);
          this.$store.dispatch("logout");
        })
        .catch((res) => {
          console.log(res);
          alert("회원탈퇴 실패하였습니다. 관리자에게 문의하세요.");
        });
    },
    showModal() {
      if (this.id == this.$store.state.myid) {
        this.$root.$emit("bv::show::modal", "chracter-modal", "#btnShow");
        this.getCharacter();
      }
    },
    followToggle() {
      axios({
        method: "POST",
        data: {
          user_pk: this.id,
        },
        url: `http://localhost:8000/accounts/${this.id}/follow/`,
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`,
        },
      }).then((res) => {
        console.log(res);
        if (res.data.status) {
          this.follow_status = true;
        } else {
          this.follow_status = false;
        }
        this.followers = res.data.followers;
        this.followings = res.data.followings;
      });
    },
    getCharacter() {
      axios({
        method: "GET",
        url: `https://api.disneyapi.dev/character?films=${this.moviename}`,
      })
        .then((res) => {
          this.pictures = res.data.data;
          // console.log('test',this.pictures)
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getFollowStatus() {
      axios({
        method: "GET",
        url: `http://localhost:8000/accounts/${this.id}/get_follow_status/`,
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`,
        },
      })
        .then((res) => {
          // console.log(res);
          if (res.data.status) {
            this.follow_status = true;
          } else {
            this.follow_status = false;
          }
          this.followings = res.data.followings;
          this.followers = res.data.followers;
        })
        .catch((err) => console.log(err));
    },
    likeClick() {
      this.like = true;
      if (this.comment) {
        this.comment = false;
      }
      if (this.dislike) {
        this.dislike = false;
      }
    },
    dislikeClick() {
      this.dislike = true;
      if (this.comment) {
        this.comment = false;
      }
      if (this.like) {
        this.like = false;
      }
    },
    commentClick() {
      this.comment = true;
      if (this.like) {
        this.like = false;
      }
      if (this.dislike) {
        this.dislike = false;
      }
    },
    toUserDetail(id) {
      this.$router.push(`/profile/${id}`);
      location.reload();
    },

    changeMovieName(movie) {
      this.moviename = movie;
      this.getCharacter();
    },
    changeCharacter(character) {
      this.tmp_pic = character;
      // console.log("test", character == this.user_picture);
      console.log("test", this.tmp_pic);
    },
    handleOk() {
      if (this.tmp_pic) {
        console.log("user_picture : ", this.tmp_pic);
        axios({
          method: "POST",
          url: `http://localhost:8000/accounts/${this.id}/picture/`,
          data: {
            picture: this.tmp_pic,
          },
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
          },
        })
          .then((res) => {
            console.log(res);
            this.$store.dispatch("getPicture");
            this.user_picture = this.tmp_pic;
            this.tmp_pic = "";
            // location.reload();
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        alert("프로필 사진을 선택해주세요");
      }
    },
  },
  created() {
    // 사용자 정보 띄우기
    this.id = this.$route.params.id;
    // console.log(this.id);
    axios({
      method: "GET",
      url: `http://localhost:8000/accounts/${this.id}/profile/`,
    })
      .then((res) => {
        this.comments = res.data.comments;
        this.like_movies = res.data.like_movies;
        this.dislike_movies = res.data.dislike_movies;
        this.person = res.data.person;
        this.user_picture = res.data.person.picture;
        // console.log(this.user_picture)
      })
      .catch((err) => console.log(err));
  },
  mounted() {
    this.getFollowStatus();
  },
};
</script>

<style>

.fav-movies {
  text-decoration: none;
  color: white;
}

.profile {
  color: white;
}

.tab > span {
  margin: 20px;
}

#delete-modal {
  height: 200px;
}

.active {
  color: black;
  background-color: white;
  border-radius: 5px;
}

.person_status span {
  margin: 10px;
  cursor: pointer;
}

.modal-content {
  height: 400px;
}

.close {
  border: none;
  background-color: white;
}

button a:hover {
  color: white;
}

.pushed {
  box-shadow: inset 0 0 20px #333;
}
</style>