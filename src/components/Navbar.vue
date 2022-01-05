<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <a class="navbar-item" href="#"> </a>
        <span class="navbar-burger burger" data-target="navbarMenu">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </div>
      <div id="navbarMenu" class="navbar-menu">
        <div class="navbar-end">
          <div class="navbar-item field">
            <p class="control has-icons-right">
              <input
                class="input"
                placeholder="Username"
                type="text"
                v-model="username"
                name="username"
                id="username"
              />
            </p>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
  props: {},
  computed: {
    username: {
      get() {
        return this.$store.state.username;
      },
      set(value) {
        this.$store.commit("updateUsername", value);
      },
    },
  },
};
</script>

<style scoped>
.navbar {
  background-color: rgb(59, 59, 59);
}
</style>
