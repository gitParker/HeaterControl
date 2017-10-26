from flask import Flask, send_from_directory, render_template, redirect, jsonify
import time
import threading
#from controlTest import *
from control import *
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


def getTime() -> str:
    return time.strftime("%b %m %Y %I:%M:%S %p")

def makeJson():
    return '{"heatOn":"' + str(control.isHeatOn()) + '", "time":"' + getTime()+ '", "temp":"'+control.getTemp()+'"}'

## socket handlers
@sio.on('clientConnect')
def handleConnect(message):
    print('connection from', message)
    jsonResult = makeJson()
    sio.emit(event='toggle', data=jsonResult, namespace='/', broadcast=True)


@sio.on('disconnect')
def disconnect():
    print('client disconnect ')
    

@sio.on('toggle')
def toggleSockIo():
    print('client sent sio: toggle')
    control.toggleHeater()
    jsonResult = makeJson()
    print ('jsonResult = ' + jsonResult)
    sio.emit(event='toggle', data=jsonResult, namespace='/', broadcast=True)
    print ('sent emit')
    

def toggle_callback(pin):
    print('detected change on %s'%pin)
    jsonResult = makeJson()
    sio.emit(event='toggle', data=jsonResult, namespace='/', broadcast=True)
    print('sio.emit(\'toggle\', ' + jsonResult + ', broadcast=True)')


## Update Temp every once in a while
def updateStatus():
    while(True):
        time.sleep(10)
        jsonResult = makeJson()
        print ('updateStatus() = ' + jsonResult)
        sio.emit(event='toggle', data=jsonResult, namespace='/', broadcast=True)

t = threading.Thread(target=updateStatus)
t.setDaemon(True)
t.start()

gpio.add_event_detect(PIN_HEAT_ON, gpio.BOTH, callback=toggle_callback, bouncetime=10)

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
    # Start server with $>python3.* web.py
