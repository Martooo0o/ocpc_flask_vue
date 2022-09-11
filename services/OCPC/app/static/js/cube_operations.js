class Cube{
	constructor(name, selections, timeHierarchy){
		this.name = name;
		this.selections = selections;
		console.log(timeHierarchy)
		this.timeHierarchy = timeHierarchy;
		// this.events = events;
		// this.objects = objects;
		this.existance = {};
		this.all = {}
	}

	construct(events, eventAttrs, objects){
		this.calcEvenetEventAttrPairs(events, eventAttrs);

		console.log("All good events attrs")
		this.calcEventObjAttrPairs(events, objects);

		this.calcObjObjAttrPairs(events, objects);
	}

	existHasPair(pairStr){
		return Object.keys(this.existance).includes(pairStr);
	}

	getObjectById(id, objects){
		var match = {};
		objects.forEach(function(entrie){
			if(entrie[0] == id){
				match=JSON.parse(JSON.stringify(entrie));
				//match = entrie;
				return;
			}
		});
		//Returneds match in the form ["880279", {ocel:type: "items", ocel:ovmap: {producer: "B", product: "iPhone X", cost: 343}}]
		return match;
	}

	static formatTimestamp(timestamp, timeHierarchy){
		let dateStr = timestamp;
		dateStr = dateStr.replace(" ", "T");
		console.log(dateStr);
		let date = new Date(dateStr);
		let newTimestamp = '';
		newTimestamp+=date.getFullYear();
		if(timeHierarchy != 'Year'){
			newTimestamp+='-';
			newTimestamp+=(date.getMonth()+1);
			console.log("Month")
			console.log(timeHierarchy != 'Month')
			console.log(timeHierarchy)
			if(timeHierarchy != 'Month'){
				newTimestamp+='-';
				newTimestamp+=date.getDate();
				if(timeHierarchy!='Day'){
					newTimestamp+=' ';
					newTimestamp+=(date.getHours()-2);
					if(timeHierarchy!='Hour'){
						newTimestamp+=':';
						newTimestamp+=date.getMinutes();
						if(timeHierarchy!='Minute'){
							newTimestamp+=':';
							newTimestamp+=date.getMinutes();
						}
					}
				}
			}
		}
		console.log("Format")
		console.log(newTimestamp)
		return newTimestamp;
	}

	/*CALCULATE EVENT EVENT PAIRS*/
	calcEvenetEventAttrPairs(events, eventAttrs){
		if(typeof(this.selections["Events"]) == "undefined") return;
		let timeHierarchy = this.timeHierarchy
		this.selections["Events"].forEach(function(element){
		 	this.selections["Events"].forEach(function(element2){
		 		
		 		//if existance contains it then materialisation does too
		 		if(this.existHasPair(element + "," + element2)
		 			|| this.existHasPair(element2 + "," + element)) {return;}
	
		 		var pairMap = {};
		 		pairMap[element + "_values"] = [];
		 		if(element !=element2){ pairMap[element2 + "_values"] = []; }
		 		pairMap["value_pair_occur"] = {};
				events.forEach(function(event){
		 			var key1 = eventAttrs.map(x => x[0]).includes(element)? element.substring(6): element;
		 			let value1 = (key1=="activity" || key1 == "timestamp")? event['ocel:' + key1] : event['ocel:vmap'][key1];
					console.log('Next Value');

				 	if (key1 == 'timestamp'){ //map value to the appropriate timestamp hierarchy
						 console.log(value1);
						 value1 = Cube.formatTimestamp(value1, timeHierarchy);
					}
		 			if( value1!='' && !(pairMap[element + "_values"].includes(value1) )){
	 				 	pairMap[element + "_values"].push( value1);
	 				}

		 			// if(element != element2){
	 				var key2 = eventAttrs.map(x => x[0]).includes(element2)? element2.substring(6) : element2;
			 		let value2 = (key2=="activity" || key2 == "timestamp")? event['ocel:'+ key2]:event['ocel:vmap'][key2];
				 	if (key2 == 'timestamp'){ //map value to the appropriate timestamp hierarchy
						 console.log(value2);
						 value2 = Cube.formatTimestamp(value2, timeHierarchy);
					}
		 			if(value2!='' && !( pairMap[element2 + "_values"].includes(value2) )){ 
						pairMap[element2 + "_values"].push( value2);
					}

					if (value1 != '' && value2 != '') {
						if(typeof(pairMap["value_pair_occur"][ [value1, value2] ]) == 'undefined'){
							pairMap["value_pair_occur"][ [value1, value2] ] = 1;
						}else{
							pairMap["value_pair_occur"][ [value1, value2] ] += 1;
						}
		 			}
	 			});
	 			this.existance[[element, element2]] = pairMap;
	 			this.all[[element, element2]] = pairMap;
	 		}.bind(this));
		}.bind(this));
	}

	/*CALCULATE EVENT OBJECT PAIRS*/
	//Helper Function
	calcEventObjExist(pairMapExistance, value1, key2, eventObjects, objects, objectType){
		var countedValues = [];//counted values for this event, so that we don't count multiple times
		for(var i = 0; i< eventObjects.length; i++){
			var obj = this.getObjectById(eventObjects[i], objects);
			// console.log("Event value: " + value1);
			// console.log("Obj id: " + eventObjects[i]);
			//check if event has object with this type and return if not
			try{
				// console.log(obj);
				if(obj[1]["ocel:type"] != objectType){
				continue;
				}
			}catch (error) {
			  console.error(error);
			  // expected output: ReferenceError: nonExistentFunction is not defined
			  // Note - error messages will vary depending on browser
			  console.log(obj);
			  console.log("Obj id: " + eventObjects[i]);
			  //TODO make program display some error that object wasn't found
			}
			
		
			var value2 = obj[1]['ocel:ovmap'][key2];
			if(value2!='' && !( pairMapExistance[key2 + "_values"].includes(value2) )){ 
				pairMapExistance[key2 + "_values"].push( value2);
			}
			// console.log("Obj value: " + value2);

			if (value1 != '' && value2 != '' && !countedValues.includes([value1, value2].join())) {
				if(typeof(pairMapExistance["value_pair_occur"][ [value1, value2] ]) == 'undefined'){
					pairMapExistance["value_pair_occur"][ [value1, value2] ] = 1;
				}else{
					pairMapExistance["value_pair_occur"][ [value1, value2] ] += 1;
				}
				countedValues.push([value1, value2].join());
				//break;
			} else{
				// console.log("Not counted");
				// console.log(value1);
				// console.log("Obj id: " + eventObjects[i]);
			}
		}
	}
	//Helper Function
	calcEventObjAll(pairMapAll, value1, key2, eventObjects, objects, objectType, objectAttr){
		var firstValue = '';
		for(var i = 0; i< eventObjects.length; i++){
			var obj = this.getObjectById(eventObjects[i], objects);
			//if object not from the specified type just move to next one
			if(obj[1]["ocel:type"] != objectType){
				continue;
			}
		
			var value2 = obj[1]['ocel:ovmap'][key2];
			if(firstValue == '' && value2!=''){ firstValue = value2;}
			else if(value2 != firstValue){
				//there are objects with different values, so don't count this event
				return;
			}

			if(value2!='' && !( pairMapAll[objectAttr + "_values"].includes(value2) )){ 
				pairMapAll[objectAttr + "_values"].push( value2);
			}
		}
		if (value1 != '' && value2 != '') {
			if(typeof(pairMapAll["value_pair_occur"][ [value1, value2] ]) == 'undefined'){
				pairMapAll["value_pair_occur"][ [value1, value2] ] = 1;
			}else{
				pairMapAll["value_pair_occur"][ [value1, value2] ] += 1;
			}
		} 
	}

	calcEventObjAttrPairs(events, objects){
		//store selections for everything except Events in tempSelections
		var tempSelections = {};
		Object.assign(tempSelections, this.selections); 
		delete tempSelections["Events"];

		if(typeof(this.selections["Events"]) == "undefined" || Object.values(tempSelections).lenght == 0) return;
		

		this.selections["Events"].forEach(function(eventAttr){ //go trough eevery event attr
			Object.keys(tempSelections).forEach(function(objectType){ //go trough every object type
				//console.log(objectType);
				this.selections[objectType].forEach(function(objectAttr){ //go trough every selected attr for this specific object type
					var pairMapExistance = {};
			 		pairMapExistance[eventAttr + "_values"] = [];
			 		pairMapExistance[objectAttr + "_values"] = [];
			 		pairMapExistance["value_pair_occur"] = {};	

			 		var pairMapAll = {};
					pairMapAll[eventAttr + "_values"] = [];
			 		pairMapAll[objectAttr + "_values"] = [];
			 		pairMapAll["value_pair_occur"] = {};	

			 		//TODO move this outside of the other loops	
					events.forEach(function(event){
			 			var key1 = eventAttr.substring(6);
			 			var value1 = (key1=="activity" || key1 == "timestamp")? event['ocel:' + key1] : event['ocel:vmap'][key1];

					 	if (key1 == 'timestamp'){ //map value to the appropriate timestamp hierarchy
							value1 = Cube.formatTimestamp(value1, this.timeHierarchy);
						}
			 			
			 			//adds every new value for 
			 			if( value1!='' && !(pairMapExistance[eventAttr + "_values"].includes(value1) )){
		 				 	pairMapExistance[eventAttr + "_values"].push( value1);
		 				 	pairMapAll[eventAttr + "_values"].push(value1);
		 				}

			 			var key2 = objectAttr;
			 			//var value2 = '';
		 				
		 				var eventObjects = [...Object.values(event["ocel:omap"])];
		 				// console.log("Currently counting for: " + JSON.stringify(event));
		 				this.calcEventObjExist(pairMapExistance, value1, key2, eventObjects, objects, objectType);

		 				this.calcEventObjAll(pairMapAll, value1, key2, eventObjects, objects, objectType, objectAttr);

		 			}.bind(this));

		 			this.existance[[eventAttr, objectAttr]] = pairMapExistance;
		 			this.all[[eventAttr, objectAttr]] = pairMapAll;
				}.bind(this));
			}.bind(this));
		}.bind(this));
	}

	/*CALCULATE OBJECT OBJECT PAIRS*/
	calcObjObjExist(eventObjects, objects, objectType, objectType2, objectAttr1, objectAttr2, pairMap, key1, key2){
		loopOverAllObjPairs:{
			var countedValues = [];//counted values for this event, so that we don't count multiple times
			for(var i = 0; i< eventObjects.length; i++){
				for(var j = 0; j<eventObjects.length;j++){
					var obj = this.getObjectById(eventObjects[i], objects);
					var obj2 = this.getObjectById(eventObjects[j], objects);

					//check if objects are from those types and return if not
					if(obj[1]["ocel:type"] != objectType || obj2[1]["ocel:type"] != objectType2){
						continue;
					}

					//add values to valueLists
					var value1 = obj[1]['ocel:ovmap'][key1];
					if(value1!='' && !( pairMap[objectAttr1 + "_values"].includes(value1) )){ 
						pairMap[objectAttr1 + "_values"].push( value1);
					}
					var value2 = obj2[1]['ocel:ovmap'][key2];
					if(value2!='' && !( pairMap[objectAttr2 + "_values"].includes(value2) )){ 
						pairMap[objectAttr2 + "_values"].push( value2);
					}

					if (value1 != '' && value2 != '' && !countedValues.includes([value1, value2].join())) {
						if(typeof(pairMap["value_pair_occur"][ [value1, value2] ]) == 'undefined'){
							pairMap["value_pair_occur"][ [value1, value2] ] = 1;
						}else{
							pairMap["value_pair_occur"][ [value1, value2] ] += 1;
						}
						countedValues.push([value1, value2].join());
						//break loopOverAllObjPairs;
	 				} 
				}
			}
		}
	}

	calcObjObjAll(eventObjects, objects, objectType, objectType2, objectAttr1, objectAttr2, pairMap, key1, key2){
		loopOverAllObjPairs:{
			var firstValue1 = '';
			var firstValue2 = '';
			for(var i = 0; i< eventObjects.length; i++){

				for(var j = 0; j<eventObjects.length;j++){
					var obj = this.getObjectById(eventObjects[i], objects);
					var obj2 = this.getObjectById(eventObjects[j], objects);

					//check if objects are from those types and return if not
					if(obj[1]["ocel:type"] != objectType || obj2[1]["ocel:type"] != objectType2){
						continue;
					}

					//add values to valueLists
					var value1 = obj[1]['ocel:ovmap'][key1];
					if(value1!='' && !( pairMap[objectAttr1 + "_values"].includes(value1) )){ 
						pairMap[objectAttr1 + "_values"].push( value1);
					}
					var value2 = obj2[1]['ocel:ovmap'][key2];
					if(value2!='' && !( pairMap[objectAttr2 + "_values"].includes(value2) )){ 
						pairMap[objectAttr2 + "_values"].push( value2);
					}

					if (value1 != '' && value2 != '') {
						if(firstValue1=='' && firstValue2==''){
							firstValue1 = value1;
							firstValue2 = value2;
						}else if(firstValue1!=value1 || firstValue2!=value2){
							break loopOverAllObjPairs;
						}
	 				} else{
 						break loopOverAllObjPairs;
	 				}
				}
			}

			if(firstValue1!='' && firstValue2!=''){
				if(typeof(pairMap["value_pair_occur"][ [firstValue1, firstValue2] ]) == 'undefined'){
					pairMap["value_pair_occur"][ [firstValue1, firstValue2] ] = 1;
				}else{
					pairMap["value_pair_occur"][ [firstValue1, firstValue2] ] += 1;
				}
			}
		}
	}

	calcObjObjAttrPairs(events, objects){
		var tempSelections = {};
		Object.assign(tempSelections, this.selections);
		delete tempSelections["Events"];
		//2 attr from a single objectType
		Object.keys(tempSelections).forEach(function(objectType){
			Object.keys(tempSelections).forEach(function(objectType2){
				this.selections[objectType].forEach(function(objectAttr1){
					this.selections[objectType2].forEach(function(objectAttr2){
						if( this.existHasPair(objectAttr1 + "," + objectAttr2)
			 			|| this.existHasPair(objectAttr2 + "," + objectAttr1)) {
			 				return;
				 		}

						var pairMap = {};
				 		pairMap[objectAttr1 + "_values"] = [];
				 		if(!(objectType == objectType2 && objectAttr1 == objectAttr2)){
				 			pairMap[objectAttr2 + "_values"] = [];
			 			}
				 		pairMap["value_pair_occur"] = {};

				 		var pairMapAll = {};
				 		pairMapAll[objectAttr1 + "_values"] = [];
				 		if(!(objectType == objectType2 && objectAttr1 == objectAttr2)){
				 			pairMapAll[objectAttr2 + "_values"] = [];
			 			}
				 		pairMapAll["value_pair_occur"] = {};

						events.forEach(function(event){

							var key1 = objectAttr1;
				 			var value1 = '';

							var key2 = objectAttr2;
				 			var value2 = '';

							var eventObjects = [...Object.values(event["ocel:omap"])];

							this.calcObjObjExist(eventObjects, objects, objectType, objectType2, objectAttr1, objectAttr2, pairMap, key1, key2);
							this.calcObjObjAll(eventObjects, objects, objectType, objectType2, objectAttr1, objectAttr2, pairMapAll, key1, key2);

						}.bind(this));

						this.existance[[objectAttr1, objectAttr2]] = pairMap;
						this.all[[objectAttr1, objectAttr2]] = pairMapAll;
					}.bind(this));
				}.bind(this));
			}.bind(this));
		}.bind(this));
	}
}

