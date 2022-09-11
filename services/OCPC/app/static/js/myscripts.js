// import Splide from '@splidejs/splide';

let jsonFromFile, events, objects, objectEntries;
var allAttrs, eventAttrs, objectsAttrs, eventActivities;
let eventAttributes, objectTypes;

var list_of_tables;
var selections;

var all_cubes;
var cube; //used when creting new cube

var cubeName; //cube name input

/*Cube Overview Vars*/
var num_overviews, curr_num_overviews = 0;
var overview_tables_wrapper, overview_tables_wrapper_list;

let DEBUG = true;

var splide;

var overviewTables = {};
var overviewSelections = {};
var filteredOCELs;
var ocelDFGs;
var freqItemAttrs;
var freqDataSet;
var freqSetSelect = {};
var assocSetSelect = {};

var initialising = false;

var reader_result;
var loading_wrapper, loading_wrapper_title, loading_wrapper_desc;


/**************
OCEL DATA INPUT
***************/
document.getElementById('upload').addEventListener('change', handleFileSelect, false);
if(DEBUG){
	fetch('short_example_eventlog.jsonocel')
	  .then(response => response.text())
	  .then(text => {
	  	initVars(text);
	  	overviewTables = {};
	  	addOverviewTables(2);
	  })
}else{

}

if(Array.prototype.equals)
    console.warn("Overriding existing Array.prototype.equals. Possible causes: New API defines the method, there's a framework conflict or you've got double inclusions in your code.");
// attach the .equals method to Array's prototype to call it on any array
Array.prototype.equals = function (array) {
    // if the other array is a falsy value, return
    if (!array)
        return false;

    // compare lengths - can save a lot of time 
    if (this.length != array.length)
        return false;

    for (var i = 0, l=this.length; i < l; i++) {
        // Check if we have nested arrays
        if (this[i] instanceof Array && array[i] instanceof Array) {
            // recurse into the nested arrays
            if (!this[i].equals(array[i]))
                return false;       
        }           
        else if (this[i] != array[i]) { 
            // Warning - two different object instances will never be equal: {x:20} != {x:20}
            return false;   
        }           
    }       
    return true;
}
// Hide method from for-in loops
Object.defineProperty(Array.prototype, "equals", {enumerable: false});


function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // use the 1st file from the list
    f = files[0];
	console.log(f['name']);
	document.getElementById('fileselect_txt').innerHTML = f['name'];
    
    var reader = new FileReader();

    // Closure to capture the file information.
    reader.onload = (function(theFile) {
        return function(e) {
			reader_result = reader.result;
        	console.log(reader.result);
          	initVars(reader.result);
		  	let numTables = Object.keys(overviewTables).length;
		  	removeOverviewTables(numTables);
		  	overviewTables = {};
          	addOverviewTables(2);
		  	initSplideSlider()
        };
      })(f);

      // Read in the image file as a data URL.
      reader.readAsBinaryString(f);
}

/*Only creates data tables after initialisation is finished
* */
function createDataTables_safe(result){
	if(!initialising){
		  createDataTables(result);
		  loading_wrapper.style.opacity = 0.0;
		  loading_wrapper.style.visibility = 'hidden';
	//change text of loading screen as well
	}else{
		setTimeout(createDataTables_safe(result),500)
	}
}

/******************************
INITIALISATION OF VARS AND DOM
*******************************/
function json2array(json){
    var result = [];
    var keys = Object.keys(json);
    keys.forEach(function(key){
        result.push(json[key]);
    });
    return result;
}

function initVars(jsonStr){
	loading_wrapper = document.getElementById("loading_wrapper");
	loading_wrapper.style.visibility = 'visible';
	loading_wrapper.style.opacity = 1.0;
	loading_wrapper_title = document.getElementById("loading_title");
	loading_wrapper_desc = document.getElementById("loading_desc");
	loading_wrapper_title.innerHTML = "Importing OCEL";
	loading_wrapper_desc.innerHTML = "";
	//change text of loading screen as well

	console.log("Root: " + $SCRIPT_ROOT);
	jsonFromFile = JSON.parse(jsonStr);

	sendOcelToFlask(jsonStr);
	filteredOCELs = {};
	freqDataSet = {};
	freqItemAttrs = {};

	events = json2array(jsonFromFile['ocel:events']);
	objects = jsonFromFile['ocel:objects'];
	objectEntries = Object.entries(objects);
	eventAttributes = jsonFromFile['ocel:global-log']['ocel:attribute-names'];
	objectTypes = jsonFromFile['ocel:global-log']['ocel:object-types'];
	eventActivities = []; //TODO maiby initialised later while cube is created
	for(var e in Object.keys(events)){
		if(!eventActivities.includes(events[e]['ocel:activity'])){
			eventActivities.push(events[e]['ocel:activity']);
			console.log('added');
		}
	}
	console.log("Event Attributes: " + eventActivities);

	num_overviews = document.getElementById('num_overviews');
	num_overviews.onchange = function(){
		var selectedNum = num_overviews.value;
		console.log('Slected Num ' + selectedNum); 
		if(curr_num_overviews != selectedNum){
			if(getNumberOverviews()>selectedNum){
				// remove some tables
				console.log('Remove ' + (getNumberOverviews()-selectedNum) + ' tables');
				removeOverviewTables(getNumberOverviews()-selectedNum);
			}else{
			 	// add some tables
			 	console.log('Add ' + (selectedNum - curr_num_overviews) + ' tables');
			 	addOverviewTables(selectedNum - curr_num_overviews);
			}
			curr_num_overviews = selectedNum;
		}
	}

	selections = {};
	all_cubes = {};

	//set up event attributes
	eventAttrs = [];
	for(let i=0;i < events.length; i++){
		let keys = Object.keys(events[i]);
		const map1 = eventAttrs.map(x => x[0]);
		for(let j = 0; j< keys.length; j++){
			if( (!map1.includes(keys[j].substring(5))) && keys[j]!="ocel:omap" && keys[j]!="ocel:vmap"){
				eventAttrs.push([ keys[j].substring(5), events[i][keys[j]] ]);
			}else if( (!map1.includes(keys[j].substring(5))) && keys[j] == "ocel:vmap"){
				//console.log("VMAP: " + keys[j])
				let stuff = Object.keys(events[i][keys[j]]);
				//console.log(stuff)
				for(let k = 0; k<stuff.length;k++){
					if(!map1.includes(stuff[k])){
						eventAttrs.push([ stuff[k], events[i][keys[j]][stuff[k]] ]);
					}
				}
			}
		}
	}
	for(let i = 0; i<eventAttrs.length; i++){
		eventAttrs[i][0] = 'event_' + eventAttrs[i][0];
	}
	eventAttrs = eventAttrs.concat(objectTypes.map(x => [x, "-"]));

	//set up attributes for all other object types
	objectsAttrs = new Map();

	for(let i=0;i < objectEntries.length; i++){
		let keys = Object.keys(objectEntries[i][1]["ocel:ovmap"]);
		type = objectEntries[i][1]["ocel:type"];
		for(let j = 0; j< keys.length; j++){
			if(typeof(objectsAttrs.get(type)) == "undefined"){
				arr = new Array([keys[j], objectEntries[i][1]["ocel:ovmap"][keys[j]]]);
				objectsAttrs.set(type, arr);
			}else{
				// const array = objectsAttrs.get(type);
				const map1 = objectsAttrs.get(type).map(x => x[0]);
				arr = objectsAttrs.get(type);
				if(!map1.includes(keys[j])){
					arr.push([ keys[j], objectEntries[i][1]["ocel:ovmap"][keys[j]] ]);
					// objectsAttrs.remove(objects[i]);
					objectsAttrs.set(type, arr);
				}
			}
		}
	}

	cubeName = document.getElementById('fname');

	overview_tables_wrapper = document.getElementById('overview_tables_wrapper');
	overview_tables_wrapper_list = document.getElementById('overview_tables_wrapper_list');
	overviewSelections = {};

	// Get all elements with class="closebtn"
	var close = document.getElementsByClassName("closebtn");
	var i;

	// Loop through all close buttons
	for (i = 0; i < close.length; i++) {
	  // When someone clicks on a close button
	  close[i].onclick = function(){

	    // Get the parent of <span class="closebtn"> (<div class="alert">)
	    var div = this.parentElement;

	    // Set the opacity of div to 0 (transparent)
	    div.style.opacity = "0";

	    // Hide the div after 600ms (the same amount of milliseconds it takes to fade out)
	    setTimeout(function(){ div.style.display = "none"; }, 600);
	  }
	}
}

