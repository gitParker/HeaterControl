from flask import Flask, send_from_directory, render_template, redirect, jsonify
import time
from controlTest import Control
#from control import Control
#from gpioSetup import *
from flask_socketio import SocketIO
import eventlet
import socketio

app = Flask(__name__)
sio = SocketIO(app)
control = Control()

## web app handlers
@app.route('/')
def index():
    return render_template('index.html', dateTime=getTime(), control=control)


@app.route('/toggle', methods=['POST', 'GET'])
def toggleJ():
    control.toggleHeater()
    print ('json =', jsonify(heatOn=control.isHeatOn(), time=getTime()))
    return jsonify(heatOn=control.isHeatOn(), time=getTime())

def getTime() -> str:
    return time.strftime("%b %m %Y %I:%M:%S %p")



## socket handlers
@sio.on('clientConnect')
def handle_messag(message):
    print('connection from', message)
    jsonResult = '{"heatOn":"' + str(control.isHeatOn()) + '", "time":"' + getTime()+ '"}'
    sio.emit('Connect 1st response: ', jsonResult, broadcast=True)

@sio.on('disconnect')
def disconnect():
    print('client disconnect')

@sio.on('toggle')
def toggleSockIo():
    print('client sent sio: toggle')
    control.toggleHeater()
    jsonResult = '{"heatOn":"' + str(control.isHeatOn()) + '", "time":"' + getTime()+ '"}'
    print ('jsonResult = ' + jsonResult)
    sio.emit('toggle', jsonResult, broadcast=True)

def toggle_callback(pin):
    print('detected change on %s'%pin)
    jsonResult = '{"heatOn":"' + str(control.isHeatOn()) + '", "time":"' + getTime()+ '"}'
    sio.emit('toggle', jsonResult, broadcast=True)
    print('sio.emit(\'toggle\', ' + jsonResult + ', broadcast=True)')

#gpio.add_event_detect(PIN_HEAT_ON, gpio.BOTH, toggle_callback, bouncetime=200)
##gpio.add_event_detect(PIN_HEAT_ON, gpio.BOTH, callback=toggle_callback, bouncetime=300)

#gpio.add_event_detect(PIN_HEAT_ON, gpio.RISING, callback=toggle_callback, bouncetime=300)
#gpio.add_event_detect(PIN_HEAT_ON, gpio.FALLING, callback=toggle_callback, bouncetime=300)

## Main start
if __name__ == '__main__':
    print("trying to start up")

    sio.run(app, debug=True, host='0.0.0.0', port=int("5000"))

    #app.run(debug=True, host='0.0.0.0', port=int("5000"))
    #sio.run(app, async_mode='eventlet')

    #app = socketio.Middleware(sio, app)
    #eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

    print("Shutting Down")
    # Use authbind to bind to port 80 https://mutelight.org/authbind
