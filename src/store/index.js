import { createStore } from 'vuex'

// import axios from 'axios'

export default createStore({
  state: {
    doNotRepeat: false,
    counter: null,
    history: [],
    available: [],
    min: 0,
    max: 100,
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
        this.commit("updateDoNotRepeat", state.doNotRepeat);
      }
      this.commit("setCounter",null);
    },
    updateMin(state, payload) {
      let min = parseInt(payload);
      if (!isNaN(min)) {
        state.min = min
        this.commit("updateDoNotRepeat", state.doNotRepeat);
      }
      this.commit("setCounter", null);
    },
    updateDoNotRepeat(state, payload) {
      state.doNotRepeat = payload;
      if (state.doNotRepeat) {
        state.available = [];
        let max = state.max;
        let min = state.min;

        for(let i = min; i <=max;i++) {

          state.available.push(i);
        }
      }
    }
  },

  actions: {
    randomCounter( { commit } ) {
      commit('randomCounter');
    }
  },
  modules: {
  },
})
