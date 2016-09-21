// AJAX request for new matches

function rotateAnimation(el,speed){
    var elem = document.getElementById(el);
    if(navigator.userAgent.match("Chrome")){
        elem.style.WebkitTransform = "rotate("+degrees+"deg)";
    } else if(navigator.userAgent.match("Firefox")){
        elem.style.MozTransform = "rotate("+degrees+"deg)";
    } else if(navigator.userAgent.match("MSIE")){
        elem.style.msTransform = "rotate("+degrees+"deg)";
    } else if(navigator.userAgent.match("Opera")){
        elem.style.OTransform = "rotate("+degrees+"deg)";
    } else {
        elem.style.transform = "rotate("+degrees+"deg)";
    }
    looper = setTimeout('rotateAnimation(\''+el+'\','+speed+')',speed);
    degrees++;
    if(degrees > 359){
        degrees = 1;
    }
}

function swipeRight() {
    $.ajax({
        url: '/newMatch',
        data: JSON.stringify({
            'item_id': $('input[name="indexSend"]').val()
        }),
        contentType : "application/json",
        type: 'POST',
        success: function(response){
            console.log("THIS IS THE SUCCESS RESPONSE");

            // var looper;
            // var degrees = 0;

            // rotateAnimation(matchBox);

            var html_1 = '<form id="newMatch" method="post"><div class="matchTileContainer" onclick=""><div class="matchName"><a style="font-weight:bold;" href="/profile/';
            var html_2 = response.itemInfo[0].concat('">',response.itemInfo[1]);
            var html_3 = '</a>: <a style="color:#9AF2A5;" href="/items/';
            var html_4 = response.itemInfo[2].concat('">',response.itemInfo[3]);
            var html_5 = '</a></div><div class="matchInfo">';
            var html_6 = response.itemInfo[4].concat('<br/>',response.itemInfo[5]);
            var html_7 = '<br/><input type="submit" class="swipeButton left" value="X" id="noMatch" name="noMatch"><input type="submit" class="swipeButton right" value="$" id="match" name="match"><input name="indexSend" id="indexSend" type="hidden" value="';
            var html_8 = response.itemInfo[2].concat('"/></div><span class="creationDate">Created on ',response.itemInfo[6],'</span></div></form>');

            var newMatch = html_1.concat(html_2, html_3, html_4, html_5, html_6, html_7, html_8);

            document.getElementById('matchBox').innerHTML = newMatch;
            reloadEvents();

        },
        error: function(error){
            console.log("THIS IS THE FAILURE RESPONSE");
            console.log(error);
        }
    });
    return false;
}

function swipeLeft() {
    $.ajax({
        url: '/noMatch',
        data: JSON.stringify({
            'message': $('input[name="messageSend"]').val(),
            'displayConvo': $('input[name="indexSend"]').val()
        }),
        contentType : "application/json",
        type: 'POST',
        success: function(response){
            console.log("THIS IS THE NO MATCH RESPONSE");

            var html_1 = '<form id="newMatch" method="post"><div class="matchTileContainer" onclick=""><div class="matchName"><a style="font-weight:bold;" href="/profile/';
            var html_2 = response.itemInfo[0].concat('">',response.itemInfo[1]);
            var html_3 = '</a>: <a style="color:#9AF2A5;" href="/items/';
            var html_4 = response.itemInfo[2].concat('">',response.itemInfo[3]);
            var html_5 = '</a></div><div class="matchInfo">';
            var html_6 = response.itemInfo[4].concat('<br/>',response.itemInfo[5]);
            var html_7 = '<br/><input type="submit" class="swipeButton left" value="X" id="noMatch" name="noMatch"><input type="submit" class="swipeButton right" value="$" id="match" name="match"><input name="indexSend" id="indexSend" type="hidden" value="';
            var html_8 = response.itemInfo[2].concat('"/></div><span class="creationDate">Created on ',response.itemInfo[6],'</span></div></form>');

            var newMatch = html_1.concat(html_2, html_3, html_4, html_5, html_6, html_7, html_8);

            document.getElementById('matchBox').innerHTML = newMatch;
            reloadEvents();
        },
        error: function(error){
            console.log(error);
        }
    });
    return false;
}

function reloadEvents() {
    $('#match').bind('click', swipeRight);
    $('#noMatch').bind('click', swipeLeft);
}

window.onload = function () {
    $('#match').bind('click', swipeRight);
    $('#noMatch').bind('click', swipeLeft);

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