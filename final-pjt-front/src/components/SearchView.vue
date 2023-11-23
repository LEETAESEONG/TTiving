<template>
  <div style="display: inline-block">
    <b-button
      v-b-modal.modal-prevent-closing
      variant="outline-light"
      style="border: none"
      ><b-icon icon="search"></b-icon
    ></b-button>
    <b-modal
      style="background-color: tranparent"
      :hide-footer="true"
      :hide-header="true"
      id="modal-prevent-closing"
      ref="modal"
      @show="resetModal"
      @hidden="resetModal"
    >
      <form ref="form" style="background-color: tranparent">
        <b-form-group
          label-for="keyword-input"
          invalid-feedback="검색어를 입력해주세요."
          :state="keywordState"
        >
          <b-form-input
            placeholder="검색어를 입력해주세요."
            autofocus
            class="rounded-pill mb-3"
            id="keyword-input"
            v-model="keyword"
            :state="keywordState"
            required
            @input="search"
          ></b-form-input>
        </b-form-group>
      </form>

      <b-container v-if="results">
        <div style="cursor:pointer;" v-for="result in results" :key="result.pk">
          <h5 @click="handleSubmit(result.id)">
            {{ result.title }}
          </h5>
        </div>
      </b-container>
    </b-modal>
    <b-modal modal-research-result> test </b-modal>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SearchView",
  data() {
    return {
      keyword: "",
      keywordState: null,
      results: [],
    };
  },
  methods: {
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.keywordState = valid;
      return valid;
    },
    resetModal() {
      this.keyword = "";
      this.keywordState = null;
    },
    search() {
      if (this.keyword) {
        axios({
          method: "GET",
          url: `http://localhost:8000/movies/search/${this.keyword}/`,
          data: {
            keyword: this.keyword,
          },
        })
          .then((res) => {
            this.results = res.data;
          })
          .catch((err) => console.log(err));
      }
    },
    handleSubmit(id) {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      // Push the keyword to submitted keywords

      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide("modal-prevent-closing");
        this.resetModal();

        console.log("test: ", id);
        this.toDetail(id);
        window.location.reload();
      });
    },
    toDetail(id) {
      console.log(id);
      if (this.$route.path != `/movieDetail/${id}`) {
        this.$router.push(`/movieDetail/${id}`);
      }
    },
  },
};
</script>

<style>
</style>