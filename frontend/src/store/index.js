import { createStore } from 'vuex'

import axios from 'axios'

export default createStore({
  state: {
    user: null,
    doNotRepeat: (JSON.parse(localStorage.getItem('doNotRepeat')) == null ? false : JSON.parse(localStorage.getItem('doNotRepeat'))),
    current_phrase: (JSON.parse(localStorage.getItem('current_phrase')) == null ? { phrase_text: '', phrase_id: null } : JSON.parse(localStorage.getItem('current_phrase'))),
    history: [],
    available: (JSON.parse(localStorage.getItem('available')) == null ? [] : JSON.parse(localStorage.getItem('available'))),
    min: (JSON.parse(localStorage.getItem('min')) == null ? 0 : JSON.parse(localStorage.getItem('min'))),
    max: (JSON.parse(localStorage.getItem('max')) == null ? 100 : JSON.parse(localStorage.getItem('max'))),
    phrases: [],
    locale: (JSON.parse(localStorage.getItem('locale')) == null ? 'en' : JSON.parse(localStorage.getItem('locale'))),
  },
  mutations: {
    increaseCounter(state) {
      state.current_phrase++
    },
    decreaseCounter(state) {
      state.current_phrase--
    },
    set_phrase(state, payload) {
      if (state.current_phrase != null) {
        state.history.push(state.current_phrase)
      }
      state.current_phrase = payload
      localStorage.setItem('current_phrase', JSON.stringify(state.current_phrase));
    },
    random_phrase(state) {
      if (state.doNotRepeat) {
        if (state.available.length <= 0) return
        let min = Math.ceil(0);
        let max = Math.floor(state.available.length - 1);
        let newNumber = Math.floor(Math.random() * (max - min + 1) + min);
        let index = state.available.indexOf(state.available.at(newNumber));
        this.commit("set_phrase", state.available.at(newNumber));
        if (index > -1) {
          state.available.splice(index, 1);
        }
        localStorage.setItem('available', JSON.stringify(state.available));

      } else {
        let min = Math.ceil(state.min);
        let max = Math.floor(state.max);

        let newNumber = Math.floor(Math.random() * (max - min + 1) + min);
        this.commit("set_phrase", state.phrases.at(newNumber));
      }
    },
    updateMax(state, payload) {
      let max = parseInt(payload);
      if (max != state.max) {
        if (!isNaN(max)) {
          state.max = max
          localStorage.setItem('max', JSON.stringify(max));
          this.commit("updateDoNotRepeat", state.doNotRepeat);
        }
        this.commit("set_phrase", { phrase_text: '', phrase_id: null },);
      }
    },
    updateMin(state, payload) {
      let min = parseInt(payload);
      if (min != state.min) {
        if (!isNaN(min)) {
          state.min = min
          localStorage.setItem('min', JSON.stringify(min));
          this.commit("updateDoNotRepeat", state.doNotRepeat);
        }
        this.commit("set_phrase", { phrase_text: '', phrase_id: null },);
      }
    },
    updateDoNotRepeat(state, payload) {
      state.doNotRepeat = payload;
      localStorage.setItem('doNotRepeat', JSON.stringify(payload));
      if (state.doNotRepeat) {
        state.available = [];
        let max = state.max;
        let min = state.min;
        for (let i = min; i <= max - 1; i++) {
          state.available.push(state.phrases.at(i));
        }
        localStorage.setItem('available', JSON.stringify(state.available));
      }
    },

    updateUser(state, payload) {
      if (payload != null) {
        state.user = payload;
      }
    },

    updatePhrases(state, payload) {
      state.phrases = payload;
    },

    updateLocale(state, payload) {
      state.locale = payload;
      localStorage.setItem('locale', JSON.stringify(payload));
    }

    // End Mutations 
  },

  actions: {
    getPhrases({ commit }) {
      axios.get('/get_phrases')
        .then(response => {
          //console.log(response.data.phrases);
          commit('updatePhrases', response.data.phrases);
          commit('updateMax', response.data.phrases.length);
          commit('updateMin', 0);

        })
        .catch(error => {
          console.log(error)
        })
    },
    random_phrase({ commit }) {
      commit('random_phrase');
    },
    getUser({ commit }) {
      function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
      }
      let csrftoken = getCookie("csrftoken");

      axios
        .post(
          "/get_user_info",
          {},
          { headers: { "X-CSRFToken": csrftoken } }
        )
        .then((response) => {
          if (response.status === 200) {
            let user = {
              username: response.data.username,
            };
            commit("updateUser", user);
          }
        })
      },

  },
  modules: {
  },
})
