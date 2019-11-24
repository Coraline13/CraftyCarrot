<template>
  <div>
    <div class="page__header">
      <div class="hero__overlay hero__overlay--gradient"></div>
      <div class="hero__mask"></div>
      <div class="page__header__inner">
        <div class="container">
          <div class="page__header__content">
            <div class="page__header__content__inner" id='navConverter'>
              <h1 class="page__header__title">Product details</h1>
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
              <li v-if="product && product.seller.isSelf">
                <router-link to="/addproduct">⬅ Products</router-link>
              </li>
              <li v-else>
                <router-link to="/store">⬅ Store</router-link>
              </li>
            </ul>
          </div>
          <div class="app__main">
            <div class="text-container" v-if="product">
              <div class="product-title-detail">
                {{ product.title }}
              </div>
              <hr><br>
              <b>Category:</b> {{ product.categoryName }}
              <br>
              <b>Description:</b> {{ product.description }}
              <br>
              <b>Quantity:</b> {{ product.quantity }}
              <br><br>
              <div class="price-detail">
                {{ product.unitPrice }} RON / {{ product.unit }}
              </div>
              <br>
              <!--                    <router-link class="button button__primary" :to="`/editproduct/${product.id}`">Edit</router-link>-->
              <button v-if="product.seller.isSelf" class="button button__delete"
                      @click="deleteProduct(product.id, index)">Delete
              </button>
              <button v-else class="button button__delete" @click="addToCart(product.id)">Add to cart</button>
            </div>
          </div>
          <br>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'ProductDetails',
        data() {
            return {
                product: null
            }
        },
        mounted() {
            this.getProduct();
        },
        methods: {
            getProduct() {
                let id = this.$route.params.id;

                axios({
                    method: 'get',
                    url: '/api/store/products/' + id + '/',
                }).then(resp => {
                    this.product = resp.data;
                });
            },
            deleteProduct: function (id) {
                let r = "";
                if (this.product.seller.isSelf)
                    r = "/addproduct";
                else
                    r = "/store";

                axios.delete('/api/store/products/' + id + '/')
                    .then(resp => this.$router.push(r))
                    .catch((error) => {
                        console.log(error);
                    });
            },
            addToCart(id) {
                axios({
                    method: 'post',
                    url: '/api/orders/cart/',
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
