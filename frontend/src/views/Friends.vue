<template>
  <div class="container">
    <h1 class="has-text-white title m-2 has-text-centered">
      {{ this.$t("friends.title") }}
    </h1>

    <div class="columns">
      <div class="column is-one-third">
        <div class="subtitle">
          {{ this.$t("friends.add-friend") }}
        </div>
        <div class="field has-addons">
          <p class="control has-icons-left">
            <input
              class="input"
              type="username"
              placeholder="username"
              v-model="searchFriend"
            />
            <span class="icon is-left has-text-primary">
              <i class="fas fa-user-plus"></i>
            </span>
          </p>
          <div class="control">
            <a
              class="button is-primary"
              id="add-button"
              @click="sendFriendRequest"
            >
              <i class="fas fa-plus"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <div class="subtitle">
          {{ this.$t("friends.requests") }}
        </div>
        <p v-if="friendRequestsReceived.length == 0" class="has-text-white">
          {{ this.$t("friends.no-request-recived") }}
        </p>
        <div class="columns is-multiline">
          <div
            class="column is-one-quarter"
            v-for="request in friendRequestsReceived"
            :key="request.id"
          >
            <div class="card">
              <div class="card-content">
                <div class="media">
                  <div class="media-left">
                    <figure class="image is-48x48">
                      <img
                        :src="request.avatar.url"
                        alt="Placeholder image"
                        class="is-rounded"
                      />
                    </figure>
                  </div>
                  <div class="media-content">
                    <p class="title">{{ request.username }}</p>
                  </div>
                </div>
              </div>
              <footer class="card-footer">
                <span
                  style="cursor: pointer"
                  class="card-footer-item"
                  @click="handle_friendship_request(request.username, true)"
                  ><strong
                    ><span class="material-icons has-text-success"
                      >done</span
                    ></strong
                  ></span
                >
                <span
                  style="cursor: pointer"
                  class="card-footer-item"
                  @click="handle_friendship_request(request.username, false)"
                  ><strong
                    ><span class="material-icons has-text-danger"
                      >close</span
                    ></strong
                  ></span
                >
              </footer>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="has-text-white subtitle">{{ this.$t("friends.friend") }}</div>
    <div class="columns has-text-black is-multiline">
      <div
        class="column is-one-third"
        v-for="friend in this.$store.state.friends"
        :key="friend.id"
      >
        <div class="card has-text-black">
          <div class="card-image">
          </div>
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img
                    :src="friend.avatar.url"
                    alt="Placeholder image"
                    class="is-rounded"
                  />
                </figure>
              </div>
              <div class="media-content">
                <p class="title">{{ friend.username }}</p>
                <div></div>
              </div>
            </div>

            <div class="content">
              <label class="">
                {{ this.$t("friends.avatar-seed") }}
                <input
                  type="text"
                  class="input"
                  disabled
                  :value="friend.avatar.seed"
                />
              </label>
              <p>{{ this.$t("friends.description") }}</p>
              <p>{{ friend.description == "" ? this.$t("profile.no-description") : friend.description }}</p>
              <div>
                <p class="has-text-grey">
                  {{ this.$t("friends.since") }}
                  {{ getHumanDate(friend.creation_date) }}
                </p>
              </div>
            </div>
            <footer class="card-footer">
              <div
                class="card-footer-item has-text-danger"
                style="cursor: pointer"
                @click="confirmRemoveFriend(friend.username)"
              >
                {{ this.$t("friends.remove") }}
                <i class="fas fa-user-slash"></i>
              </div>
            </footer>
          </div>
        </div>
      </div>
    </div>

    <div id="modal-friends-remove" class="modal">
      <div class="modal-background"></div>
      <div class="modal-card  mx-2">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ $t("friends.modal.remove.title") }}</p>
          <button class="delete" aria-label="close"></button>
        </header>
        <section class="modal-card-body">
          {{ $t("friends.modal.remove.text", removeFriendUsername) }}
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="RemoveFriend">
            {{ $t("friends.modal.remove.button-agree") }}
          </button>
          <button class="button">
            {{ $t("friends.modal.remove.button-deny") }}
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

export default {
  data: function () {
    return {
      removeFriendUsername: "",
      searchFriend: "",
      friendRequestsReceived: [],
    };
  },
  methods: {
    getHumanDate(data) {
      //console.log(data);
      var options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      };
      var date = new Date(data);
      return date.toLocaleDateString(navigator.language, options);
    },

    RemoveFriend() {
      var csrftoken = getCookie("csrftoken");

      axios
        .post(
          "/api/remove_friend",
          { username: this.removeFriendUsername },
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then((response) => {
          if (response.status === 200) {
            this.getFriendshipRequests();
            this.$store.dispatch("getUserData");
            toast({
              message: this.$t("friends.friend-removed"),
              type: "is-success",
              duration: 6000,
            });
          }
        })
        .catch((error) => {
          if (error.response.status != 500) {
            let description = error.response.data.description;
            if (description == null) {
              description = "Generic error";
            }
            toast({
              message: this.$t(description),
              type: "is-danger",
              duration: 10000,
            });
          }
        });
    },

    confirmRemoveFriend(username) {
      this.removeFriendUsername = username;
      // Functions to open and close a modal
      function openModal($el) {
        $el.classList.add("is-active");
      }
      openModal(document.getElementById("modal-friends-remove"));
    },

    handle_friendship_request(username, accepted) {
      var csrftoken = getCookie("csrftoken");
      axios
        .post(
          "/api/handle_friendship_requests",
          {
            username: username,
            accepted: accepted,
          },
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then((response) => {
          if (response.status === 200) {
            this.getFriendshipRequests();
            this.$store.dispatch("getUserData");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getFriendshipRequests() {
      var csrftoken = getCookie("csrftoken");
      axios
        .post(
          "/api/get_friendship_requests",
          {},
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then((response) => {
          if (response.status === 200) {
            this.friendRequestsReceived = response.data.requests;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    sendFriendRequest() {
      document.getElementById("add-button").classList.add("is-loading");
      var csrftoken = getCookie("csrftoken");
      axios
        .post(
          "/api/new_friendship_request",
          { username: this.searchFriend },
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then((response) => {
          if (response.status === 200) {
            toast({
              message: this.$t("friends.request-sent"),
              type: "is-success",
              duration: 6000,
            });
          }
          document.getElementById("add-button").classList.remove("is-loading");
        })
        .catch((error) => {
          if (error.response.status != 500) {
            let description = error.response.data.description;
            if (description == null) {
              description = "Generic error";
            }
            toast({
              message: this.$t(description),
              type: "is-danger",
              duration: 10000,
            });
          }
          document.getElementById("add-button").classList.remove("is-loading");
        });
    },
  },
  mounted() {
    this.$store.dispatch("getUserData");
    this.getFriendshipRequests();

    function closeModal($el) {
      $el.classList.remove("is-active");
    }

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
  },
};
</script>
