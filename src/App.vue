<template>
<body>
 <Navbar></Navbar>
 <Home></Home>
</body>
</template>

<script>
import Home from './components/Home.vue'
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  data() {
    },
  components: {
    Navbar,
    Home,
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
@import "https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css";

body {
 user-select: none;
 background-color: #383838;
 color: white;
}

body img {
 pointer-events: none;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
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
