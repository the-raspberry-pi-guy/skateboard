# Main.py
# Program for DIY Electric Skateboard
# Created by Matthew Timmons-Brown, The Raspberry Pi Guy

import pigpio
import time
import cwiid

pi = pigpio.pi()

motor = 18
led = 17
button = 27

global speed
speed = 1000

pi.set_PWM_frequency(motor,50)
pi.set_mode(led,pigpio.OUTPUT)
pi.set_mode(button,pigpio.INPUT)
pi.set_pull_up_down(button, pigpio.PUD_UP)

def blinky(times,period):
        for i in range (1,times):
                pi.write(led,1)
                time.sleep(period)
                pi.write(led,0)
                time.sleep(period)

def connection_process():
        connected = False
#       pi.set_servo_pulsewidth(18,1000)
        while not connected:
                blinky(5,0.5)
                try:
                        global wii
                        wii = cwiid.Wiimote(bdaddr=00:1F:C5:86:3E:85)
                        connected = True
                        blinky(40,0.03)
                        wii.rpt_mode = cwiid.RPT_BTN
                        wii.rumble = 1
                        time.sleep(1)
                        wii.rumble = 0
                        return wii
                except RuntimeError:
                        pass

def run_process():
        pi.write(led,1)
        global speed
        buttons = wii.state['buttons']

        if (buttons & cwiid.BTN_B):
                if speed<=1700:
                        speed=1350
                elif speed >= 1700:
                        for i in range(speed,1350,-1):
                                speed=i

        if (buttons & cwiid.BTN_UP):
                speed=speed+5
        if (buttons & cwiid.BTN_DOWN):
                speed=speed-10

        #if speed<:
        #       speed=1000
        if speed>2050:
                speed=2000
        return int(speed)

# Main Program

blinky(35,0.05)
connection_process()

while True:
        power=run_process()
        print power
        pi.set_servo_pulsewidth(18,power)
