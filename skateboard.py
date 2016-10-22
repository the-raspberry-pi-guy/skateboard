# skateboard.py
# DIY Electric Skateboard
# Created by Matthew Timmons-Brown, The Raspberry Pi Guy

import pigpio
import time
import cwiid

class Skateboard:
	"""An all-powerful skateboard controller"""
	pi = pigpio.pi()
	motor = 18
	led = 17
	button = 27
	
	def __init__(self):
		pi.set_PWM_frequency(motor,50)
		pi.set_mode(led,pigpio.OUTPUT)
		pi.set_mode(button,pigpio.INPUT)
		pi.set_pull_up_down(button, pigpio.PUD_UP)

	def blinky(self,times,period):
		for i in range (1,self.times):
			pi.write(led,1)
			time.sleep(self.period)
			pi.write(led,0)
			time.sleep(self.period)

	def connection_process(self):
		connected = False
		while not connected:
			self.blinky(5,0.4)
			try:
				self.wii = cwiid.Wiimote(bdaddr="00:1F:C5:86:3E:85")
				connected = True
				self.blinky(40,0.03)
				wii.rpt_mode = cwiid.RPT_BTN
				wii.rumble = 1
				time.sleep(1)
				wii.rumble = 0
				return wii
			except RuntimeError:
				pass

	def run_process(self):
		pi.write(led,1)
		self.buttons = wii.state['buttons']

		if (self.buttons & cwiid.BTN_B):
			if speed>=1300:
				speed=1500
			elif speed < 1300:
				for i in range(speed,1501,1):
					speed=i
					time.sleep(0.01)

		if (self.buttons & cwiid.BTN_DOWN):
			speed=speed+1
		if (self.buttons & cwiid.BTN_UP):
			speed=speed-1
		if speed<1000:
			speed=1000
		if speed>1720:
			speed=1720

### Main Program ###

skate = Skateboard()
skate.connection_process()
