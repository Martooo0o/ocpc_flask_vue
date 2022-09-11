<template>
  <div>
    <router-link to="/performance"><Button txt="Performance" @click="openPerfomance" ></Button></router-link> 
    <br/>
    <Button @click="logout" txt="Logout" color="#FF0000"></Button>   
  </div>
     
</template>
  
<script>

// import HelloWorld from './components/HelloWorld.vue'
import Button from '../components/ui/Button'
import { mapActions, mapGetters } from 'vuex';
export default {
   
  props: {
        // txt: String,
        // color: String
        // cubes: Object,
        // logs: Array,
        log_inspect_obj: Object,
        input_inspect: String,
        analysies: Object
    },
  components: {
    Button
},
   computed: {
        ...mapGetters({
            getStoreLog: 'main/logs',
            getStoreCubes: 'main/cubes',
            getSpecCubeStore: 'main/specCube'
        })
    },
  methods:{
      ...mapActions({
          logoutUsr: 'auth/logoutUser',
        }),
        async logout(){
            await this.logoutUsr()
            .then(()=>{
                this.$router.push('/');
            });
        }

    },
    emits: ['select-log', 'select-cube'],
    data() {
        return {
        
        }
    },
    created(){
   
  }
}
</script>

<style>


</style>
