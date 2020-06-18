let counter = 10;

setInterval(() => {
	document.querySelector('h2').innerText = "Next update: " + counter;
	counter--;
	
	if (counter < 0) {
		window.location.reload(true);
	}
	
}, 1000)