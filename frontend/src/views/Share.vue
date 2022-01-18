<template>
  <div class="hero is-fullheight">
    <div class="columns">
      <div class="column is-one-third is-offset-one-third">
        <div class="card has-text-black m-6 p-4">
          <div>
            <strong> #UUID {{ sentence.id }}</strong>
          </div>
          <div class="card-body">
            {{ sentence.text }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data: function () {
    return {
      sentence: {
        id: null,
        text: "",
      },
    };
  },
  mounted() {
    //console.log("Share mounted");
    this.$route.params.id;
    axios
      .post("/api/get_by_id", {
        id: this.$route.params.id,
      })
      .then((res) => {
        //console.log(res);
        this.sentence = res.data.sentence;
      });
  },
};
</script>
