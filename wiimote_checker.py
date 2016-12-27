import pigpio
import os
import subprocess
import sys
import time

from timeout import timeout, TimeoutError

is_debug = "debug" in sys.argv

pi = pigpio.pi()
motor = 18

@timeout(2)
def try_comms(bdaddr):
	command = str(os.popen("sudo l2ping -c 1 -t 1 " + bdaddr).read())
	return command

pi.set_PWM_frequency(motor, 50)

while True:
	output = try_comms("00:1F:C5:86:3E:85")
	if ("100% loss") in output:
		pi.set_servo_pulsewidth(motor, 1500)
		os.system("sudo pkill python")		
	time.sleep(1)
