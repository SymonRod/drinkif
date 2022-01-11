<template>
  <div class="container">
    <h1 class="has-text-white title m-2 has-text-centered">
      {{ this.$t("profile.title") }}
    </h1>
    <div class="columns  has-text-black">
      <div class="column is-half is-offset-one-quarter">
        <div class="card has-text-black">
          <div class="card-image">
            <!-- <figure class="image is-4by3">
              <img
                :src="this.$store.state.user.avatar.url"
                alt="Placeholder image"
              />
            </figure> -->
          </div>
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-48x48">
                  <img
                    :src="this.$store.state.user.avatar.url"
                    alt="Placeholder image"
                    class="is-rounded"
                  />
                </figure>
              </div>
              <div class="media-content ">
                <p class="title">{{this.$store.state.user.username}}</p>
                <div>
                     <p class="is-6 has-text-black">
                         {{this.$t("profile.avatar-seed")}}
                     </p>
                     <input type="text" class="input" disabled :value="this.$store.state.user.avatar.seed"/>
                </div>
              </div>
            </div>

            <div class="content">
                
                <p> {{this.$t("profile.description")}}</p>
                <p> {{this.$store.state.user.description}} </p>
              <br />
              <div >
                  
                <p class="has-text-grey">{{this.$t("profile.since")}} {{date_joined}} </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data: function () {
    return {};
  },
  computed: {
      date_joined: function () {
          var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
          var date = new Date(this.$store.state.user.creation_date);
          return date.toLocaleDateString(navigator.language, options);
      },
  }
};
</script>