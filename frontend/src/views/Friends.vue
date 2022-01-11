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
            <span class="icon material-icons has-text-primary is-left m-2">
              person_add
            </span>
          </p>
          <div class="control">
            <a class="button is-primary" id="add-button">
              <span class="material-icons" @click="sendFriendRequest">
                add_circle_outline
              </span>
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
        <div class="columns">
          <div
            class="column is-one-third"
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
                <span style="cursor:pointer;" class="card-footer-item" @click="handle_friendship_request(request.username,true)"
                  ><strong
                    ><span class="material-icons has-text-success"
                      >done</span
                    ></strong
                  ></span
                >
                <span style="cursor:pointer;" class="card-footer-item" @click="handle_friendship_request(request.username,false)"><strong
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
    <div class="columns has-text-black">
      <div class="column is-one-third">
        <div
          class="card has-text-black"
          v-for="friend in this.$store.state.friends"
          :key="friend.id"
        >
          <div class="card-image">
            <!-- <figure class="image is-4by3">
              <img
                :src="this.$store.state.user.avatar.url"
                alt="Placeholder image"
              />
            </figure> -->
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
                <div>
                  <p class="is-6 has-text-black">
                    {{ this.$t("friends.avatar-seed") }}
                  </p>
                  <input
                    type="text"
                    class="input"
                    disabled
                    :value="friend.avatar.seed"
                  />
                </div>
              </div>
            </div>

            <div class="content">
              <p>{{ this.$t("friends.description") }}</p>
              <p>{{ friend.description }}</p>
              <br />
              <div>
                <p class="has-text-grey">
                  {{ this.$t("friends.since") }}
                  {{ getHumanDate(friend.creation_date) }}
                </p>
              </div>
            </div>
          </div>
        </div>
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
      searchFriend: "",
      friendRequestsReceived: [],
    };
  },
  methods: {
    getHumanDate(data) {
      console.log(data);
      var options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      };
      var date = new Date(data);
      return date.toLocaleDateString(navigator.language, options);
    },
    handle_friendship_request(username, accepted) {
      var csrftoken = getCookie("csrftoken");
      axios
        .post(
          "/handle_friendship_requests",
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
          "/get_friendship_requests",
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
          "/new_friendship_request",
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
    this.getFriendshipRequests();
  },
};
</script>