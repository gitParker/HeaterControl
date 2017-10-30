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
	
	$('#gauge').jqxLinearGauge({
		orientation: 'horizontal',
		labels: { interval: 20, position: 'far' },
		ticksMajor: { size: '10%', interval: 10 },
		ticksMinor: { size: '5%', interval: 2.5, style: { 'stroke-width': 1, stroke: '#aaaaaa'} },
		min: -20,
		max: 110,
		pointer: { size: '6%' },
		colorScheme: 'scheme04',
		showRanges: false,
		animationDuration: 0,
		width: 300,
		height: 60
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

