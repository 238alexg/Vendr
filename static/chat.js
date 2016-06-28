// chat.js


function init() {
	var ul = document.getElementById("ul");
	var items = ul.getElementsByTagName("li");
	for (var i = 0; i < items.length; ++i) {
		console.log(items[i].value);
	}
}

window.onload = init;