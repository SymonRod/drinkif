import { defineStore } from 'pinia'
// import api from '~/plugins/api'

import axios from 'axios'

// useStore could be anything like useUser, useCart
// the first argument is a unique id of the store across your application
export const useAuthStore = defineStore('authStore', {
  // state

  state: () => {
    return {
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    }
  },

  // actions
  actions: {

    // login
    async login({ commit }) {

      axios.post('http://127.0.0.1:8000/api/login', { username:"rod", password:"Ciao1234!" }).then(response => {
        api.get('http://127.0.0.1:8000/api/get_user_info').then(response => {
          console.log(response);

        })
      })


    },

    getToken() {
      console.log('getToken')

      this.isLoading = true
      this.error = null

      // make a request to the server
      // the server will return a token
      // the token will be saved in the state

      axios.get('http://127.0.0.1:8000/api/csrf').then(response => {
        console.log(response);
        let cookieHeaders = response.headers;
        console.log(cookieHeaders);
      });
    },
  },

  // getters
})
