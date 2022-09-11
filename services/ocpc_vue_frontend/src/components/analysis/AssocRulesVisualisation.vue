<template>
    <div class="wrap">
        <h3 class="card-4">Association Rules</h3>
        <div class="freq_settings_wrap">
            <div id="container">
                <div id="dummy"></div>
                <div id="element">
                    <div class="vert_slidecontainer" id="slider1">
                        <label class="slider_label">Min. Set Size: {{visualisation['set_size']}}</label>
                        <input @change="onChangeSetSize($event)" type="range"  min="1" max="10" :value="visualisation['set_size']" class="vert_slider" id="myRange">
                    </div>

                    <div class="vert_slidecontainer" id="slider2">
                        <label class="slider_label">Min. Support: {{visualisation['min_supp']}}</label>
                        <input @change="onChangeSupp($event)" type="range"  min="0.01" max="1" step="0.01" :value="visualisation['min_supp']" class="vert_slider" id="myRange">
                    </div>

                     <div class="vert_slidecontainer" id="slider3">
                        <label class="slider_label">Min. Conf.: {{visualisation['min_conf']}}</label>
                        <input @change="onChangeConf($event)" type="range"  min="0.01" max="1" step="0.01" :value="visualisation['min_conf']" class="vert_slider" id="myRange">
                    </div>

                     <div class="vert_slidecontainer" id="slider4">
                        <label class="slider_label">Min. Lift: {{visualisation['min_lift']}}</label>
                        <input @change="onChangeLift($event)" type="range"  min="0.01" max="1" step="0.01" :value="visualisation['min_lift']" class="vert_slider" id="myRange">
                    </div>
                </div>
            </div>
             <div class="selected_attrs">
                <FreqAttrsDisplay :dimens="this.visualisation.attrs" @edit-freq-attrs="this.$emit('edit-freq-attrs')"></FreqAttrsDisplay>
            </div>
        </div>
        <div class="table_wrapper">
             <table class="freq_items_table" ref="table"  v-if="data!==undefined">
                <thead v-if="data!==undefined && data.length">
                    <tr>
                        <td>Set Size</td>
                        <td>Antecedents</td>
                        <td>Consequents</td>
                        <td>Support</td>
                        <td>Confidence</td>
                        <td>Lift</td>
                    </tr>
                </thead>
                <tbody>
                    <tr :key="set" v-for="set in data">
                        <!-- <td :key="column" v-for="column in Object.keys(data)">{{data[column][row]}}</td> -->
                        <td>{{set[0]}}</td>
                        <td>{{set[1]}}</td>
                        <td>{{set[2]}}</td>
                        <td>{{set[3]}}</td>
                        <td>{{set[4]}}</td>
                        <td>{{set[5]}}</td>
                    </tr> 
                </tbody>
            </table>
        </div>
        <!-- <table class="freq_items_table"></table> -->
    </div>
</template>

