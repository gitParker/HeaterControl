$(function() {
	if (screenfull.enabled) {
		screenfull.request();
	}
	
	/*
	// Http request toggle method
    $('#toggleBtn').on('click', function(e) {
        $.getJSON('/toggle', function(data) {
            if (data.heatOn) {
                $('body').removeClass('heatOff')
                $('body').addClass('heatOn');
                $('#toggleBtn').html('On');
            } else {
                $('body').removeClass('heatOn')
                $('body').addClass('heatOff');
                $('#toggleBtn').html('Off');
            }
			$('#time').html(data.time);
        })
        .fail(function(xhr) {
            alert("ajax call failed: status=" + xhr.status + ", msg=" + xhr.statusText);
        });
    })
	*/
	
	socket = io.connect();
	
	socket.on('connect', function() {
		socket.emit('clientConnect', navigator.platform + ', ' + navigator.vendor + ', ' + navigator.userAgent);
	});
	
	$('#toggleBtn').on('click', function(e) {
		console.log('client sending: toggle');
		socket.emit('toggle');
	});
	
	socket.on('toggle', function(dataStr) {
		let data = $.parseJSON(dataStr);
		if (data.heatOn === 'True') {
			$('body').removeClass('heatOff')
			$('body').addClass('heatOn');
			$('#toggleBtn').html('On');
		} else {
			$('body').removeClass('heatOn')
			$('body').addClass('heatOff');
			$('#toggleBtn').html('Off');
		}
		$('#time').html(data.time);
	});
});

