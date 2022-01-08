<template>
<div>
  <div class="columns">
    <div id="phrases-view" class="column is-half is-offset-one-quarter">
      <div class="card m-auto p-4">
        <h1 class="has-text-black title">Add phrases</h1>
        <p class="has-text-black">Add phrases here</p>
        <textarea class="textarea" placeholder="" v-model="phrases"></textarea>
        <div class="m-1">
          <button class="button is-primary is-outlined" @click="add_phrases()">
            Add phrases
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="title has-text-white m-3 has-text-centered">
    Yours sentences
  </div>
  <ul>
    <li v-for="phrase in $store.state.phrases" :key="phrase.id" class="">
      <div class="columns">
        <div
          class="
            column
            is-one-third is-offset-one-third
          "
        >
        <div class="card m-2 p-3">
          <div class="columns">
            <div class="column has-text-black">
              {{ phrase.phrase_text }}
            </div>
            <button
              class="button is-danger is-outlined m-2"
              @click="delete_phrase(phrase.id)"
            >
              Delete
            </button>
          </div>
          </div>
        </div>
      </div>
    </li>
  </ul>
</div>
</template>

<script>
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

import axios from "axios";
import router from "../router";

export default {
  methods: {
    delete_phrase(id) {
      
      let csrftoken = getCookie("csrftoken");
      axios
        .post(`/delete_phrase`,{ 'id': id },{ headers: { "X-CSRFToken": csrftoken } })
        .then(response => {
          console.log(response);
          this.$store.dispatch('getPhrases');	
        })
        .catch(error => {
          console.log(error);
        });
    },

    add_phrases() {
      var list_phrases = this.phrases.split(/\r?\n/);

      for (var i = 0; i < list_phrases.length; i++) {
        var phrase = list_phrases[i];
        var phrases = phrase.split(". ");
        if (phrases.length > 1) {
          list_phrases[i] = phrases[1];
        } else {
          list_phrases[i] = phrases[0];
        }
      }

      console.log(list_phrases);

      let csrftoken = getCookie("csrftoken");
      axios
        .post(
          "/add_phrases",
          { phrases: list_phrases },
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then((response) => {
          if (response.status === 200) {
            router.push("/");
          }
        });
    },
  },
};
</script>

<style>
</style>