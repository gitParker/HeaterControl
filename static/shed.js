$(function() {
	if (screenfull.enabled) {
		screenfull.request();
	}
	
	socket = io.connect();

	socket.on('connect', function() {
		socket.emit('clientConnect', navigator.platform + ', ' + navigator.vendor + ', ' + navigator.userAgent);
	});
	
	$('#toggleBtn').on('toggle', function(e, isOn) {
		console.log('client sending: toggle');
		socket.emit('toggle');
	});
	
	socket.on('toggle', function(dataStr) {
		var data = $.parseJSON(dataStr);
		var theToggle = $('#toggleBtn').data('toggles');
		console.log('receiving: ' + dataStr);
		
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
		$('#gauge').jqxLinearGauge('value', data.temp);
		$('#date').html(data.date);
		$('#time').html(data.time);
	});
});

