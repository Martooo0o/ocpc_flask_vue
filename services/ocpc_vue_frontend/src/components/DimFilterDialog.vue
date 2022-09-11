
<template>
    <div id="new_cube_wrapper">
        <div id="cube_form" class="card-4">
            <h3 class="card-4">New Filter</h3>

            <button id="close_btn" @click="onClose" class="card-4">X</button>

            <div class="filter_attr">
                <label>Materialiasation</label>
                <Select ref="mat" :options="['Existence', 'All']" @select="onSelectMat"></Select>
            </div>
           
           <div class="filter_attr">
                <label>Dimension 1</label>
                <SelectDimen :dimens="dimens" @select="onSelectDim1"></SelectDimen>
           </div>
           
            <div class="filter_attr">
                <label>Dimension 2</label>
                <SelectDimen :dimens="dimens" @select="onSelectDim2"></SelectDimen>
            </div>

            <div id="error_div" v-if="this.error !== '' || this.error === ''">{{this.error}}</div>

            <div id="table_wrapper" class="cube-table-wrapper card-4">
                <table id="logs_table" ref="logsTable" v-if="this.type1 !== undefined">
                    <tr >
                        <td></td>
                        <!-- <td :key="dimV" v-for="dimV in new Set(Object.keys(JSON.parse(this.currCube[(mat == 'Existence') ? 'freq_existence':'freq_all'])[this.dim1 + ',' + this.dim2]).map(x => x.split(',')[0]))">{{dimV}}</td> -->
                         <td :key="dimV" v-for="dimV in dim1Values">{{dimV}}</td>
                    </tr>
                    <!-- <tr :key="dimV" v-for="dimV in new Set(Object.keys(JSON.parse(this.currCube[(mat == 'Existence') ? 'freq_existence':'freq_all'])[this.dim1 + ',' + this.dim2]).map(x => x.split(',')[1]))"> -->
                    <tr :key="dimV2" v-for="dimV2 in dim2Values">
                        <td>{{dimV2}}</td>
                        <!-- <td @click="onSelectTD($event)" :key="dimV2" v-for="dimV2 in new Set(Object.keys(JSON.parse(this.currCube[(mat == 'Existence') ? 'freq_existence':'freq_all'])[this.dim1 + ',' + this.dim2]).map(x => x.split(',')[0]))"> -->
                        <td @click="onSelectTD($event)" :key="dimV" v-for="dimV in dim1Values">
                            <!-- {{JSON.parse(this.currCube[(mat == 'Existence') ? 'freq_existence':'freq_all'])[this.dim1 + ","+ this.dim2][dimV2 + "," + dimV]}} -->
                            {{currDimens[dimV + "," + dimV2]}}
                            <!-- {{Object.keys(this.currDimens)[this.dim1 + ","+this.dim2][dimV + "," +dimV2]}} -->
                        </td>
                    </tr>
                </table >
            </div>

            <Button txt="Save Filter" @click="onSaveFilter()"></Button>
        
        </div>
    </div>
</template>

