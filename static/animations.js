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

// Enable new user submit button if all validation ok
function canSubmitNewUser() {
	var submitNewUser = document.getElementById('completeSignUp');

	if (document.getElementsByClassName("false").length != 0) {
		submitNewUser.disabled = true;
		$(submitNewUser).removeClass();
		submitNewUser.classList.add('cannotSubmit');
	}
	else {
		submitNewUser.disabled = false;
		$(submitNewUser).removeClass();
		submitNewUser.classList.add('canSubmit');
	}
}

function init() {
	var createProfileButton = document.getElementById("signUp");
	var tags = document.getElementById("tags");

	/*
		SIGN UP VALIDATION
	*/

	// Email validation for user creation with AJAX
	$('input[name="email"]').on('blur',function () {
        $.getJSON('/emailValidate', {
	        email: $('input[name="email"]').val()
	    }, 
	    function(data) {
	        var emailValid = document.getElementById('emailValidation');
	        $(emailValid).empty();
	        if (data.valid == 0) {
	            $(emailValid).html("Valid Email");
	            $(emailValid).removeClass();
	            emailValid.classList.add('true');
	        }
	        else if (data.valid == 1) {
	        	$(emailValid).html("Email must have format me@email.com");
	            $(emailValid).removeClass();
	            emailValid.classList.add('false');
	        }
	        else {
	        	$(emailValid).html("Email already in use!");
	            $(emailValid).removeClass();
	            emailValid.classList.add('false');
	        }
	        canSubmitNewUser();
	    });
	    return false;
    });

	// Password validation
	$('input[name="password"]').on('blur',function () {
		var pass = document.getElementById('password');
		var passValid = document.getElementById('passwordValidation');
		var conPassValid = document.getElementById('passConfirmation');

		$(conPassValid).html("&nbsp");

		if ($(pass).val().length < 7) {
			$(passValid).html("Password must be ≥ 7 characters");
            $(passValid).removeClass();
            passValid.classList.add('false');
        }
        else {
        	$(passValid).html("&nbsp");
            $(passValid).removeClass();
            passValid.classList.add('true');
        }
        canSubmitNewUser();
	});

	// Password confirm validation
	$('input[name="confirmPass"]').on('blur',function () {
		var pass = document.getElementById('password');
		var conPass = document.getElementById('confirmPass');
		var conPassValid = document.getElementById('passConfirmation');

		if ($(pass).val().length < 7) {
			$(conPassValid).html("Password must be ≥ 7 characters");
            $(conPassValid).removeClass();
            conPassValid.classList.add('false');
        }
        else if ($(pass).val() != $(conPass).val()) {
        	console.log($(pass).val());
        	console.log($(conPass).val());
        	$(conPassValid).html("Password does not match");
            $(conPassValid).removeClass();
            conPassValid.classList.add('false');
        }
        else {
        	$(conPassValid).html("Passwords Match!");
            $(conPassValid).removeClass();
            conPassValid.classList.add('true');
        }
        canSubmitNewUser();
	});

	// Nickname validation with AJAX
	$('input[name="nickname"]').on('blur',function () {
		$('#nicknameValidation').html('&nbsp');
		if ($('input[name="nickname"]').val() != "") {
		    $.getJSON('/nicknameValidate', {
		        nickname: $('input[name="nickname"]').val()
		    }, 
		    function(data) {
		        var emailValid = document.getElementById('nicknameValidation');
		        if (data.valid == true) {
		            $(emailValid).html("Nickname Available!");
		            $(emailValid).removeClass();
		            emailValid.classList.add('true');
		        }
		        else {
		        	$(emailValid).html("Nickname Unavailable");
		            $(emailValid).removeClass();
		            emailValid.classList.add('false');
		        }
		        canSubmitNewUser();
		    });
		    return false;
		};
    });

	/*
		LOGIN VALIDATION
	*/

	// Email validation for user login with AJAX
	$('button[name="loginButton"]').on('click',function () {
	    $.ajax({
            url: '/loginValidate',
            data: JSON.stringify({
	        	'email': $('input[name="logEmail"]').val(),
	        	'password': $('input[name="logPass"]').val()
	    	}),
            contentType : "application/json",
            type: 'POST',
            success: function(response){
            	var emailValid = document.getElementById("logEmailValidation");
            	var passValid = document.getElementById("logPassValidation");
            	$(emailValid).empty();
            	$(passValid).empty();
                if (response.valid == 0) {
                	$(emailValid).html("Email not found");
                }
                else if (response.valid == 1) {
                	$(passValid).html("Incorrect password");
                }
                else {
                	$("#login").submit();
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    });


	createProfileButton.onclick = createProfileAnimation;
}

window.onload = init;



