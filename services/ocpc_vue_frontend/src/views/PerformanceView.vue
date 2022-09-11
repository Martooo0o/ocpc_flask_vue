<template>
    <div>
        <h2>Performance</h2>
        <Button txt="Calculate" @click="calcPerformance"></Button>
        {{getPerf}}
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
    Button,
    Button
},
  computed: {
       ...mapGetters({
           getPerf: 'main/perf',
       })
   },
 methods:{
     ...mapActions({
         calcStats: 'main/getPerfor',
       }),
       async logout(){
           await this.logoutUsr()
           .then(()=>{
               this.$router.push('/');
           });
       },
       calcPerformance(){
            this.calcStats();
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
