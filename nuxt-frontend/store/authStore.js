import { defineStore } from 'pinia'
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

      axios.post('login', { username:"rod", password:"Ciao1234!" }).then(response => {
        axios.get('get_user_info').then(response => {
          console.log(response);
        })
      })


    },

    getToken: (state) => {
      console.log('getToken')

      state.isLoading = true
      state.error = null

      // make a request to the server
      // the server will return a token
      // the token will be saved in the state

      axios.get('get_user_info');
    },
  },

  // getters
})
