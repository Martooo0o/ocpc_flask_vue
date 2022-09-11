
<template>
    <header class="card-4">
    <img id = 'ocel_logo' src="@/assets/ocel.png" />
      <h2>OCP Cubes</h2>
      

      <!-- <ul>
          <li> -->
              <nav class="card-4">
                  <router-link to="/"><img id="home_icon" src="@/assets/home.png"></router-link>
                  <router-link to="/logs">Data</router-link>
                  <router-link to="/analyses">Analyses</router-link>
              </nav>
          <!-- </li>
      </ul> -->
      <!-- <Button txt="Get Started" color="green"></Button> -->
      <img v-if="authenticated" @click="$emit('open-profile')" id = 'acc_logo' src="@/assets/acc_icon.png" class="card-4"/>
      <Button class="card-4" @click="$emit('open-login')" v-if="!authenticated" txt="Get Started"></Button>
    </header>
</template>

<script>
import Button from './ui/Button';
// import { defineComponent } from '@vue/composition-api'
export default {
    name: 'Header',
    components: {
    Button
    },
    props: {
        authenticated: Boolean,
    },
    created(){
        // this.home = home;
    },
    emits: ['home', 'open-login', 'open-profile'],
    methods:{
        // onClick(home){
        //     this.home = home;
        // }
    },
    data(){
        return {
          home: this.authenticated  
        };
    }
    
}
</script>

<style scoped>
    #home_icon{
        width: 20px;
        height: 20px;
    }
    header{
        display: flex;
        justify-content: space-between;
        align-content: center;
        margin: 0 0 20px 0;
        background-color: #333333;
        vertical-align: middle;
        position: fixed;
        width: 100%;
        top:0px;
        z-index: 10;
    }
    #ocel_logo{
        widows: 100px;
        height: 100px;
        scale: 0.75;
    }
    #acc_logo{
         widows: 100px;
        height: 100px;
        scale: 0.4;
    }
    h2{
        color: #F6C666;
        margin: 5px 0;
        height: 90px;
        width: 100px;
        position: absolute;
        top: 50%;
        left: 75px;  
        transform: translate(0, -40%);
        text-align: center;
    }

    nav {
    width: fit-content;
    height: fit-content;
    
    font-size: 20px;
    text-align: center;
    position: absolute;
    top: 50%;
    padding: 0 0;
    left: 50%;
    transform: translate(-50%, -50%);
    /* transform: translateX(-50%); */
    display: inline-block;
    margin: 0 auto;
    border-radius: 10px;
    display: block;
    }
    nav a:nth-of-type(3n+1){
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
    }
    nav a:nth-last-of-type(3n+1){
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
    }

    nav a{
        background-color: gray;
        /* width: 100px; */
        text-decoration: none;
        color: aliceblue;
        margin: 0;
        display: inline-block;
        min-width: 100px;
        padding: 1rem 2rem;
        border-left: 1px solid var(--color-border); 
    }

    nav a.router-link-exact-active {
    color: var(green);
    font-weight: bolder;
    background-color: #E6B656;
    }

    nav a:hover {
    background-color: #E6B656;
    }

    nav a:first-of-type {
    border: 0;
    }
    Button{
        height: fit-content;
        position: absolute;
        padding: 5px 15px;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
    }
    Button:hover{
        height: fit-content;
        position: absolute;
        padding: 5px 15px;
        right: 20px;
        /* top: calc(50% + 2px); */
        transform: translateY(-50%);
    }
    Button:active{
        scale: 0.98;
    }
</style>
