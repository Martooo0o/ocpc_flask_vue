<template>
    
    <div class="wrap" id="logs_vis" @click="onClick()" >
        <h3 class="card-4">Logs</h3>
        <div class="table_wrapper">
             <table class="logs_table" ref="table"  v-if="data!==undefined">
                <tr >
                    <th :key="column" v-for="column in Object.keys(data)">{{column}}</th>
                </tr>
                <tr :key="row" v-for="row in Object.keys(data['event_id'])">
                    <td :key="column" v-for="column in Object.keys(data)">{{data[column][row]}}</td>
                </tr>
            </table>
        </div>
    </div>
</template>

<script>
import Button from '../ui/Button.vue';
import Select from '../ui/Select.vue';
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "LogVisualisation",
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
        // let tableEl = this.$refs.table
        // console.log(this.data)
        // if(this.data!== undefined){
        //     // HEADER
        //     let row = tableEl.insertRow(0);
        //     for(var i=0;i<Object.keys(this.data).length;i++){
        //         let cell = row.insertCell(i)
        //         cell.innerHTML = Object.keys(this.data)[i]
        //     }
        // }   
    },
    components: { Button, Select },
    emits: ['select-analysis']
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

/* Log Vis. Styles */
.table_wrapper{
    height: calc(100% - 56px);
    width: calc(100% - 20px);
    margin: 10px;
    background: white;
    border-radius: 10px;
    overflow: scroll;
}
.logs_table{
   
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

table{
     border-spacing:0; /* Removes the cell spacing via CSS */
     border-collapse: collapse;
}

.logs_table caption{
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
.logs_table th{
    padding:5px 10px;
    font-weight: normal;
}

.logs_table th:not(:last-child){
    border-right: 1px solid #cccccc;
}

.logs_table td:not(:last-child){
    border-right: 1px solid #888888;
}

.logs_table thead tr {
    background-color: #00549F;
    color: #ffffff;
    text-align: center;
    font-weight: normal;
    padding-bottom: 5px;
    font-family: 'Roboto', sans-serif;
}

.logs_table tr:not(:last-child) {
    border-bottom: 1px solid #888888;
}

.logs_table, .logs_table tbody,.last-row {
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}
.last-row td:first-child{
    border-bottom-left-radius: 10px;
}

.last-row td:last-child{
    border-bottom-right-radius: 10px;
}

.logs_table input{
    float: left;
    display: inline-block;
} 

.logs_table div{
    clear: left;
    display: inline-block;
}
.logs_table td{
    height:100%;
    padding: 5px;
    font-family: 'Roboto', sans-serif;
}
</style>
