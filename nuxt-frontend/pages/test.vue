<script setup>

import { useStore } from '~/store';

const store = useStore();

</script>

<template>
    <v-container>
        <h1>Test</h1>
        <br>
        <v-btn class="bg-primary" @click="store.increment">{{ store.counter }}</v-btn>
        <br>
        <v-btn @click="store.double(store)">Double</v-btn>

    </v-container>
    <v-container>
        <ul>
            <li v-for="n in store.primeList">
                {{ n }}
            </li>
        </ul>
    </v-container>
</template>