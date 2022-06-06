<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/authStore'

const authStore = useAuthStore()

var drawer = ref(false)
</script>

<template>
  <v-app-bar>
    <v-app-bar-nav-icon @click="drawer = !drawer" />
    <v-btn v-for="route in $router.getRoutes()" :key="route.name" :to="route.path">
      {{ route.name }}
    </v-btn>
    <v-spacer />
      <v-btn @click="authStore.login" color="primary">Login</v-btn>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer">
    <v-list>
      <v-list-item v-for="route in $router.getRoutes()" :key="route.name" :to="route.path">
        <v-list-item-title >{{route.name}}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
