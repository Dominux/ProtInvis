function getInfo(condition) {

	let elements = ['guideUniprotId','guideTheDye'];

	for (let i = elements.length - 1; i >= 0; i--) {

		document.getElementById(elements[i]).style.visibility = condition;
	
	};

}