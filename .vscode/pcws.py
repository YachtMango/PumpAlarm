#!/usr/bin/env python3
# Simple Python Web Server to display voltahes and temperature of the Pump Control 
# Nigel Armstrong Jan 2023
# v1
#
#
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import automationhat as ahm
from vcgencmd import Vcgencmd
from w1thermsensor import W1ThermSensor

EXTTEMPID = '0b228128f0d0'
INTTEMPID = '0315034334ff'

vcgm = Vcgencmd()
extemp = W1ThermSensor(sensor_id=EXTTEMPID)
intemp = W1ThermSensor(sensor_id=INTTEMPID)

volts = ahm.analog.one.read() # Battery Voltage at ahm
tnow = datetime.now().strftime("%a %d/%m/%Y, %H:%M")
ctemp = vcgm.measure_temp() # CPU temp
etemp = extemp.get_temperature() # external temp
itemp = intemp.get_temperature() # internal temp

html_content = f"""
	<!DOCTYPE html>
	<html lang="en">
	<head>
	<meta charset="utf-8">
	<title>Pump Control Status</title>
	</head>
	<body>
	<center>
		<h1>Pump Control Status @ {tnow} </h1>
		<hr />
		<form  method = "post">
			<input type="button" id='script' name="Update" value="Update">
		</form>
		<h2>Voltage</h2>
		<p>Battery voltage = {volts} </p>
		<h2>CPU Temperature</h2>
		<p>CPU Temperature = {ctemp}</p>		
		<h2>External Temperature</h2>
		<p>External Temperature = { etemp }</p>
		<h2>Internal Temperature</h2>
		<p>Internal Temperature = { itemp }</p>
	</center>
	</body>
	</html>"""

with open("status.html", "w") as html_file:
	html_file.write(html_content)
	print("Success creating html page")

class Serv(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/':
			self.path = '/status.html'
		try:
			f = open(self.path[1:]).read()
			self.send_response(200)
		except:
			f = "File not  found"
			self.send_response(404)
		self.send_header("Content-type","text/html")
		self.end_headers()
		self.wfile.write(bytes(f,'utf-8'))

if __name__ == '__main__': 	
    WS = HTTPServer(('0.0.0.0', 8080), Serv)
    print('Server started')
    try:
        WS.serve_forever()
    except KeyboardInterrupt:
        print('Stopping server')
        pass
    WS.server_close()