<template>
    <analysis-nav></analysis-nav>
    <div id="analysis_wrapper" style="background: #CCCCCC;">
        <div id="analysis" class="card-4">
          <Analysis></Analysis>
        </div>
    </div>
</template>
  
<script>

// import HelloWorld from './components/HelloWorld.vue'
import Logs from '../components/ListLogs'
import LogInspector from '../components/LogInspector'
import CubeInspector from '../components/CubeInspector'
import ListCubes from '../components/ListCubes'
import NewCubeDialog from '@/components/NewCubeDialog.vue'
import Analysis from '@/components/analysis/Analysis.vue'
import AnalysisNav from '@/components/analysis/AnalysisNav.vue'
export default {
  
  props: {
        // txt: String,
        // color: String
        cubes: Object,
        logs: Array,
        log_ex_obj: Object,
        input_inspect: String,
        analysies: Object
    },
  components: {
    Logs,
    LogInspector,
    ListCubes,
    CubeInspector,
    NewCubeDialog,
    Analysis,
    AnalysisNav
},
  created(){
    this.inspect = input_inspect
  },
  methods:{
    onSelectLog(log){
      console.log("Select LogsView: " + log)
      this.$emit('select-log', log)
      this.inspect = "log"
    },
    onSelectCube(cube){
      console.log("Select LogsView: " + cube)
      this.$emit('select-cube', cube)
      this.inspect = "cube"
    },
    newCube(){
      console.log("Display New Cube Pop")
      this.new_cube = true
    },
    createCube(){
      this.new_cube = false
    }
  },
  emits: ['select-log', 'select-cube'],
  data() {
  	return {
	    inspect: this.inspect,
      new_cube: this.new_cube
  	}
	},

  // data(){
  //   return {
  //     log_file_names: [],
  //     log_selections: [],
  //     example_log: {},
  //     cubes: {}
  //   }
  // },
  created(){
    this.inspect = "log",
    this.new_cube = false
  }
}
</script>

<style scoped>
#verical_wrapper{
  display: inline-block;
  width: calc(30% - 1px );
  height: 100%;
  border-right: 2px solid steelblue;
  float: left;
}
#analysis_wrapper{
  overflow-y: scroll;
  height: calc(100% - 34px)
}
#analysis{
  margin: 0 20px 40px 20px;
  border-radius: 10px;
  background: white;
  position: relative;
  top: 20px;
  height: fit-content;
}
</style>
