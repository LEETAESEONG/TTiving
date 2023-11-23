<template>
  <b-container role="group" class="p-5 signup-form">
    <h1 style="color:black;">회원가입</h1>
    <b-row>
      <label for="input-username">ID</label>
      <b-form-input
        placeholder="아이디"
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
        placeholder="비밀번호"
        v-model="password1"
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
      <label for="input-password-confirm">PW Confirmation</label>
      <b-form-input
        autocomplete="false"
        id="input-password-confirm"
        placeholder="비밀번호 확인"
        v-model="password2"
        trim
        type="password"
        :state="passwordConfirmState"
        aria-describedby="input-live-feedback"
      ></b-form-input>
      <b-form-invalid-feedback
        autocomplete="false"
        id="input-password-feedback"
        class="text-right"
        >비밀번호와 일치하지 않습니다.</b-form-invalid-feedback
      >
      <b-button class="mt-4" variant="success" @click="signup">회원가입</b-button>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: "SignupView",
  data() {
    return {
      username: "",
      password1: "",
      password2: "",
    };
  },
  computed: {
    nameState() {
      return this.username.length > 2 ? true : false;
    },
    passwordState() {
      return this.password1.length > 7 ? true : false;
    },
    passwordConfirmState() {
      return (this.password2 == this.password1) & this.passwordState
        ? true
        : false;
    },
  },
  methods: {
    signup() {
      const username = this.username;
      const password1 = this.password1;
      const password2 = this.password2;

      const payload = {
        username,
        password1,
        password2,
      };
      // console.log(payload)
      this.$store.dispatch("signup", payload)
      this.username = ""
      this.password1 = ""
      this.password2 = ""
    },
  },
};
</script>

<style>
.signup-form {
  border-radius: 10px;
  box-shadow: 5px 5px 10px black;
  background-color: white;
}
</style>