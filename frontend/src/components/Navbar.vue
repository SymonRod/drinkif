<template>
  <nav class="navbar  has-background-dark">
    <div class="container">
      <div class="navbar-brand">
        <p class="title mt-3 mb-1 ml-2 has-text-primary	">
            <router-link to="/">DrinkIf</router-link>
          </p>
        <a class="navbar-item" href="#"> </a>
        <span class="navbar-burger burger" data-target="navbarMenu">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </div>
      <div id="navbarMenu" class="navbar-menu has-background-dark">
        <div class="navbar-end">
          <div class="navbar-item" v-if="$store.state.user != null">
            <router-link to="/phrases" >Yours phrases</router-link>
          </div>
          <div class="navbar-item">
            <router-link to="/login" v-if="$store.state.user == null">Login</router-link>
            <a href="/logout" v-if="$store.state.user != null">Logout</a>
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
  },
};

document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');

      });
    });
  }

});
</script>

<style scoped>
.navbar {
  background-color: rgb(59, 59, 59);
}
</style>
