// profileButtons.js

function editProfInfo () {
	console.log("Got here");
	$(".editInfo").toggleClass("editable");
}


function updateProfileToDB () {
	

	errors = [false,false,false]

	// Validate inputs (email format and size ok, name size ok, interest size ok)
		$(".editInfo").toggleClass("editable");
		$('.editInfo').attr('contenteditable','false');
		// Update the DB with the 3 profile input entries here

	// Else display error and do not change Done button
		// Throw errors
}

// Validates profile info checking
function validateForm() {
	var nickname = document.getElementById("nickname").innerHTML;
	var email = document.getElementById("email").innerHTML;
	var interests = document.getElementById("interests").innerHTML;

	console.log("Got data: " + nickname + " , " + email + " , " + interests)

	errors = [null,null,null];

	if (nickname == '') {
		errors[0] = ("Must have a nickname");
	}
	if (email == '' || email == null) {
		errors[1] = ("Must have an email");
	}
	// Check for correct email format
	else {
		var emailTokens = email.split("@");
		if (emailTokens.length != 2) {
			errors[1] = ("Email must have format me@email.com");
		}
		else {
			var websiteTokens = emailTokens[1].split(".");
			if (websiteTokens.length < 2) {
				errors[1] = ("Email must have format me@email.com");
			}
			else if ( emailTokens.indexOf("") != -1 || websiteTokens.indexOf("") != -1  ) {
				errors[1] = ("Email must have format me@email.com");
			}
		}
	}
	if (interests == '') {
		errors[2] = ("Must have interests");
	}

	console.log("ERRORS: ")
	for (var i = 0; i <= errors.length - 1; i++) {
		console.log(errors[i]);
	};
	// Return false prevents submit
	if (errors.indexOf("") != -1) { return false; }
	// If form is validated and there are no errors, return true to submit
	else { return true; }

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