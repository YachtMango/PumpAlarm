from time import sleep
from vcgencmd import Vcgencmd
vcgm = Vcgencmd()
try:
    while True:
        ctemp=vcgm.measure_temp()
        print(ctemp)
        sleep(20)
except KeyboardInterrupt:
    print(" Ctrl-C - quit")