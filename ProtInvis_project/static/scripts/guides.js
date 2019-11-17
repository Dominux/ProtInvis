function getInfo(element, switcher) {
	
	let ids = {
		"js-uniprotId":"guideUniprotId",
		"js-theDye":"guideTheDye"
	};

	current_element = ids[element.id];

	if (switcher == true) {
		let act = document.getElementById(current_element).style.visibility = "visible";
	} else {
		let act = document.getElementById(current_element).style.visibility = "hidden";
	};

}