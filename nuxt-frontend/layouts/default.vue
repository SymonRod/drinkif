<script setup>
import { ref } from 'vue'
import { useAuthStore } from '~/store/authStore'

const store = useAuthStore()
const drawer = ref(false)

</script>

<template>
  <!-- App.vue -->

  <v-app>
    <nav-bar></nav-bar>
    <v-main>
      <v-container>
        <slot />
      </v-container>
    </v-main>
  </v-app>
</template>
