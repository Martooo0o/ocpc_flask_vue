
<template>
    <div id="new_cube_wrapper">
        <div id="cube_form" class="card-4">
            <h3 class="card-4">New Itemset Filter</h3>

            <button id="close_btn" @click="onClose" class="card-4">X</button>
            
            <div id="selections_wrapper">
                <FreqDimSelector @selection-changed="displayTable" :notifySelection="true" ref="selections" :attrs="this.currCube.dimens" :selected="{}" ></FreqDimSelector>
            </div>

            <div id="slider_wrapper">
                <div class="slidecontainer">
                    <label class="slider_label">Set Size: </label>
                    <input @change="onChangeSetSize($event)" type="range" min="1" max="20" :value="visualisation!=undefined?visualisation['edge_threshold']:''" class="slider" id="myRange">
                </div>
    
                <div class="slidecontainer">
                    <label class="slider_label">Min. Support: </label>
                    <input @change="onChangeMinSupp($event)" type="range" min="1" max="20" :value="visualisation!=undefined?visualisation['edge_threshold']:''" class="slider" id="myRange">
                </div>
            </div>

            <div class="table_wrapper">
                <table class="freq_items_table" ref="table"  v-if="tableData!==undefined">
                    <thead v-if="tableData!==undefined && tableData.length">
                        <tr>
                            <td>Set Size</td>
                            <td>Set</td>
                            <td>Support</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr :key="set" v-for="set in tableData" @click="onSelectTR">
                            <!-- <td :key="column" v-for="column in Object.keys(data)">{{data[column][row]}}</td> -->
                            <td>{{set[0]}}</td>
                            <td>{{set[1]}}</td>
                            <td>{{set[2]}}</td>
                        </tr> 
                    </tbody>
                </table>
            </div>

            <Button txt="Save Filter" @click="onSaveFilter()"></Button>
        
        </div>
    </div>
</template>

<script>
import Button from '../ui/Button.vue';
import TextInput from '../ui/TextInput.vue';
import Select from '../ui/Select.vue';
import SelectDimen from '../ui/SelectDimen.vue';
import FreqDimSelector from '../FreqDimSelector.vue'
import { mapActions, mapGetters } from 'vuex';
// import { defineComponent } from '@vue/composition-api'
export default {
    data(){
        return {
            type1: undefined,
            error: ""
        }
    },
    name: 'ItemsetFilterDialog',
    components: {
    Button,
    TextInput,
    Select,
    SelectDimen,
    FreqDimSelector
},
props: {
        // txt: String,
        // color: String
        dimens: Object,
        tableData: Object
    },
     computed: {
        ...mapGetters({
            currDimens: 'main/currDimens',
            currCube: 'main/specCube',
            aFilterData: 'main/currAnalysisFilterData'
        }),
        dimValues(){
            let freqAll = JSON.parse(this.currCube['freq_all']);
            return Set(Object.keys(freqAll[this.type1 + ',' + this.type2][this.dim1 + ',' + this.dim2]).map(x => x.split(',')[0]))
        }

    },
    methods: {
        ...mapActions({
            getDims: 'main/getCubeDimens',
            resetTable: 'main/resetCurrAFilterData'
        }),
        onSelectTR(event){
            let target = event.currentTarget
            console.log(target); // returns 'foo'
            console.log(this.selections);

            let row = target;
            console.log(row);
            console.log("Row Index: " + row.rowIndex);

            let rowIndex = parseInt(row.rowIndex);
            console.log(rowIndex);
            console.log(typeof(rowIndex))

            let table = row.parentElement;
            console.log(table);
            console.log(this.aFilterData)
            console.log(this.aFilterData[rowIndex-1][1])
            console.log(this.selections.includes(this.tableData[rowIndex-1][1]))
            
            if(this.selections.includes(this.tableData[rowIndex-1][1])){
                target.style.backgroundColor = "#FFFFFF";
                this.selections.splice(this.tableData[rowIndex-1][1], 1);
                //this.selections.splice(dim2 + "," + dim1, 1);
                console.log(this.selections) 
            }else{
                target.style.backgroundColor = "#AAAAAA";
                // this.selections.remove([dim1, dim2]);
                this.selections.push(this.tableData[rowIndex-1][1]);
                console.log(this.selections)
            }
            // let tableData = document.
        },
        onClose(){
            this.$emit('close-new-itemset-filter')
        },
        
        onChangeSetSize(event){
            console.log("Min Set Size Changed: ")
            console.log(event.target.value)
            this.set_size = event.target.value;
        },
        onChangeMinSupp(event){
            console.log("Min Support Changed: ")
            console.log(event.target.value)
            this.min_supp = event.target.value;
        },
        async displayTable(){
            // await this.getDims({cubename: this.currCube.cube, mat: this.mat, dim1: this.dim1, dim2: this.dim2})
            let selectedAttrs = this.$refs['selections'].dim_selections;
            console.log(selectedAttrs)
            let params = {'attrs': selectedAttrs,
            'min_supp': this.min_supp,
            'set_size': this.set_size}
            this.$emit('new_params_for_fitems_filter', params)
        },
        onSaveFilter(){
            console.log("works");
            console.log(this.selections);
            // if(this.mat === undefined){
            //     this.error = "You need to select at least materialisation!"
            //     return;
            // }
            // else if(this.dim1 === undefined && this.dim2 === undefined){
            //     this.error = "You need to select at least one dimension!"
            //     return;
            // }else if(this.selections.length === 0){
            //     // console.log("Selections is null");
            //     this.error = "Please select at least one value pair from the table!"
            //     console.log(this.error);
            //     // this.error = "Please select at least one value pair from the table!";
            //     return;
            // }else{
            //     this.error = "";
            // }
            let selectedAttrs = this.$refs['selections'].dim_selections;
            console.log(selectedAttrs);
            let params = {'selections': this.selections,
            'attrs': selectedAttrs}
            this.$emit('create-filter', params
            // , this.dim1, this.dim2, this.selections, this.mat
            )
        },
    },
    emits:['create-filter', 'close-new-itemset-filter', 'new_params_for_fitems_filter'],
    created(){
        this.min_supp = 0.01;
        this.set_size = 0;
        this.selections = [];
        this.resetTable();
    }
}

