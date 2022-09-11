<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
     <!-- <Button txt="test"></Button> -->
<div class="wrapper is-4 is-offset-4 card-4">
    <h3 class="title card-4">New User</h3>
    <div class="box">
        <!-- <form method="POST" action="/signup"> -->
        <div >
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
                <div class="control">
                    <TextInput ref="pass2" type="password" name="password" placeholder="Repeat Password"></TextInput>
                    <!-- <input class="input is-large" type="password" name="password" placeholder="Your Password"> -->
                </div>
            </div>
            <!-- <div class="field">
                <label class="checkbox">
                    <input type="checkbox" name="remember">
                    Remember me
                </label>
            </div> -->
            <p id="pass_missmatch" v-if="missmath">Passwords are not matching</p>
            <Button @click="tryRegister" class="button is-block is-info is-large is-fullwidth card-4" txt="Register">Register</Button>

            <!-- <div id="reg_wrap">
              You don't have an account yet?
              <br/>
              <a id="reg_btn" @click="this.$emit('register')">Register Now</a>
            </div> -->
        </div>
    </div>
</div>
     
  
</template>
  
<script>
import Button from '../components/ui/Button'
import TextInput from '../components/ui/TextInput'
export default {
  data(){
    return{
      // email: "",
      // pass: "",
      // pass2: "",
      missmath: false
    }
  },
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
  methods:{
    tryRegister(){
      // let games = await register();
      // console.log("After getGames");
      // console.log("games: " + games)
        this.missmath = (this.$refs.pass.obj != this.$refs.pass2.obj);
        if(!this.missmath){
          (async () => {
            const rawResponse = await fetch('http://0.0.0.0:5000/auth/signup', {
              method: 'POST',
              headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ email: this.$refs.email.obj,
                  password: this.$refs.pass.obj,})
            });
            const content = await rawResponse.json();

            console.log(content);

            if('success' in content){
              this.$emit('open-login');
            }
          })();
        }
    },
  },
  emits: ['open-login']
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
#pass_missmatch{
  color: red;
}
</style>
