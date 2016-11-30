import serial,time
import pynmea2
from threading import Timer

ser = 0
latitude=''
longitude=''

def init_serial():
    global ser
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = '/dev/serial0'
    ser.timeout = 1
    ser.open()
    if ser.isOpen():
        print 'Open: ' + ser.portstr

def output_gps():
     print str(latitude)+","+str(longitude)
     repeat_thread = Timer(0.1,output_gps)
     repeat_thread.start()

init_serial()
repeat_thread = Timer(1, output_gps)
repeat_thread.start()

while True:
        if ser.inWaiting() > 0 :
                recv=ser.readline()
                if recv.find('$GPGGA')!=-1:
                        msg=pynmea2.parse(recv)
                        latitude=msg.latitude
                        longitude=msg.longitude

