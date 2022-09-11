<template>
   <Header @open-profile="openProfile" @open-login="openLogin" class="card-5" :authenticated="isLoggedIn"></Header>
  <div class="container">
     <router-view id='router' :analysies="analysies" 
     @select-log="onSelectLog" 
     :logs="logs"
     :log_inspect_obj="example_log" :cubes="cubes" 
     @register="openRegister"
     @open-login="openLogin"
     @login-success="loginSuccess"
     ></router-view>
  </div>
</template>
<script>

// import HelloWorld from './components/HelloWorld.vue'
import Header from './components/Header'
import Logs from './components/ListLogs'
import { mapActions, mapGetters } from 'vuex'
import { authService } from './api'
import store from './store'
export default {
  name: 'App',
  components: {
  Header, Logs
},
  data(){
    return {
      log_file_names: [],
      log_selections: [],
      example_log: {},
      cubes: {},
      analysies: {},
      user: {},
      // isLogedIn
    }
  },
  computed: {
    ...mapGetters({
      authUser: 'auth/user',
      isLoggedIn: 'auth/isLoggedIn',
      // logs: 'main/logs'
    })
  },
  created(){
    // export const serverURL = 'ROOT_API';
    // let baseURL = process.env.ROOT_API;
    // console.log(baseURL);

    authService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
    const response = authService.post('/check_jwt')
    .then(function(value){
      console.log(value);
      if(value.status !== 200){
        store.dispatch('auth/actionIsLoggedIn', false);
        localStorage.removeItem('jwt');
        localStorage.removeItem('jwt_refresh');
      }else{
        store.dispatch('auth/actionIsLoggedIn', true);
      }
    })
    this.user = {

    }
    this.log_selections = []
    this.example_log = {
  "ocel:global-event": {
    "ocel:activity": "__INVALID__"
  },
  "ocel:global-object": {
    "ocel:type": "__INVALID__"
  },
  "ocel:global-log": {
    "ocel:attribute-names": [
      "age",
      "bankaccount",
      "cost",
      "price",
      "producer",
      "product",
      "weight(category)"
    ],
    "ocel:object-types": [
      "customers",
      "items",
      "orders",
      "packages"
    ]
  },
  "ocel:events": {
    "2.0": {
      "ocel:activity": "place order",
      "ocel:timestamp": "2019-05-20 10:35:21+00:00",
      "ocel:omap": [
        "Gyunam Park",
        "880007",
        "880006",
        "880008"
      ],
      "ocel:vmap": {
        "price": 543.0,
        "weight(category)": "heavy"
      }
    },
    "3.0": {
      "ocel:activity": "pick item",
      "ocel:timestamp": "2019-05-20 10:38:17+00:00",
      "ocel:omap": [
        "880006",
        "Gyunam Park"
      ],
      "ocel:vmap": {
        "price": 674.0,
        "weight(category)": "heavy"
      }
    },
    "4.0": {
      "ocel:activity": "confirm order",
      "ocel:timestamp": "2019-05-20 11:13:54+00:00",
      "ocel:omap": [
        "Marco Pegoraro",
        "880003",
        "880002",
        "880004",
        "880001"
      ],
      "ocel:vmap": {
        "price": 124.0,
        "weight(category)": "light"
      }
    },
    "5.0": {
      "ocel:activity": "pick item",
      "ocel:timestamp": "2019-05-20 11:20:13+00:00",
      "ocel:omap": [
        "Marco Pegoraro",
        "880002"
      ],
      "ocel:vmap": {
        "price": 234.0,
        "weight(category)": "medium"
      }
    },
    "6.0": {
      "ocel:activity": "place order",
      "ocel:timestamp": "2019-05-20 12:30:30+00:00",
      "ocel:omap": [
        "880011",
        "Majid Rafiei",
        "880012",
        "880009",
        "880010",
        "880008"
      ],
      "ocel:vmap": {
        "price": 232.0,
        "weight(category)": "heavy"
      }
    },
    "7.0": {
      "ocel:activity": "confirm order",
      "ocel:timestamp": "2019-05-20 12:34:16+00:00",
      "ocel:omap": [
        "880011",
        "Majid Rafiei",
        "880012",
        "880009",
        "880010"
      ],
      "ocel:vmap": {
        "price": 674.0,
        "weight(category)": "light"
      }
    },
    "8.0": {
      "ocel:activity": "item out of stock",
      "ocel:timestamp": "2019-05-20 13:54:37+00:00",
      "ocel:omap": [
        "Marco Pegoraro",
        "880004"
      ],
      "ocel:vmap": {
        "price": 434.0,
        "weight(category)": "medium"
      }
    },
    "9.0": {
      "ocel:activity": "place order",
      "ocel:timestamp": "2019-05-20 14:20:47+00:00",
      "ocel:omap": [
        "880013",
        "880014",
        "Junxiong Gao"
      ],
      "ocel:vmap": {
        "price": 643.0,
        "weight(category)": "heavy"
      }
    },
    "10.0": {
      "ocel:activity": "item out of stock",
      "ocel:timestamp": "2019-05-20 15:19:49+00:00",
      "ocel:omap": [
        "Majid Rafiei",
        "880009"
      ],
      "ocel:vmap": {
        "price": 232.0,
        "weight(category)": "light"
      }
    },
    "210.0": {
      "ocel:activity": "confirm order",
      "ocel:timestamp": "2019-05-24 16:32:09+00:00",
      "ocel:omap": [
        "880104",
        "880107",
        "Junxiong Gao",
        "880106",
        "880103",
        "880109",
        "880105",
        "880108"
      ],
      "ocel:vmap": {
        "price": 124.0,
        "weight(category)": "medium"
      }
    },
    "531.0": {
      "ocel:activity": "place order",
      "ocel:timestamp": "2019-05-30 17:09:26+00:00",
      "ocel:omap": [
        "880273",
        "880272",
        "Gyunam Park"
      ],
      "ocel:vmap": {
        "price": 674.0,
        "weight(category)": "light"
      }
    },
    "680.0": {
      "ocel:activity": "item out of stock",
      "ocel:timestamp": "2019-06-03 17:13:35+00:00",
      "ocel:omap": [
        "Majid Rafiei",
        "880279"
      ],
      "ocel:vmap": {
        "price": 234.0,
        "weight(category)": "heavy"
      }
    }
  },
  "ocel:objects": {
    "Marco Pegoraro": {
      "ocel:type": "customers",
      "ocel:ovmap": {
        "age": 50.0,
        "bankaccount": 91248.0
      }
    },
    "Gyunam Park": {
      "ocel:type": "customers",
      "ocel:ovmap": {
        "age": 55.0,
        "bankaccount": 27275.0
      }
    },
    "Majid Rafiei": {
      "ocel:type": "customers",
      "ocel:ovmap": {
        "age": 46.0,
        "bankaccount": 74370.0
      }
    },
    "Junxiong Gao": {
      "ocel:type": "customers",
      "ocel:ovmap": {
        "age": 52.0,
        "bankaccount": 96270.0
      }
    },
    "880001": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Show 8",
        "cost": 323.0
      }
    },
    "880002": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Fire Stick 4K",
        "cost": 434.0
      }
    },
    "880003": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo",
        "cost": 124.0
      }
    },
    "880004": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "C",
        "product": "Echo Studio",
        "cost": 674.0
      }
    },
    "880005": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad Air",
        "cost": 434.0
      }
    },
    "880006": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "MacBook Air",
        "cost": 434.0
      }
    },
    "880007": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone 11",
        "cost": 674.0
      }
    },
    "880008": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "C",
        "product": "Fire Stick",
        "cost": 234.0
      }
    },
    "880009": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad Pro",
        "cost": 643.0
      }
    },
    "880010": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone X",
        "cost": 200.0
      }
    },
    "880011": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Dot",
        "cost": 643.0
      }
    },
    "880012": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Kindle Paperwhite",
        "cost": 234.0
      }
    },
    "880013": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad mini",
        "cost": 124.0
      }
    },
    "880014": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone 8",
        "cost": 232.0
      }
    },
    "880015": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Show 5",
        "cost": 323.0
      }
    },
    "880016": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Show 8",
        "cost": 124.0
      }
    },
    "880100": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Studio",
        "cost": 432.0
      }
    },
    "880101": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad",
        "cost": 124.0
      }
    },
    "880102": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Kindle",
        "cost": 232.0
      }
    },
    "880103": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone 11",
        "cost": 643.0
      }
    },
    "880104": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Fire Stick",
        "cost": 234.0
      }
    },
    "880105": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone 11 Pro",
        "cost": 124.0
      }
    },
    "880106": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad Pro",
        "cost": 674.0
      }
    },
    "880107": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone X",
        "cost": 232.0
      }
    },
    "880108": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Dot",
        "cost": 242.0
      }
    },
    "880109": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Kindle Paperwhite",
        "cost": 323.0
      }
    },
    "880110": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad mini",
        "cost": 200.0
      }
    },
    "880111": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone 8",
        "cost": 674.0
      }
    },
    "880199": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Plus",
        "cost": 234.0
      }
    },
    "880270": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Dot",
        "cost": 200.0
      }
    },
    "880271": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Plus",
        "cost": 564.0
      }
    },
    "880272": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Show 5",
        "cost": 234.0
      }
    },
    "880273": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Show 8",
        "cost": 242.0
      }
    },
    "880274": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad",
        "cost": 232.0
      }
    },
    "880275": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Kindle",
        "cost": 323.0
      }
    },
    "880276": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad Air",
        "cost": 234.0
      }
    },
    "880277": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone 11 Pro",
        "cost": 564.0
      }
    },
    "880278": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPad Pro",
        "cost": 232.0
      }
    },
    "880279": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone X",
        "cost": 343.0
      }
    },
    "880280": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Plus",
        "cost": 200.0
      }
    },
    "880281": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone 8",
        "cost": 343.0
      }
    },
    "880282": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "MacBook Pro",
        "cost": 564.0
      }
    },
    "880283": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo Show 5",
        "cost": 242.0
      }
    },
    "880284": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Echo",
        "cost": 242.0
      }
    },
    "880285": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Kindle",
        "cost": 674.0
      }
    },
    "880286": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "iPhone 11",
        "cost": 124.0
      }
    },
    "880287": {
      "ocel:type": "items",
      "ocel:ovmap": {
        "producer": "B",
        "product": "Fire Stick",
        "cost": 124.0
      }
    }
  },
  "ocel:version": "0.1"
}
  },
  methods:{
     ...mapActions({
      getUser: 'auth/fetchUser',
      getLogs: 'main/getLogs',
      getCubes: 'main/getCubes',
      setIsLoggedIn: 'auth/actionIsLoggedIn'
    }),
    onSelectLog(log){
      console.log("Select App: " + log)
      // $emit('select-log', name)

    },
    openLogin(){
      this.$router.push('/login')
    },
    openProfile(){
      this.$router.push('/profile')
    },
    openRegister(){
      this.$router.push('/register')
    },
    async makeRequestWithJWT() {
      const options = {
        method: 'post',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('jwt')}`,
        }
      };
      // const response = await 
      
      try {
        const result = await fetch('http://localhost:5000/auth/user', options)
         console.log(result)
       const resultJson = await result.json();
        console.log(resultJson)
        return resultJson;
      } catch(err) {
        alert(err); // Failed to fetch
        return null;
      }
      // .then(function (response) {
      //       return response;
      //   });
      // const result = await response.json();
    },
    async loginSuccess(email, pass){
        console.log("before getting logs")
        await this.getLogs()
        await this.getCubes()
        .then(()=>{
           this.$router.push('/logs');
        });
    },
    
  }
}
</script>

<style>
body{
  margin: 0;
  overflow: hidden;
}
h3{
  padding: 5px 20px;
    width: fit-content;
    color: white;
    margin: 0;
    background-color: #E6B656;
    z-index: 5;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding: 0;
  height: calc( 100vh - 100px);
}
.container {
  max-width: 9;
  height: 100%;
  /* overflow: auto; */
  min-height: 300px;
  border: 1px solid steelblue;
  /* padding: 30px; */
  position: relative;
  margin-top: 100px;
}
.btn {
  display: inline-block;
  background: #000;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  font-size: 15px;
  font-family: inherit;
}
.btn:focus {
  outline: none;
}
.btn:active {
  transform: scale(0.98);
}
.btn-block {
  display: block;
  width: 100%;
}
#logs{
  position: relative;
}
.card-4 {
  box-shadow: 0 3px 10px rgba(0,0,0,0.25), 0 2px 5px rgba(0,0,0,0.22);
}
 
</style>
