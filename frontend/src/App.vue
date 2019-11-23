<template>
  <div>
    <div class="navbar">
      <nav class="nav__mobile"></nav>
      <div class="container">
        <div class="navbar__inner">
          <a href="#" class="navbar__logo">
            <router-link to="/"><img class="nav-logo" src="./assets/logo.svg"/></router-link>
          </a>
          <nav class="navbar__menu">
            <ul>
              <li v-if="!isLoggedIn">
                <router-link to="/login">Login</router-link>
              </li>
              <li v-if="!isLoggedIn">
                <router-link to="/register">Register</router-link>
              </li>
              <li v-if="isLoggedIn">
                <router-link to="/account">Account</router-link>
              </li>
              <li v-if="isLoggedIn">
                <router-link to="/cart">Cart</router-link>
              </li>
              <li v-if="isLoggedIn">
                <a style="cursor: pointer;" @click="logout">Logout</a>
              </li>
            </ul>
          </nav>
          <!--          TODO: pe mobile nu merge logout-->
          <div class="navbar__menu-mob"><a href="" id='toggle'>
            <svg role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
              <path fill="currentColor"
                    d="M16 132h416c8.837 0 16-7.163 16-16V76c0-8.837-7.163-16-16-16H16C7.163 60 0 67.163 0 76v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16z"
                    class=""></path>
            </svg>
          </a></div>
        </div>
      </div>
    </div>
    <router-view/>
  </div>
</template>

<script>
  import './responsive.js'

  export default {
    computed: {
      isLoggedIn: function () {
        return this.$store.getters.isLoggedIn
      }
    },
    methods: {
      logout: function () {
        this.$store.dispatch('logout')
          .then(() => {
            this.$router.push('/login')
          })
      }
    },
    // TODO: unde tre sa stea created??
    created: function () {
      this.$http.interceptors.response.use(undefined, function (err) {
        return new Promise(function (resolve, reject) {
          if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
            this.$store.dispatch('logout')
          }
          throw err;
        });
      });
    }
  }
</script>

<style>
  @import "style.css";
</style>
