$(function() {
	if (screenfull.enabled) {
		screenfull.request();
	}
	
	socket = io.connect();

	socket.on('connect', function() {
		socket.emit('clientConnect', navigator.platform + ', ' + navigator.vendor + ', ' + navigator.userAgent);
	});
	
	$('.toggle').toggles({
		on: false,
		height: 50,
		width: 100
	});
	
	$('#toggleBtn').on('toggle', function(e, isOn) {
		console.log('client sending: toggle');
		socket.emit('toggle');
	});
	
	socket.on('toggle', function(dataStr) {
		let data = $.parseJSON(dataStr);
		let theToggle = $('#toggleBtn').data('toggles');
		if (data.heatOn === 'True') {
			$('body').removeClass('heatOff')
			$('body').addClass('heatOn');
			theToggle.toggle(true, false, true)
		} else {
			$('body').removeClass('heatOn')
			$('body').addClass('heatOff');
			theToggle.toggle(false, false, true)
		}
		$('#temp').html(data.temp + '&deg;');
		$('#time').html(data.time);
	});
});

