<template>
  <div>
    <div class="columns">
      <div id="phrases-view" class="column is-half is-offset-one-quarter">
        <div class="card m-auto p-4">
          <h1 class="has-text-black title">Add phrases</h1>
          <p class="has-text-black">Add phrases here</p>
          <textarea
            class="textarea"
            placeholder=""
            v-model="phrases"
          ></textarea>
          <div class="m-1">
            <button
              class="button is-primary is-outlined"
              @click="add_phrases()"
            >
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
      <li
        v-for="phrase in $store.state.phrases.slice().reverse()"
        :key="phrase.id"
        class=""
      >
        <div class="columns">
          <div class="column is-one-third is-offset-one-third">
            <div class="card m-2 p-3">
              <div class="columns">
                <div class="column has-text-black">
                  {{ phrase.phrase_text }}
                </div>
                <button
                  class="button is-danger is-outlined m-2 js-modal-trigger"
                  data-target="modal-confirm-delete"
                  @click="set_delete_id(phrase.id)"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </li>
    </ul>
    <div id="modal-confirm-delete" class="modal">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirm deltion</p>
          <button class="delete" aria-label="close"></button>
        </header>
        <section class="modal-card-body">
          Are you sure you want to delete this phrase?
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="confirm_delete">I am sure delete it!</button>
          <button class="button">No way!</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

import axios from "axios";

import { toast } from "bulma-toast";

export default {
  data: function () {
    return {
      delete_id: -1,
    };
  },
  methods: {
    confirm_delete() {
      let csrftoken = getCookie("csrftoken");
      axios
        .post(
          `/delete_phrase`,
          { id: this.delete_id },
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then(() => {
          this.$store.dispatch("getPhrases");
          toast({
            message: "Sentences deleted!",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 3000,
            position: "top-right",
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },
    set_delete_id(id) {
      //console.log(id);
      this.delete_id = id;

      function openModal($el) {
        $el.classList.add("is-active");
      }

      openModal(document.getElementById("modal-confirm-delete"));
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

      let csrftoken = getCookie("csrftoken");
      axios
        .post(
          "/add_phrases",
          { phrases: list_phrases },
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then((response) => {
          if (response.status === 200) {
            this.$store.dispatch("getPhrases");
            this.phrases = "";
            toast({
              message: "Sentences added!",
              type: "is-success",
              dismissible: true,
              pauseOnHover: true,
              duration: 3000,
              position: "top-right",
            });
          }
        });
    },
  },
  mounted() {
    console.log("Phrases.vue mounted");


    // Functions to open and close a modal
    function openModal($el) {
      $el.classList.add("is-active");
    }

    function closeModal($el) {
      $el.classList.remove("is-active");
    }

    function closeAllModals() {
      (document.querySelectorAll(".modal") || []).forEach(($modal) => {
        closeModal($modal);
      });
    }

    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll(".js-modal-trigger") || []).forEach(
      ($trigger) => {
        const modal = $trigger.dataset.target;
        //console.log("trigger dataset", $trigger.dataset);
        const $target = document.getElementById(modal);
        $trigger.addEventListener("click", () => {
          openModal($target);
        });
      }
    );

    // Add a click event on various child elements to close the parent modal
    (
      document.querySelectorAll(
        ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button"
      ) || []
    ).forEach(($close) => {
      const $target = $close.closest(".modal");

      $close.addEventListener("click", () => {
        closeModal($target);
      });
    });

    // Add a keyboard event to close all modals
    document.addEventListener("keydown", (event) => {
      const e = event || window.event;

      if (e.keyCode === 27) {
        // Escape key
        closeAllModals();
      }
    });
  },
};
</script>

<style>
</style>