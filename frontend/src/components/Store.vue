<template>
  <div>
    <div class="page__header">
      <div class="hero__overlay hero__overlay--gradient"></div>
      <div class="hero__mask"></div>
      <div class="page__header__inner">
        <div class="container">
          <div class="page__header__content">
            <div class="page__header__content__inner" id='navConverter'>
              <h1 class="page__header__title">Store</h1>
              <p class="page__header__text">Find the products you want or even sell your own products!</p>
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
                <router-link class="vMenu--active" to="/store">☰ list view</router-link>
              </li>
              <li>
                <router-link to="/store">▦ grid view</router-link>
              </li>
              <li>
                <router-link to="/store">🖈 map view</router-link>
              </li>
              <br>
              <li>
                <router-link to="/addproduct">
                  <button class="button button__delete">Sell product</button>
                </router-link>
              </li>
            </ul>
          </div>
          <div class="app__main">
            <div class="text-container">
              <div v-if="!products || !products.length">
                <p>There are no products to show!</p>
              </div>
              <div v-else>
                <div v-for="product in products">
                  <router-link class="product-card" :to="`/productdetails/${product.id}`">
                    <div class="product-title">
                      {{ product.title }}
                    </div>
                    <div class="price">
                      {{ product.unitPrice }} RON / {{ product.unit }}
                    </div>
                    <br>
                    <button v-if="product.seller.isSelf" class="button button__primary" disabled="true"
                            @click="addToCart(product.id)">Add to cart
                    </button>
                    <button v-else class="button button__delete" @click="addToCart(product.id)">Add to cart</button>
                  </router-link>
                </div>
              </div>
              <br>
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
        name: 'Store',
        data() {
            return {
                products: [],
                view: "list"
            }
        },
        mounted() {
            this.getProducts();
        },
        methods: {
            getProducts() {
                axios({
                    method: 'get',
                    url: 'api/store/products/'
                }).then(resp => {
                    this.products = resp.data;
                });
            },
            addToCart(id) {
                axios({
                    method: 'post',
                    url: 'api/orders/cart/',
                    data: {
                        product: id,
                        quantity: 1
                    }
                }).then(resp => {
                    this.$router.push('/cart')
                }).catch(err => {
                    console.log(err);
                })
            }
        }
    }
</script>

<style scoped>

</style>
