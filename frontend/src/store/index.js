import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: (JSON.parse(localStorage.getItem('user')) == null ? null : JSON.parse(localStorage.getItem('user'))),
    friends: [],
    doNotRepeat: (JSON.parse(localStorage.getItem('doNotRepeat')) == null ? false : JSON.parse(localStorage.getItem('doNotRepeat'))),
    current_phrase: (JSON.parse(localStorage.getItem('current_phrase')) == null ? { phrase_text: '', phrase_id: null } : JSON.parse(localStorage.getItem('current_phrase'))),
    history: [],
    available: (JSON.parse(localStorage.getItem('available')) == null ? [] : JSON.parse(localStorage.getItem('available'))),
    min: (JSON.parse(localStorage.getItem('min')) == null ? 0 : JSON.parse(localStorage.getItem('min'))),
    max: (JSON.parse(localStorage.getItem('max')) == null ? 100 : JSON.parse(localStorage.getItem('max'))),
    phrases: (JSON.parse(localStorage.getItem('sentences')) == null ? [] : JSON.parse(localStorage.getItem('sentences'))),
    errors: [],
  },
  mutations: {
    set_phrase(state, payload) {
      state.current_phrase = payload
      localStorage.setItem('current_phrase', JSON.stringify(state.current_phrase));
    },
    random_phrase(state) {
      if (state.phrases.length == 0) {
        //console.log('No phrases available')
        state.errors.push('no-sentences-available');
      } else {
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
      state.doNotRepeat = payload
    },

    updateAvailable(state, payload) {
      state.available = payload
      localStorage.setItem('available', JSON.stringify(state.available));
    },

    clear_errors(state) {
      state.errors = [];
    },

    updateUser(state, payload) {
      state.user = payload;
      localStorage.setItem('user', JSON.stringify(state.user));
    },

    updatePhrases(state, payload) {
      state.phrases = payload;
      localStorage.setItem('sentences', JSON.stringify(state.phrases));
    },
    updateFriends(state, payload) {
      state.friends = payload;
    },

    clearHistory(state) {
      state.history = [];
    },

    addToHistory(state, payload) {
      var data = { phrase_text: payload.phrase_text, id: payload.id, creator:payload.creator};
      //console.log(data)
      state.history.push(data);
    }

    // End Mutations 
  },

  actions: {
    doNotRepeat({commit,state},value) {
      var includeFriends = value.includeFriends
      commit('updateDoNotRepeat', value.doNotRepeat);
      localStorage.setItem('doNotRepeat', JSON.stringify(value));


      if (state.doNotRepeat) {
        var available = state.phrases.filter((phrase) => {
          if(!phrase.public) return false;

          if(phrase.creator == state.user.username) {
            return true;
          }
          //console.log("includeFriends",includeFriends);
          if(includeFriends[phrase.creator]) {
            return true;
          }
        });
        commit('updateAvailable', available);
        localStorage.setItem('available', JSON.stringify(state.available));
      }
    },

    getFriends({commit}) {
      // Get frineds  
      axios.get("/api/get_friends")
        .then((response) => {
          if (response.status === 200) {
            commit('updateFriends', response.data.friends);
          }
        });
    },

    setSentenceVisibility({commit,state},value) {

      var id = value.id;
      var visibility = value.visibility;
      var trigger = value.trigger;

      trigger.classList.add('is-loading');

      function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(";").shift();
      }

      var csrftoken = getCookie('csrftoken');

      axios.post("/api/change_sentence_visibility", 
        {id:id,visibility:visibility},
        {headers: { "X-CSRFToken": csrftoken }}
      )
        .then((response) => {
          trigger.classList.remove('is-loading');
          if (response.status === 200) {
            var senteces = state.phrases;
            senteces.forEach((sentence) => {
              if(sentence.id==id) {
                sentence.public = visibility;
              }
            });
            commit('updatePhrases', senteces);
          }
        });
    },

    getPhrases({ commit }) {
      axios.get('/api/get_phrases')
        .then(response => {
          //console.log(response.data.phrases);
          commit('updatePhrases', response.data.phrases);
          commit('updateMax', response.data.phrases.length);
          commit('updateMin', 0);

        })
        .catch(() => {
          //console.log(error)
        })
    },
    random_phrase({ commit }) {
      commit('random_phrase');
    },
    getUserData({ commit }) {
      // Get user info
      axios.get("/api/get_user_info")
        .then((response) => {
          if (response.status === 200) {
            commit('updateUser', response.data);
            this.dispatch("getPhrases");
            this.dispatch("getFriends");
          }
        }).catch((error) => {
          if(error.response.status == 403) {
            commit('updateUser', null);
          }
        })
    },
  },
  modules: {
  },
})
