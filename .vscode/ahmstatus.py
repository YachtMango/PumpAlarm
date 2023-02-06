#!/usr/bin/env python3
# AutomationHat mini status of volts and temperstures 
# Nigel Armstrong Nov 2022
# v1
EXTTEMPID = '00000de08f5a'
INTTEMPID = '0315034334ff'
import automationhat as ahm
from vcgencmd import Vcgencmd
from w1thermsensor import W1ThermSensor
extemp = W1ThermSensor(sensor_id=EXTTEMPID)
intemp = W1ThermSensor(sensor_id=INTTEMPID)
vcgm = Vcgencmd()
ctemp = vcgm.measure_temp() # CPU temp
etemp = extemp.get_temperature() # external temp
itemp = intemp.get_temperature() # internal temp
v = ahm.analog.one.read()
print(f"Volts = {v}; CPU Temp = {ctemp}, Int Temp = {itemp}, Ext Temp =  {etemp} *C")