<script>
import Button from '../ui/Button.vue';
import Select from '../ui/Select.vue';
import { mapActions, mapGetters } from 'vuex';
import FreqAttrsDisplay from './FreqAttrsDisplay.vue';
export default {
    name: "AssocRulesVisualisation",
    props: {
        visualisation: Object,
        data: Object
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
        onChangeSetSize(event){
            let selectedValue = event.target.value
            console.log("Selected Min Conf: " + selectedValue)
            let props = {}
            props['set_size'] = selectedValue
            console.log(this.visualisation)
            props['min_supp'] = this.visualisation['min_supp']
            props['min_conf'] = this.visualisation['min_conf']
            props['min_lift'] = this.visualisation['min_lift']
            props['attrs'] = this.visualisation['attrs']
            
            console.log("Assoc_Rules_vis: ")
            console.log(props)
            this.$emit('assoc_rules_props_changed', props)
        },
        onChangeSupp(event){
             let selectedValue = event.target.value
            console.log("Selected Min Conf: " + selectedValue)
            let props = {}
            props['min_supp'] = selectedValue
            console.log(this.visualisation)
            props['min_conf'] = this.visualisation['min_conf']
            props['min_lift'] = this.visualisation['min_lift']
            props['attrs'] = this.visualisation['attrs']
            props['set_size'] = this.visualisation['set_size']
            
            console.log("Assoc_Rules_vis: ")
            console.log(props)
            this.$emit('assoc_rules_props_changed', props)
        },
        onChangeConf(event){
            let selectedValue = event.target.value
            console.log("Selected Min Conf: " + selectedValue)
            let props = {}
            props['min_conf'] = selectedValue
            console.log(this.visualisation)
             props['min_supp'] = this.visualisation['min_supp']
              props['min_lift'] = this.visualisation['min_lift']
            props['attrs'] = this.visualisation['attrs']
            props['set_size'] = this.visualisation['set_size']
            
            console.log("Assoc_Rules_vis: ")
            console.log(props)
            this.$emit('assoc_rules_props_changed', props)
        },
        onChangeLift(event){
             let selectedValue = event.target.value
            console.log("Selected Min Conf: " + selectedValue)
            let props = {}
            props['min_lift'] = selectedValue
            console.log(this.visualisation)
            props['min_supp'] = this.visualisation['min_supp']
            props['min_conf'] = this.visualisation['min_conf']
            props['attrs'] = this.visualisation['attrs']
            props['set_size'] = this.visualisation['set_size']
            
            console.log("Assoc_Rules_vis: ")
            console.log(props)
            this.$emit('assoc_rules_props_changed', props)
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
        console.log(this.visualisation)
        console.log(this.visualisation.attrs)
    },
    components: { Button, Select, FreqAttrsDisplay },
    emits: ['select-analysis', 'edit-freq-attrs', 'assoc_rules_props_changed']
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
#values_wrapper{
     display: inline-block;
    padding: 10px;
    width: calc(100% - 250px);
    position: relative;
    top: -15px;
    left: 170px;
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

h3{
    margin: 0 auto;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
.vert_slidecontainer {
    width: 70%;
    position: absolute;
    top: 45%;
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
    width: calc(100% - 10px);
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
    height: calc(35%);
    position: relative;
}
.selected_attrs{
    width: calc(100% - 185px);
    height: 100%;
    display: inline-block;
    position: absolute;
    left: 0;
    overflow-x: scroll;
}
.table_wrapper{
    height: calc(65% - 56px);
    width: calc(100% - 20px);
    margin: 10px;
    background: white;
    border-radius: 10px;
    overflow: scroll;
}

.freq_items_table{
    /* width: calc(100% - 20px);
    margin: 10px 10px 0 10px;
    
    background: white;
    position: relative;
    border-radius: 10px; */
}


#container {
  display: inline-block;
  position: absolute;
  right: 0;
  width: 50%;
}

#dummy {
  margin-top: 75%;
  /* 4:3 aspect ratio */
}

#element {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

#slider1{
    right: 10px;
}

#slider2{
    right: 55px;
}
#slider3{
    right: 100px;
}

#slider4{
    right: 145px;
}

table{
     border-spacing:0; /* Removes the cell spacing via CSS */
     border-collapse: collapse;
}

.freq_items_table caption{
    position: relative;
    background: #00549F;
    padding: 5px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    color: #FFFFFF;
    font-weight: bolder;
    margin-bottom: 0px;
    font-size: 20px;
    font-family: 'Roboto', sans-serif;
    border-bottom: 1px solid #cccccc;
}
.freq_items_table th{
    padding:5px 10px;
    font-weight: normal;
}

.freq_items_table th:not(:last-child){
    border-right: 1px solid #cccccc;
}

.freq_items_table td:not(:last-child){
    border-right: 1px solid #888888;
}

.freq_items_table thead tr {
    background-color: #E6B656;
    color: #ffffff;
    text-align: center;
    font-weight: normal;
    padding-bottom: 5px;
    font-family: 'Roboto', sans-serif;
}

.freq_items_table tr:not(:last-child) {
    border-bottom: 1px solid #888888;
}

.freq_items_table, .freq_items_table tbody,.last-row {
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}
.last-row td:first-child{
    border-bottom-left-radius: 10px;
}

.last-row td:last-child{
    border-bottom-right-radius: 10px;
}

.freq_items_table input{
    float: left;
    display: inline-block;
} 

.freq_items_table div{
    clear: left;
    display: inline-block;
}
.freq_items_table td{
    height:100%;
    padding: 5px;
    font-family: 'Roboto', sans-serif;
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
    right: 15px;
    width: fit-content;
    writing-mode: vertical-rl;
    text-orientation: sideways;
    transform: rotate(180deg) translateY(50px);
    white-space: nowrap;
}
</style>
