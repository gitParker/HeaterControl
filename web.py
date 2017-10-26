from flask import Flask, send_from_directory, render_template, redirect, jsonify
import time
import threading
#from controlTest import Control
from control import Control
from gpioSetup import *
from flask_socketio import SocketIO
import eventlet
import socketio

app = Flask(__name__)
sio = SocketIO(app, async_mode='threading')
control = Control()
clients = {}

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
def handleConnect(message):
    print('connection from', message)
    #addClient(request.namespace, request.namespace.socket.sessid)
    jsonResult = '{"heatOn":"' + str(control.isHeatOn()) + '", "time":"' + getTime()+ '"}'
    sio.emit('Connect 1st response: ', jsonResult)

def addClient(namespace, sessid):
    if not sessid in clients:
        clients[sessid] = namespace
        print ('added ', sessid)

def sendToAll(action, data):
    if clients.keys():
        for c in clients.keys():
            clients[c].socketio.emit(action, data)

@sio.on('disconnect')
def disconnect():
    print('client disconnect ')
    #del clients[request.namespace.socket.sessid]
    

@sio.on('toggle')
def toggleSockIo():
    print('client sent sio: toggle')
    control.toggleHeater()
    jsonResult = '{"heatOn":"' + str(control.isHeatOn()) + '", "time":"' + getTime()+ '"}'
    print ('jsonResult = ' + jsonResult)
    sio.emit(event='toggle', data=jsonResult, namespace='/', broadcast=True)
    #sendToAll('toggle', jsonResult)
    print ('sent emit')
    

def toggle_callback(pin):
    print('detected change on %s'%pin)
    jsonResult = '{"heatOn":"' + str(control.isHeatOn()) + '", "time":"' + getTime()+ '"}'
    sio.emit(event='toggle', data=jsonResult, namespace='/', broadcast=True)
    print('sio.emit(\'toggle\', ' + jsonResult + ', broadcast=True)')


## Testing server generated events
def flippingStatus():
    while(True):
        time.sleep(5)
        print ('flippingStatus()')
        control.toggleHeater()
        jsonResult = '{"heatOn":"' + str(control.isHeatOn()) + '", "time":"' + getTime()+ '"}'
        print ('jsonResult = ' + jsonResult)
        sio.emit(event='toggle', data=jsonResult, namespace='/', broadcast=True)
        #sendToAll('toggle', jsonResult)
        print ('emited flip')

#t = threading.Thread(target=flippingStatus)
#t.setDaemon(True)
#t.start()

#gpio.add_event_detect(PIN_HEAT_ON, gpio.BOTH, toggle_callback, bouncetime=200)
gpio.add_event_detect(PIN_HEAT_ON, gpio.BOTH, callback=toggle_callback, bouncetime=10)

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
