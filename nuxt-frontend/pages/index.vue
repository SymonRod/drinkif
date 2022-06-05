<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '~/store/authStore'

const counter = ref(0)

function increment() {
  counter.value++
}

const authStore = useAuthStore()

const login = () => {
  authStore.login('rod', 'Ciao1234!')
}
</script>

<template>
  <v-container>
    <v-btn class="bg-primary" @click="authStore.login">{{ counter }}</v-btn>
  </v-container>
</template>

<script></script>