function sendOcelToFlask(jsonStr){
	$.get( $SCRIPT_ROOT + "/init_ocel", 
			{
				'ocel_str':  jsonStr,
			}
			).done(function( data ) {
				console.log(data.result);
				// displayFreqTable(index, data.result['data']);
				createDataTables_safe(reader_result);
			});			
}

/**********************
OCEL DATA VISUALISATION
***********************/

function createDataTables(jsonStr){
	document.getElementById("no-file-uploaded").style.display = "none";
	list_of_tables = document.getElementById('list_tables');
	list_of_tables.innerHTML = "";
	allTables = new Array();
	allTables.push("Events");
	allTables = allTables.concat(objectTypes)

	console.log('Tables: ' + allTables)
	allTables.forEach(function callbackFn(element, index) {
		var li = document.createElement('li');

		let num = document.createElement('div');
		let numTxt = document.createElement('label');
		getElementStats(element, numTxt);

		num.appendChild(numTxt);
		num.classList.add('num_stat');
		li.appendChild(num);

		var table = document.createElement('table');
		table.className = 'custom-table';
		var caption = document.createElement('caption');
		caption.id = 'caption_' + element;
		caption.innerHTML = ("" + element);
		table.appendChild(caption);

		//Create headers
		thead = document.createElement('thead');
		headers = document.createElement('tr');
		th = document.createElement('th');
		th.innerHTML = "";
		headers.appendChild(th);
		th = document.createElement('th');
		th.className = "headers"
		th.innerHTML = "Dimension";
		headers.appendChild(th);
		th = document.createElement('th');
		th.className = "headers"
		th.innerHTML = "Example";
		headers.appendChild(th);
		thead.appendChild(headers);
		table.appendChild(thead);

		let allAttrs;
		let tbody = document.createElement('tbody');
		tbody.id = 'body';
		if(element == "Events"){
			allAttrs = eventAttrs;
			var last_tr;
			allAttrs.forEach(function addRows(element1){
				tr = document.createElement('tr');
				td = document.createElement('td');
				var checkbox = document.createElement('input');
		        checkbox.type = "checkbox";
		        checkbox.value = 1;
		        checkbox.id = 'checkbox_' + "Events" + "_" + element1[0];
		        checkbox.onclick = function (){changedSelection("Events", element1[0])};
		       	var checkmark = document.createElement('span');
		       	checkmark.className = "checkmark";
		       	td.appendChild(checkbox);
		       	tr.appendChild(td);
				td = document.createElement('td');

		       	txtBox = document.createElement('div');
		       	txtBox.innerHTML = element1[0];
		       	txtBox.id = 'attr_' + "Events" + "_" + element1[0];
		       	td.appendChild(txtBox);

				tr.appendChild(td);
				last_tr = tr;
				td = document.createElement('td');
				td.innerHTML = element1[1];
				tr.appendChild(td);
				tbody.appendChild(tr);
			});
			last_tr.classList.add("last-row");
		}else{
			allAttrs = objectsAttrs;
			stored = objectsAttrs.get(element)
			if(typeof(stored) == "undefined") {return 0;} //behaves as continue
			var last_row;
			objectsAttrs.get(element).forEach(function(element1){
				tr = document.createElement('tr');
				td = document.createElement('td');
				var checkbox = document.createElement('input');
		        checkbox.type = "checkbox";
		        checkbox.value = 1;
		        checkbox.id = 'checkbox_' + element + "_" + element1[0];
		        checkbox.disabled = true;
		        checkbox.onclick = function (){changedSelection(element, element1[0])};
		       	td.appendChild(checkbox);
		       	tr.appendChild(td);
				td = document.createElement('td');

		       	txtBox = document.createElement('div');
		       	txtBox.id = 'attr_' + element + "_" + element1[0];
		       	txtBox.innerHTML = element1[0];
		       	td.appendChild(txtBox);

				tr.appendChild(td);
				td = document.createElement('td');
				td.innerHTML = element1[1];
				tr.appendChild(td);
				tbody.appendChild(tr);
				last_row = tr;
			});
			last_row.classList.add("last-row");
		}
		table.appendChild(tbody);
	
		

		li.appendChild(table);
		list_of_tables.appendChild(li);
	});

	newCubeBlock = document.getElementById('create_cube');
	newCubeBlock.style.visibility = "visible";
	newCubeBtn = document.getElementById('create_cube_btn');
	newCubeBtn.onclick = function(){
		createCube(cubeName.value);
	};
}

function getElementStats(element, obj){
	$.get( $SCRIPT_ROOT + "/get_stats" + '?' + performance.now(), 
			{
				// 'ocel_str':  jsonStr,
			}
			).done(function( data ) {
				console.log("Stats")
				console.log(data);
				if(element == 'Events'){
					obj.innerHTML = data['number-of-events'];
				}
				else{
					obj.innerHTML = data[element];
					loading_wrapper.style.opacity = 0.0;
				  	loading_wrapper.style.visibility = 'hidden';
				}
			});
}

function resetSelections(){
	selections = {};

	for(let i = 0;i<list_of_tables.childNodes.length;i++){
		let li = list_of_tables.childNodes[i];
		console.log('Li: ' + li);
		let table = list_of_tables.childNodes[i].childNodes[1];
		console.log('Table: ' + table);
		console.log(table.rows);
		for(let j=1;j<table.rows.length;j++){
			let row = table.rows[j];
			row.cells[0].childNodes[0].checked = false;
		}
	}
}

//used on click of the checkbox of an attribute in table
function changedSelection(tableName, attr){
	let txt = document.getElementById('attr_' + tableName + "_" + attr);
	let checkbox = document.getElementById('checkbox_' + tableName + "_" + attr);

	console.log("Attr", attr);
	//activate object table if selection is an objectType
	if(tableName == "Events" && Object.values(objectTypes).includes(attr)){
		//attr in this situation is the name of the table f.E. customers, items and so on 
		changeObjTableCheckboxesActivity(attr, checkbox.checked);
		return;
	}

	let previousSelections = new Array();
	if(typeof(selections[tableName]) != 'undefined'){
		previousSelections = selections[tableName];
	}

	if (checkbox.checked) {
	//add to selections
		previousSelections.push(txt.innerHTML);
		selections[tableName] =  previousSelections;
	} else {
	//remove from selections
		const index = previousSelections.indexOf(txt.innerHTML);
		if (index > -1) {
		  previousSelections.splice(index, 1);
		}

		selections[tableName] = previousSelections;
	}
	console.log([...Object.entries(selections)]);
}

/*Used to activate/deactivate attr checkboxes in object Tables when objectType from 'Events' table is selected*/
function changeObjTableCheckboxesActivity(objectType, activate){
	
	list = list_of_tables.getElementsByTagName("table");
	console.log(list);
	Object.values(list).forEach(function (table){
		caption = table.querySelector('#caption_' + objectType);
		console.log(objectType + " " + typeof(caption));
		if(typeof(caption) == "undefined" || caption == null){return;}
		console.log(caption.innerHTML);
		//This should now be the table for this specific ObjectType

		//Activate all checkboxes
		checkboxes = table.querySelectorAll("input[type='checkbox']");
		console.log(checkboxes);
		Object.values(checkboxes).forEach(function(cb){
			cb.disabled = !activate;
		});
	});
}

