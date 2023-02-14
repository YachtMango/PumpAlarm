#!/usr/bin/env python3
# Flask app to show AutomationHat mini status of volts and temperatures 
# Nigel Armstrong Jan 2023
# v2
#
EXTTEMPID = '0b228128f0d0'
INTTEMPID = '0315034334ff'

from datetime import datetime 
from time import sleep
from flask import Flask , render_template, request
import automationhat as ahm
from vcgencmd import Vcgencmd
from w1thermsensor import W1ThermSensor

extemp = W1ThermSensor(sensor_id=EXTTEMPID)
intemp = W1ThermSensor(sensor_id=INTTEMPID)
vcgm = Vcgencmd()

volts = ahm.analog.one.read()
ctemp = vcgm.measure_temp()
etemp = extemp.get_temperature() 
itemp = intemp.get_temperature()
tnow = datetime.now().strftime("%a %d/%m/%Y, %H:%M")

# a simple page that shows stats 
app = Flask(__name__)
@app.route('/',methods=['POST', 'GET'])
def status(): 
	return render_template('stats.html',volts=volts,etemp=etemp,ctemp=ctemp,itemp=itemp,tnow=tnow)
@app.route("/update/", methods=['GET','POST'])
def update():
    volts = ahm.analog.one.read()
    ctemp = vcgm.measure_temp()
    etemp = extemp.get_temperature() 
    itemp = intemp.get_temperature()
    tnow = datetime.now().strftime("%a %d/%m/%Y, %H:%M")
    return render_template('stats.html',volts=volts,etemp=etemp,ctemp=ctemp,itemp=itemp,tnow=tnow)
