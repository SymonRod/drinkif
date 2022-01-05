<template>
  <section class="hero is-fullheight">
    <div class="container">
      <div>
        <p class="title">DrinkIf</p>

        <figure alt="Drunk"  class="image is-128x128 is-inline-block">
            <img src="@/assets/drunk.png" alt="">
        </figure>

        <div class="counter">
          {{ $store.state.counter }}
        </div>
        <!-- <div class="range">
          <input type="text" v-model="min" name="min" id="min" />
          <input type="text" v-model="max" name="max" id="max" />
        </div> -->
        
        </div>
        <div class="buttons">
          <label for="doNotRepeat">
            <input type="checkbox" v-model="doNotRepeat" id="doNotRepeat" />
            Do not repeat
          </label>
          <button @click="$store.dispatch('randomCounter')">Random</button>
        </div>
        <div class="info" v-if="doNotRepeat">
          There are still available {{ $store.state.available.length }} numbers
        </div>
      </div>
  </section>

</template>

<script>
export default {
  name: "Home",
  props: {},
  computed: {
    doNotRepeat: {
      get() {
        return this.$store.state.doNotRepeat;
      },
      set(value) {
        this.$store.commit("updateDoNotRepeat", value);
      },
    },
    min: {
      get() {
        return this.$store.state.min;
      },
      set(value) {
        this.$store.commit("updateMin", value);
      },
    },
    max: {
      get() {
        return this.$store.state.max;
      },
      set(value) {
        this.$store.commit("updateMax", value);
      },
    },
  },
};
</script>

<style scoped>
.title {
    color: white;
}

</style>
