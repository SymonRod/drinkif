<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <div class="counter">
    {{ $store.state.counter }}
  </div>
  <div class="range">
    <input type="text" v-model="min" name="min" id="min">
    <input type="text" v-model="max" name="max" id="max">
  </div>
  <div class="username">
    <input type="text" v-model="username" name="username" id="username">
  </div>
  <div class="buttons">
    <label for="doNotRepeat">
      <input type="checkbox" v-model="doNotRepeat" id="doNotRepeat">
      Do not repeat 
    </label>
    <button @click="$store.dispatch('randomCounter')">Random</button>
  </div>
  <div class="info" v-if="doNotRepeat">
    There are still available {{$store.state.available.length}} numbers
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
    }
  },
  methods: {
  },
  computed: {
    doNotRepeat: {
      get() { return this.$store.state.doNotRepeat },
      set(value) { this.$store.commit('updateDoNotRepeat', value) }
    },
    min: {
      get() { return this.$store.state.min },
      set(value) { this.$store.commit('updateMin', value) }
    },
    max: {
      get() { return this.$store.state.max },
      set(value) { this.$store.commit('updateMax', value) }
    },
    username: {
      get() { return this.$store.state.username },
      set(value) { this.$store.commit('updateUsername', value) }
    }
  },
}
</script>

<style>
body {
 user-select: none;

}

body img {
 pointer-events: none;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.buttons button  {
  padding: 10px;
  min-width: 50px;
  margin: 10px;
}

.counter {
  font-size: 36px;
  line-height: 50px;
}

.range input {
  margin: 5px;
  padding: 5px;
  width: 30px;
}
</style>
