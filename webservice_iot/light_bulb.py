import RPi.GPIO as GPIO

class Light_bulb:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setupwarnings(False)
        GPIO.setup(16, GPIO.OUT)

    def light_on(self):
        print("Ligou")
        GPIO.output(16, GPIO.HIGH)

    def light_off(self):
        print("Desligou")
        GPIO.output(16, GPIO.LOW)
