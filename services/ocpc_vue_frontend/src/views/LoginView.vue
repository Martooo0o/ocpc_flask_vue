<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
     <!-- <Button txt="test"></Button> -->
<div class="wrapper is-4 is-offset-4 card-4">
    <h3 class="title card-4">Welcome Back!</h3>
    <div class="box">
        <!-- <form method="POST" action="/login"> -->
          <div>
            <div class="field">
                <div class="control">
                    <!-- <input class="input is-large" type="email" name="email" placeholder="Your Email" autofocus=""> -->
                    <TextInput ref="email" type="email" name="email" placeholder="Email"></TextInput>
                </div>
            </div>

            <div class="field">
                <div class="control">
                    <TextInput ref="pass" type="password" name="password" placeholder="Password"></TextInput>
                    <!-- <input class="input is-large" type="password" name="password" placeholder="Your Password"> -->
                </div>
            </div>
            <div class="field">
                <label class="checkbox">
                    <input type="checkbox" name="remember">
                    Remember me
                </label>
            </div>
            <Button @click="login" class="button is-block is-info is-large is-fullwidth card-4" txt="Login">Login</Button>

            <div id="reg_wrap">
              You don't have an account yet?
              <br/>
              <a id="reg_btn" @click="this.$emit('register')">Register Now</a>
            </div>
        </div>
    </div>
</div>
     
  
</template>
  
<script>
import Button from '../components/ui/Button'
import TextInput from '../components/ui/TextInput'
import { mapActions, mapGetters, makeRequestWithJWT } from 'vuex'
export default {
  data: () => ({
    user: {
      email: "",
      password: ""
    }
  }),
  props: {
        // txt: String,
        // color: String
        cubes: Object,
        logs: Array,
        log_ex_obj: Object
    },
  components: {
    TextInput,
    Button
},
computed: {
    ...mapGetters({
      authUser: 'auth/user',
      isLoggedIn: 'auth/isLoggedIn'
    })
  },
  methods:{
     ...mapActions({
      loginUser: 'auth/loginUser'
    }),
    async login() {
    let baseURL = process.env.ROOT_API;
      console.log(baseURL);
      let usr = {
        email: this.$refs.email.obj,
        password: this.$refs.pass.obj
      }
      console.log("User in View");
      console.log(usr);
      await this.loginUser(usr)
        .then(() => {
          this.$emit('login-success', usr.email, usr.password);
        })
        .catch((error) => {
          console.log(error)
        })
      
    }
  },
  emits: ['login-success']
}
</script>

<style scoped>
.wrapper{
  display: block;
  width: fit-content;
  min-width: 300px;
  height: fit-content;
  /* border-right: 2px solid steelblue; */
  background: #CCCCCC;
  margin: 20px auto;
  border-radius: 10px;
  padding-bottom: 10px;
  padding-left: 10px;
  padding-right: 10px;
  color: white;
}
h3{
    margin: 0 auto 20px auto;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
.field{
    padding: 0px;
    margin: 0 auto 10px;
}
#reg_wrap{
  color: white;
}
#reg_btn{
  font-weight: bold;
  color: white;
  pointer-events: all;
  cursor: pointer;
}
#reg_btn:hover{
  font-weight: bold;
  color: #E6B656;
  
}
</style>
