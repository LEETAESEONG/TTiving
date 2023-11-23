<template>
  <b-container role="group" class="p-5 login-form" >
    <h1>로그인</h1>
    <b-row>
      <label for="input-username">ID</label>
      <b-form-input
        placeholder="ID"
        trim
        v-model="username"
        id="input-username"
        :state="nameState"
        aria-describedby="input-live-feedback"
      ></b-form-input>

      <b-form-invalid-feedback id="input-username-feedback" class="text-right"
        >알파벳/숫자 3글자 이상</b-form-invalid-feedback
      >

      <label for="input-password">PW</label>
      <b-form-input
        autocomplete="false"
        id="input-password"
        placeholder="PW"
        v-model="password"
        trim
        type="password"
        :state="passwordState"
        aria-describedby="input-live-feedback"
      ></b-form-input>
      <b-form-invalid-feedback
        autocomplete="false"
        id="input-password-feedback"
        class="text-right"
        >알파벳/숫자 8글자 이상</b-form-invalid-feedback
      >
      <b-button class="mt-4" variant="success" @click="login">로그인</b-button>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  computed: {
    nameState() {
      return this.username.length > 2 ? true : false;
    },
    passwordState() {
      return this.password.length > 7 ? true : false;
    },
  },
  methods: {
    login() {
      const username = this.username;
      const password = this.password;

      const payload = {
        username,
        password,
      };

      this.$store.dispatch("login", payload);      
    },
  },
};
</script>

<style scoped>
h1{
  color: black;
}

.login-form {
  border-radius: 10px;
  box-shadow: 5px 5px 10px black;
  background-color: white;
}
</style>