<template>
  <section class="hero">
    <div class="container">
      <div>
        <div class="has-text-centered m-3">
          <figure alt="Drunk" class="image is-128x128 is-inline-block">
            <img src="@/assets/drunk.png" alt="" />
          </figure>
        </div>
        <div class="title has-text-centered">
          {{ $store.state.current_phrase.phrase_text }}
        </div>

        <!-- <div class="range">
          <input type="text" v-model="min" name="min" id="min" />
          <input type="text" v-model="max" name="max" id="max" />
        </div> -->
      </div>
      <div class="has-text-centered m-3">
        <button
          @click="$store.dispatch('random_phrase')"
          class="button is-primary is-outlined"
        >
          New Phrase
        </button>
      </div>
      <div class="has-text-centered m-3">
        <label for="doNotRepeat" class="has-text-white">
          <input type="checkbox" v-model="doNotRepeat" id="doNotRepeat" />
          Do not repeat
        </label>
      </div>

      <article class="message is-primary" v-if="doNotRepeat">
        <div class="message-body" >
          <p>
          There are still available <strong> {{ $store.state.available.length }} </strong> phrases.
        </p>
        </div>
      </article>
    </div>
  </section>
</template>

<script>
export default {
  name: "Home",
  props: {},
  mounted: function() {
  },
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
