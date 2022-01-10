<template>
  <div class="columns">
    <div id="login-view" class="column is-half is-offset-one-quarter">
      <div class="card m-6 p-4">
        <h1 class="has-text-black title">{{$t('login.title')}}</h1>
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" type="username" placeholder="username" v-model="username"/>
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
              <i class="fas fa-check"></i>
            </span>
          </p>
        </div>
        <div class="field">
          <p class="control has-icons-left">
            <input class="input" type="password" placeholder="Password" v-model="password"/>
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
          </p>
        </div>
        <div>
        <button @click="login()" id="login-button" class="button">{{$t('login.button')}}</button>  
        <div class="button ml-2"><router-link to="/register">{{$t('login.create-account')}}</router-link></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export default {
  data() {
    return { username: "", password: "" };
  },
  methods: {
    login() {
      let csrftoken = getCookie('csrftoken');
      axios.post('/login',{username: this.username, password: this.password},{headers:{"X-CSRFToken":csrftoken}}).then(response => {
          if(response.status === 200){
              this.$store.dispatch('getUser');
              this.$router.push('/');
          }
      })
    },
  },
};
</script>

<style>
form input {
  display: block;
}
</style>