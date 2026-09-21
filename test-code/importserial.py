
import serial.tools.list_ports
import sys, threading, queue, serial
from subprocess import Popen


baudRate = 115200
arduinoQueue = queue.Queue()
localQueue = queue.Queue()


ports = serial.tools.list_ports.comports()
for index, value in enumerate(sorted(ports)):
    print(index, '\t', value.name, '\t', value.manufacturer, '\t', value.pid)

ser = serial.Serial('/dev/cu.usbmodem2101',9600)

while True:
    command = ser.read(1)
    if command:
        # flush serial for unprocessed data
        ser.flushInput()
        print(f"new command: {command}")
