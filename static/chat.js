// chat.js


window.onload = function () {
    $('#messageSend').keydown(function (e) {
	    if(e.keyCode == 13){
	        $.getJSON('/newMessage', {
		        message: $('input[name="messageSend"]').val()
		    },
		    function(data) {
		    	var ul = document.getElementById('currentChat');
		        var newDate = document.createElement('li');
		        var newMessage = document.createElement('li');
		        var newMessageSpan = document.createElement('span');


		        newDate.appendChild(document.createTextNode(data.date));
		        newDate.classList.add('dateCreated','self');
		        ul.appendChild(newDate);

		        newMessageSpan.appendChild(document.createTextNode(data.message));
		        newMessageSpan.classList.add('chatInside','self');
		        newMessage.appendChild(newMessageSpan);
		        ul.appendChild(newMessage);
		    });
		};
		return false;
	});
};