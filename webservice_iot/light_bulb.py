#import RPi.GPIO as GPIO

class Light_bulb:

	def __init__(self):
		self.dimmer_value = 0
		self.light_status = "OFF"
#       GPIO.setmode(GPIO.BOARD)
#       GPIO.setupwarnings(False)
#       GPIO.setup(16, GPIO.OUT)

	def light_on(self):
		self.dimmer_value = 10
		self.light_status = "ON"
		print("Ligou")
#        GPIO.output(16, GPIO.HIGH)

	def light_off(self):
		self.dimmer_value = 0
		self.light_status = "OFF"
		print("Desligou")
#       GPIO.output(16, GPIO.LOW)

#	def set_dimmer_value(new_value):
#		if (new_value < 0):
#			self.dimmer_value = 0
#		elif (new_value > 10):
#			self.dimmer_value = 10
#		else:
#			self.dimmer_value = new_value

#		return self.dimmer_value
