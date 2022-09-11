<template>
<div id="inspector">
    <div  id="title" class="card-4">
        <h3>Log Instepctor:</h3>
        <label id="logname">{{Object.keys(specLog).length===0 ?'No Log Selected':specLog['log']}} </label>
        <img class="vis_type_img selected_vis_type" ref="code" src="@/assets/code_icon.png" @click="visTypeSelected('code')"/>
        <img class="vis_type_img" ref="data" src="@/assets/insp_data_icon.png" @click="visTypeSelected('data')"/>
        <div @click="this.$emit('del-log', specLog['log'])" class="close_btn card-4">
            <p>X</p>
        </div>
    </div>
    <div id = "cube_inspector_contents">
        <pre v-if="this.type === 'code' && Object.keys(specLog).length!==0">{{JSON.stringify(log_obj, undefined, 4)}}</pre>

        <div v-if="this.type === 'data' && Object.keys(specLog).length!==0">
            <div class="half card-4" style="margin-right: 10px">
                <label class="label_count">Event Count:</label><span class="span_count">{{specLog.num_events}}</span>
            </div>
            <div class="half card-4">
                <label class="label_count">Object Count:</label><span class="span_count">{{specLog.num_objs}}</span>
            </div>
        </div>
    </div>
</div>
    
</template>

<script>
import ItemLog from './ItemLog.vue';
import Button from './ui/Button.vue';
import { mapActions, mapGetters } from 'vuex';
export default {
    data(){
        return {
            type : this.type,
            // log_name: this.specLog.log
        }
    },
    name: "LogInspector",
    props: {
        // txt: String,
        // color: String
        log_obj: Object
    },
    methods: {
        // onSelect(log){
        //     console.log("Selected ListLogs: " +log)
        //     this.$emit('select-log', log)
        // },
        visTypeSelected(type){
            this.type = type;
            if(this.type == "code"){
                this.$refs["code"].classList.add('selected_vis_type');
                this.$refs["data"].classList.remove('selected_vis_type');
            }else{
                this.$refs["data"].classList.add('selected_vis_type');
                this.$refs["code"].classList.remove('selected_vis_type');
            }
            
        }
    },
    created(){
        this.type = 'code';
    },
    computed: {
        ...mapGetters({
            specLog: 'main/specLog',
        })
    },
    // components: { ItemLog , Button},
    emits: ['select-log', 'del-log']
}
</script>

<style scoped>
h3{
    margin-top: 0;
    display: inline-block;
    /* position: fixed;
    left: calc(30% + 1px);
    border-bottom-right-radius: 10px; */
    /* background: none; */
    border-bottom-left-radius: 5px;
    transform: translateY(-30%);
    padding-right: 5px;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 5px;
}
#logname{
    height: 36px;
    text-align: center;
    display: inline-block;
    transform: translateY(-30%);
    margin-left: 5px;
    margin-right: 10px;
}
#inspector{
    display: inline-block;
    position: relative;
    height: 100%;
    width: calc(70% - 1px);
    color: black;
    /* overflow: auto; */
}
pre{
    display: block;
    height: calc(100% - 36px);
    /* overflow: auto; */
    text-align: start;
    margin: 0px 0 0 0 ;
    /* padding-top: 20px; */
}
#title{
    position: absolute;
    left: 50%;
    width: fit-content;
    transform: translateX(-50%);
    top: 0;
    /* background: #E6B656; */
    height: 30px;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    border: 3px #E6B656 solid;
}
.vis_type_img{
    width: 16px;
    height: 16px;
    padding:5px;
    margin-top: 2px ;
    margin-bottom: 2px ;
    margin-right: 10px;
    border-radius: 10px;
}
.vis_type_img:hover{
    background: #CCCCCC;
}
.vis_type_img:last-of-type{
    margin-right: 5px;
}

.selected_vis_type{
    background: #E6B656;
}

#cube_inspector_contents{
    display: block;
    height: calc(100% - 36px);
    overflow: auto;
    text-align: start;
    margin: 0px 0 0 0 ;
    padding: 50px 20px 0 20px; 
}

.label_count{
    width: fit-content;
    color: black;
    display: inline-block;
    width: fit-content;
    padding: 5px 10px;
    background-color: #CCCCCC;
    width: fit-content;
    z-index: 5;
    border-radius: 8px;
    padding: 10px 10px;
}
.span_count{
    margin-left: 20px;
    margin-right: 20px;
}

.half{
    width: calc( 50% - 30px);
    display: inline-block;
    border: 1px solid#CCCCCC;
    border-radius: 20px;
    position: relative;
    left: 20px;
}

.close_btn{
    background: red;
    color: white;
    position: relative;
    /* right: -15px;
    top: -15px; */
    /* padding: 10px; */
    height: 23px;
    width: 23px;
    border-radius: 20px;
    display: inline-block;
    float: right;
    top: 50%;
    transform: translateY(-50%);
    margin-right: 5px;
}
.close_btn p{
    padding: 0;
    margin: 0 auto;
    display: block;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: xx-small;
}

.close_btn:hover{
    background: white;
    color: red;
    font-size: xx-small;
}
</style>
