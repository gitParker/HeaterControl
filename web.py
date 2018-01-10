from flask import Flask, send_from_directory, render_template, redirect, jsonify
import time
import threading
import json
##from controlTest import *
from control import *
from gpioSetup import *
from flask_socketio import SocketIO
import eventlet
import socketio

app = Flask(__name__)
sio = SocketIO(app, async_mode='threading')
control = Control()
clients = {}
prevStatus = {'temp': None, 'heatOn': None}

## web app handlers
@app.route('/')
def index():
    global prevStatus
    (dateStr, timeStr) = getTime()
    return render_template('index.html', date=dateStr, time=timeStr, isHeadOn=control.isHeatOn(), temp=prevStatus['temp'])


def getTime() -> str:
    return (time.strftime("%b %d %Y"), time.strftime("%I:%M:%S %p"))

def makeJson():
    global prevStatus
    (dateStr, timeStr) = getTime()
    return '{"heatOn":"' + str(control.isHeatOn()) + '", "date":"' + dateStr + '", "time":"'+timeStr+'", "temp":"'+str(prevStatus['temp'])+'"}'

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
    

def toggle_callback(pin):
    global prevStatus
    print('detected change on %s'%pin, 'calling makeJson()')
    jsonResult = makeJson()
    sio.emit(event='toggle', data=jsonResult, namespace='/', broadcast=True)
    print('sio.emit(\'toggle\', ' + jsonResult + ', broadcast=True)')


## Update Temp every once in a while
def updateStatus():
    global prevStatus
    while(True):
        curTemp = control.getTemp()
        jsonObj = json.loads(makeJson())
        jsonObj['temp'] = curTemp
        if (prevStatus['temp'] is None or prevStatus['heatOn'] is None):
            print('setting prevStatus:', json.dumps(jsonObj))
            prevStatus = jsonObj 
        elif (prevStatus['temp'] != jsonObj['temp'] or prevStatus['heatOn'] != jsonObj['heatOn']):
            prevStatus = jsonObj 
            print('emit from daemon thread:', json.dumps(jsonObj))
            sio.emit(event='toggle', data=json.dumps(jsonObj), namespace='/', broadcast=True)
        time.sleep(20)

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
