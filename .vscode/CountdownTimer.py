import time
import sys
INPUTA = 10
INPUTB = 15

for i in reversed(range(0,INPUTA)):
    time.sleep(1 - time.time() % 1)
    print('\r%4d' % i)
    #print (i),
    