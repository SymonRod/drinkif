<template>
  <div class="container">
    <h1 class="has-text-white title m-2 has-text-centered">
      {{ this.$t("profile.title") }}
    </h1>
    <div class="columns has-text-black">
      <div class="column is-half is-offset-one-quarter">
        <div class="card has-text-black m-3">
          <div class="card-image"></div>
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img
                    :src="this.$store.state.user.avatar.url"
                    alt="Placeholder image"
                    class="is-rounded"
                  />
                </figure>
              </div>
              <div class="media-content">
                <p class="is-size-3 has-text-weight-bold">
                  {{ this.$store.state.user.username }}
                </p>
              </div>
            </div>
            <div class="content">
              <div class="mb-1">
                <label for="avatar-seed" class="field has-addons">
                  {{ this.$t("profile.avatar-seed") }}
                  <input
                    id="avatar-seed"
                    type="text"
                    class="input"
                    disabled
                    :value="this.$store.state.user.avatar.seed"
                  />
                  
                  <div class="control">
                    <a
                      class="button is-primary"
                      id="add-button"
                      @click="newAvatarSeed"
                    >
                      <i class="fas fa-dice-d20"></i>
                    </a>
                  </div>
                </label>
                </div>
                

              <p>{{ this.$t("profile.description") }}</p>
              <p>
                {{
                  this.$store.state.user.description == ""
                    ? this.$t("profile.no-description")
                    : this.$store.state.user.description
                }}
              </p>
              <p class="has-text-grey">
                {{ this.$t("profile.since") }} {{ date_joined }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from 'axios';

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

export default {
  data: function () {
    return {};
  },
  methods: {
    newAvatarSeed: function() {
      var cookie = getCookie("csrftoken");
      Axios.post('/new_seed',{},{
        headers: {
          'X-CSRFToken': cookie
        }
      }).then(() => {
        this.$store.dispatch("getUserData");
      }).catch(error => {
        console.log(error);
      });
    }
  },
  computed: {
    date_joined: function () {
      var options = {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      };
      var date = new Date(this.$store.state.user.creation_date);
      return date.toLocaleDateString(navigator.language, options);
    },
  },
};
</script>
