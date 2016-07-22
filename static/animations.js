// animate.js

var hasSlid = 0;

function createProfileAnimation() {
	if (hasSlid == 1) {
		// Do nothing
	}
	else if (hasSlid == 0) {
		hasSlid = 1; //Animation in progress
		var sliderBox = document.getElementById("slider");
		var button = document.getElementById("signUp");
		var pos = 13;
		var id = setInterval(frame,5);

		button.innerHTML = "<";
		
		function frame() {
			if (pos == 280) {
				clearInterval(id);
			} else if (pos < 250) {
				pos += 5;
				sliderBox.style.left = pos/3 + '%';
			} else if (pos < 270) {
				pos += 2;
				sliderBox.style.left = pos/3 + '%';
			} else {
				pos++;
				sliderBox.style.left = pos/3 + '%';
			}
		}
		hasSlid = 2;
	}
	else {
		hasSlid = 1; //Animation in progress
		var sliderBox = document.getElementById("slider");
		var button = document.getElementById("signUp");
		var pos = 280;
		var id = setInterval(frame2,5);

		button.innerHTML = ">";
		
		function frame2() {
			if (pos == 15) {
				clearInterval(id);
			} else if (pos > 45) {
				pos -= 5;
				sliderBox.style.left = pos/3 + '%';
			} else if (pos > 25) {
				pos -= 2;
				sliderBox.style.left = pos/3 + '%';
			} else {
				pos--;
				sliderBox.style.left = pos/3 + '%';
			}
		}
		hasSlid = 0;
	}
}

// Split tags with spaces and commas, do not include empty string tags
// function splitTagsNoEmpty(s) {
// 	strTok = s.split(/,| /);
// 	tags = [];
// 	for (var i = 0; i <= strTok.length - 1; i++) {
// 		if (strTok[i] != "") {
// 			tags.push(strTok[i]);
// 		}
// 		console.log(tags);
// 	};
//     return tags;
// }

function init() {
	var createProfileButton = document.getElementById("signUp");
	var tags = document.getElementById("tags");

	createProfileButton.onclick = createProfileAnimation;
	// $('input[name="tags"]').keydown(function (e) {
	// 	// console.log(e.keyCode);
	//     if((e.keyCode == 188) || (e.keyCode == 32)){
	//     	rawTags = $('input[name="tags"]').val();
	//     	tagToks = splitTagsNoEmpty(rawTags);
	//     	console.log(tagToks);
	//     	tags.innerHTML = tagToks;
	//     }
	// });
}

window.onload = init;



