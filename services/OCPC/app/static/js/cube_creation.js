onmessage = function(e) {
	// import Cube from './js/cube_operations'; 
	//const cubeModule = require('./js/cube_operations');
  	importScripts('./cube_operations.js');  
  	console.log('Message received from main script');
	  console.log(e.data[5]);
  	let cube = new Cube(e.data[0], e.data[1], e.data[5]); // params ( name, selections, timeHierarchy)
	cube.construct(e.data[2], e.data[3], e.data[4]); //params (events, eventAttrs, objects)
  	postMessage(cube);
}