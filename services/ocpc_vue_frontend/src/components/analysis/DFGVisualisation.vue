<template>
    <div class="wrap">
        <h3 class="card-4">Directly-Follows Graph</h3>
        <div class="filter_attr">
            <label>DFG Type: </label>
            <Select 
            :selected="visualisation!=undefined?visualisation['dfg_type']:''"
            :options="['Frequency', 'Performance']"
            @select="onSelectDfgType"></Select>
        </div>
        <img class="dfg_img" ref="dfg_img" :src="data"
    onerror="this.src=this.data"/>
        <div class="slidecontainer">
            <label class="slider_label">Edge Frequency: {{visualisation['edge_threshold']}}</label>
            <input @change="onChangeEdgeTresh($event)" type="range" min="1" max="100" :value="visualisation!=undefined?visualisation['edge_threshold']:''" class="slider" id="myRange">
        </div>

         <div class="vert_slidecontainer">
             <label class="slider_label">Activity Frequency: {{visualisation['act_threshold']}}</label>
             <input @change="onChangeActTresh($event)" type="range"  min="1" max="100" :value="visualisation!=undefined?visualisation['act_threshold']:''" class="vert_slider" id="myRange">
        </div>
    </div>
</template>

<script>
import Button from '../ui/Button.vue';
import Select from '../ui/Select.vue';
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "DFGVisualisation",
    props: {
        visualisation: Object,
        data: String
    },
    methods: {
         ...mapActions({
            setFilters: 'main/setAFilters',
            setVis: 'main/setAVis',
        }),
        onClick(name) {
            console.log("Selected ItemLog: " +this.name)
            this.$emit('select-analysis', this.name)
        },
        onSelectDfgType(type){
            console.log("Slected Type: " + type)
            let props = {}
            props['dfg_type'] = type
            console.log(this.visualisation)
            props['edge_threshold'] = this.visualisation['edge_threshold']
            props['act_threshold'] = this.visualisation['act_threshold']
            console.log("DFG_vis: ")
            console.log(props)
            this.$emit('dfg_props_changed', props)
        },
        onChangeEdgeTresh(event){
            let selectedValue = event.target.value
            console.log("Slected Edge Treshold: " + selectedValue)
            let props = {}
            props['edge_threshold'] = selectedValue
            console.log(this.visualisation)
            props['dfg_type'] = this.visualisation['dfg_type']
            props['act_threshold'] = this.visualisation['act_threshold']
            console.log("DFG_vis: ")
            console.log(props)
            this.$emit('dfg_props_changed', props)
        },
        onChangeActTresh(event){
            let selectedValue = event.target.value
            console.log("Slected Actvity Treshold: " + selectedValue)
            let props = {}
            props['edge_threshold'] = this.visualisation['edge_threshold']
            console.log(this.visualisation)
            props['dfg_type'] = this.visualisation['dfg_type']
            props['act_threshold'] = selectedValue
            console.log("DFG_vis: ")
            console.log(props)
            this.$emit('dfg_props_changed', props)
        }
    },
    computed: {
        ...mapGetters({
            aVisData: 'main/curr_analysis_vis_data',
        }),
        dimValues(){
            return this.filter.selections
        },
        visType(){
            return this.visualisation.type
        }
    },
    created(){
        
    },
    components: { Button, Select },
    emits: ['select-analysis', 'dfg_props_changed']
}
</script>

<style scoped>
#wrapper{
        background: none;
        border: none;
        padding: 5px;
        position: relative;
        width: calc(50% - 40px);
        height: fit-content;
        background: white;
        border-radius: 10px;
        margin: 10px 0px 10px 20px;
        align-items: baseline;
        text-align: left;
    }
#wrapper_btn:nth-of-type(){
    border-radius: 10px;
}
#wrapper_btn:hover{
    background: #888888;
}
#dimens{
    background: #E6B656;
    display: inline-block;
    padding: 10px;
    color: white;
    font-weight: bolder;
    border-radius: 10px;
    width: 150px;
    position: absolute;
    left: 0;
    top: 0;
}
#values_wrapper{
     display: inline-block;
    padding: 10px;
    width: calc(100% - 250px);
    position: relative;
    top: -15px;
    left: 170px;
}

#mat{
    background: #CCCCCC;
    display: inline-block;
    padding: 10px;
    color: white;
    font-weight: bolder;
    border-radius: 10px;
    float: right;
    position: absolute;
    right: 0;
    top: 0px;
    width: 60px;
    text-align: center;
}
.item{
    display: inline-block;
     font-weight: bold;
    border-radius: 10px;
    margin-right: 10px;
    margin-bottom: 10px;
}
.left_item, .right_item{
    display: inline-block;
}
.left_item{
    background: #E6B65680;
    
    padding: 10px;
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}
.right_item{
    background: #CCCCCC80;
    padding: 10px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}
.wrap{
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: silver;
         border-radius: 10px;
   }
.close_btn{
    background: red;
    color: white;
    position: absolute;
    right: -15px;
    top: -15px;
    padding: 10px;
    height: 20px;
    width: 20px;
    border-radius: 20px;
}
.close_btn:hover{
    background: white;
    color: red;
}

h3{
    margin: 0 auto;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}

/* DFG Vis. Styles */
.dfg_img{
    height: calc(100% - 118px);
    width: calc(100% - 20px);
    margin: 10px;
    background: white;
    border-radius: 10px;
}

.slidecontainer {
  width: calc(100% - 10px); /* Width of the outside container */
   position: absolute;
  bottom: 20px;
  left: 0px;
}
.vert_slidecontainer {
    width: calc(100% - 106px);
    position: absolute;
    top: calc(50% + 30px);
    right: 0px;
}

/* The slider itself */
.slider {
  -webkit-appearance: none;
  width: calc(100% - 60px);
  height: 15px;
  border-radius: 5px;   
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  border-radius: 50%; 
  background: #E6B656;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #E6B656;
  cursor: pointer;
}

.vert_slider{
    -webkit-appearance: none;
    transform: rotate(270deg);
    transform-origin: center;
    width: calc(100% - 60px);
    height: 15px;
    border-radius: 5px;   
    background: #d3d3d3;
    outline: none;
    opacity: 0.7;
    -webkit-transition: .2s;
    transition: opacity .2s;
    position: absolute;
}
.vert_slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  border-radius: 50%; 
  background: #E6B656;
  cursor: pointer;
}

.vert_slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #E6B656;
  cursor: pointer;
}

.slider_label{
    position: relative;
    display: block;
    widows: fit-content;
    width: 100%;
    text-align: center;
    opacity: 0.6;
}
.vert_slidecontainer .slider_label{
    position: absolute;
    right: 35px;
    width: fit-content;
    writing-mode: vertical-rl;
    text-orientation: sideways;
    transform: rotate(180deg) translateY(50px);
    white-space: nowrap;
}
</style>
