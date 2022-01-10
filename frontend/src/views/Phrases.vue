<template>
  <div>
    <div class="columns">
      <div id="phrases-view" class="column is-half is-offset-one-quarter">
        <div class="card m-auto p-4">
          <h1 class="has-text-black title">{{ $t("add-sentences") }}</h1>
          <p class="has-text-black">{{ $t("add-sentences-here") }}</p>
          <textarea
            class="textarea"
            placeholder=""
            v-model="phrases"
          ></textarea>
          <div class="m-1">
            <button class="button is-primary is-outlined" @click="add_phrases">
              {{ $t("add-phrases") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="title has-text-white m-3 has-text-centered">
      {{ $t("your-sentences") }}
    </div>

    <div class="container">
      <div class="columns is-centered is-mobile">
        <div class="column auto has-text-centered">
          <button class="button" @click="firstPage" :disabled="search != ''">
            {{ $t("paginator.first") }}
          </button>
          <button class="button" @click="previousPage" :disabled="search != ''">
            {{ $t("paginator.previous") }}
          </button>
          <span class="has-text-white m-2 subtitle">
            {{ currentPage }}
          </span>
          <button class="button" @click="nextPage" :disabled="search != ''">
            {{ $t("paginator.next") }}
          </button>
          <button class="button" @click="lastPage" :disabled="search != ''">
            {{ $t("paginator.last") }}
          </button>
        </div>
      </div>
    </div>
    <div lass="columns is-centered">
      <div
        class="column auto has-text-centered is-one-third is-offset-one-third"
      >
        <input
          type="text"
          name=""
          id=""
          :placeholder="$t('paginator.search')"
          class="input"
          v-model="search"
        />
      </div>
    </div>

    <div v-for="phrase in page" :key="phrase.id" class="">
      <div class="columns">
        <div class="column is-one-third is-offset-one-third">
          <div class="card m-2 p-3">
            <div class="has-text-black columns is-flex is-vcentered m-0">
              <strong> UUID </strong> #{{ phrase.id }}
              <span
                class="material-icons has-text-primary"
                @click="share(phrase.id)"
                style="position: absolute; right: 10px; top: 5px;"
                >share</span
              >
            </div>
            <div class="columns">
              <div class="column has-text-black">
                {{ phrase.phrase_text }}
              </div>
            </div>
            <div>
              <button
                class="button is-danger is-outlined m-2 js-modal-trigger"
                data-target="modal-confirm-delete"
                @click="set_delete_id(phrase.id)"
              >
                <span class="material-icons">delete</span>
              </button>
              <button
                class="button is-primary is-outlined m-2 js-modal-trigger"
                @click="set_edit_id(phrase.id)"
              >
                <span class="material-icons" data-target="modal-edit"
                  >edit</span
                >
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="modal-edit" class="modal">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ $t("modal-edit.title") }}</p>
          <button class="delete" aria-label="close"></button>
        </header>
        <section class="modal-card-body">
          <textarea
            name=""
            id=""
            cols="30"
            rows="3"
            v-model="edit_text"
            class="textarea"
          />
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="confirm_save">
            {{ $t("modal-edit.save") }}
          </button>
          <button class="button">
            {{ $t("modal-edit.cancel") }}
          </button>
        </footer>
      </div>
    </div>

    <div id="modal-confirm-delete" class="modal">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ $t("confirm-deletion") }}</p>
          <button class="delete" aria-label="close"></button>
        </header>
        <section class="modal-card-body">
          {{ $t("confirm-deletion-text") }}
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="confirm_delete">
            {{ $t("confirm-deletion-button-agree") }}
          </button>
          <button class="button">
            {{ $t("confirm-deletion-button-deny") }}
          </button>
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
      edit_id: -1,
      edit_text: "",
      itemPerPage: 5,
      currentPage:
        localStorage.getItem("currentPage") == null
          ? 1
          : localStorage.getItem("currentPage"),
      search: "",
      phrases: "",
    };
  },
  computed: {
    page: {
      get() {
        let page = [];
        if (this.search != "") {
          page = this.$store.state.phrases.filter((phrase) => {
            let sentence = phrase.phrase_text.toLowerCase();
            let search = this.search.toLowerCase();

            return sentence.includes(search);
          });
        } else {
          page = this.$store.state.phrases.slice(
            (this.currentPage - 1) * this.itemPerPage,
            this.currentPage * this.itemPerPage
          );
        }

        return page;
      },
    },
  },
  methods: {
    firstPage() {
      this.currentPage = 1;
    },

    lastPage() {
      this.currentPage = Math.ceil(
        this.$store.state.phrases.length / this.itemPerPage
      );
    },

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },

    nextPage() {
      if (
        this.currentPage <
        this.$store.state.phrases.length / this.itemPerPage
      ) {
        this.currentPage++;
      }
    },

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
            message: this.$t("sentence-deleted"),
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

    set_edit_id(id) {
      //console.log(id);
      this.edit_id = id;

      this.edit_text = this.$store.state.phrases.find(
        (phrase) => phrase.id == id
      ).phrase_text;

      function openModal($el) {
        $el.classList.add("is-active");
      }

      openModal(document.getElementById("modal-edit"));
    },

    confirm_save() {
      let csrftoken = getCookie("csrftoken");
      axios
        .post(
          `/edit_phrase`,
          {
            id: this.edit_id,
            text: this.edit_text,
          },
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then(() => {
          this.$store.dispatch("getPhrases");
          toast({
            message: this.$t("sentence-edited"),
            type: "is-success",
            pauseOnHover: true,
            duration: 3000,
            position: "top-right",
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },

    add_phrases() {
      console.log("add_phrases");
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
    share(id) {
      var getUrl = window.location;
      var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
      navigator.share({
        title: 'DrinkIf',
        text: this.$t('share-text'),
        url: baseUrl + '#/share/' + id,
      })
    }
  },

  mounted() {
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
        console.log("trigger dataset", $trigger.dataset);
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

  watch: {
    currentPage: function (newPage) {
      localStorage.setItem("currentPage", newPage);
    },
  },
};
</script>

<style></style>