function createCube(name){
	//await 1;
	// cube = new Cube(name, selections);
	// cube.construct(events, objectEntries);
	document.getElementById("loading_wrapper").style.visibility = 'visible';
	document.getElementById("loading_wrapper").style.opacity = 1.0;
	loading_wrapper_title.innerHTML = "Creating Cube";
	loading_wrapper_desc.innerHTML = "";
	let timeHierarchy = document.getElementById("new_c_time_h").value;
	console.log("TIme Val");
	console.log(timeHierarchy);
	const myWorker = new Worker("js/cube_creation.js");
	myWorker.onmessage = function(e) {
		console.log('Message received from worker');
		console.log(e.data);
		all_cubes[name] = e.data;
		updateDropdowns(name);

		document.getElementById("loading_wrapper").style.opacity = 0.0;
		document.getElementById("loading_wrapper").style.visibility = 'hidden';

		cubeName.value = "";

		//remove all selections
		resetSelections();

	}
	myWorker.postMessage([name, selections, events, eventAttrs, objectEntries, timeHierarchy]);
	//await 2;
}

/***********
Display cube 
************/

function getNumberOverviews(){
	return document.getElementsByClassName('splide__slide').length;
}

function initSplideSlider(){
	if(splide == null){
		splide = new Splide( '.splide' ,  {
					  perPage: 2,
					  rewind : true,
					} );
	 	splide.on( 'mounted', function () {
		  // do something
		  if(getNumberOverviews()>2){
		  	var value = 14*Math.floor(getNumberOverviews()/2);
		  	console.log("Slidesnum: " + Number(Math.floor(getNumberOverviews()/2)));
			document.getElementsByClassName('splide__pagination')[0].style.width = ''+value+'px';
		  }
		});
	  	splide.on( 'refresh', function () {
		  if(getNumberOverviews()>2){
		  	var value = 14*Math.ceil(getNumberOverviews()/2);
		  	console.log("Overviews: " + getNumberOverviews());
		  	console.log("Slidesnum: " + Number(Math.floor(getNumberOverviews()/2)));
			document.getElementsByClassName('splide__pagination')[0].style.width = ''+value+'px';
		  }
	  	});
		splide.mount();
	}else{
		splide.refresh();
	}
	// if(document.getElementsByClassName('splide__pagination').length>0){
	// 	document.getElementsByClassName('splide__pagination')[0].remove();	
	// }
}

