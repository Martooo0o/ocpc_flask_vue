<template>
<div id="inspector">
    <div  id="title" class="card-4">
        <h3>Cube Instepctor: </h3>
        <label id="cubename">{{cube !== undefined && Object.keys(cube).length===0 ?'No Log Selected':cube['cube']}} </label>
        <!-- <img class="vis_type_img selected_vis_type" ref="code" src="@/assets/code_icon.png" @click="visTypeSelected('code')"/>
        <img class="vis_type_img" ref="data" src="@/assets/insp_data_icon.png" @click="visTypeSelected('data')"/> -->
        <div @click="this.$emit('del-cube', cube['cube'])" class="close_btn card-4">
            <p>X</p>
        </div>
    </div>
   
    <div id = "cube_inspector_contents">
        
        <div class="half card-4" style="margin-right: 10px">
            <label >Cube Name:</label><span>{{cube.cube}}</span>
        </div>
        <div class="half card-4">
            <label >Source Log:</label><span>{{cube.sourcelog}}</span>
        </div>
        

        <div id="dim_display">
            <DimDispaly :dimens="cube.dimens"></DimDispaly>
        </div>

         <div id="analysis_display">
            <ListAnalysies @delete-analysis="openDelAnalysisDialog" @new-analysis="this.$emit('new-analysis')" :analyses="cube.analyses === undefined? []: cube.analyses"></ListAnalysies>
        </div>
    </div>
</div>
    
</template>

<script>
import ItemLog from './ItemLog.vue';
import Button from './ui/Button.vue';
import DimDispaly from './DimDispaly.vue';
import ListAnalysies from './analysis/ListAnalysies.vue';
export default {
    name: "CubeInspector",
    props: {
        // txt: String,
        // color: String
        // analysies: Object,
        cube: Object
    },
    methods: {
    // onSelect(log){
    //     console.log("Selected ListLogs: " +log)
    //     this.$emit('select-log', log)
    // },
    openDelAnalysisDialog(name){
            console.log("Delete " + name + "?");
            this.$emit('delete-analysis', name);
        }, 
    },
    components: { DimDispaly, ListAnalysies },
    emits: ['new-analysis', 'delete-analysis']
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
    padding-right: 5px;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 5px;
}

#cube_inspector{

    z-index: 4;
    /* transform: translate(150px, 0px) */
    height: fit-content;
}
#inspector{
    display: inline-block;
    position: relative;
    height: 100%;
    width: calc(70% - 1px);
    color: black;
    /* overflow: auto; */
}
#cube_inspector_contents{
    display: block;
    height: calc(100% - 36px);
    overflow: auto;
    text-align: start;
    margin: 0px 0 0 0 ;
    padding: 50px 20px 0 20px; 
}
label{
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
span{
    margin-left: 20px;
    margin-right: 20px;
}
.half{
    width: calc( 50% - 30px);
    display: inline-block;
    border: 1px solid#CCCCCC;
    border-radius: 10px;
    position: relative;
    left: 20px;
}
#dim_display{
    margin-top: 20px;
}
#analysis_display{
    margin: 20px 0;
    padding-bottom: 5px;
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

#cubename{
    height: 36px;
    text-align: center;
    display: inline-block;
    position: relative;
    top: 50%;
    transform: translateY(-50%);
    margin-left: 5px;
    margin-right: 10px;
    background: none;
    padding: 0px 0px;
}

</style>
