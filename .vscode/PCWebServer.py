#!/usr/bin/env python3
# Simple Python Web Server to display voltahes and temperature of the Pump Control 
# Nigel Armstrong Jan 2023
# v1
#
#
#
EXTTEMPID = '0b228128f0d0'
INTTEMPID = '0315034334ff'
#
from datetime import datetime
import time 
import automationhat as ahm
from vcgencmd import Vcgencmd
from w1thermsensor import W1ThermSensor

vcgm = Vcgencmd()
extemp = W1ThermSensor(sensor_id=EXTTEMPID)
intemp = W1ThermSensor(sensor_id=INTTEMPID)
tnow = datetime.now().strftime("%a %d/%m/%Y, %H:%M")
volts = ahm.analog.one.read() # Battery Voltage at ahm
ctemp = vcgm.measure_temp() # CPU temp
etemp = extemp.get_temperature() # external temp
itemp = intemp.get_temperature() # internal temp


from http.server import HTTPServer, BaseHTTPRequestHandler

class Serv(BaseHTTPRequestHandler):


    print(tnow,volts,ctemp,etemp,itemp,)

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type","text/html")
        tnow = datetime.now().strftime("%a %d/%m/%Y, %H:%M")
        volts = ahm.analog.one.read() # Battery Voltage at ahm
        self.end_headers()

        ctemp = vcgm.measure_temp() # CPU temp
        etemp = extemp.get_temperature() # external temp
        itemp = intemp.get_temperature() # internal temp
        self.wfile.write(bytes("<html>\
    <head>\
        <title>Pump Control Status</title>\
     <style>\
                body {\
                        background: skyblue;\
                        font-family: Tahoma, Verdana, Arial, sans-serif;\
                        }\
        </style>\
    </head>\
    <body background:red;>\
    <center>\
        <h1>Pump Control Status @ {tnow}  </h1>\
        <hr />\
        <h2>Voltage</h2>\
        <p>Battery voltage =  {volts}  </p>\
        <h2>CPU Temperature</h2>\
        <p>CPU Temperature = {ctemp}</p>\
        <h2>External Temperature</h2>\
        <p>External Temperature = {etemp}</p>\
        <h2>Internal Temperature</h2>\
        <p>Internal Temperature = {itemp}</p>\
    </center>\
    </body>\
    </html>",'utf-8'))

httpd = HTTPServer(('0.0.0.0', 8080), Serv)
httpd.serve_forever()