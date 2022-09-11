<template class="container">

    <div id="logs_wrapper">
        <h3 class="card-4">Logs</h3>
        <UploadBtn @log-uploaded="uploadLog" id="upload_log_btn" txt="Import Log"></UploadBtn>
        <div id="items_wrapper">
            <div class="item" :key="log" v-for="log in logs">
                <ItemLog  @select-log="onSelect(log)" :name="log"></ItemLog>
            </div> 
        </div>
        <label id="no_logs" v-if="logs.length == 0">No logs</label>
    </div>
</template>

<script>
import ItemLog from './ItemLog.vue';
import Button from './ui/Button.vue';
import UploadBtn from './ui/UploadBtn.vue';
import { mapActions, mapGetters } from 'vuex';
import store from '../store';
export default {
    name: "Logs",
    props: {
        // txt: String,
        // color: String
        logs: Array
    },
    // computed: {
    //     ...mapGetters({
    //         getStoreLog: 'auth/logs',
    //     })
    // },
    methods: {
        onSelect(log){
            console.log("Selected ListLogs: " +log)
            this.$emit('select-log', log)
        },
        uploadLog(log){
            console.log("ListLogs: File Uploaded");
            console.log(log);
            this.$emit("upload-log", log);
            // await store._actions['logs/uploadLog'][0](log)
            //     .then(() => {
            //         console.log("uploadLog: Start of return in View")
            //         console.log( this.logs = this.getStoreLog)
            //         this.logs = this.getStoreLog
            //     })
            //     .catch((error) => {
            //     console.log(error)
            //     })
        },
        ...mapActions({
            userLogs: 'auth/getLogs'
        }),
        
    },
    components: { ItemLog, Button, UploadBtn },
    emits: ['select-log', 'upload-log']
}
</script>

<style scoped>
h3{
    color: white;
    background-color: #E6B656;
    margin: 0;
    width: fit-content;
    min-width: 120px;
    padding: 5px 10px;
    border-bottom-right-radius: 10px;
    position: fixed;
    z-index: 5;
}
#items_wrapper{
   position: relative;
    height: 100%;
     overflow: scroll;
}
.item{
    display: block;
    padding: 10px;
    margin: 0 10px;
    position: relative;
    height: 41px;
}
.item:first-of-type{
     margin-top: 50px;
}
.item:last-of-type{
     margin-bottom: 50px;
}

.item:hover{
    background: #999999;
    border-radius: 20px;
}
#upload_log_btn{
    position: absolute;
    z-index: 5;
    bottom: calc(10px);
    margin: 0 auto;
    width: calc(100% - 20px);
    left: 5px;
}
#logs_wrapper{
  display: inline-block;
  width: 100%;
  height: 50%;
  border-right: 2px solid #808080;
  float: left;
  border-bottom: 2px solid #808080;
  position: relative;
}
#no_logs{
    position:absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
