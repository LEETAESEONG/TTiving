import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '@/router'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [
    createPersistedState(),
  ],
  state: {
    myid: null,
    token: null,
    articles: null,
    posters: {},
    selected_genres: [],
    all_movie_ids: [],
    recommend_movie_list: [],
    bestMovies: [],
    mypicture: null,
  },
  getters: {
    loggedIn(state) {
      return state.token ? true : false
    },
    ID(state){
      return state.myid;
    },
    Pic(state){
      return state.mypicture
    }
  },
  mutations: {
    SAVE_TOKEN(state, userItems) {
      state.token = userItems.token
      state.myid = userItems.id
      
    },
    DELETE_TOKEN(state) {
      state.token = null
      state.myid = null
      state.mypicture = null
      state.selected_genres = []
    },
    GET_POSTERS(state, posters) {
      state.posters[posters.genreId] = posters.genrePosterPath
    },
    GET_SELECTED_GENRES(state, selected_genres) {
      state.selected_genres = selected_genres.map(item => item.id)
    },
    GET_ALL_MOVIE_IDS(state, all_movie_ids) {
      state.all_movie_ids = all_movie_ids
    },
    RECOMMEND_MOVIE(state, movie_list) {
      state.recommend_movie_list = movie_list
    },
    GET_BEST_MOVIE(state, bestMovies) {
      state.bestMovies = bestMovies
    },
    GET_PICTURE(state, mypic) {
      state.mypicture = mypic;
      console.log(state.mypicture)
      // location.reload();
    }
  },
  actions: {
    signup(context, payload) {
      const username = payload.username
      const password1 = payload.password1
      const password2 = payload.password2

      // console.log('test', username, password1, password2)
      axios({
        method: 'post',
        url: 'http://localhost:8000/auth/signup/',
        data: {
          username, password1, password2
        }
      })
        .then(res => {
          console.log(res)
          const userItems = {
            token: res.data.access,
            id: res.data.user.pk
          }
          context.commit('SAVE_TOKEN', userItems)
          router.push({ name: 'home' })
        })
        .catch(err => {
          console.log(err)
          alert('이미 존재하는 아이디 입니다.')
        })
      },
      login(context, payload) {
        const username = payload.username
        const password = payload.password
        
        axios({
          method: 'post',
          url: 'http://localhost:8000/auth/login/',
          data: {
            username, password
          }
        })
        .then(res => {
          const userItems = {
            token: res.data.access,
            id: res.data.user.pk
          }
          console.log(userItems)
          context.commit('SAVE_TOKEN', userItems)
          context.dispatch('getPicture')
          router.push({ name: 'home' })
        })
        .catch(err => {
          console.log(err)
          alert('일치하는 회원정보가 없습니다. 아이디, 비밀번호를 확인해주세요.')
        })
    },
    getPicture(context) {
      axios({
        method: "GET",
        url: `http://localhost:8000/accounts/${context.state.myid}/profile/`,
      })
        .then(res => {
          console.log('test', res.data.person.picture)
          context.commit('GET_PICTURE', res.data.person.picture)
        })
        .catch(err => console.log(err))
    },
    logout(context) {
      context.commit('DELETE_TOKEN')
      // location.reload() : Vuex Store, Axios header 클리어.
      location.reload();
      axios({
        methods: 'post',
        url: 'http://127.0.0.1:8000/auth/logout/',
        headers: {
          Authorization: `Token ${this.state.token}`
        }
      })
        .then(() => {
          router.push({ name: 'home' })
        })
        .catch(err => console.log(err))
    },
    getPoster(context, posters) {
      context.commit("GET_POSTERS", posters)
    },
    getSelectedGenres(context, selected_genres) {
      context.commit("GET_SELECTED_GENRES", selected_genres)
    },
    getAllMovieIds(context) {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/movies"
      })
        .then((res) => {
          const all_movie_ids = res.data.map((item) => item.id)
          context.commit("GET_ALL_MOVIE_IDS", all_movie_ids)
        })
        .catch((err) => {
          console.log(err)
        })
    },
    recommendMovie(context, movie_list) {
      context.commit("RECOMMEND_MOVIE", movie_list)
    },
    getBestMovie(context) {
      axios({
        url: "http://127.0.0.1:8000/movies/find_best_movie/",
        method: "GET"
      })
        .then((res) => {
          context.commit("GET_BEST_MOVIE", res.data)
        })
        .catch((err) => {
          console.log(err)
        })
    }
  },
  modules: {
  }
})

