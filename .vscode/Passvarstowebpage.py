#!/usr/bin/env python3
# 
# Nigel Armstrong Dec 2022
# v1
#
# Programme to update webpage with variables
#
EXTTEMPID = '00000de08f5a'
INTTEMPID = '0315034334ff'

f = open("/var/www/html/index.php","r")
html = f.read()
f.close()

import automationhat as ahm
from w1thermsensor import W1ThermSensor
extemp = W1ThermSensor(sensor_id=EXTTEMPID)
intemp = W1ThermSensor(sensor_id=INTTEMPID)

volts = ahm.analog.one.read()
etemp = extemp.get_temperature() # external temp
itemp = intemp.get_temperature() # internal temp