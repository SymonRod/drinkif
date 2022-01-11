<template>
  <div class="columns">
    <div id="login-view" class="column is-half is-offset-one-quarter">
      <div class="card m-6 p-4">
        <h1 class="has-text-black title">{{ $t("sign-up.title") }}</h1>
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input
              class="input"
              type="username"
              placeholder="Username"
              v-model="username"
            />
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
              <i class="fas fa-check"></i>
            </span>
          </p>
        </div>
        <div class="field">
          <p class="control has-icons-left has-text-black p-2">
            {{ $t("password-requirements") }}
            <input
              class="input mt-1"
              type="password"
              placeholder="Password"
              v-model="password"
            />
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
          </p>
        </div>
        <div>
          <button @click="register(inputs)" id="register-button" class="button">
            {{ $t("sign-up.button") }}
          </button>
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
  data() {
    return { username: "", password: "" };
  },
  methods: {
    register() {
      let csrftoken = getCookie("csrftoken");
      axios
        .post(
          "/register",
          { username: this.username, password: this.password },
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then((response) => {
          if (response.status === 200) {
            if (response.data.description != null) {
              toast({
                message: response.data.description,
                type: "is-success",
                duration: 10000,
              });
            }
            window.location.href = "/";
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
  },
};
</script>

<style>
form input {
  display: block;
}
</style>
