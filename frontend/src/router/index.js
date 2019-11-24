import Vue from 'vue'
import Router from 'vue-router'
import store from '../store/store.js'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Cart from '@/components/cart'
import Account from "@/components/Account"
import Profile from '@/components/Profile'
import Store from "../components/Store";
import AddProduct from "../components/AddProduct";
import ProductDetails from "../components/ProductDetails";
import Orders from "../components/Orders";

Vue.use(Router);

const scrollBehavior = (to, from, savedPosition) => {
  return { x: 0, y: 0 };
};

let router = new Router({
  mode: 'history',
  scrollBehavior,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/store',
      name: 'Store',
      component: Store
    },
    {
      path: '/addproduct',
      name: 'AddProduct',
      component: AddProduct,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/productdetails/:id',
      name: 'productdetails',
      component: ProductDetails,
      meta: {
        requiresAuth: true
      }
    },
    // {
    //   path: '/editproduct/:id',
    //   name: 'editproduct',
    //   component: EditProduct,
    //   meta: {
    //     requiresAuth: true
    //   }
    // },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/orders',
      name: 'Orders',
      component: Orders,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/account',
      name: 'account',
      component: Account,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: {
        requiresAuth: true
      }
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next();
      return
    }
    next('/login')
  } else {
    next()
  }
});

export default router
