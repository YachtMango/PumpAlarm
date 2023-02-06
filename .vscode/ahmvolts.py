import automationhat as ahm
from vcgencmd import Vcgencmd
vcgm = Vcgencmd()
t = vcgm.measure_temp()
v = ahm.analog.one.read()
print (str(v) + " volts" + " &" , str(t) + "C")

