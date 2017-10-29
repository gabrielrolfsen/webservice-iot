import RPi.GPIO as GPIO

class Light_bulb:

	def __init__(self):
		self.timer_dimmer = 0.0
		self.dimmer_value = 0
		self.light_status = "OFF"
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(15, GPIO.OUT)

	def light_on(self):
		self.dimmer_value = 10
		self.light_status = "ON"
		print("Ligou")
		GPIO.output(15, GPIO.HIGH)

	def light_off(self):
		self.dimmer_value = 0
		self.light_status = "OFF"
		print("Desligou")
		GPIO.output(15, GPIO.LOW)

	def set_dimmer_value(self,new_value):
		if (new_value == 0) or (new_value < 0):
			self.dimmer_value = 0
			self.light_status = "OFF"

		elif (new_value == 1):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.0045

		elif (new_value == 2):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.004

		elif (new_value == 3):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.0035

		elif (new_value == 4):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.0030

		elif (new_value == 5):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.0025

		elif (new_value == 6):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.002

		elif (new_value == 7):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.0015

		elif (new_value == 8):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.001

		elif (new_value == 9):
			self.dimmer_value = new_value
			self.light_status = "ON"
			self.timer_dimmer = 0.0005

		elif (new_value == 10) or (new_value > 10):
			self.dimmer_value = 10
			self.light_status = "ON"

		else:
			self.dimmer_value = new_value
			self.light_status = "ON"
			