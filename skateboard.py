# skateboard.py
# DIY Electric Skateboard
# Created by Matthew Timmons-Brown, The Raspberry Pi Guy
# Matt's safety procedures were designed and coded by Simon Beal.
# If I die, it is his fault
# Simon accepts no responsibility for any damage caused by the use of this program
# to the extent allowed by UK law

import pigpio
import time
import cwiid
import os
import sys

from timeout import timeout, TimeoutError

pi = pigpio.pi()
is_debug = "debug" in sys.argv

class Skateboard(object):
	"""An all-powerful skateboard controller"""
	motor = 18
	led = 17
	button = 27

	min_speed = 1720
	max_speed = 1100

	servo_smooth = 2
	smooth_sleep = 0.005
	accel_sleep = 0.001
	
	def __init__(self):
		pi.set_PWM_frequency(Skateboard.motor, 50)
		pi.set_mode(Skateboard.led, pigpio.OUTPUT)
		pi.set_mode(Skateboard.button, pigpio.INPUT)
		pi.set_pull_up_down(Skateboard.button, pigpio.PUD_UP)
		self.__speed = 1500
		self.speed=1500

	@property
	def speed(self):
		return self.__speed

	@speed.setter
	def speed(self, value):
		value = max(min(value, Skateboard.min_speed), Skateboard.max_speed)
		while abs(value-self.__speed) > Skateboard.servo_smooth:
			direction = cmp(value, self.__speed)
			self.__speed += direction * Skateboard.servo_smooth
			pi.set_servo_pulsewidth(Skateboard.motor, self.__speed)
			time.sleep(Skateboard.smooth_sleep)
		pi.set_servo_pulsewidth(Skateboard.motor, value)		
		self.__speed = value
		time.sleep(Skateboard.accel_sleep)

	def blinky(self,times,period):
		for i in range (1,times):
			pi.write(self.led,1)
			time.sleep(period)
			pi.write(self.led,0)
			time.sleep(period)

	def connection_process(self):
		connected = False
		while not connected:
			self.blinky(5,0.4)
			try:
				self.wii = cwiid.Wiimote(bdaddr="00:1F:C5:86:3E:85")
				connected = True
				self.blinky(40,0.03)
				self.wii.rpt_mode = cwiid.RPT_BTN
				self.wii.rumble = 1
				time.sleep(1)
				self.wii.rumble = 0
			except RuntimeError:
				pass

	def run_process(self):
		pi.write(self.led, 1)
		self.get_status()
		if self.status_button:
			raise RuntimeError("Status Button")

		if (self.buttons & cwiid.BTN_B):
			self.speed = 1500
			time.sleep(3)
		if (self.buttons & cwiid.BTN_DOWN):
			self.speed += 1
		if (self.buttons & cwiid.BTN_UP):
			self.speed -= 1

	@timeout(0.4)
	def get_status(self):
		self.buttons = self.wii.state['buttons']
		self.status_button = not pi.read(Skateboard.button)

	
### Main Program ###

skate = Skateboard()
skate.blinky(20,0.05)
skate.connection_process()
while True:
	try:
		skate.run_process()
		print(skate.speed)
	except KeyboardInterrupt:
		raise
	except:
		skate.speed = 1500
		if is_debug:
			raise
		else:
			os.system("poweroff")
