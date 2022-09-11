<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
     <!-- <Button txt="test"></Button> -->
     <div>
      <h4>Bachelor Thesis of Martin Vichev</h4>
     </div>
</template>
  
<script>

// import HelloWorld from './components/HelloWorld.vue'
import Logs from '../components/ListLogs'
import LogInspector from '../components/LogInspector'
import ListCubes from '../components/ListCubes'
import Button from '@/components/ui/Button.vue'
export default {
  
  props: {
        // txt: String,
        // color: String
        cubes: Object,
        logs: Array,
        log_ex_obj: Object
    },
  components: {
    Logs,
    LogInspector,
    ListCubes,
    ListCubes,
    Button
},
  methods:{
    onSelectLog(log){
      console.log("Select LogsView: " + log)
      this.$emit('select-log', log)
    },
    
  },
  emits: ['select-log']
}
</script>

<style>
#verical_wrapper{
  display: inline-block;
  width: calc(30% - 1px );
  height: 100%;
  border-right: 2px solid steelblue;
  float: left;
}
</style>
