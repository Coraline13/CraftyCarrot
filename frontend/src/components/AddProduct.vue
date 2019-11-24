<template>
  <div>
    <div class="page__header">
      <div class="hero__overlay hero__overlay--gradient"></div>
      <div class="hero__mask"></div>
      <div class="page__header__inner">
        <div class="container">
          <div class="page__header__content">
            <div class="page__header__content__inner" id='navConverter'>
              <h1 class="page__header__title">Products you sell</h1>
              <p class="page__header__text">The list of products you posted</p>
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
                <router-link to="/account">Overview</router-link>
              </li>
              <li>
                <router-link to="/profile">Profile</router-link>
              </li>
              <li>
                <router-link class="vMenu--active" to="/chatbots">Products</router-link>
              </li>
              <li>
                <router-link to="/cart">Cart</router-link>
              </li>
            </ul>
          </div>
          <div class="app__main">
            <div class="text-container">
              <h3 class="app__main__title">Add a new product</h3><br>
              <form @submit.prevent="addProduct" action="/" class="form" method='post' role1w="presentation">
                <label for='title'>Title</label>
                <input id='title' placeholder="Fabulous carrots" type="text" v-model="title">
                <label for="categ">Category</label>
                <select id="categ" v-model="categ">
                  <option v-for="c in categories" :value="c">{{ c.name }}</option>
                </select>
                <label for="category">Subcategory</label>
                <select id="category" v-model="category">
                  <option v-for="category in categ.children" :value="category.slug">{{ category.name }}</option>
                </select>
                <label for='description'>Description</label>
                <textarea id='description' placeholder="Marvellous carrots from own garden." type="text"
                          v-model="description"></textarea>
                <label for='quantity'>Quantity</label>
                <input id='quantity' placeholder="3" type="text" v-model="quantity">
                <div class="double">
                  <div class="half">
                    <label for="unitPrice">Unit Price (RON)</label>
                    <input type="text" id="unitPrice" placeholder="6.2 RON" v-model="unitPrice">
                  </div>
                  <div class="half">
                    <label for="unit">Unit</label>
                    <input type="text" id="unit" placeholder="kg" v-model="unit">
                  </div>
                </div>
                <button class="button button__primary" type='submit'>Add product</button>
              </form>

              <h3 class="app__main__title">Your products</h3><br>
              <div v-if="!products || !products.length">
                <p>You do not have any products yet!</p>
              </div>
              <div v-else>
                <div v-for="(product, index) in products">
                  <router-link class="product-card" :to="`/productdetails/${product.id}`">
                    <div class="product-title">
                      {{ product.title }}
                    </div>
<!--                    <div class="categ">-->
<!--                      {{ product.categoryName }}-->
<!--                    </div>-->
<!--                    <br>-->
                    <div class="price">
                      {{ product.unitPrice }} RON / {{ product.unit }}
                    </div>
                    <br>
<!--                    <router-link class="button button__primary" :to="`/editproduct/${product.id}`">Edit</router-link>-->
<!--                    <button class="button button__delete" @click="deleteProduct(product.id, index)">Delete</button>-->
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
        name: 'AddProduct',
        data() {
            return {
                products: [],
                categories: [],
                categ: '',
                title: '',
                category: '',
                description: '',
                quantity: '',
                unitPrice: '',
                unit: ''
            }
        },
        mounted() {
            this.getProducts();
            this.getCategories();
        },
        methods: {
            addProduct() {
                if (this.title) {
                    axios({
                        method: 'post',
                        url: 'api/store/products/',
                        data: {
                            title: this.title,
                            category: this.category,
                            description: this.description,
                            quantity: this.quantity,
                            unitPrice: this.unitPrice,
                            unit: this.unit
                        }
                    }).then((resp) => {
                        console.log(resp);
                        let newProduct = {
                            'id': resp.data.id,
                            'title': resp.data.title,
                            'category': resp.data.category,
                            'description': resp.data.description,
                            'quantity': resp.data.quantity,
                            'unitPrice': resp.data.unitPrice,
                            'unit': resp.data.unit
                        };
                        this.products.push(newProduct);

                        this.title = '';
                        this.category = '';
                        this.description = '';
                        this.quantity = '';
                        this.unitPrice = '';
                        this.unit = '';
                    }).catch((error) => {
                        console.log(error);
                    });
                }
            },
            getCategories() {
                axios({
                    method: 'get',
                    url: 'api/store/categories/?flat=false',
                }).then(resp => {
                    this.categories = resp.data;
                });
            },
            getProducts() {
                axios({
                    method: 'get',
                    url: 'api/store/profile/',
                }).then(resp => {
                    this.products = resp.data.products;
                });
            },
            deleteProduct: function (id, index) {
                axios.delete('api/store/products/' + id + '/')
                    .then(resp => {
                        this.products.splice(index, 1);
                        console.log(this.products);
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },
        }
    }
</script>

<style scoped>

</style>
