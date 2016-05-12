// animate.js

var hasSlid = false;

function createProfileAnimation() {
	if (hasSlid == false) {
		var sliderBox = document.getElementById("slider");
		var button = document.getElementById("signUp");
		var pos = 13;
		var id = setInterval(frame,5);

		button.innerHTML = "<";
		
		function frame() {
			if (pos == 280) {
				clearInterval(id);
			}
			else if (pos < 250) {
				pos += 5;
				sliderBox.style.left = pos/3 + '%';
			}
			else if (pos < 270) {
				pos += 2;
				sliderBox.style.left = pos/3 + '%';
			}
			else {
				pos++;
				sliderBox.style.left = pos/3 + '%';
			}
		}
		hasSlid = true;
	}
	else {
		var sliderBox = document.getElementById("slider");
		var button = document.getElementById("signUp");
		var pos = 280;
		var id = setInterval(frame2,5);

		button.innerHTML = ">";
		
		function frame2() {
			if (pos == 15) {
				clearInterval(id);
			}
			else if (pos > 45) {
				pos -= 5;
				sliderBox.style.left = pos/3 + '%';
			}
			else if (pos > 25) {
				pos -= 2;
				sliderBox.style.left = pos/3 + '%';
			}
			else {
				pos--;
				sliderBox.style.left = pos/3 + '%';
			}
		}
		hasSlid = false;
	}
}


function init() {
	var createProfileButton = document.getElementById("signUp");
	createProfileButton.onclick = createProfileAnimation;
}

window.onload = init;