<template>
  <div class="auth">
    <div class="container">
      <div class="auth__inner">
        <div class="auth__media">
          <img src="../assets/login.svg">
        </div>
        <div class="auth__auth">
          <h1 class="auth__title">Access your account</h1>
          <p>Fill in your email and password to proceed</p>
          <form @submit.prevent="login" action="/" autocomplete="new-password" class="form" method='post'
                role="presentation">
            <input class="fake-field" name="email">
            <label>Email</label>
            <input id='email' placeholder="jelly@bot.com" type="text" v-model="email">
            <p v-if="errors.email" class="error">{{ errors.email[0] }}</p>
            <label>Password</label>
            <input autocomplete="off" id='password' placeholder="j3llyfishAREawes0me!" type="password"
                   v-model="password">
            <p v-if="errors.password" class="error">{{ errors.password[0] }}</p>
            <button class="button button__accent" type='submit'>Log in</button>
            <a href=""><h6 class="left-align">Forgot your password?</h6></a>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'Login',
        data() {
            return {
                email: '',
                password: '',
                errors: {
                    email: "",
                    password: ""
                }
            }
        },
        methods: {
            login: function () {
                let email = this.email;
                let password = this.password;
                this.$store.dispatch('login', {email, password})
                    .then((res) => this.$router.push('/profile'))
                    .catch(err => {
                        console.log(err);
                        this.errors['email'] = err.response.data.email;
                        this.errors['password'] = err.response.data.password;
                        console.log(this.errors);
                    })
            }
        }
    }
</script>

<style scoped>

</style>
