<template>
  <div>
    <div class="page__header">
      <div class="hero__overlay hero__overlay--gradient"></div>
      <div class="hero__mask"></div>
      <div class="page__header__inner">
        <div class="container">
          <div class="page__header__content">
            <div class="page__header__content__inner" id='navConverter'>
              <h1 class="page__header__title" v-if="profile !== null">Profile</h1>
              <h1 class="page__header__title" v-else>Complete your profile</h1>
              <p class="page__header__text" v-if="profile !== null">Your personal data</p>
              <p class="page__header__text" v-else>Tell us a bit about yourself.</p>
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
                <router-link class="vMenu--active" to="/profile">Profile</router-link>
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
            <div class="text-container" v-if="fetched && !edit">
              <div>
                <img class="profile-img" :src="gravatar()">
              </div>
              <form>
                <div class="text-container">
                  <h3 class="app__main__title">Email</h3>
                  <p>{{ profile.email }}</p>
                </div>
                <div class="double">
                  <div class="half">
                    <h3 class="app__main__title">First name</h3>
                  </div>
                  <div class="half" v-on:click="startEdit">
                    <svg class="edit-img" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
                         xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                         viewBox="0 0 401 401" style="enable-background:new 0 0 401 401;" xml:space="preserve">
                    <path d="M367.1,19.5c-23.9-23.9-62.7-23.9-86.7,0L37.5,262.4c-1.7,1.7-2.9,3.7-3.5,6L2.1,383.7c-1.3,4.7,0,9.8,3.5,13.3
                    	c3.5,3.5,8.5,4.8,13.3,3.5l115.3-32c2.3-0.6,4.3-1.8,6-3.5l242.9-242.9c23.9-23.9,23.9-62.7,0-86.7L367.1,19.5z M67.2,271.3
                    	L266,72.4l64.1,64.1L131.3,335.4L67.2,271.3z M54.4,297l51.2,51.2l-70.9,19.6L54.4,297z M363.8,102.9l-14.4,14.4l-64.1-64.1
                    	l14.4-14.4c13.3-13.3,34.8-13.3,48.1,0l16,16C377.1,68,377.1,89.6,363.8,102.9z"/>
                    </svg>
                  </div>
                </div>
              </form>
              <!--              <img class="edit-img" src="../assets/edit.svg">-->
              <p>{{ profile.firstName }}</p>
              <br>
              <div class="text-container">
                <h3 class="app__main__title">Last name</h3>
                <p>{{ profile.lastName }}</p>
              </div>
              <br>
              <div class="text-container">
                <h3 class="app__main__title">Phone number</h3>
                <p>{{ profile.phone }}</p>
              </div>
              <br>
              <div class="text-container">
                <h3 class="app__main__title">City</h3>
                <p>{{ profile.city }}</p>
              </div>
              <br>
              <div class="text-container">
                <h3 class="app__main__title">Address</h3>
                <p>{{ profile.address }}</p>
              </div>
              <br>
              <div class="text-container">
                <h3 class="app__main__title">Buying as a</h3>
                <p>{{ profile.personType }}</p>
              </div>
              <br>
              <div class="text-container">
                <h3 class="app__main__title">Selling to</h3>
                <p>{{ profile.sellerType }}</p>
              </div>
            </div>
            <div v-else>
              <div>
                <img class="completeprofile-img" src="../assets/completeprofile.svg">
              </div>
              <h3 class="app__main__title">Add your info</h3>
              <form @submit.prevent="createProfile" action="/" class="form" method='post' role="presentation">
                <div class="double">
                  <div class="half">
                    <label for="firstName">First name</label>
                    <input type="text" id="firstName" placeholder="Veg" v-model="profile.firstName">
                    <p v-if="errors.firstName" class="error">{{ errors.firstName[0] }}</p>
                  </div>
                  <div class="half">
                    <label for="lastName">Last name</label>
                    <input type="text" id="lastName" placeholder="McCarrot" v-model="profile.lastName">
                  </div>
                </div>
                <label for='phoneNumber'>Phone number</label>
                <input id='phoneNumber' placeholder="+40 7..." type="text" v-model="profile.phone">
                <label for='city'>City</label>
                <input id='city' placeholder="Manchester" type="text" v-model="profile.city">
                <label for='address'>Address</label>
                <input id='address' placeholder="Marble Street, no. 42" type="text" v-model="profile.address">
                <div class="double">
                  <div class="half">
                    <label for='personType'>Buying as a</label>
                    <select id="personType" v-model="profile.personType">
                      <option value="private">private</option>
                      <option value="company">company</option>
                    </select>
                  </div>
                  <div class="half">
                    <label for='sellerType'>Selling to</label>
                    <select id="sellerType" v-model="profile.sellerType">
                      <option value="private">private</option>
                      <option value="company">company</option>
                    </select>
                  </div>
                </div>
                <p v-if="errors.nonFieldErrors" class="error">{{ errors.nonFieldErrors[0] }}</p>
                <button class="button button__primary">Save</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import axios from 'axios'
    import * as md5 from 'md5'

    export default {
        name: "Profile",
        data() {
            return {
                fetched: false,
                edit: false,
                method: 'post',
                profile: {
                    email: '',
                    firstName: '',
                    lastName: '',
                    phone: '',
                    city: '',
                    address: '',
                    personType: '',
                    sellerType: '',
                },
                errors: {
                    firstName: '',
                    lastName: '',
                    phone: '',
                    city: '',
                    address: '',
                    personType: '',
                    sellerType: '',
                    nonFieldErrors: '',
                }
            };
        },
        created() {
            this.loadProfile();
        },
        methods: {
            gravatar() {
                return `https://www.gravatar.com/avatar/${md5(this.profile.email.toLowerCase())}?s=400`;
            },
            startEdit() {
                this.edit = true;
                this.method = 'patch';
            },
            loadProfile() {
                axios.get('api/store/profile/')
                    .then(response => {
                        Object.assign(this.profile, response.data);
                    })
                    .catch(error => {
                        if (!error.response || error.response.status !== 404) {
                            throw error;
                        }

                        this.edit = true;
                    }).finally(() => this.fetched = true);
            },
            createProfile() {
                let req = {...this.profile};
                delete req.products;
                axios({
                    method: this.method,
                    url: 'api/store/profile/',
                    data: req,
                }).then((resp) => {
                    Object.assign(this.profile, resp.data);
                    this.edit = false;
                }).catch((error) => {
                    console.log(error);
                    if (error.response) {
                        Object.assign(this.errors, error.response.data);
                    }
                });
            },
        }
    }
</script>

<style scoped>

</style>
