const activities = ['place order', 'pick item', 'confirm order', 'item out of stock'];

function findActIndex(act){
	let i = -1;
	activities.forEach( function(element, index) {
		// statements
		if(element == act){
			i = index;
		}
	});
	return i;
}


function compareActivities(act1, act2){
	let x = findActIndex(act1);
	let y = findActIndex(act2);

	if(x>y) return 1;
	else if(x<y) return -1;
	else return 0;
}