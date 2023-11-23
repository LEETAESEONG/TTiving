<template>
  <div id="app">
    <nav class="d-flex justify-content-between">
      <div>
        <router-link to="/"
          ><img style="width: 100px" src="@/assets/TTiving2.png" alt=""
        /></router-link>
        <router-link to="/movieList">영화목록</router-link> |
        <router-link to="/findBestMovie">영화순위</router-link> |
        <router-link to="/mapView">지도</router-link> |
        <span class="rounded log-out" v-if="this.loggedIn"><a @click="logout">로그아웃</a></span>
        <span v-else>
          <router-link to="/login">로그인</router-link> |
          <router-link to="/signup">회원가입</router-link>
        </span>
      </div>

      <div>
        <search-view-vue class="mx-2"></search-view-vue>
        <router-link class="pt-1 py-2" :to="`/profile/${this.$store.state.myid}`">
          <b-avatar class="p-1" :src="mypic" > </b-avatar
        ></router-link>
      </div>
    </nav>
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
import SearchViewVue from "./components/SearchView.vue";
export default {
  name: "App",
  components: {
    SearchViewVue,
  },
  data() {
    return {
    };
  },
  computed: {
    loggedIn() {
      return this.$store.getters.loggedIn;
    },
    mypic() {
      return this.$store.getters.Pic;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR&family=Noto+Serif+KR:wght@500;900&display=swap");

#app {
  font-family: "Noto Serif KR", serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
  position: fixed;
  width: 100%;
  height: auto;
  top: 0;
  left: 0;

  background-color: black;
  height: 100vh;
  margin: 0;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

.content {
  overflow-y: scroll;
  height: calc(100vh - 80px); /* Nav의 높이에 따라 조절 */
  overscroll-behavior: none; /* 스크롤 오버 시 효과 제거 */
}

.content::-webkit-scrollbar {
  display: none;
}

nav {
  padding: 30px;
  background-color: black;
}

nav a {
  font-weight: bold;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}

nav a:hover, .log-out:hover {
  color: black;
  background-color: white;
}

nav a.router-link-exact-active {
  font-weight: bolder;
  text-shadow: 1px lightgray;
}

</style>