// Creates the innerTable for a cube overview
function addOverviewTables(addNumTables){
	for(var i = 0; i<addNumTables;i++){
		var listItem = document.createElement('li');
		listItem.classList.add('splide__slide');
		var itemWrapper = document.createElement('div');
		itemWrapper.id = 'cube_wrapper' + (curr_num_overviews+1);
		itemWrapper.classList.add('table_overview_wrapper');
		// tableWrapper.style.width = '50%';
		// tableWrapper.style.height = '600px';

		var tableTitle = document.createElement('h3');
		console.log("Num slider: " + getNumberOverviews());
		tableTitle.classList.add('cube-overview-title');
		tableTitle.style.fontFamily = "'Roboto', sans-serif";
		tableTitle.innerHTML = 'Cube ' + Number(getNumberOverviews() + 1);
		itemWrapper.appendChild(tableTitle);

		var wrapperForm = document.createElement('form');
		wrapperForm.classList.add('wrapper_form');

		var labelName = document.createElement('label');
		labelName.innerHTML = 'Cube Name';
		labelName.classList.add('label');
		wrapperForm.appendChild(labelName);

		let nameSelect = document.createElement('select');
		let numTables = Object.keys(overviewTables).length;
		overviewTables[numTables + 1]={};
		console.log(overviewTables);
		console.log(numTables);

		overviewSelections[numTables + 1] = [];

		overviewTables[numTables + 1]['nameSelect'] = nameSelect;
		let optionNone = document.createElement('option');
		optionNone.value='';
		optionNone.innerHTML = '';
		nameSelect.appendChild(optionNone);
		Object.keys(all_cubes).forEach(function(obj){
			optionNone = document.createElement('option');
			optionNone.value = obj;
			optionNone.innerHTML = obj;
		});
		nameSelect.appendChild(optionNone);
		nameSelect.classList.add('dropdowns');

		let materialName = document.createElement('label');
		materialName.innerHTML = 'Materialization';
		materialName.classList.add('label');

		let materialSelect = document.createElement('select');
		overviewTables[numTables + 1]['materialSelect'] = materialSelect;
		optionNone = document.createElement('option');
		optionNone.value='none';
		optionNone.innerHTML = '';
		materialSelect.appendChild(optionNone);
		let optionAll = document.createElement('option');
		optionAll.innerHTML = 'All';
		optionAll.value = 'all';
		materialSelect.appendChild(optionAll);
		let optionExist = document.createElement('option');
		optionExist.innerHTML = 'Existance';
		optionExist.values = 'existance';
		materialSelect.appendChild(optionExist);
		materialSelect.classList.add('dropdowns');

		let dim1Label = document.createElement('label');
		dim1Label.innerHTML = 'Dimension 1';
		dim1Label.classList.add('label');

		let dim1Select = document.createElement('select');
		overviewTables[numTables + 1]['dim1Select'] = dim1Select;
		dim1Select.classList.add('dropdowns');

		let dim2Label = document.createElement('label');
		dim2Label.innerHTML = 'Dimension 2';
		dim2Label.classList.add('label');

		let dim2Select = document.createElement('select');
		overviewTables[numTables + 1]['dim2Select'] = dim2Select;
		dim2Select.classList.add('dropdowns');

		// let timeHirarchyLabel = document.createElement('label');
		// timeHirarchyLabel.innerHTML = 'Time Hirarchy';
		// timeHirarchyLabel.classList.add('label');
		//
		// let optMinute = document.createElement('option');
		// optMinute.innerHTML = 'Minute';
		// optMinute.value = 'Minute';
		//
		// let optMinute2 = document.createElement('option');
		// optMinute2.innerHTML = 'Minute';
		// optMinute2.value = 'Minute';
		//
		// let optHour = document.createElement('option');
		// optHour.innerHTML = 'Hour';
		// optHour.value = 'Hour';
		//
		// let optDay = document.createElement('option');
		// optDay.innerHTML = 'Day';
		// optDay.value = 'Day';
		//
		// let optMonth = document.createElement('option');
		// optMonth.innerHTML = 'Month';
		// optMonth.value = 'Month';
		//
		// let optYear = document.createElement('option');
		// optMinute.innerHTML = 'Year';
		// optMinute.value = 'Year';
		//
		// let timeHierarchy = document.createElement('select');
		// timeHierarchy.appendChild(optMinute);
		// timeHierarchy.appendChild(optMinute2);
		// timeHierarchy.appendChild(optHour);
		// timeHierarchy.appendChild(optDay);
		// timeHierarchy.appendChild(optMonth);
		// timeHierarchy.appendChild(optYear);
		// overviewTables[numTables + 1]['timeHierarchy'] = timeHierarchy;
		// timeHierarchy.classList.add('dropdowns');

		freqDataSet[numTables+1] = {};

		nameSelect.onchange = function(){
			let index = getIndexByDom(nameSelect, 'nameSelect');
			console.log('Name change on index ' + index);
			let name = overviewTables[index]['nameSelect'];
			let mat = overviewTables[index]['materialSelect'];
			let dim1 = overviewTables[index]['dim1Select'];
			let dim2 = overviewTables[index]['dim2Select'];
			let act = overviewTables[index]['activitySelect'];
			let attr = overviewTables[index]['attrSelect'];
			let logsFlaten = overviewTables[index]['logs-flatten-select'];

			console.log(this.value);
			if( (typeof(this.value)=='undefined') || (this.value == "") || (this.value == " ")){
				mat.disabled = true;
				dim1.disabled = true;
				dim2.disabled = true;
				logsFlaten.disabled = true;
				// this.disabled = true;
				// this.innerHTML = "";
				this.removeAttribute('disabled');
			}
			else{
				mat.removeAttribute('disabled');
				dim1.removeAttribute('disabled');
				dim2.removeAttribute('disabled');
				logsFlaten.removeAttribute('disabled');

				//dimens = new Set();
				// var name = overviewTables[numTables + 1]['name'] = dim1Select;
				// console.log(overviewTables[numTables + 1]['dim1Select'] = dim1Select.value);
				// console.log(this.value);
				// console.log(Object.keys(all_cubes[this.value]['existance']));

				// console.log(dimens);

				dim1.innerHTML = "";
				option = document.createElement('option');
				option.innerHTML = "";
				dim1.appendChild(option);

				dim2.innerHTML = "";
				option = document.createElement('option');
				option.innerHTML = "";
				dim2.appendChild(option);

				attr.innerHTML = "";
				option = document.createElement('option');
				option.innerHTML = "";
				attr.appendChild(option);

				let name = this.value;

				Object.keys(all_cubes[name]['selections']).forEach(function(type){
					devider = document.createElement('optgroup');
					devider.label = type;
					for(var x of all_cubes[name]['selections'][type]){
						option = document.createElement('option');
						option.innerHTML = x;
						devider.appendChild(option);
					}
					dim1.appendChild(devider);
				});

				Object.keys(all_cubes[name]['selections']).forEach(function(type){
					devider = document.createElement('optgroup');
					devider.label = type;
					for(var x of all_cubes[name]['selections'][type]){
						option = document.createElement('option');
						option.innerHTML = x;
						devider.appendChild(option);
					}
					dim2.appendChild(devider);
				});

				Object.keys(all_cubes[name]['selections']).forEach(function(type){
					devider = document.createElement('optgroup');
					devider.label = type;
					for(var x of all_cubes[name]['selections'][type]){
						option = document.createElement('option');
						option.innerHTML = x;
						devider.appendChild(option);
					}
					attr.appendChild(devider);
				});

				logsFlaten.innerHTML = "";
				option = document.createElement('option');
				option.innerHTML = "";
				logsFlaten.appendChild(option);

				Object.keys(all_cubes[this.value]['selections']).forEach(function(type){
					if(type != 'Events'){
						option = document.createElement('option');
						option.innerHTML = type;
						logsFlaten.appendChild(option);
					}
				});
			}
		}

		materialSelect.onchange = function(){
			let index = getIndexByDom(dim2Select, 'dim2Select');
			console.log("Index: " +index);
			onEditCubeDimen(index);
		}

		dim1Select.onchange = function(){
			let index = getIndexByDom(dim1Select, 'dim1Select');
			console.log("Index: " +index);
			onEditCubeDimen(index);
		}

		dim2Select.onchange = function(){
			let index = getIndexByDom(dim2Select, 'dim2Select');
			console.log("Index: " +index);
			onEditCubeDimen(index);
		}

		wrapperForm.appendChild(nameSelect);
		wrapperForm.appendChild(materialName);
		wrapperForm.appendChild(materialSelect);

		var br = document.createElement('br');
		wrapperForm.appendChild(br);
		br = document.createElement('br');
		wrapperForm.appendChild(br);

		wrapperForm.appendChild(dim1Label);
		wrapperForm.appendChild(dim1Select);
		wrapperForm.appendChild(dim2Label);
		wrapperForm.appendChild(dim2Select);
		// wrapperForm.appendChild(timeHirarchyLabel);
		// wrapperForm.appendChild(timeHierarchy);
		itemWrapper.appendChild(wrapperForm)

		var br = document.createElement('br');
		itemWrapper.appendChild(br);

		//CREATE TABLE FOR SELECTING INFO YOU'RE INTERESTED IN
		let innerTableWrapper = document.createElement('div');
		// innerTableWrapper.style.height = '400px';
		innerTableWrapper.classList.add('cube-table-wrapper');
		overviewTables[numTables + 1]['cube-table-wrapper'] = innerTableWrapper;
		let table = document.createElement('table');
		// table.on("click", "td", changedOverviewSelections(numTables + 1));
		overviewTables[numTables + 1]['table'] = table;
		table.classList.add('cube-table');
		table.id = 'cube-table' + (curr_num_overviews+1);
		innerTableWrapper.appendChild(table);
		// innerTableWrapper.style.display = 'none';
		itemWrapper.appendChild(innerTableWrapper);

		let filterBtn = document.createElement('button');
		filterBtn.innerHTML ='Filter';
		filterBtn.classList.add('filter-btn');
		overviewTables[numTables + 1]['cube-table-filterBtn'] = filterBtn;
		filterBtn.onclick = function(){
			let index = getIndexByDom(filterBtn, 'cube-table-filterBtn');
			filterOcel(index);
		};
		itemWrapper.appendChild(filterBtn);
		itemWrapper.appendChild(document.createElement('br'));

		//NAVIGATION UI

		let nav = document.createElement('ul');
		nav.classList.add('overview-nav');

		let logs = document.createElement('li');
		let logsTxt = document.createElement('p');
		logsTxt.innerHTML = 'Analysed Logs';
		logsTxt.classList.add('active');
		logsTxt.onclick = function(){
			let index = getIndexByDom(logsTxt, 'logsTxt');
			console.log("Index: " +index);
			onOverviewTypeChange(index, 0);
		}
		overviewTables[numTables + 1]['logsTxt'] = logsTxt;
		logs.appendChild(logsTxt);

		nav.appendChild(logs);

		let dfg = document.createElement('li');
		let dfgTxt = document.createElement('p');
		dfgTxt.innerHTML = 'OC-DFG';
		dfgTxt.onclick = function(){
			let index = getIndexByDom(dfgTxt, 'dfgTxt');
			console.log("Index: " +index);
			onOverviewTypeChange(index, 1);
		}
		overviewTables[numTables + 1]['dfgTxt'] = dfgTxt;
		dfg.appendChild(dfgTxt);
		nav.appendChild(dfg);

		let freq = document.createElement('li');
		let freqTxt = document.createElement('p');
		freqTxt.innerHTML = 'Frequent Items';
		freqTxt.onclick = function(){
			let index = getIndexByDom(freqTxt, 'freqTxt');
			console.log("Index: " +index);
			onOverviewTypeChange(index, 2);
		}
		overviewTables[numTables + 1]['freqTxt'] = freqTxt;
		freq.appendChild(freqTxt);

		nav.appendChild(freq);

		itemWrapper.appendChild(nav);

		var br = document.createElement('br');
		itemWrapper.appendChild(br);

		// LOGS UI
		let logsWrapper = document.createElement('div');
		overviewTables[numTables+1]['logs-wrapper'] = logsWrapper;
		logsWrapper.classList.add('logs-wrapper');

		let logsOptWrapper = document.createElement('div');
		logsOptWrapper.classList.add('logs-opt-wrapper');

		let flattenTxt = document.createElement('label');
		flattenTxt.style.marginRight = '20px';
		flattenTxt.innerHTML = 'Flatten by:';

		let flatten = document.createElement('select');
		flatten.classList.add('dropdowns');
		let optionFlatten = document.createElement('option');
		optionFlatten.innerHTML = '';
		optionFlatten.value = '';
		flatten.appendChild(optionFlatten);
		overviewTables[numTables+1]['logs-flatten-select'] = flatten;

		let innerLogsTableWrapper = document.createElement('div');
		innerLogsTableWrapper.style.margin = '20px';
		innerLogsTableWrapper.classList.add('cube-table-wrapper');
		overviewTables[numTables + 1]['logs-table-wrapper'] = innerLogsTableWrapper;
		table = document.createElement('table');
		// table.on("click", "td", changedOverviewSelections(numTables + 1));
		overviewTables[numTables + 1]['table_logs'] = table;
		//table.classList.add('cube-table');
		// table.id = 'cube-table' + (curr_num_overviews+1);
		innerLogsTableWrapper.appendChild(table);
		// innerTableWrapper.style.display = 'none';

		logsOptWrapper.appendChild(flattenTxt);
		logsOptWrapper.appendChild(flatten);
		logsWrapper.appendChild(logsOptWrapper);
		logsWrapper.appendChild(innerLogsTableWrapper);
		itemWrapper.appendChild(logsWrapper);

		flatten.onchange = function(){
			let index = getIndexByDom(nameSelect, 'nameSelect');
			dispalyFlattenedLogs(index);
		};

		// DFG UI
		let dfgBlockWrapper = document.createElement('div');
		let dfgFormWrapper = document.createElement('div');
		dfgFormWrapper.style.width = 'fit-content';
		dfgFormWrapper.style.marginLeft = 'auto';
		dfgFormWrapper.style.marginRight = 'auto';
		dfgBlockWrapper.style.display = 'none';

		let dfgTypeLabel = document.createElement('label');
		dfgTypeLabel.innerHTML = 'DFG Type: ';
		let dfgTypeSelect = document.createElement('select');
		let optFreq = document.createElement('option');
		optFreq.innerHTML = 'Frequency';
		optFreq.value = 'Performance';
		let optPerf = document.createElement('option');
		optPerf.innerHTML = 'Performance';
		optPerf.value = 'Performance';
		dfgTypeSelect.appendChild(optFreq);
		dfgTypeSelect.appendChild(optPerf);
		dfgFormWrapper.appendChild(dfgTypeLabel);
		dfgFormWrapper.appendChild(dfgTypeSelect);

		let dfgAggregation = document.createElement('label');
		dfgAggregation.innerHTML = 'Aggregation Measure: ';
		dfgAggregation.style.display = 'none';
		let dfgAggregSelect = document.createElement('select');
		dfgAggregSelect.style.display = 'none';
		let optMedian = document.createElement('option');
		optMedian.innerHTML = 'median';
		optMedian.value = 'median';
		let optMean = document.createElement('option');
		optMean.innerHTML = 'mean';
		optMean.value = 'mean';
		let optMin = document.createElement('option');
		optMin.innerHTML = 'min';
		optMin.value = 'min';
		let optMax = document.createElement('option');
		optMax.innerHTML = 'max';
		optMax.value = 'max';
		let optSum = document.createElement('option');
		optSum.innerHTML = 'sum';
		optSum.value = 'sum';

		dfgAggregSelect.appendChild(optMedian);
		dfgAggregSelect.appendChild(optMean);
		dfgAggregSelect.appendChild(optMin);
		dfgAggregSelect.appendChild(optMax);
		dfgAggregSelect.appendChild(optSum);
		dfgFormWrapper.appendChild(dfgAggregation);
		dfgFormWrapper.appendChild(dfgAggregSelect);

		dfgFormWrapper.appendChild(document.createElement('br'));

		let edgeThreshold = document.createElement('label');
		edgeThreshold.innerHTML = 'Edge Threshold: ';
		// edgeThreshold.style.display = 'none';
		let edgeThresholdInput = document.createElement('input');
		edgeThresholdInput.type = 'number';
		edgeThresholdInput.min = '0';
		edgeThresholdInput.value = '0';
		edgeThresholdInput.style.display = 'inline-block';
		// edgeThresholdInput.style.display = 'none';
		dfgFormWrapper.appendChild(edgeThreshold);
		dfgFormWrapper.appendChild(edgeThresholdInput);

		let actThreshold = document.createElement('label');
		actThreshold.innerHTML = 'Activity Threshold: ';
		// actThreshold.style.display = 'none';
		let actThresholdInput = document.createElement('input');
		actThresholdInput.type = 'number';
		actThresholdInput.min = '0';
		actThresholdInput.value = '0';
		// actThresholdInput.style.display = 'none';
		dfgFormWrapper.appendChild(actThreshold);
		dfgFormWrapper.appendChild(actThresholdInput);

		dfgBlockWrapper.appendChild(dfgFormWrapper);

		let createDFGBtn = document.createElement('button');
		createDFGBtn.onclick = function(){
			// console.log("FIX THIS, SHOULD SEND INDEX NOT CURR_NUM_OVERVIEWS");
			let index = getIndexByDom(createDFGBtn, 'dfg_btn');
			createDFG(index);
		};
		overviewTables[numTables + 1]['dfg_btn'] = createDFGBtn;
		createDFGBtn.style.display = 'none';
		createDFGBtn.innerHTML = 'Generate DFG';
		createDFGBtn.style.marginLeft = 'auto';
		createDFGBtn.style.marginRight = 'auto';
		createDFGBtn.style.marginTop = '20px';
		dfgBlockWrapper.appendChild(createDFGBtn);

		let dfgWrapper = document.createElement('div');
		dfgWrapper.id = 'dfg' + (numTables+1);
		// dfgWrapper.id = 'canvas';
		dfgBlockWrapper.appendChild(dfgWrapper);
		itemWrapper.appendChild(dfgBlockWrapper);
		overviewTables[numTables + 1]['dfg'] = dfgWrapper;
		overviewTables[numTables + 1]['dfg_form'] = dfgFormWrapper;
		overviewTables[numTables + 1]['dfg_type'] = dfgTypeSelect;
		overviewTables[numTables + 1]['dfg_aggreg'] = dfgAggregSelect;
		overviewTables[numTables + 1]['dfg_edge_threshold'] = edgeThresholdInput;
		overviewTables[numTables + 1]['dfg_act_threshold'] = actThresholdInput;
		overviewTables[numTables + 1]['dfg_wrapper'] = dfgBlockWrapper;

		dfgTypeSelect.onchange = function(){
			let index = getIndexByDom(dfgTypeSelect, 'dfg_type');
			let type = overviewTables[index]['dfg_type'].options[overviewTables[index]['dfg_type'].selectedIndex].text;
			console.log("Index: " + index);

			if(type == 'Performance'){
				dfgAggregation.style.display = 'inline-block';
				dfgAggregSelect.style.display = 'inline-block';
			}else{
				dfgAggregation.style.display = 'none';
				dfgAggregSelect.style.display = 'none';
			}
		};

		//FREQ ITEMS UI
		let frequentItemsWrapper = document.createElement('div');
		frequentItemsWrapper.style.display = 'none';
		frequentItemsWrapper.classList.add('freq-tem-wrapper');
		overviewTables[numTables + 1]['freq-item-wrapper'] = frequentItemsWrapper;
		// frequentItemsWrapper.classList.add('dropdowns');

		// let actLabel = document.createElement('label');
		// actLabel.innerHTML = 'Activity';
		// frequentItemsWrapper.appendChild(actLabel);
		// let activitySelect = document.createElement('select');
		// activitySelect.classList.add('dropdowns');
		// var option = document.createElement('option');
		// option.innerHTML = '';
		// option.value = '';
		// activitySelect.appendChild(option);
		// eventActivities.forEach(function(act){
		// 	var option = document.createElement('option');
		// 	option.innerHTML = act;
		// 	option.value = act;
		// 	activitySelect.appendChild(option);
		// });
		// overviewTables[numTables + 1]['activitySelect'] = activitySelect;
		// frequentItemsWrapper.appendChild(activitySelect);

		let frequentItemsFormWrapper = document.createElement('div');
		frequentItemsFormWrapper.style.width = 'fit-content';
		frequentItemsFormWrapper.style.margin = '0 auto';

		let attrLabel = document.createElement('label');
		attrLabel.innerHTML = 'Object Attribute:';
		frequentItemsFormWrapper.appendChild(attrLabel);
		let attrSelect = document.createElement('select');
		overviewTables[numTables + 1]['attrSelect'] = attrSelect;
		attrSelect.classList.add('dropdowns');
		var option = document.createElement('option');
		option.innerHTML = '';
		option.value = '';
		attrSelect.appendChild(option);
		frequentItemsFormWrapper.appendChild(attrSelect);

		let addAttrBtn = document.createElement('button');
		addAttrBtn.textContent = 'Add Attribute';
		addAttrBtn.onclick = function (){
			let index = getIndexByDom(addAttrBtn, 'addFreqAttrBtn');
			if(freqItemAttrs[index] == null){
				freqItemAttrs[index] = {};
			}
			let attrSelect = overviewTables[index]['attrSelect'];
			console.log("Obj_Type" + attrSelect.parentNode);
			let objType = attrSelect.options[attrSelect.selectedIndex].parentNode.label;;
			let ojAttr = attrSelect.options[attrSelect.selectedIndex].text;

			if(freqItemAttrs[index][objType] == null){
				freqItemAttrs[index][objType] = [];
			}
			freqItemAttrs[index][objType].push(ojAttr);
			console.log(freqItemAttrs)

			let newItem = document.createElement('li');
			let newItemDiv = document.createElement('div');
			let attrLabel = document.createElement('label');
			attrLabel.innerHTML = ojAttr;
			let removeBtn = document.createElement('button');
			removeBtn.innerHTML = 'X';
			let wrapper = overviewTables[index]['selFreqAttrList'];

			newItemDiv.appendChild(attrLabel);
			newItemDiv.appendChild(removeBtn);
			newItem.appendChild(newItemDiv);
			wrapper.appendChild(newItem);
		};
		frequentItemsFormWrapper.appendChild(addAttrBtn);
		overviewTables[numTables + 1]['addFreqAttrBtn'] = addAttrBtn;

		frequentItemsFormWrapper.appendChild(document.createElement('br'));

		let selFreqAttrList = document.createElement('ul');
		selFreqAttrList.style.display = 'block';
		selFreqAttrList.style.height = 'fit-content';
		frequentItemsFormWrapper.appendChild(selFreqAttrList);
		overviewTables[numTables + 1]['selFreqAttrList'] = selFreqAttrList;

		frequentItemsFormWrapper.appendChild(document.createElement('br'));

		let sizeLabel = document.createElement('label');
		sizeLabel.innerHTML = 'Min. Set Size:';
		let setSizeSlideWrap = document.createElement('div');
		setSizeSlideWrap.style.display = 'inline-block';
		setSizeSlideWrap.style.width = 'fit-content';
		let setSizeTxt = document.createElement('p');
		setSizeTxt.innerHTML = '2';
		let sliderIn = document.createElement('input');
		sliderIn.type = 'range';
		sliderIn.value = 2;
		sliderIn.min = 1;
		sliderIn.max = 20;
		sliderIn.classList.add('slider');
		sliderIn.oninput = function() {
			setSizeTxt.innerHTML = this.value;
		}
		setSizeSlideWrap.appendChild(sizeLabel);
		setSizeSlideWrap.appendChild(document.createElement('br'));
		setSizeSlideWrap.appendChild(sliderIn);
		setSizeSlideWrap.appendChild(setSizeTxt);
		frequentItemsFormWrapper.appendChild(setSizeSlideWrap);

		let suppLabel = document.createElement('label');
		suppLabel.innerHTML = 'Min. Support:';
		let minSupWrap = document.createElement('div');
		minSupWrap.style.width = 'fit-content';
		minSupWrap.style.float = 'left';
		let minSuppTxt = document.createElement('p');
		minSuppTxt.innerHTML = '50%';
		let sliderSupp = document.createElement('input');
		sliderSupp.type = 'range';
		sliderSupp.value = 50;
		sliderSupp.min = 0;
		sliderSupp.max = 100;
		sliderSupp.classList.add('slider');
		sliderSupp.oninput = function() {
			minSuppTxt.innerHTML = this.value + "%";
		}
		minSupWrap.appendChild(suppLabel);
		minSupWrap.appendChild(document.createElement('br'));
		minSupWrap.appendChild(sliderSupp);
		minSupWrap.appendChild(minSuppTxt);
		frequentItemsFormWrapper.appendChild(minSupWrap);

		frequentItemsWrapper.appendChild(frequentItemsFormWrapper);

		let calcFreqBtn = document.createElement('button');
		calcFreqBtn.innerHTML = 'Find Sets';
		overviewTables[numTables + 1]['calcFreqBtn'] = calcFreqBtn;
		frequentItemsWrapper.appendChild(calcFreqBtn);
		calcFreqBtn.onclick = function(){
			let index = getIndexByDom(calcFreqBtn, 'calcFreqBtn');
			prepFreqDataSet(index);
			$.get( $SCRIPT_ROOT + "/get_freq_items" + '?' + performance.now(),
			{
				attr:  attrSelect.value,
				min_supp: parseInt(sliderSupp.value),
				set_size: sliderIn.value,
				dataset: JSON.stringify(freqDataSet[index])
			}
			).done(function( data ) {
				console.log(data.result);
				displayFreqTable(index, data.result['freq_itemsets']);
				displayAssocTable(index, data.result['assoc_rules']);
			});
		};
		calcFreqBtn.style.clear = 'both';
		calcFreqBtn.style.display = 'block';
		calcFreqBtn.style.margin = '10px auto';

		let frecItemsHeader = document.createElement('h3');
		frecItemsHeader.innerHTML = "Frequent Item Sets";
		frequentItemsWrapper.appendChild(frecItemsHeader);

		let innerFreqTableWrap = document.createElement('div');
		innerFreqTableWrap.classList.add('freq-table-wrapper');
		overviewTables[numTables + 1]['freq-table-wrapper'] = innerFreqTableWrap;
		let tableFreq = document.createElement('table');
		overviewTables[numTables + 1]['freq-table'] = tableFreq;
		tableFreq.classList.add('freq-table');
		tableFreq.id = 'freq-table' + (curr_num_overviews+1);
		innerFreqTableWrap.appendChild(tableFreq);
		frequentItemsWrapper.appendChild(innerFreqTableWrap);

		let createFreqItemsDFGBtn = document.createElement('button');
		createFreqItemsDFGBtn.onclick = function(){
			let index = getIndexByDom(createFreqItemsDFGBtn, 'freq_item_dfg_btn');
			displayFreqItemsDfg(index, 'set');;
		};
		overviewTables[numTables + 1]['freq_item_dfg_btn'] = createFreqItemsDFGBtn;
		createFreqItemsDFGBtn.style.display = 'block';
		createFreqItemsDFGBtn.innerHTML = 'Generate Freq DFG';
		createFreqItemsDFGBtn.style.marginLeft = 'auto';
		createFreqItemsDFGBtn.style.marginRight = 'auto';
		createFreqItemsDFGBtn.style.marginTop = '20px';
		frequentItemsWrapper.appendChild(createFreqItemsDFGBtn);

		let asocHeader = document.createElement('h3');
		asocHeader.innerHTML = "Association Rules";
		frequentItemsWrapper.appendChild(asocHeader);

		let innerAssocTableWrap = document.createElement('div');
		innerAssocTableWrap.classList.add('freq-table-wrapper');
		innerAssocTableWrap.style.marginTop= '20px'
		overviewTables[numTables + 1]['assoc-table-wrapper'] = innerAssocTableWrap;
		let tableAssoc = document.createElement('table');
		overviewTables[numTables + 1]['assoc-table'] = tableAssoc;
		tableAssoc.classList.add('freq-table');
		tableAssoc.id = 'assoc-table' + (curr_num_overviews+1);
		innerAssocTableWrap.appendChild(tableAssoc);
		frequentItemsWrapper.appendChild(innerAssocTableWrap);

		let createAssocDFGBtn = document.createElement('button');
		createAssocDFGBtn.onclick = function(){
			let index = getIndexByDom(createFreqItemsDFGBtn, 'freq_item_dfg_btn');
			displayFreqItemsDfg(index, 'rule');
		};
		overviewTables[numTables + 1]['assoc_dfg_btn'] = createAssocDFGBtn;
		createAssocDFGBtn.style.display = 'block';
		createAssocDFGBtn.innerHTML = 'Generate Assoc DFG';
		createAssocDFGBtn.style.marginLeft = 'auto';
		createAssocDFGBtn.style.marginRight = 'auto';
		createAssocDFGBtn.style.marginTop = '20px';

		frequentItemsWrapper.appendChild(createAssocDFGBtn);

		let freqDfgWrapper = document.createElement('div');
		overviewTables[numTables + 1]['freq_dfg'] = freqDfgWrapper;
		freqDfgWrapper.id = 'freq_dfg' + (numTables+1);
		frequentItemsWrapper.appendChild(freqDfgWrapper);

		itemWrapper.appendChild(frequentItemsWrapper);

		curr_num_overviews+=1;
		listItem.appendChild(itemWrapper);
		overview_tables_wrapper_list.appendChild(listItem);
	}

	initSplideSlider();
}

