#!/usr/bin/env python3
# Flask app to show AutomationHat mini status of volts and temperatures 
# Nigel Armstrong Dec 2022
# v1
#
from datetime import datetime 
from time import sleep
import os
from flask import Flask , render_template, request
EXTTEMPID = '0b228128f0d0'
INTTEMPID = '0315034334ff'
#import automationhat as ahm
from vcgencmd import Vcgencmd
from w1thermsensor import W1ThermSensor
extemp = W1ThermSensor(sensor_id=EXTTEMPID)
intemp = W1ThermSensor(sensor_id=INTTEMPID)
vcgm = Vcgencmd()

#volts = ahm.analog.one.read()
ctemp = vcgm.measure_temp()
etemp = extemp.get_temperature() 
itemp = intemp.get_temperature()
tnow = datetime.now().strftime("%a %d/%m/%Y, %H:%M")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


# a simple page that shows status 
    @app.route('/',methods=['POST', 'GET'])
    def status(): 
#        if request.method == "POST":
#            #volts = ahm.analog.one.read()
#            ctemp = vcgm.measure_temp()
#            etemp = extemp.get_temperature() 
#            itemp = intemp.get_temperature()
#            tnow = datetime.now().strftime("%a %d/%m/%Y, %H:%M")     
#        return render_template('status.html',volts = volts,etemp=etemp,ctemp=ctemp,itemp=itemp,tnow=tnow)
        return render_template('status.html',etemp=etemp,ctemp=ctemp,itemp=itemp,tnow=tnow)

    return app