<template>
  <div>
    <Navbar></Navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  },
  mounted() {
    this.$store.commit('updateUser',window.user);
    this.$store.dispatch('getPhrases');
  }
}
</script>


<style lang="scss">

</style>
