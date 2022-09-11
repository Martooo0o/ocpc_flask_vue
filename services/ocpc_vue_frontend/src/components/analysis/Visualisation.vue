<template>
    
    <div class="item_a"  >
      <LogVisualisation v-if="visType === 'log'" :data="aVisData[this.visualisation.index]" id="logs_vis" ></LogVisualisation>
      
      <DFGVisualisation v-if="visType === 'dfg'" 
      :visualisation="this.visualisation" 
      :data="aVisData[this.visualisation.index]"
      @dfg_props_changed="(props) => this.$emit('dfg_props_changed', props)"></DFGVisualisation>

      <FreqItemsVisualisation v-if="visType === 'freq_items'" 
      :visualisation="this.visualisation" 
      :data="aVisData[this.visualisation.index]" 
      @edit-freq-attrs="this.$emit('edit-freq-attrs')"
      @fitems_props_changed="(props) => this.$emit('fitems_props_changed', props)"
      ></FreqItemsVisualisation>

      <AssocRulesVisualisation 
        v-if="visType === 'ass_rules'"
        :visualisation="this.visualisation" 
        :data="aVisData[this.visualisation.index]" 
        @edit-freq-attrs="this.$emit('edit-freq-attrs')"
        @assoc_rules_props_changed="(props) => this.$emit('assoc_rules_props_changed', props)"
        >
        </AssocRulesVisualisation>
    </div>
     <div class="close_btn card-4" @click="deleteVis">
        X
    </div>
</template>

<script>
import Button from '../ui/Button.vue';
import Select from '../ui/Select.vue';
import { mapActions, mapGetters } from 'vuex';
import LogVisualisation from './LogVisualisation.vue';
import DFGVisualisation from './DFGVisualisation.vue';
import FreqItemsVisualisation from './FreqItemsVisualisation.vue';
import AssocRulesVisualisation from './AssocRulesVisualisation.vue';
// import { emit } from 'process';
export default {
    name: "Visualisation",
    data(){
        return {
            // visualisation : {},
        }
    },
    props: {
        visualisation: Object
    },
    methods: {
         ...mapActions({
            setFilters: 'main/setAFilters',
            setVis: 'main/setAVis',
            // getFLog: 'main/getFlattenedLog',
            // getDFG: 'main/getDFG'
        }),
        onClick(name) {
            console.log("Selected ItemLog: " + this.name)
            this.$emit('select-analysis', this.name)
        },
        async deleteVis(){
            // this.aVisData.splice(this.visualisation.index)
            // setVis()

            let eA = {}
            eA['name'] = this.currentAnalysis['name']
            if(this.currentAnalysis['visualisations'] == []){
                eA['visualisations'] = []
            }else{
                console.log(this.currentAnalysis['visualisations'])
                eA['visualisations'] = this.currentAnalysis['visualisations']
                console.log(typeof(eA['visualisations']))
            }

            eA['visualisations'].splice(this.visualisation.index)
            console.log(eA)
            await this.setVis(eA)
        }
        // async getFlattenLog(){
        //     // await this.getFLog({
        //     //     'analysisname': params["analysisame"]
        //     // // , 'type': params['type']
        //     // })
        // }
    },
    computed: {
        ...mapGetters({
            aVisData: 'main/currAnalysisVisData',
            currentAnalysis: 'main/currAnalysis',
        }),
        dimValues(){
            return this.filter.selections
        },
        visType(){
            return this.visualisation.type
        }
    },
    created(){
        console.log("New Vis created")
        console.log(this.visualisation)
        console.log("Vis Data")
        console.log(this.aVisData)
        if(this.visualisation.type === "log"){
            console.log("Vis Index")
            console.log(this.visualisation.index)
            this.$emit('get-flat-log', this.visualisation.index)
        }
        else if(this.visualisation.type === "dfg" && this.visualisation.dfg_type !== undefined){
            console.log("Vis Index")
            console.log(this.visualisation.index)
            this.$emit('get-dfg', this.visualisation.index)
        }else if(this.visualisation.type === "freq_items"){
            console.log("Vis Index")
            console.log(this.visualisation.index)
            this.$emit('get-freq-items', this.visualisation.index)
        }
        else if(this.visualisation.type === "ass_rules"){
            console.log("Vis Index")
            console.log(this.visualisation.index)
            this.$emit('get-ass-rules', this.visualisation.index)
        }
    },
    components: { Button, Select, LogVisualisation, DFGVisualisation, FreqItemsVisualisation, AssocRulesVisualisation},
    emits: ['select-analysis', 'get-flat-log', 'get-dfg', 'edit-freq-attrs', 'get-freq-items', 'dfg_props_changed', 'fitems_props_changed', 'assoc_rules_props_changed, get-ass-rules']
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
.item_a{
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

/* Log Vis. Styles */
.logs_table{
   height: calc(100% - 118px);
    width: calc(100% - 20px);
    margin: 10px;
    background: white;
    border-radius: 10px;
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

/* Freq Items Vis. Styles */
.freq_settings_wrap{
    width: 100%;
    height: calc(35% - 36px);
    background: white;
}
.selected_attrs{
    width: 50%;
    height: 100%;
    background: red;
    display: inline-block;
}
.freq_sliders{
    width: 50%;
    height: 100%;
    background: orange;
    display: inline-block;
    position: relative;
}
.freq_items_table{
     width: 100%;
    height: calc(75% - 56px);
    background: green;
    position: relative;
    border-radius: 10px;
}
</style>
