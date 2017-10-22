import RPi.GPIO as GPIO
import time

class Servo:
    OPEN = 12
    CLOSED = 2
    
    def __init__(self, servoPin = 40, freq = 40):
        self.state = self.CLOSED
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(servoPin, freq)
        self.pwm.start(0)

    def open(self):
        self.pwm.ChangeDutyCycle(OPEN)
        time.sleep(0.4)
        self.state = OPEN

    def close(self):
        self.pwm.ChangeDutyCycle(CLOSE)
        time.sleep(0.4)
        self.state = CLOSE

    def estado(self):
    if self.state is OPEN:
        return "OPEN"
    else
        return "CLOSED"

    def toggle(self):
        if self.state is OPEN:
            self.close()
        else:
            self.open()

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()