function onEditCubeDimen(index){
	var name = overviewTables[index]['nameSelect']; 
	var mat = overviewTables[index]['materialSelect'];
	var dim1 = overviewTables[index]['dim1Select'];
	var dim2 = overviewTables[index]['dim2Select'];
	let timeHierarchy = overviewTables[index]['timeHierarchy'];
	var table = overviewTables[index]['table'];
	console.log("Dimen changed on: " + index);
	console.log(mat.value)
	if(typeof(mat.value) == 'undefined' || mat.value == 'none'){
		table.innerHTML = "";
		return;
	}

	if( ( (typeof(dim1.value)=='undefined') || (dim1.value == "") || (dim1.value == " ") ) 
		&& ( (typeof(dim2.value)=='undefined') || (dim2.value == "") || (dim2.value == " ") ) ){
		table.innerHTML = "";

	}
	else if( (((typeof(dim1.value)=='undefined') || (dim1.value == "") || (dim1.value == " ") )
		&& !( (typeof(dim2.value)=='undefined') || (dim2.value == "") || (dim2.value == " ") ) )) {
		console.log("Only d2 has value");
		dimen_values = new Set();
		pair = [dim2.value, dim2.value]
		material = mat.value.toLowerCase();
		//TODO add materualisations here
		all_cubes[name.value][material][pair][(dim2.value + "_values")].forEach(function(value){dimen_values.add(value)});
		dimen_values = Array.from(dimen_values);

		table.innerHTML = "";

		row1 = table.insertRow(0);
		header_cell1 = row1.insertCell(0);
		header_cell1.innerHTML = "Values";
		header_cell1.classList.add("table_heading");

		row2 = table.insertRow(1);
		header_cell2 = row2.insertCell(0);
		header_cell2.innerHTML = "Count";
		header_cell2.classList.add("table_heading");

		for( i = 0; i < dimen_values.length; i++){
			console.log("Index: " + i);
			cell1 = row1.insertCell(i+1);
			cell1.innerHTML = dimen_values[i];
			cell1.classList.add("table_heading");

			cell2 = row2.insertCell(i+1);
			cell2.innerHTML = all_cubes[name.value][material][pair][ "value_pair_occur"][[dimen_values[i], dimen_values[i]]];
			cell2.onclick = function(){
				changedOverviewSelections(index, 2, i+1);
			};
		}
	}
	else if( !( (typeof(dim1.value)=='undefined') || (dim1.value == "") || (dim1.value == " ") )
		&& ( (typeof(dim2.value)=='undefined') || (dim2.value == "") || (dim2.value == " ") ) 
		|| 
		(!((typeof(dim1.value)=='undefined') || (dim1.value == "") || (dim1.value == " ") )
		&& !( (typeof(dim2.value)=='undefined') || (dim2.value == "") || (dim2.value == " ") )  
		&& dim1.value == dim2.value ) ) {
		console.log("Only d1 has value");
		dimen_values = new Set();
		pair = [dim1.value, dim1.value]
		material = mat.value.toLowerCase();

		all_cubes[name.value][material][pair][(dim1.value + "_values")].forEach(function(value){dimen_values.add(value)});
		dimen_values = Array.from(dimen_values);

		table.innerHTML = "";

		//header = cube1_table.insertRow();

		row = table.insertRow(0);
		cell = row.insertCell(0);
		cell.innerHTML = "Values";
		cell.classList.add("table_heading");
		cell = row.insertCell(1);
		cell.innerHTML = "Count";
		cell.classList.add("table_heading");

		// body = cube1_table.createTBody();
		for( i = 0; i < dimen_values.length; i++){
			row = table.insertRow(i+1);
			cell = row.insertCell(0);
			cell.innerHTML = dimen_values[i];
			cell.classList.add("table_heading");

			cell = row.insertCell(1);
			cell.innerHTML = all_cubes[name.value][material][pair][ "value_pair_occur"][[dimen_values[i], dimen_values[i]]];
			cell.onclick = function(){
				changedOverviewSelections(index, 2, i+1);
			};
		}
		dimen_values.forEach(function(dimen_value){
			row = table.insertRow(1);
			cell = row.insertCell(0);
			cell.innerHTML = dimen_value;
			cell.classList.add("table_heading");

			cell = row.insertCell(1);
			cell.innerHTML = all_cubes[name.value][material][pair][ "value_pair_occur"][[dimen_value, dimen_value]];
			cell.onclick = function(){
				changedOverviewSelections(index, 2, i+1);
			};
		});
	}
	else{ //IF BOTH DIMEN DROPDOWNS HAVE A VALUE
		console.log("Both dimens have value");
		let curr_cube = all_cubes[name.value];

		dimen1_values = new Set();
		pair = [dim1.value, dim1.value];
		material = mat.value.toLowerCase();
		all_cubes[name.value][material][pair][(dim1.value + "_values")].forEach(function(value){dimen1_values.add(value)});
		dimen1_values = Array.from(dimen1_values);

		dimen2_values = new Set();
		pair = [dim2.value, dim2.value];
		all_cubes[name.value][material][pair][(dim2.value + "_values")].forEach(function(value){dimen2_values.add(value)});
		dimen2_values = Array.from(dimen2_values);

		table.innerHTML = "";
		row = table.insertRow(0);
		cell = row.insertCell(0);
		cell.innerHTML = "";
		cell.classList.add("table_heading");

		//top row containing all values for Dimen2
		for(i = 0; i< dimen2_values.length; i++){
			cell = row.insertCell(i+1);
			cell.innerHTML = dimen2_values[i];
			cell.classList.add("table_heading");
		}

		//rest of rows beginning with a value
		for(let i = 0; i< dimen1_values.length; i++){
			row = table.insertRow(i+1);
			cell = row.insertCell(0);
			cell.innerHTML = dimen1_values[i];
			cell.classList.add("table_heading");
			for(let j = 0;j< dimen2_values.length;j++){
				cell = row.insertCell(j+1);
				// console.log(Object.keys(curr_cube[material]));
				let attr_pair = Object.keys(curr_cube[material]).includes(dim1.value + ',' + dim2.value)?dim1.value + ',' + dim2.value:dim2.value + ',' + dim1.value;
				let value_pair = Object.keys(curr_cube[material]).includes(dim1.value + ',' + dim2.value)?[dimen1_values[i], dimen2_values[j]] : [dimen2_values[j], dimen1_values[i]];
				cell.innerHTML = typeof(curr_cube[material][attr_pair]["value_pair_occur"][value_pair])=="undefined"? "0": curr_cube[material][attr_pair]["value_pair_occur"][value_pair];
				cell.onclick = function(){
					changedOverviewSelections(index, i+1, j+1);
				};
			}
		}
	}	
}
function changedOverviewSelections(index, row, column){
	let tableDOM = overviewTables[index];
	let tableCube = all_cubes[tableDOM['nameSelect'].value];

	let dim1 = tableDOM['dim1Select'].value;
	console.log('Cell Dim1: ' + dim1);
	let dim2 = tableDOM['dim2Select'].value;
	console.log('Cell Dim2: ' + dim2);

	let cellD1Value = tableDOM['table'].rows[row].cells[0].innerHTML;
	console.log('Cell Dim1 Value: ' + cellD1Value);
	let cellD2Value = tableDOM['table'].rows[0].cells[column].innerHTML;
	console.log('Cell Dim2 Value: ' + cellD2Value);
	let cellD1D2 = tableDOM['table'].rows[row].cells[column];
	console.log('Cell Dim1 Dim2: ' + cellD1D2);

	let prevSelect = {};

	if(dim1!='ocel:activity' && dim2!='ocel:activity'){
		console.log('Info not associated with any activity');
		//return;
	}

	let newAct = (dim1=='ocel:activity'? dim1: dim2);
	let newNonAct = (dim1=='ocel:activity'? dim2: dim1);
	let newActValue =  (dim1=='ocel:activity'? cellD1Value: cellD2Value);
	let newNonActValue =  (dim1=='ocel:activity'? cellD2Value: cellD1Value);

	let pair = [newAct, newNonAct];
	let valuePair = [newActValue, newNonActValue];
	let occur = tableDOM['table'].rows[row].cells[column].innerHTML;

	//find pair index in overview selection
	let pairIndex = -1;
	for(var i=0;i<overviewSelections[index].length; i++){
		console.log(overviewSelections[index][i]);
		console.log(overviewSelections[index][i].equals([row, column]));
		if(typeof(overviewSelections[index][i]) != 'undefined'
		&& overviewSelections[index][i].equals([row, column])){
			pairIndex = i;
		}
	}

	//add remove selection
	if(pairIndex==-1){
		overviewSelections[index].push([row, column]);
		cellD1D2.style.backgroundColor = '#22ff22';
	}else{
		overviewSelections[index].splice([row, column], 1);
		cellD1D2.style.backgroundColor = 'transparent';
		console.log('Removed');
	}
	console.log(overviewSelections);
}
</script>

