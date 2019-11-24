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
            </ul>
          </div>
          <div class="app__main">
            <div class="text-container">
              <h3 class="app__main__title">Username</h3>
<!--              <p>{{ user.username }}</p>-->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "account"
  }
</script>

<style scoped>

</style>
