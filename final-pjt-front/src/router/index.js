import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/accounts/LoginView.vue'
import SignupView from '../views/accounts/SignupView.vue'
import ProfileView from '../views/accounts/ProfileView.vue'
import MovieList from '../views/movies/MovieList.vue'
import MovieDetail from '../views/movies/MovieDetail.vue'
import UpdateView from "@/views/accounts/UpdateView.vue"
import VideoPlayer from '@/views/movies/VideoPlayer.vue'
import AllMovie from "@/views/movies/sub_movies/AllMovie.vue"
import FindBestMovie from "@/views/movies/FindBestMovie.vue"
import MapView from "@/views/movies/MapView.vue"
import ShowMovieList from "@/views/movies/sub_movies/ShowMovieList.vue"

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(() => {
        return window.location.reload()
    })
};

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/movieList',
    name: 'movieList',
    component: MovieList
  },
  {
    path: '/movieDetail/:id',
    name: 'movieDetail',
    component: MovieDetail,
    beforeEnter: (to, from, next) => {
      next();
      if (from.name == "player") {
        location.reload()
      }
    },
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: ProfileView,
  },
  {
    path: '/Update',
    name: 'update',
    component: UpdateView
  },
  {
    path: '/player/:videoId',
    name: 'player',
    component: VideoPlayer
  },
  {
    path: '/allMovie/:contentId',
    name: 'allMovie',
    component: AllMovie
  },
  {
    path: '/findBestMovie',
    name: 'findBestMovie',
    component: FindBestMovie
  },
  {
    path: '/mapView',
    name: 'MapView',
    component: MapView
  },
  {
    path: '/showMovieList',
    name: 'ShowMovieList',
    component: ShowMovieList
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  fallback: true
})

router.beforeEach((to, from, next) => {

  const isLoggedIn = JSON.parse(localStorage.getItem('vuex'))
  const authPages = ['update']

  const isAuthRequired = authPages.includes(to.name)

  if (isAuthRequired && !(isLoggedIn.myid)) {
    alert('로그인이 필요한 페이지입니다.')
    next({ name: 'login' })
  } else {
    next()
  }

})

export default router