<style scoped>
    h3{
        border-bottom-right-radius: 10px;
        border-bottom-left-radius: 10px;
        margin: 0 auto;
    }
    #close_btn{
        position: absolute;
        top: 10px;
        left: 10px;
        background: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        height: 40px;
        width: 40px;
        font-size: large;
        color: gray;
    }
    #close_btn:hover{
        position: absolute;
        top: 10px;
        left: 10px;
        font-weight: bolder;
        background: #E6B656;
        border: none;
        border-radius: 10px;
        padding: 10px;
        height: 40px;
        width: 40px;
        font-size: large;
        color: white;
    }
    #new_cube_wrapper{
        position: fixed;
        width: 100%;  
        top:0px;
        left:0px;
        padding-top:100px;
        background: #33333399;
        height: calc(80% + 100px);
        z-index: 20;
        transform: translate(0, -100px);
    }
    #cube_form{
        position: relative;
        margin: 0 50px;
        height: fit-content;
        min-height: 470px;
        max-height: 80%;
        top: 120px;
        background: #CCCCCC;
        border-radius: 10px;
        padding-bottom:  10px;
        overflow-y: scroll;
    }
    #selections_wrapper{
        position: relative;
        margin-top: 40px;
    }

    #btn{
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
    }
    .filter_attr {
        width: fit-content;
        display: inline-block;
        margin: 20px 0;
    }
    label{
        display: block;
    }
    #logs_table{
        width: calc(100% - 40px);
        background: white;
        /* border-radius: 10px; */

    }

    .cube-table-wrapper{
    width: 95%;
    overflow-y: auto;    /* Trigger vertical scroll    */
    overflow-x: auto;  /* Hide the horizontal scroll */
    background:  #DDDDDD;
    height:400px;
    margin: 20px auto 0 auto;
    /* border-radius: 10px;
    -webkit-border-radius: 10px;
-moz-border-radius: 10px; */
    overflow-x: scroll;
    overflow-y: scroll;
}
.cube-table{
	border: 1px solid #888888;
	/* border-radius: 10px; */
}
.cube-table-wrapper td, .cube-table-wrapper th{
	width: 100px;
	text-align: center;
	border: 1px solid #888888;
}
.cube-table-wrapper th{
	background: #00549F;
    color: white;
}

.table_heading{
	background-color: #00549F;
    color: #ffffff;
    text-align: center;
    font-weight: bold;
    padding-bottom: 5px;
    font-family: 'Roboto', sans-serif;
    padding: 5px;
}
Button{
    margin-top: 15px;
}
#error_div{
    color: #ff222288
}


/* Slider Design */
#slider_wrapper{
    position: relative;
    width: 100%;
}

.slidecontainer{
    position: relative;
    display: inline-block;
    width: 50%;
}

.slider {
  -webkit-appearance: none;
  width: calc(100% - 60px);
  height: 15px;
  border-radius: 5px;   
  background: #e3e3e3;
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

.table_wrapper{
    margin: 20px 0;
}

table{
     border-spacing:0; /* Removes the cell spacing via CSS */
     border-collapse: collapse;
     margin: 0 auto;
     background: white;
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
    border-top-right-radius: 10px;
    border-top-left-radius: 10px;
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

</style>
