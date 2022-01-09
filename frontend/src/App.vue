<template>
  <div>
    <Navbar></Navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    const { t } = useI18n({
      inheritLocale: true,
      useScope: 'local'
    })

    // Something todo ..

    return { t }
  },
  components: {
    Navbar
  },
  mounted() {

    axios.post('csrf').then(() => {
      this.$store.commit('updateUser',window.user);
      this.$store.dispatch('getPhrases');
      this.$i18n.locale = this.$store.state.locale;
      this.$store.dispatch('getUser');
    });
  },
  watch: {
    '$i18n.locale': {
      handler(newLocale) {
        this.$store.commit('updateLocale', newLocale);
      },
      immediate: false
    }
  },
}
</script>


<style lang="scss">

</style>
