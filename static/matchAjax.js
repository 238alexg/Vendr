// AJAX request for new matches

window.onload = function () {
    $('#send_data').bind('click', function() {
        $.getJSON('/loadMatches', {
        newWord: $('input[name="newWord"]').val()
    }, 
    function(data) {
        var ul = document.getElementById('resultContainer');
        $(ul).empty();
        for (var i = data.result.length - 1; i >= 0; i--) {
            var newLi = document.createElement('li');
            console.log(newLi);
            newLi.appendChild(document.createTextNode(data.result[i]));
            newLi.classList.add('searchResult');
            ul.appendChild(newLi);
        };
    });
    return false;
    });
};