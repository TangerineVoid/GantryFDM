#!/usr/bin/python2
import argparse
import glob
import sys
import time
from datetime import datetime
import hal

parser = argparse.ArgumentParser(description='HAL component to write data to file text')
parser.add_argument('-n','--name', help='HAL component name',required=True)
parser.add_argument('-i', '--interval', help='Writing update interval', default=1)
parser.add_argument('-fn', '--file_name', help='Writing file name', default='saved_data.txt')

args = parser.parse_args()

updateInterval = float(args.interval)
error = False
watchdog = True
now = datetime.now()
filename = args.file_name + now.strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
print filename

h = hal.component(args.name)
halpin = h.newpin("write", hal.HAL_FLOAT, hal.HAL_IN)
halpin2 = h.newpin("raw",hal.HAL_FLOAT, hal.HAL_IN)
halpin3 = h.newpin("man",hal.HAL_FLOAT, hal.HAL_IN)
halpin4 = h.newpin("set",hal.HAL_FLOAT, hal.HAL_IN)
#h.write = 1
halErrorPin = h.newpin("error", hal.HAL_BIT, hal.HAL_OUT)
halNoErrorPin = h.newpin("no-error", hal.HAL_BIT, hal.HAL_OUT)
halWatchdogPin = h.newpin("watchdog", hal.HAL_BIT, hal.HAL_OUT)
h.ready()

halErrorPin.value = error
halNoErrorPin.value = not error
halWatchdogPin.value = watchdog


try:
    while (True):
        try:
            #print "saving file"
	    f = open(filename, 'a')
            #Como consultar el dato de hal
            #val = "prueba"
	    then = datetime.now()
	    delta = str(then-now)
	    delta = datetime.strptime(delta, "%H:%M:%S.%f")
	    val = str(h.write) + ' ' + str(h.raw) + ' ' + str(h.man) + ' ' + str(h.set) + ' ' + str(delta.strftime("%H %M %S %f")[:~2]) + '\n'
	    f.write(val)
            f.close()
            error = False
        except IOError:
            error = True

        halErrorPin.value = error
        halNoErrorPin.value = not error
        watchdog = not watchdog
        halWatchdogPin.value = watchdog
        time.sleep(updateInterval)
except:
    print(("exiting HAL component " + args.name))
    h.exit()

