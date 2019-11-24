<template>
  <div>
    <div class="page__header">
      <div class="hero__overlay hero__overlay--gradient"></div>
      <div class="hero__mask"></div>
      <div class="page__header__inner">
        <div class="container">
          <div class="page__header__content">
            <div class="page__header__content__inner" id='navConverter'>
              <h1 class="page__header__title">Order history</h1>
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
                <router-link to="/cart">Cart</router-link>
              </li>
              <li>
                <router-link class="vMenu--active" to="/orders">Orders</router-link>
              </li>
            </ul>
          </div>
          <div class="app__main">
            <div class="text-container">
              <div v-if="!orders || !orders.length">
                <p>You have no order history!</p>
              </div>
              <div v-else>
                <div v-for="(order, index) in orders">
                  <div class="product-card">
                    <div class="product-title">
                      Order no. {{ index + 1}}
                    </div>
                    <br>
                    <b>Buyer: </b>{{ order.buyer.firstName }} {{ order.buyer.lastName }}
                    <br>
                    <b>Seller: </b>{{ order.seller.firstName }} {{ order.seller.lastName }}
                    <br>
                    <b>Items: </b>
                      <ul>
                        <li v-for="item in order.items">{{ item.product }}, {{ item.quantity }} {{ item.unit }}</li>
                      </ul>
                    <hr>
                    Total price: {{ order.totalPrice }} RON
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
        name: 'Orders',
        data() {
            return {
                orders: [],
                total: 0
            }
        },
        mounted() {
            this.getOrders();
        },
        methods: {
            getOrders() {
                axios({
                    method: 'get',
                    url: 'api/orders/history/'
                }).then(resp => {
                    this.orders = resp.data;

                    let i;
                    this.total = 0;
                    for (i = 0; i < this.orders.length; i++) {
                        console.log("plm")
                        this.total += parseFloat(this.orders[i].totalPrice);
                        console.log("total" + total);
                    }
                });
            },
        }
    }
</script>

<style scoped>

</style>
