import RPi.GPIO as GPIO
import time

class Servo:
    OPEN = 12
    CLOSE = 2

    def __init__(self, pin = 40, freq = 40):
        self.state = self.CLOSE
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, freq)
        self.pwm.start(0)
        servo_status = "CLOSE"
        return

    def open(self):
        self.pwm.ChangeDutyCycle(Servo.OPEN)
        time.sleep(0.4)
        self.state = Servo.OPEN
        self.servo_status = "OPEN"
        print("RODANDO OPEN")

    def close(self):
        self.pwm.ChangeDutyCycle(Servo.CLOSE)
        time.sleep(0.6)
        self.state = Servo.CLOSE
        self.servo_status = "CLOSE"
        print("RODANDO CLOSE")

    def estado(self):
        if self.state is Servo.OPEN:
            return "OPEN"
        else:
            return "CLOSE"

    def toggle(self):
        if self.state is Servo.OPEN:
            self.close()
        else:
            self.open()

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()
        return
