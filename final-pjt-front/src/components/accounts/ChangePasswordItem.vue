<template>
  <b-container role="group" class="p-5 signup-form">
    <h1 style="color: black; font-weight: 400;">비밀번호 변경</h1>
    <b-row>
      <label for="input-new_password1">PW</label>
      <b-form-input
        autocomplete="false"
        id="input-new_password1"
        placeholder="PW"
        v-model="new_password1"
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
      <label for="input-new_password2">PW Confirmation</label>
      <b-form-input
        autocomplete="false"
        id="input-new_password2"
        placeholder="PW-confirm"
        v-model="new_password2"
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
      <b-button variant="success" @click="changePassword">비밀번호 변경</b-button>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios"

export default {
  name: "ChangePasswordItem",
  data() {
    return {
      new_password1: "",
      new_password2: "",
    };
  },
  computed: {
    passwordState() {
      return this.new_password1.length > 7 ? true : false
    },
    passwordConfirmState() {
      return (this.new_password1 == this.new_password2) & this.passwordState ? true : false
    },
  },
  methods: {
    changePassword() {
      const new_password1 = this.new_password1
      const new_password2 = this.new_password2

      const context = {
        new_password1,
        new_password2
      }
      
      axios({
        method : "POST",
        url : "http://127.0.0.1:8000/auth/password/change/",
        data: context,
        headers : {
          Authorization: "Bearer " + this.$store.state.token
        }
      })
      .then((res) => {
        console.log(res.data)
        this.new_password1 = ""
        this.new_password2 = ""
        this.$emit("completeCPF")
      })
      .catch((err) => {
        console.log(err)
      })
    }
  }
};
</script>

<style>
</style>