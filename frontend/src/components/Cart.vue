<template>
  <div>
    <div class="page__header">
      <div class="hero__overlay hero__overlay--gradient"></div>
      <div class="hero__mask"></div>
      <div class="page__header__inner">
        <div class="container">
          <div class="page__header__content">
            <div class="page__header__content__inner" id='navConverter'>
              <h1 class="page__header__title">Cart</h1>
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
                <router-link to="/addproduct">Products</router-link>
              </li>
              <li>
                <router-link class="vMenu--active" to="/cart">Cart</router-link>
              </li>
              <li>
                <router-link to="/orders">Orders</router-link>
              </li>
            </ul>
          </div>
          <div class="app__main">
            <div class="text-container">
              <div v-if="!cartItems || !cartItems.length">
                <p>There are no products in your cart!</p>
              </div>
              <div v-else>
                <div v-for="(item, index) in cartItems">
                  <div class="product-card">
                    <div class="product-title">
                      {{ item.product.title }}
                    </div>
                    <br>
                    <b>Quantity: </b>{{ item.quantity }} {{ item.product.unit }}
                    <span class="cart-plus" @click="adjustQuantity(item, 1)">+1</span>
                    <span class="cart-minus" @click="adjustQuantity(item, -1)">-1</span>
                    <span class="cart-x" @click="removeItem(item.product.id, index)">X</span>
                    <br>
                    <b>Price: </b>{{ item.product.unitPrice }} RON / {{ item.product.unit }}
                    <hr>
                    {{ parseFloat(item.product.unitPrice) * parseFloat(item.quantity) }} RON
                  </div>
                </div>
                <hr>
                <span class="total">Total: </span><span style="font-size: x-large">{{ total }} RON</span>
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
        name: 'Cart',
        data() {
            return {
                cartItems: [],
                total: 0
            }
        },
        mounted() {
            this.getCartItems();
        },
        methods: {
            getCartItems() {
                axios({
                    method: 'get',
                    url: 'api/orders/cart/'
                }).then(resp => {
                    this.cartItems = resp.data;
                    this.totalCart()
                });
            },
            totalCart() {
                let i;
                this.total = 0;
                for (i = 0; i < this.cartItems.length; i++) {
                    this.total += (parseFloat(this.cartItems[i].product.unitPrice) * parseFloat(this.cartItems[i].quantity));
                }
                console.log("total" + this.total)
            },
            removeItem: function (id, index) {
                axios.delete('/api/orders/cart/' + id + '/')
                    .then(resp => {
                        this.cartItems.splice(index, 1);
                        this.totalCart();
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },
            adjustQuantity(item, delta) {
                const newQuantity = item.quantity + delta;
                if (newQuantity <= 0) {
                    this.removeItem(item.product.id);
                    console.log("item removed");
                    return;
                }
                axios({
                    method: 'post',
                    url: 'api/orders/cart/',
                    data: {
                        product: item.product.id,
                        quantity: newQuantity
                    }
                }).then(resp => {
                    item.quantity = resp.data.quantity;
                    this.totalCart();
                }).catch(err => {
                    console.log(err);
                })
            },
        }
    }
</script>

<style scoped>

</style>
