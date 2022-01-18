<template>
  <div>
    <Navbar></Navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Navbar
  },
  mounted() {
    var locale = '';
    
    if (localStorage.getItem('locale') == null) {
      localStorage.setItem('locale',locale);
      console.log('locale local storage null',this.$i18n.locale);
    } else{
      locale = localStorage.getItem('locale')
      console.log('locale local storage',this.$i18n.locale);
    }

    axios.post('/api/csrf').then(() => {
      this.$store.commit('updateUser',window.user);
      this.$store.dispatch('getUserData');
    });
  },
}
</script>


<style lang="scss">

</style>
