# skateboard.py
# DIY Electric Skateboard
# Created by Matthew Timmons-Brown, The Raspberry Pi Guy

import pigpio
import time
import cwiid

pi = pigpio.pi()

class Skateboard:
	"""An all-powerful skateboard controller"""
	motor = 18
	led = 17
	button = 27
	
	def __init__(self):
		pi.set_PWM_frequency(self.motor,50)
		pi.set_mode(self.led,pigpio.OUTPUT)
		pi.set_mode(self.button,pigpio.INPUT)
		pi.set_pull_up_down(self.button, pigpio.PUD_UP)
		self.speed=1500

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
		pi.write(self.led,1)
		self.buttons = self.wii.state['buttons']

		if (self.buttons & cwiid.BTN_B):
			if self.speed>=1300:
				self.speed=1500
			elif self.speed < 1300:
				for i in range(self.speed,1501,1):
					self.speed=i
					time.sleep(0.01)

		if (self.buttons & cwiid.BTN_DOWN):
			self.speed=self.speed+1
		if (self.buttons & cwiid.BTN_UP):
			self.speed=self.speed-1
		if self.speed<1000:
			self.speed=1000
		if self.speed>1720:
			self.speed=1720

### Main Program ###

skate = Skateboard()
#skate.blinky(35,0.05)
skate.connection_process()
while True:
	print(skate.speed)
	skate.run_process()
	pi.set_servo_pulsewidth(18,skate.speed)
