<script setup>
import { ref, computed } from 'vue'

const counter = ref(0)

function increment() {
  counter.value++
}

</script>

<template>
  <v-container>
    <v-btn class="bg-primary" @click="increment">{{ counter }}</v-btn>
  </v-container>
</template>

<script></script>