<script>
import Button from './ui/Button.vue';
import TextInput from './ui/TextInput.vue';
import LogSelector from './LogSelector.vue';
import DimSelector from './DimSelector.vue';
import Select from './ui/Select.vue';
import SelectDimen from './ui/SelectDimen.vue';
import { mapActions, mapGetters } from 'vuex';
// import { defineComponent } from '@vue/composition-api'
export default {
    data(){
        return {
            active : "name",
            type1: undefined,
            selections:[],
            error: ""
        }
    },
    name: 'DimFilterDialog',
    components: {
    Button,
    TextInput,
    LogSelector,
    DimSelector,
    Select,
    SelectDimen
},
props: {
        // txt: String,
        // color: String
        dimens: Object
    },
     computed: {
        ...mapGetters({
            currDimens: 'main/currDimens',
            currCube: 'main/specCube',
        }),
        dim1Values(){
            let stuff = new Set(Object.keys(this.currDimens).map(x => x.split(',')[0]))
            return stuff
        },
        dim2Values(){
            let stuff = new Set(Object.keys(this.currDimens).map(x => x.split(',')[1]))
            return stuff
        }

    },
    methods: {
        ...mapActions({
            getDims: 'main/getCubeDimens'
        }),
        created(){
            this.mat = "";
            this.type1 = "";
            this.type2 = "";
            this.dim1="";
            this.dim2="";
            this.selections=[];
            this.error="";
        },
        onSelectTD(event){
            let target = event.currentTarget
            console.log(target); // returns 'foo'
            console.log(this.selections);
            console.log("Cell index: " + target.cellIndex)

            let row = target.parentElement;
            console.log(row);
            console.log("Row Index: " + row.rowIndex);

            let table = row.parentElement;
            console.log(table);

            let dim1 = table.rows[0].cells[target.cellIndex].innerHTML;
            let dim2 = table.rows[row.rowIndex].cells[0].innerHTML;
            
            console.log(this.selections.includes([dim1, dim2]))

            if(this.selections.includes(dim1 + "," +dim2) || this.selections.includes(dim2 + "," + dim1)){
                target.style.backgroundColor = "#FFFFFF";
                this.selections.splice(dim1 + "," + dim2, 1);
                //this.selections.splice(dim2 + "," + dim1, 1);
                console.log(this.selections) 
            }else{
                target.style.backgroundColor = "#888888";
                // this.selections.remove([dim1, dim2]);
                this.selections.push(dim1 + "," +dim2);
                console.log(this.selections)
            }
            // let tableData = document.
        },
        onCreateCube(){
            if(this.active === 'name'){
                this.active = "log";
            }else if(this.active === 'log'){
                this.active = "dim";
            }else{
                this.$emit('create-filter', "cube")
            }
        },
        onSelectNav(nav){
            this.active = nav;
        },
        onClose(){
            this.$emit('close-new-filter')
        },
        onSaveFilter(){
            console.log("works");
            console.log(this.selections);
            if(this.mat === undefined){
                this.error = "You need to select at least materialisation!"
                return;
            }
            else if(this.dim1 === undefined && this.dim2 === undefined){
                this.error = "You need to select at least one dimension!"
                return;
            }else if(this.selections.length === 0){
                // console.log("Selections is null");
                this.error = "Please select at least one value pair from the table!"
                console.log(this.error);
                // this.error = "Please select at least one value pair from the table!";
                return;
            }else{
                this.error = "";
            }
            this.$emit('create-filter', this.type1 ,this.dim1, this.type2, this.dim2, this.selections, this.mat)
        },
        async onSelectDim1(value, type){
            console.log(value)
            console.log(type)
            this.type1 = type;
            this.dim1 = value;    
            await this.displayTable();
        },
        async onSelectDim2(value, type){
            console.log(value)
            console.log(type)
            this.type2 = type;
            this.dim2 = value;
            await this.displayTable();
        },
        async onSelectMat(value){
            // let mat = this.$refs['mat']
            console.log(value)
            this.mat = value;
            if(value !="" && 
            ( (this.dim1!= undefined && this.dim1!="") || (this.dim2!=undefined && this.dim2!=""))){
                console.log(this.dim1)
                console.log(this.dim2)
                await this.displayTable();
            }
        },
        async displayTable(){
            let localType1 = this.type1;
            let localType2 = this.type2;
            let localDim1 = this.dim1;
            let localDim2 = this.dim2;
            if(localType2 === "" || localType2 == undefined){
                localType2 = localType1;
                localDim2 = localDim1;
            }
            else if(localType1 === "" || localType1 == undefined){
                localType1 = localType2;
                localDim1 = localDim;
            }
            this.getDims({cubename: this.currCube.cube, mat: this.mat, dim1: localDim1, dim2: localDim2})
        }
    },
    emits:['create-filter', 'close-new-filter'],
    created(){
        this.active = "name";
        this.overviewTables = {0:{}}
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
    #home_icon{
        width: 20px;
        height: 20px;
    }
    header{
        display: flex;
        justify-content: space-between;
        align-content: center;
        margin: 0 0 20px 0;
        background-color: #333333;
        vertical-align: middle;
        position: fixed;
        width: 100%;
        top:0px;
        z-index: 10;
    }
    #ocel_logo{
        widows: 100px;
        height: 100px;
        scale: 0.75;
    }

    nav {
    width: fit-content;
    font-size: 20px;
    text-align: center;
    position: relative;
    height: 59px;
    border-radius: 10px;
    display: block;
    border: 2px solid #E6B656;
    padding: 0;
    margin: 20px auto 0 auto;
    background: #E6B656;
    }
    nav a:nth-of-type(3n+1){
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
    }
    nav a:nth-last-of-type(3n+1){
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
    }

    nav a{
        background-color: white;
        width: 100px;
        text-decoration: none;
        color: lighgray;
        margin: 0;
        position: relative;
        top: 50%;
        -ms-transform: translateY(-50%);
        transform: translateY(-50%);
        display: inline-block;
        padding: 1rem 2rem;
        border-left: 1px solid var(--color-border); 
    }

    nav a.active {
    color: var(green);
    font-weight: bolder;
    background-color: #E6B656;
    color: white;
    }

    nav a:hover {
    background-color: #E6B656;
    color:white;
    }

    nav a:first-of-type {
    border: 0;
    }
    #new_cube_wrapper{
        position: fixed;
        width: 100%;
        top:0px;
        left:0px;
        padding-top:100px;
        background: #33333399;
        height: calc(100% + 100px);
        z-index: 20;
        transform: translate(0, -100px);
    }
    #cube_form{
        position: relative;
        margin: 0 50px;
        height: fit-content;
        min-height: 470px;
        top: 120px;
        background: #CCCCCC;
        border-radius: 10px;
        padding-bottom:  10px;
    }
    /* #contents_wrap{
        margin-bottom: 40px;
    } */
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


    /* Inout design */

</style>
