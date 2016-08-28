// chat.js

function sendMessage() {
    $.ajax({
        url: '/newMessage',
        data: JSON.stringify({
        	'message': $('input[name="messageSend"]').val(),
        	'displayConvo': $('input[name="indexSend"]').val()
    	}),
        contentType : "application/json",
        type: 'POST',
        success: function(response){
            var ul = document.getElementById('currentChat');
	        var newDate = document.createElement('li');
	        var newMessage = document.createElement('li');
	        var newMessageSpan = document.createElement('span');
	        var objDiv = document.getElementById("currentChatContainer");
            var messageTextBox = document.getElementById("messageSend");

	        newDate.appendChild(document.createTextNode(response.result[0]));
	        newDate.classList.add('dateCreated','self');
	        ul.appendChild(newDate);

	        newMessageSpan.appendChild(document.createTextNode(response.result[1]));
	        newMessageSpan.classList.add('chatInside','self');
	        newMessage.classList.add('chatBubble','self')
	        newMessage.appendChild(newMessageSpan);
	        ul.appendChild(newMessage);

	        messageTextBox.value = '';
            objDiv.scrollTop = objDiv.scrollHeight;
            messageTextBox.select();
        },
        error: function(error){
            console.log(error);
    	}
	});
	return false;
};