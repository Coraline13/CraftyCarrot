<template>
  <div>
    <div class="page__header">
      <div class="hero__overlay hero__overlay--gradient"></div>
      <div class="hero__mask"></div>
      <div class="page__header__inner">
        <div class="container">
          <div class="page__header__content">
            <div class="page__header__content__inner" id='navConverter'>
              <h1 class="page__header__title">Overview</h1>
              <p class="page__header__text">Welcome to your account!</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="app">
      <div class="container">
        <div class="app__inner">
          <div class="app__menu">
            <ul class="vMenu">
              <li>
                <router-link class="vMenu--active" to="/account">Overview</router-link>
              </li>
              <li>
                <router-link to="/profile">Profile</router-link>
              </li>
              <li>
                <router-link to="/addproduct">Products</router-link>
              </li>
              <li>
                <router-link to="/cart">Cart</router-link>
              </li>
              <li>
                <router-link to="/orders">Orders</router-link>
              </li>
            </ul>
          </div>
          <div class="app__main">
            <div class="text-container">
              <h3 class="app__main__title">Hi, {{ profile.firstName }}!</h3>
              <p>Here are a few interesting facts about your account:</p>

              <div class="expanded landing__section">
                <div class="container">
                  <div class="expanded__inner">
                    <div class="expanded__media">
                      <img src="../assets/posts.svg" class="expanded__image">
                    </div>
                    <div class="expanded__content">
                      <h2 class="expanded__title">Seller experience</h2>
                      <p class="expanded__text">Since you created your account, you published 7 products in order to
                        sell them.</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="expanded landing__section">
                <div class="container">
                  <div class="expanded__inner">
                    <div class="expanded__media">
                      <img src="../assets/food.svg" class="expanded__image">
                    </div>
                    <div class="expanded__content">
                      <h2 class="expanded__title">Buyer experience</h2>
                      <p class="expanded__text">You managed to improve your life by buying a total of 6 agricultural
                        and handcrafted goods.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "Profile",
        data() {
            return {
                profile: null
            };
        },
        created() {
            this.loadProfile();
        },
        methods: {
            loadProfile() {
                axios.get('api/store/profile/')
                    .then(response => {
                        this.profile = response.data;
                    })
                    .catch(error => {
                        if (!error.response || error.response.status !== 404) {
                            throw error;
                        }
                    });
            },
        }
    }
</script>

<style scoped>

</style>