function getIndexByDom(domElement, name){
	var index = 0;
	console.log(domElement);
	for(var j = 0;j<Object.keys(overviewTables).length;j++){
		index = index +1;
		console.log('index '+ index);
		console.log('Currently checxking: ');
		console.log(overviewTables[(j+1)][name]);
		console.log(overviewTables[(j+1)][name]);
		if(overviewTables[(j+1)][name] === domElement) {
			break;
		}
	}
	if(index>Object.keys(overviewTables).length){
		console.log('Table name select not found!');
		return;
	}
	return index;
}

function removeOverviewTables(removeTables){
	// var slides = overview_tables_wrapper_list.getChildNodes();
	for(var j = 0; j<removeTables;j++){
		// var len = slides.length;
		overview_tables_wrapper_list.lastChild.remove();
		// var tableToTelete = 
	}
	initSplideSlider();
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

function createDFG(index){
	let tableDOM = overviewTables[index];
	let tableCube = all_cubes[tableDOM['nameSelect'].value];
	overviewTables[index]['dfg'].innerHTML = "";
	let type = overviewTables[index]['dfg_type'].options[overviewTables[index]['dfg_type'].selectedIndex].text;
	let aggreg = overviewTables[index]['dfg_aggreg'].options[overviewTables[index]['dfg_aggreg'].selectedIndex].text;
	let edgeThreshold = overviewTables[index]['dfg_edge_threshold'].value;
	let actThreshold = overviewTables[index]['dfg_act_threshold'].value;

	console.log("Index: " + index);
	console.log("type: " + type);
	console.log("aggreg: " + aggreg);
	console.log("edge_threshold: " + edgeThreshold);
	console.log("act_threshold: " + actThreshold);

	$.get( $SCRIPT_ROOT + "/generate_dfg?"+ performance.now(),
	{'index': index,
		'type': type,
		'performace_measure': aggreg,
		'edge_threshold': edgeThreshold,
		'act_threshold': actThreshold
	}
	).done(function( data ) {
		setTimeout(true, 1000);
		console.log(data);
		img = document.createElement('img');
		img.src = 'http://127.0.0.1:5000/get_svg/'+index + '?' + performance.now(); 
		img.classList.add('dfg_img');

		overviewTables[index]['dfg'].appendChild(img);
	});	
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

function updateDropdowns(cubeName){
	// c1_name_drop.innerHTML=""
	// option = document.createElement('option');
	// option.innerHTML = "";
	// c1_name_drop.appendChild(option);

	// c2_name_drop.innerHTML=""
	// option = document.createElement('option');
	// option.innerHTML = "";
	// c2_name_drop.appendChild(option);

	// Object.keys(all_cubes).forEach(function(cube_name){
	Object.keys(overviewTables).forEach(function(index){
		var option = document.createElement('option');
		option.innerHTML = cubeName;
		option.value = cubeName;
		console.log("Update " + index);
		overviewTables[index]['nameSelect'].appendChild(option);
	});

		// var option = document.createElement('option');
		// option.innerHTML = cubeName;
		// c1_name_drop.appendChild(option);
		// option = document.createElement('option');
		// option.innerHTML = cubeName;
		// c2_name_drop.appendChild(option);
	// });
}

// type: 0 - logs, 1 - dfg , 2 - frequent items 
function onOverviewTypeChange(index, type){
	if(type == 0){
		//mark logs as active in nav
		overviewTables[index]['logsTxt'].classList.add('active');
		overviewTables[index]['dfgTxt'].classList.remove('active');
		overviewTables[index]['freqTxt'].classList.remove('active');

		//HIDE FREQ STUFF
		overviewTables[index]['freq-item-wrapper'].style.display = "none";
		// overviewTables[index]['dfg_btn'].style.display = "block";

		//HIDE DFG STUFF
		overviewTables[index]['dfg'].style.display = "none";
		overviewTables[index]['dfg_btn'].style.display = "none";
		overviewTables[index]['dfg_wrapper'].style.display = "none";

		//SHOW LOGS
		overviewTables[index]['logs-wrapper'].style.display = "block";

	}
	else if(type == 1){
		overviewTables[index]['dfgTxt'].classList.add('active');
		overviewTables[index]['logsTxt'].classList.remove('active');
		overviewTables[index]['freqTxt'].classList.remove('active');

		//SHOW DFG STUFF
		// overviewTables[index]['cube-table-wrapper'].style.display = "block";
		overviewTables[index]['dfg_btn'].style.display = "block";
		overviewTables[index]['dfg'].style.display = "block";
		overviewTables[index]['dfg_wrapper'].style.display = "block";

		//HIDE FREQ STUFF
		overviewTables[index]['freq-item-wrapper'].style.display = "none";
		overviewTables[index]['logs-wrapper'].style.display = "none";
		// overviewTables[index]['dfg_btn'].style.display = "block";
		
	}else{
		overviewTables[index]['dfgTxt'].classList.remove('active');
		overviewTables[index]['freqTxt'].classList.add('active');
		overviewTables[index]['logsTxt'].classList.remove('active');

		//SHOW FREQ STUFF
		overviewTables[index]['freq-item-wrapper'].style.display = "block";

		//HIDE DFG STUFF
		overviewTables[index]['dfg'].style.display = "none";
		overviewTables[index]['dfg_btn'].style.display = "none";
		overviewTables[index]['dfg_wrapper'].style.display = "none";
		overviewTables[index]['logs-wrapper'].style.display = "none";
	}
	console.log("DONE");
}

// Extract and form a dataset from the givenlogs to feed to the Apriori algorithm
function prepFreqDataSet(index){
	// TODO usee filtere logs here
	freqDataSet[index] = [];
	
	//dataset: map of every activity to list of lists of objects for every event with this activity

	// eventActivities.forEach(function(act){
	// 	freqDataSet[index][act] = [];
	// });
	// console.log("Freq with empty acts: ");
	// console.log(freqDataSet);

	let usedEvents = JSON.parse(filteredOCELs[index])['ocel:events'];
	for(var e of Object.keys(usedEvents)){
		e = usedEvents[e];
		let objs = [];
		for(var objID of e['ocel:omap']){ // go trough all objects of event
			let obj = getObjectById(objID, objects)[1];
			console.log(obj);
			for(var type of Object.keys(freqItemAttrs[index])){
				if (type == obj['ocel:type']){
					for(attr of freqItemAttrs[index][type]){
						console.log(attr);
						if(Object.keys(obj['ocel:ovmap']).includes(attr)){
							objs.push(String(obj['ocel:ovmap'][attr]));
						}
					}
				}
			}
			// if(Object.keys(obj['ocel:ovmap']).includes(attr)){
			// 	objs.push(obj['ocel:ovmap'][attr]);
			// }
		}
		try{
			freqDataSet[index].push(objs);
		}catch(error){
			console.log(error);
			console.log(objs);
			console.log(e['ocel:omap']);
		}	
	}
	console.log(freqDataSet)
}

function displayFreqTable(index, data){
	let table = overviewTables[index]['freq-table'];
	let cubeName = overviewTables[index]['nameSelect'];

	let objAttr = overviewTables[index]['attrSelect'].value;

	// let mappedData = [];
	// for(var pair of data){
	// 	let aSet = [];
	// 	let listItems = pair[0];
	// 	for(var item of listItems){
	// 		let obj = getObjectById(item,objects)[1];
	// 		console.log(obj);
	// 		aSet.push(obj);
	// 	}
	// 	mappedData.push([aSet,pair[1]]);
	// }

	console.log(data);
	// console.log(mappedData);
	table.innerHTML = '';
	let head = table.insertRow(0);
	let setLabel = head.insertCell(0);
	setLabel.innerHTML = "Set";
	let suppLabel = head.insertCell(1);
	suppLabel.innerHTML = "Support";
	let sizeLabel = head.insertCell(2);
	sizeLabel.innerHTML = "Set Size";
	let checkbox = head.insertCell(3);
	checkbox.innerHTML = "Check";
	for(let itemSet of data){
		console.log(itemSet)
		let newRow = table.insertRow(1);
		let setCell = newRow.insertCell(0);
		setCell.innerHTML = "[" + itemSet[0] + "]";

		let suppCell = newRow.insertCell(1);
		suppCell.innerHTML = itemSet[1];

		let sizeCell = newRow.insertCell(2);
		sizeCell.innerHTML = itemSet[0].length;

		let cbCell = newRow.insertCell(3);
		let checkbox = document.createElement('input');
		        checkbox.type = "checkbox";
		        // checkbox.value = 1;
		        // checkbox.id = 'checkbox_' + "Events" + "_" + element1[0];
		        checkbox.onclick = function (){
					changedFreqSelection(index, itemSet)
				};
		cbCell.appendChild(checkbox);
	}
}

function displayAssocTable(index, data){
	let table = overviewTables[index]['assoc-table'];
	// console.log(data);
	// console.log(mappedData);
	table.innerHTML = '';
	let head = table.insertRow(0);
	let setLabelX = head.insertCell(0);
	setLabelX.innerHTML = "X";
	let arrow = head.insertCell(1);
	arrow.innerHTML = "-->";
	let setLabelY = head.insertCell(2);
	setLabelY.innerHTML = "Y";
	let suppLabel = head.insertCell(3);
	suppLabel.innerHTML = "Confidence";
	// let sizeLabel = head.insertCell(2);
	// sizeLabel.innerHTML = "Set Size";
	// let checkbox = head.insertCell(3);
	// checkbox.innerHTML = "Check";
	for(let itemSet of data){
		// console.log(itemSet)
		let newRow = table.insertRow(1);
		let setXCell = newRow.insertCell(0);
		setXCell.innerHTML = "[" + itemSet[0] + "]";

		let arrowCell = newRow.insertCell(1);
		arrowCell.innerHTML = ' --> ';

		let setYCell = newRow.insertCell(2);
		setYCell.innerHTML = "[" + itemSet[1] + "]";

		let suppCell = newRow.insertCell(3);
		suppCell.innerHTML = itemSet[2];

		// let sizeCell = newRow.insertCell(2);
		// sizeCell.innerHTML = itemSet[0].length;
		//
		// let cbCell = newRow.insertCell(3);
		// cbCell.appendChild(checkbox);
		// let checkbox = document.createElement('input');
		//         checkbox.type = "checkbox";
		//         // checkbox.value = 1;
		//         // checkbox.id = 'checkbox_' + "Events" + "_" + element1[0];
		//         checkbox.onclick = function (){
		// 			changedFreqSelection(index, itemSet)
		// 		};

		let cbCell = newRow.insertCell(3);
		let checkbox = document.createElement('input');
		        checkbox.type = "checkbox";
		        // checkbox.value = 1;
		        // checkbox.id = 'checkbox_' + "Events" + "_" + element1[0];
		        checkbox.onclick = function (){
					changedAssocRuleSelection(index, (itemSet[0] + itemSet[1]))
				};
		cbCell.appendChild(checkbox);

	}
}

function changedFreqSelection(index, itemset){
	if (freqSetSelect[index] == null){
		freqSetSelect[index] = [];
	}

	if(!freqSetSelect[index].includes(itemset)){
		freqSetSelect[index].push(itemset);
	}
}

function changedAssocRuleSelection(index, itemset){
	if (assocSetSelect[index] == null){
		assocSetSelect[index] = [];
	}

	if(!assocSetSelect[index].includes(itemset)){
		assocSetSelect[index].push(itemset);
	}
}

function displayFreqItemsDfg(index, type){
	// freqItemAttrs[index][objType]

	//TODO def freqItemSetSelectins

	console.log("Display DFG")
	console.log("type: " + type)

	itemset = freqSetSelect[index];

	data = []
	if(type == "set"){
		itemset = freqSetSelect[index];
	}else{
		itemset = assocSetSelect[index];
	}

	print(freqItemAttrs[index])
	$.get( $SCRIPT_ROOT + "/freq_items/filtered_dfg" + '?' + performance.now(),
	{	'itemsets': itemset,
		'filter': JSON.stringify(freqItemAttrs[index]),
		// 'index': index,
		// 'type': type,
		// 'performace_measure': aggreg,
		// 'edge_threshold': edgeThreshold,
		// 'act_threshold': actThreshold
	}
	).done(function( data ) {
		// console.log(data.result);
		// // displayFreqTable(index, data.result['data']);
		// // filteredOCELs[index] = data.result
		// filteredOCELs[index] = data.result;
		//
		setTimeout(true, 1000);
		console.log(data);
		let img = document.createElement('img');
		img.src = 'http://127.0.0.1:5000/freq_items/get_dfg_svg/'+index + '?' + performance.now();
		img.classList.add('dfg_img');
	    overviewTables[index]['freq_dfg'].innerHTML = "";
		overviewTables[index]['freq_dfg'].appendChild(img);
	});
}

function getObjectById(id, objects){
	var match = {};
	//console.log(objects)
	Object.entries(objects).forEach(function(entrie){
		if(entrie[0] == id){
			match=JSON.parse(JSON.stringify(entrie));
			//match = entrie;
			return;
		}
	});
	//Returneds match in the form ["880279", {ocel:type: "items", ocel:ovmap: {producer: "B", product: "iPhone X", cost: 343}}]
	return match;
}

function filterOcel(index){
	let tableDOM = overviewTables[index];
	let cubeName = tableDOM['nameSelect'].value;
	// overviewTables[index]['table'] = table;

	console.log('Cube Name: ' + cubeName);

	let filters = {
		'type_filter': [],
		// 'event_attr_filter': [],
		'overview_filter': {
			'type_row': tableDOM['dim1Select'].options[tableDOM['dim1Select'].selectedIndex].parentNode.label,
			'type_column': tableDOM['dim2Select'].options[tableDOM['dim2Select'].selectedIndex].parentNode.label,
			'row': '',
			'column': '',
			'selections': [] //[ [rowValue, columnValue], ... ]
		}
	};

	//Type Filter
	Object.keys(all_cubes[cubeName]['selections']).forEach(function(type){
		filters['type_filter'].push(type);
	});

	//Event attr
	// if(Object.keys(all_cubes[cubeName]['selections']).includes('Events')){
	// 	filters['event_attr_filter'] = all_cubes[cubeName]['selections']['Events'];
	// }

	//Overview Filter


	let sizeRow = tableDOM['table'].rows[0].length;
	// let sizeColumn = tableDOM['table'].columns.length;
	filters['overview_filter']['row'] = tableDOM['dim1Select'].value;
	filters['overview_filter']['column'] = tableDOM['dim2Select'].value;
	for( var item of overviewSelections[index]){
		let row = item[0];
		let column = item[1];
		let rowValue = tableDOM['table'].rows[row].cells[0].innerHTML;
		let columnValue = tableDOM['table'].rows[0].cells[column].innerHTML;
		console.log(rowValue);
		console.log(columnValue);
		console.log(typeof(columnValue));
		filters['overview_filter']['selections'].push([rowValue, columnValue]);
	}
	console.log(filters);

	let timeHierarchy = document.getElementById("new_c_time_h").value;

	$.get( $SCRIPT_ROOT + "/filter_ocel" + '?' + performance.now(),
	{	'materialisation': tableDOM['materialSelect'].value,
		'filter': JSON.stringify(filters),
		'index': index,
		'time_hierarchy': timeHierarchy
	}
	).done(function( data ) {
		console.log(data.result);
		// displayFreqTable(index, data.result['data']);
		// filteredOCELs[index] = data.result
		filteredOCELs[index] = data.result;
	});	
}

function dispalyFlattenedLogs(index, data){
	$.get( $SCRIPT_ROOT + "/flatten_ocel?"+ performance.now(),
			{'index': index,
			'type': this.value,
			}
			).done(function( data ) {
				console.log(data);
				let as_obj = JSON.parse(data.data);
				console.log(as_obj);

				let table =  overviewTables[index]['table_logs'];
				table.innerHTML = "";

				let thead = document.createElement('thead');
				let tbody = document.createElement('tbody');

				//add first row
				console.log(Object.keys(as_obj));

				Object.keys(as_obj).forEach(function(key){
					thead.appendChild(document.createElement('th')).appendChild(document.createTextNode(key));
				});
				table.appendChild(thead);

				let numRows = Object.entries(as_obj['event_id']).length;
				console.log(numRows);
				for(var i = 0;i<numRows;i++){
					var row = document.createElement('tr');

					Object.keys(as_obj).forEach(function(key){

						var cell = document.createElement('td');
						// set text
						if(objectTypes.includes(key)){
							cell.textContent = '[' + as_obj[key][i] + ']';
						}else{
							cell.textContent = as_obj[key][i];
						}
						// append td to tr
						row.appendChild(cell);
					});
					tbody.appendChild(row);
				}
				table.appendChild(tbody);
			});
}
