import { createStore } from 'vuex'

// import axios from 'axios'

export default createStore({
  state: {
    username: JSON.parse(localStorage.getItem('username')),
    doNotRepeat: (JSON.parse(localStorage.getItem('doNotRepeat')) == null ? false : JSON.parse(localStorage.getItem('doNotRepeat'))),
    counter: JSON.parse(localStorage.getItem('counter')),
    history: [],
    available: (JSON.parse(localStorage.getItem('min')) == null ? [] : JSON.parse(localStorage.getItem('available'))),
    min: (JSON.parse(localStorage.getItem('min')) == null ?  0 : JSON.parse(localStorage.getItem('min'))),
    max: (JSON.parse(localStorage.getItem('max')) == null ? 100 :  JSON.parse(localStorage.getItem('max'))),
  },
  mutations: {
    increaseCounter (state) {
      state.counter++
    },
    decreaseCounter(state) {
      state.counter--
    },
    setCounter(state, payload) {
      if (state.counter != null) {
        state.history.push(state.counter)
      } 
      state.counter = payload
      localStorage.setItem('counter', JSON.stringify(state.counter));
    },
    randomCounter(state) {
      if (state.doNotRepeat) {
        if (state.available.length <= 0 ) return
        let min = Math.ceil(0);
        let max = Math.floor(state.available.length-1);
        let newNumber = Math.floor(Math.random() * (max - min + 1) + min);
        let index = state.available.indexOf(state.available.at(newNumber));
        this.commit("setCounter", state.available.at(newNumber));
        if (index > -1) {
          state.available.splice(index, 1);
        }
        localStorage.setItem('available', JSON.stringify(state.available));
      } else {
        let min = Math.ceil(state.min);
        let max = Math.floor(state.max);
        this.commit("setCounter", Math.floor(Math.random() * (max - min + 1) + min)) 
      }
    },
    updateMax(state, payload) {
      let max = parseInt(payload);
      if (!isNaN(max)) {
        state.max = max
        localStorage.setItem('max', JSON.stringify(max));
        this.commit("updateDoNotRepeat", state.doNotRepeat);
      }
      this.commit("setCounter",null);
    },
    updateMin(state, payload) {
      let min = parseInt(payload);
      if (!isNaN(min)) {
        state.min = min
        localStorage.setItem('min', JSON.stringify(min));
        this.commit("updateDoNotRepeat", state.doNotRepeat);
      }
      this.commit("setCounter", null);
    },
    updateDoNotRepeat(state, payload) {
      state.doNotRepeat = payload;
      localStorage.setItem('doNotRepeat', JSON.stringify(payload));
      if (state.doNotRepeat) {
        state.available = [];
        let max = state.max;
        let min = state.min;
        for(let i = min; i <=max;i++) {
          state.available.push(i);
        }
        localStorage.setItem('available', JSON.stringify(state.available));
      }
    },
    updateUsername(state, payload) {
      if (payload != null) {
        state.username = payload;
        localStorage.setItem('username', JSON.stringify(payload));
      }
    },
  },

  actions: {
    randomCounter( { commit } ) {
      commit('randomCounter');
    }
  },
  modules: {
  },
})
