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
            <label for="category">Filer by category</label>
            <select id="category" v-model="filter.category" v-on:change="getProducts">
              <option value="">----</option>
              <option v-for="category in categories" :value="category">
                {{ category.name }}
              </option>
            </select>
            <label for="city">Filer by seller city</label>
            <select id="city" v-model="filter.city" v-on:change="getProducts">
              <option value="">----</option>
              <option v-for="city in cities" :value="city">
                {{ city }}
              </option>
            </select>
            <label for="sort">Sort by</label>
            <select id="sort" v-model="filter.sort" v-on:change="getProducts">
              <option value="-created">Most recently added</option>
              <option value="created">Least recently added</option>
              <option value="-unit_price">Price (descending)</option>
              <option value="unit_price">Price (ascending)</option>
            </select>
            <!--                <div class="double">-->
            <!--                  <div class="half">-->
            <!--                    <label for="minPrice">Min price</label>-->
            <!--                    <input type="text" id="minPrice" placeholder="50">-->
            <!--                  </div>-->
            <!--                  <div class="half">-->
            <!--                    <label for="maxPrice">Max Price</label>-->
            <!--                    <input type="text" id="maxPrice" placeholder="100">-->
            <!--                  </div>-->
            <!--                </div>-->
            <br><hr><br><br>
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
                categories: [],
                cities: [],
                view: "list",
                filter: {
                    category: null,
                    city: null,
                    sort: null,
                }
            }
        },
        mounted() {
            this.getProducts();
            this.getCategories();
            this.getCities();
        },
        methods: {
            getProducts() {
                let params = {};
                if (this.filter.category) {
                    params.category = this.filter.category.slug;
                }
                if (this.filter.city) {
                    params.city = this.filter.city;
                }
                if (this.filter.sort) {
                    params.sort = this.filter.sort;
                }
                axios({
                    method: 'get',
                    url: 'api/store/products/',
                    params: params,
                }).then(resp => {
                    this.products = resp.data;
                });
            },
            getCategories() {
                axios({
                    method: 'get',
                    url: 'api/store/categories/?flat=true',
                }).then(resp => {
                    this.categories = resp.data;
                });
            },
            getCities() {
                axios({
                    method: 'get',
                    url: 'api/store/cities',
                }).then(resp => {
                    this.cities = resp.data;
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
