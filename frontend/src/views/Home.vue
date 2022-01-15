<template>
  <section class="hero">
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
      <div class="has-text-centered" v-if="$store.state.user != null && isStarted">
        <span class="has-text-white is-size-3 has-text-weight-bold">{{
          $store.state.current_phrase.phrase_text
        }}</span>
        <!-- <span
          class="is-size-5 has-text-grey"
          v-if="$store.state.current_phrase != null"
        >
          by
          <span class="has-text-weight-bold">{{
            $store.state.current_phrase.creator
          }}</span></span
        > -->
      </div>
    </div>
    <div v-if="$store.state.user != null">
      <div class="has-text-centered m-3">
        <button @click="startGame" class="button is-primary" v-if="!isStarted">
          {{ $t("start-game") }}
        </button>
        <button @click="extractSentece" class="button is-primary is-outlined" v-else>
          {{ $t("new-sentence") }}
        </button>
      </div>
      <div class="columns" v-if="$store.state.friends.length > 0 && !isStarted">
        <div class="column is-4 is-offset-4">
          <div class="card has-text-black">
            <p class="is-size-5 p-2 has-text-black has-text-weight-bold">
              {{ $t("home.include-friends-sentences") }}
            </p>
            <label
              v-for="friend in $store.state.friends"
              :key="friend.id"
              :for="'check-sentences-' + friend.username"
              class="checkbox column"
            >
              <input
                type="checkbox"
                name=""
                :id="'check-sentences-' + friend.username"
                v-model="includeFriends[friend.username]"
              />
              {{ friend.username }}
            </label>
          </div>
        </div>
      </div>
      <div class="has-text-centered m-3" v-if="isStarted">
        <!-- <label for="doNotRepeat" class="has-text-white">
          <input type="checkbox" v-model="doNotRepeat" id="doNotRepeat" />
          {{ $t("do-not-repeat") }}
        </label> -->
        <label for="enableTTS" class="has-text-white ml-5">
          <input type="checkbox" v-model="enableTTS" id="enableTTS" />
          {{ $t("home.enable-tts") }}
        </label>
      </div>
      <div class="columns" v-if="isStarted">
        <div class="column is-4 is-offset-4">
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
        </div>
      </div>
      <div class="columns" v-if="isStarted">
        <div class="column is-4 is-offset-4 has-text-centered has-text-white ">
            <div class="button is-danger" @click="stopGame">
              
               <span class="icon is-small">
              <i class="fas fa-hand-paper"></i>
            </span>
            <span>{{$t('stop-game')}}</span>
            </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { toast } from "bulma-toast";
import axios from 'axios';

export default {
  name: "Home",
  data() {
    return {
      isStarted: JSON.parse(localStorage.getItem("isStarted")) == null ? false : JSON.parse(localStorage.getItem("isStarted")),
      includeFriends: {},
      friendsSentences: {},
      enableTTS: false,
      audio: new Audio(),
    };
  },

  methods: {
    startGame: function() {
      this.isStarted = true;
      localStorage.setItem("isStarted", true);
      this.$store.dispatch("doNotRepeat", {
          doNotRepeat: true,
          includeFriends: this.includeFriends,
        });
    },

    stopGame: function() {
      this.isStarted = false;
      localStorage.setItem("isStarted", false);
      this.$store.dispatch("doNotRepeat", {
          doNotRepeat: false,
          includeFriends: this.includeFriends,
        });
    },

    extractSentece: function () {
      this.$store.dispatch("random_phrase");
      if (this.sentences.length == 0) {
        toast({
          message: this.$t("no-sentences-available"),
          type: "is-warning",
          position: "top-right",
          duration: 12000,
          dismissible: true,
        });
      } else {
        if (this.$store.state.doNotRepeat) {
          if (this.$store.state.available.length <= 0) return;
          let min = Math.ceil(0);
          let max = Math.floor(this.$store.state.available.length - 1);
          let newNumber = Math.floor(Math.random() * (max - min + 1) + min);
          let index = this.$store.state.available.indexOf(
            this.$store.state.available.at(newNumber)
          );
           this.$store.commit("set_phrase", this.$store.state.available.at(newNumber));
          if (index > -1) {
            this.$store.state.available.splice(index, 1);
          }
          localStorage.setItem(
            "available",
            JSON.stringify(this.$store.state.available)
          );
        } else {
          let min = Math.ceil(0);
          let max = Math.floor(this.sentences.length - 1);

          let newNumber = Math.floor(Math.random() * (max - min + 1) + min);
          this.$store.commit("set_phrase", this.sentences.at(newNumber));
        }

        
        if(this.enableTTS) {
          axios.get('/gtts?sentence='+encodeURIComponent(this.$store.state.current_phrase.phrase_text)).then(response => {
            this.audio.pause();
            this.audio.currentTime = 0;
            this.audio.src = response.data.url;
            this.audio.play();
          }).catch((error) => {
            console.log(error);
            toast({
              message: this.$t("tts-error"),
              type: "is-warning",
              position: "top-right",
              duration: 12000,
              dismissible: true,
            });
          });
        }
      }

    },
  },
  mounted: function () {},
  computed: {
    sentences() {
      return this.$store.state.phrases.filter((phrase) => {
        if (phrase.creator == this.$store.state.user.username) {
          return true;
        }
        if (this.includeFriends[phrase.creator]) {
          return true;
        }
      });
    },
    doNotRepeat: {
      get() {
        return this.$store.state.doNotRepeat;
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
