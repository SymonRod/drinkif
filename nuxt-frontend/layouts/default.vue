<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/store/authStore'

const authStore = useAuthStore()
const drawer = ref(false)

onMounted(() => {
  authStore.getToken()
})

</script>

<template>
  <!-- App.vue -->

  <v-app>
    <NavBar></NavBar>
    <v-main>
      <v-container>
        <slot />
      </v-container>
    </v-main>
  </v-app>
</template>
