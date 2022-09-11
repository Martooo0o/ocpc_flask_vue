<template class="container">

    <div id="logs_wrapper">
        <h3 class="card-4">Select Log</h3>

        <div class="tinput">
            <TextInput></TextInput>
        </div>
        <div id="items_wrapper">
            <div class="item" :key="log" v-for="log in logs" :class="{ 'selected' : selected.includes(log)}">
                <ItemLog @select-log="onSelect(log)" :name="log"></ItemLog>
            </div>
        </div>
        
    </div>
</template>

<script>
import ItemLog from './ItemLog.vue';
import Button from './ui/Button.vue';
import TextInput from './ui/TextInput.vue';
export default {
    data(){
        return {
        selected: []
        }
    },
    name: "Logs",
    props: {
        // txt: String,
        // color: String
        logs: Array,
    },
    methods: {
        onSelect(log){
            console.log("Selected ListLogs: " +log)
            if(this.selected.includes(log)){
                this.selected = this.selected.filter(function(value, index, arr){ 
                    return value != log;
                });
                this.$emit('select-log', null)
            }else{
                this.selected = []
                this.selected.push(log)
                this.$emit('select-log', log)    
            }
        },
    },
    created(){
        this.selected = [];
    },
    components: { ItemLog, Button, TextInput },
    emits: ['select-log']
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
    border-top-left-radius: 10px;
    position: fixed;
    z-index: 5;
}
#items_wrapper{
   margin-top: 70px;
   position: relative;
    height: 100%;
}
.item{
    display: block;
    padding: 10px;
    margin: 0 10px;
    position: relative;
    height: 41px;
}

.item:hover, .selected{
    background: #999999;
    border-radius: 20px;
}

#upload_log_btn{
    position: absolute;
    left:5px;
    z-index: 5;
    width:calc(30% - 20px);
    bottom: calc(50% + 10px);
}
#logs_wrapper{
  display: inline-block;
  width: calc(100% - 30px);
  height: 300px;
  border-right: 2px solid #808080;
  float: left;
  overflow: scroll;
  border-bottom: 2px solid #808080;
  background: white;
  margin: 10px 15px 20px 15px;
  border-radius: 10px;
  position: relative;
}
.tinput{
    left: 200px;
    position: fixed;
    width: calc(100% - 270px);
    margin-top: 10px;

}
  .selected{
        background: #888888;
    }
</style>
