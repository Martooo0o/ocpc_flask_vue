<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
     <!-- <Button txt="test"></Button> -->

  <div >
    <div id="wrapper">
      <div id="verical_wrapper" class="card-4">
       <Logs @select-log="onSelectLog" @upload-log="uploadLog" :logs = "getStoreLog"></Logs>   
       <ListCubes @new-cube="newCube" @select-cube="onSelectCube" :cubes="getStoreCubes"></ListCubes>
     </div>
    <LogInspector @del-log="deleteLog" v-if="inspect === 'log' " :log_obj="log_inspect_obj"></LogInspector>
    <CubeInspector @del-cube="deleteCube" @delete-analysis="openDeleteAnalysisDialog" @new-analysis="newAnalysis" v-else-if="inspect === 'cube' " :cube="getSpecCubeStore" ></CubeInspector>

    <NewCubeDialog  @close-new-cube="closeNewCube" @create_cube="createCube" v-if="new_cube" :logs = "getStoreLog"></NewCubeDialog>
    <NewAnalysisDialog @close-new-analysis="closeNewAnalysis" @create-analysis="createAnalysis" v-if="new_analysis" :logname = "getSpecCubeStore.sourcelog" :cubename = "getSpecCubeStore.cube"></NewAnalysisDialog>
     
    <DelAnalysisDialog v-if="del_a_dialog" :log="getSpecCubeStore.sourcelog" :cubename="getSpecCubeStore.cube" :analysis="this.delAName" @close-del-analysis="closeDelADialog"></DelAnalysisDialog>
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
import NewAnalysisDialog from '@/components/NewAnalysisDialog.vue'
import DelAnalysisDialog from '@/components/DelAnalysisDialog.vue'
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
    Logs,
    LogInspector,
    ListCubes,
    CubeInspector,
    NewCubeDialog,
    NewAnalysisDialog,
    DelAnalysisDialog
},
   computed: {
        ...mapGetters({
            getStoreLog: 'main/logs',
            getStoreCubes: 'main/cubes',
            getSpecCubeStore: 'main/specCube',
            getSpecLogStore: 'main/specLog'
        }),
    },
  methods:{
      ...mapActions({
        uploadLogServer: 'main/uploadLog',
        getSpecLog: 'main/getSpecLog',
        getSpecCube: 'main/getSpecCube',
        createCubeServer: 'main/createCube',
        getLogs: 'main/getLogs',
        getCubes: 'main/getCubes',
        delLogStore: 'main/delLog',
        delCubeStore: 'main/delCube'
    }),
    openDeleteAnalysisDialog(name){
      console.log("OPEN DEL DIALOG")
      console.log(name);
      this.del_a_dialog = true;
      this.delAName = name;
    },
    closeDelADialog(){
      this.del_a_dialog = false
    },
    onSelectLog(log){
      console.log("Select Log in LogsView: " + log)
      this.$emit('select-log', log)
      this.getSpecLog(log)
      this.inspect = "log"
    },
    async deleteLog(log){
      console.log("Deleteing log " + log)
      await this.delLogStore(log).then(() => {
          console.log("Donec Deleting log")
          console.log(this.getSpecLogStore)
        })
        .catch((error) => {
          console.log(error)
        });
    },
    async deleteCube(cube){
      console.log("Deleteing cube " + cube)
      await this.delCubeStore(cube).then(() => {
          console.log("Donec Deleting cube")
          console.log(this.getSpecCubeStore)
        })
        .catch((error) => {
          console.log(error)
        });
    },
    onSelectCube(cube){
      console.log("Select Cube in LogsView: " + cube)
      this.$emit('select-cube', cube)
      this.getSpecCube(cube)
      this.inspect = "cube"
    },
    newCube(){
      console.log("Display New Cube Pop")
      this.new_cube = true
    },
    closeNewCube(){
      console.log("Close New Cube Pop")
      this.new_cube = false
    },
    newAnalysis(){
      console.log("Display New Analysis Pop")
      this.new_analysis = true
      console.log(getSpecCubeStore.name)
      console.log(getSpecCubeStore.logname)
    },
    closeNewAnalysis(){
      console.log("Close New Analysis Pop")
      this.new_analysis = false
    },
    createAnalysis(){
      
    },
    async createCube(cubeName, log, selections){
      console.log(cubeName)
      console.log(log)
      console.log(selections)

      this.new_cube = false;
       var cube = {
        "name": cubeName,
        "logname": log,
        "dimens": selections
      };
      await this.createCubeServer(cube);
    },
    async uploadLog(log){
      console.log("LogsView: File Upload");
      // await store._actions['logs/uploadLog'][0](log)
            //     .then(() => {
            //         console.log("uploadLog: Start of return in View")
            //         console.log( this.logs = this.getStoreLog)
            //         this.logs = this.getStoreLog
            //     })
            //     .catch((error) => {
            //     console.log(error)
            //     })
      console.log(log)
      await this.uploadLogServer(log)
        .then(() => {
          console.log("Donec Upload")
        })
        .catch((error) => {
          console.log(error)
        })
    }
  },
  emits: ['select-log', 'select-cube', 'delete-analysis'],
  data() {
  	return {
	    inspect: this.inspect,
      new_cube: this.new_cube,
      new_analysis: this.new_analysis,
      delAName: this.delAName,
      del_a_dialog: this.del_a_dialog
  	}
	},
  created(){
    this.inspect = "log";
    this.new_cube = false;
    this.new_analysis = false;
    this.del_a_dialog = false;
    this.delAName = "";
    this.getLogs();
    this.getCubes();
  }
}
</script>

<style>
  #wrapper{
    display: block;
    position: absolute;
    height: 100%;
    width: 100%;
    /* width: calc(70% - 1px); */
    color: black;
  }
#verical_wrapper{
  display: inline-block;
  width: calc(30% - 1px );
  height: 100%;
  border-right: 2px solid steelblue;
  float: left;
}
/* #newc{
} */

</style>
