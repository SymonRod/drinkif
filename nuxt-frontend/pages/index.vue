<script setup>
import { ref, computed } from 'vue'
import { useStore } from '../store'

const store = useStore()


</script>

<template>
  <v-container>
    <v-btn class="bg-primary" @click="store.counter++">{{ store.counter }}</v-btn>
  </v-container>
</template>
