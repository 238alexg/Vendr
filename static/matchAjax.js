// AJAX request for new matches

window.onload = function () {
    $('#match').bind('click', function() {
        $.ajax({
            url: '/newMatch',
            data: JSON.stringify({
                'item_id': $('input[name="indexSend"]').val()
            }),
            contentType : "application/json",
            type: 'POST',
            success: function(response){
                // var ul = document.getElementById('currentChat');
                // var newDate = document.createElement('li');
                // var newMessage = document.createElement('li');
                // var newMessageSpan = document.createElement('span');
                // var objDiv = document.getElementById("currentChatContainer");
                // var messageTextBox = document.getElementById("messageSend");

                // newDate.appendChild(document.createTextNode(response.result[0]));
                // newDate.classList.add('dateCreated','self');
                // ul.appendChild(newDate);

                // newMessageSpan.appendChild(document.createTextNode(response.result[1]));
                // newMessageSpan.classList.add('chatInside','self');
                // newMessage.classList.add('chatBubble','self')
                // newMessage.appendChild(newMessageSpan);
                // ul.appendChild(newMessage);

                // messageTextBox.value = '';
                // objDiv.scrollTop = objDiv.scrollHeight;
                // messageTextBox.select();
            },
            error: function(error){
                console.log(error);
            }
        });
        return false;
    });

    $('#noMatch').bind('click', function() {
        $.ajax({
            url: '/noMatch',
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
    });

    // // For swiping right (matching)
    // $('#match').bind('click', function() {
    //     $.getJSON('/newMatch', {
    //     newWord: $('input[name="newWord"]').val(),
    //     newWord: $('input[name="newWord"]').val()
    // }, 
    // function(data) {
    //     var ul = document.getElementById('resultContainer');
    //     $(ul).empty();
    //     for (var i = data.result.length - 1; i >= 0; i--) {
    //         var newLi = document.createElement('li');
    //         console.log(newLi);
    //         newLi.appendChild(document.createTextNode(data.result[i]));
    //         newLi.classList.add('searchResult');
    //         ul.appendChild(newLi);
    //     };
    // });
    // return false;
    // });


    // // For swiping left (no match)
    // $('#noMatch').bind('click', function() {
    //     $.getJSON('/loadMatches', {
    //     newWord: $('input[name="newWord"]').val()
    // }, 
    // function(data) {
    //     var ul = document.getElementById('resultContainer');
    //     $(ul).empty();
    //     for (var i = data.result.length - 1; i >= 0; i--) {
    //         var newLi = document.createElement('li');
    //         console.log(newLi);
    //         newLi.appendChild(document.createTextNode(data.result[i]));
    //         newLi.classList.add('searchResult');
    //         ul.appendChild(newLi);
    //     };
    // });
    // return false;
    // });

};