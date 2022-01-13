<template>
  <section class="hero">
    <div class="container">
      <div>
        <div class="has-text-centered m-3 title">
          <p
            v-html="
              this.$store.state.user != null ? '' : this.$t('home.need-login')
            "
          ></p>
        </div>
        <div class="has-text-centered m-3">
          <figure alt="Drunk" class="image is-128x128 is-inline-block">
            <img src="@/assets/drunk.png" alt="" />
          </figure>
        </div>
        <div class="has-text-centered" v-if="$store.state.user != null">
          <span class="has-text-white is-size-3 has-text-weight-bold">{{
            $store.state.current_phrase.phrase_text
          }}</span>
          <span class="is-size-5 has-text-grey" v-if="$store.state.current_phrase != null">
            by
            <span class="has-text-weight-bold">{{
              $store.state.current_phrase.creator
            }}</span></span
          >
        </div>
      </div>
      <div v-if="$store.state.user != null">
        <div class="has-text-centered m-3">
          <button @click="extractSentece" class="button is-primary is-outlined">
            {{ $t("new-sentence") }}
          </button>
        </div>
        <div class="has-text-centered">
          <div class="dropdown is-hoverable">
            <div class="dropdown-trigger">
              <button
                class="button"
                aria-haspopup="true"
                aria-controls="dropdown-menu4"
              >
                <span>Hover me</span>
                <span class="icon is-small">
                  <i class="fas fa-angle-down" aria-hidden="true"></i>
                </span>
              </button>
            </div>
            <div class="dropdown-menu has-text-left" id="dropdown-menu4" role="menu">
              <div class="dropdown-content">
                <div
                  v-for="friend in this.$store.state.friends"
                  :key="friend.id"
                >
                  <div class="dropdown-item has-text-black columns">
                    <label
                      :for="'check-sentences-' + friend.username"
                      class="checkbox column"
                    >
                      <input
                        type="checkbox"
                        name=""
                        :id="'check-sentences-' + friend.username"
                      />
                      {{ friend.username }}
                      <hr
                        class="dropdown-divider"
                        v-if="this.$store.state.friends > 1"
                      />
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <article class="message is-primary" v-if="doNotRepeat">
          <div class="message-body">
            <p
              v-html="
                $t('sentence-available', {
                  count: $store.state.available.length,
                })
              "
            ></p>
          </div>
        </article>
        <div class="has-text-centered m-3">
          <label for="doNotRepeat" class="has-text-white">
            <input type="checkbox" v-model="doNotRepeat" id="doNotRepeat" />
            {{ $t("do-not-repeat") }}
          </label>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { toast } from "bulma-toast";

export default {
  name: "Home",
  props: {},
  mounted: function () {},
  methods: {
    extractSentece: function () {
      this.$store.dispatch("random_phrase");

      if (this.state_errors.length > 0) {
        this.state_errors.forEach((error) => {
          toast({
            message: this.$t(error),
            type: "is-warning",
            position: "top-right",
            duration: 12000,
            dismissible: true,
          });
        });

        this.$store.commit("clear_errors");
      }
    },
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
    state_errors: {
      get() {
        return this.$store.state.errors;
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
