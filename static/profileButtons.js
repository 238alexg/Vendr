// profileButtons.js

function editProfInfo () {
	console.log("Got here");
	$(".editInfo").toggleClass("editable");
}


function updateProfileToDB () {
	var nickname = document.getElementById("nickname").innerHTML;
	var email = document.getElementById("email").innerHTML;
	var interests = document.getElementById("interests").innerHTML;

	errors = [false,false,false]

	// Validate inputs (email format and size ok, name size ok, interest size ok)
		$(".editInfo").toggleClass("editable");
		$('.editInfo').attr('contenteditable','false');
		// Update the DB with the 3 profile input entries here

	// Else display error and do not change Done button
		// Throw errors
}


function init() {
	var hasClickedProf = 0;
	var editProf = document.getElementById("editProf");
	
	// Edit Profile Info
	editProf.onclick = function() {
		// To edit
		if (hasClickedProf == 0) {
			editProf.innerHTML = "Done";
			editProf.style.fontSize = "120%";
			editProf.style.paddingTop = 10 + "px";
			editProf.style.paddingBottom = 8 + "px";
			$('.editInfo').attr('contenteditable','true');
			editProfInfo();
			hasClickedProf = 1;
		} 
		// To finish edit and save changes
		else {
			// CHANGE TO BACK END VALIDATION
			// Checks new form validation
			editProf.innerHTML = "+";
			editProf.style.fontSize = "220%";
			editProf.style.paddingTop = 0;
			editProf.style.paddingBottom = 0;
			hasClickedProf = 0;
			updateProfileToDB();
		}
	}
	$(".editInfo").keypress(function(e){ return e.which != 13; });

}

window.onload = init;