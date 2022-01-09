<template>
  <div>
    <Navbar></Navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import { useI18n } from 'vue-i18n'

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
    this.$store.commit('updateUser',window.user);
    this.$store.dispatch('getPhrases');
    console.log("Local storage locle",JSON.parse(localStorage.getItem('locale')));
    this.$i18n.locale = this.$store.state.locale;
  },
  watch: {
    '$i18n.locale': {
      handler(newLocale) {
        this.$store.commit('updateLocale', newLocale);
        console.log(newLocale);
      },
      immediate: false
    }
  },
}
</script>


<style lang="scss">

</style>
