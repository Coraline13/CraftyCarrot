<template>
  <div class="auth">
    <div class="container">
      <div class="auth__inner">
        <div class="auth__media">
          <img src="../assets/register.svg">
        </div>
        <div class="auth__auth">
          <h1 class="auth__title">Create an account</h1>
          <p>Fill in your info to proceed</p>
          <form @submit.prevent="register" action="/" autocomplete="new-password" class="form" method='post'
                role="presentation">
            <input class="fake-field" name="email">
            <label>Email</label>
            <input id='email' placeholder="jelly@bot.com" type="text" v-model="email">
            <p v-if="errors.email" class="error">{{ errors.email[0] }}</p>
            <label>Password</label>
            <input autocomplete="off" id='password' placeholder="j3llyfishAREawes0me!" type="password"
                   v-model="password1">
            <p v-if="errors.password1" class="error">{{ errors.password1[0] }}</p>
            <label>Confirm password</label>
            <input autocomplete="off" id='password_confirmation' placeholder="j3llyfishAREawes0me!"
                   type="password"
                   v-model="password2">
            <p v-if="errors.password2" class="error">{{ errors.password2[0] }}</p>
            <input type="checkbox" id="check"/>
            <label for="check">I agree with the <b>Terms and conditions</b>.</label>
            <br><br>
            <button class="button button__accent" type='submit'>Register</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: "Register",
        data() {
            return {
                email: "",
                password1: "",
                password2: "",
                errors: {
                    email: "",
                    password1: "",
                    password2: ""
                }
            }
        },
        methods: {
            register: function (e) {
                let data = {};
                data['email'] = this.email;
                data['password'] = this.password1;

                if (this.password1 !== this.password2) {
                    this.errors['password2'] = ["The passwords don't match!"];
                    e.preventDefault();
                }

                this.$store.dispatch('register', data)
                    .then(() => this.$router.push('/'))
                    .catch(err => {
                        console.log(err);
                        this.errors['email'] = err.response.data.email;
                        this.errors['password1'] = err.response.data.password;
                        e.preventDefault();
                        console.log(this.errors);
                    })
            }
        }
    }
</script>

<style scoped>

</style>
