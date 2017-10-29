from RPIO.PWM import Servo
import RPIO

import time

class Lock:
    LOCKED = 1
    UNLOCKED = 6

    TURN_TIME = 1000

    def __init__(self, pin, frequency = 20):
        self.servo = Servo(subcycle_time_us = frequency * 1000)
        self.pin = pin
        self.servo.set_servo(self.pin, Lock.LOCKED * 1000)

    def lock(self):
        self.servo.set_servo(self.pin, Lock.LOCKED * 1000)
        time.sleep(0.4)
        self.state = Lock.LOCKED

    def unlock(self):
        self.servo.set_servo(self.pin, Lock.UNLOCKED * 1000)
        time.sleep(0.6)
        self.state = Lock.UNLOCKED
        

    def state(self):
        if self.state is Lock.LOCKED:
            return "LOCKED"
        else:
            return "UNLOCKED"

    def toggle(self):
        if self.state is Lock.LOCKED:
            self.unlock()
        else:
            self.lock()

    def set_tcp_interrupt(self, port):
        def callback(socket, command):
            if command == "STATE":
                socket.send(self.state())
            elif command == "LOCK":
                self.lock()
            elif command == "UNLOCK":
                self.unlock()
            elif command == "TOGGLE":
                self.toggle()

            RPIO.close_tcp_client(socket.fileno())

        RPIO.add_tcp_callback(port, callback= callback, threaded_callback= True)


    def set_gpio_interrupt(self, pin):
        def callback(pin, val):
            if val:
                self.unlock()

        RPIO.add_interrupt_callback(pin, callback= callback, threaded_callback= True)

    def __del__(self):
        self.servo.stop_servo(self.pin)