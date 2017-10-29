import RPIO

class Bulb:

    def __init__(self, pin):
        self.pin = pin
        self.dimmer = 0
        self.timer = 0.0
        RPIO.setup(self.pin, RPIO.OUT, initial = RPIO.LOW)

    def on(self):
        self.dimmer = 10
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        self.dimmer_value = 0
        GPIO.output(self.pin, GPIO.LOW)

    def set_dimmer(self, new_value):
        self.dimmer = new_value
        self.on()

        if new_value <= 0:
            self.dimmer = 0
            self.off()

        elif new_value == 1:
            self.timer = 0.0005

        elif new_value == 2:
            self.timer = 0.001

        elif new_value == 3:
            self.timer = 0.002

        elif new_value == 4:
            self.timer = 0.0025

        elif new_value == 5:
            self.timer = 0.003

        elif new_value == 6:
            self.timer = 0.004

        elif new_value == 7:
            self.timer = 0.005

        elif new_value == 8:
            self.timer = 0.0055

        elif new_value == 9:
            self.timer = 0.006

        else:
            self.dimmer = 10

    def state(self):
        if self.dimmer <= 0:
            return "OFF,0"
        else:
            return "ON," + str(self.dimmer)

    def toggle(self):
        if self.dimmer <= 0:
            self.on()
        else:
            self.off()

    def set_tcp_interrupt(self, port):
        def callback(socket, command):
            if command == "STATE":
                socket.send(self.state())
            elif command == "ON":
                self.on()
            elif command == "OFF":
                self.off()
            elif command == "TOGGLE":
                self.toggle()
            elif command.split(',')[0] == "SET":
                self.set_dimmer(int(command.split(',')[1]))

            RPIO.close_tcp_client(socket.fileno())

        RPIO.add_tcp_callback(port, callback= callback, threaded_callback= True)


    def set_gpio_interrupt(self, pin):
        def callback(pin, val):
            if val:
                self.unlock()

        RPIO.add_interrupt_callback(pin, callback= callback, threaded_callback= True, pull_up_down= GPIO.PUD_DOWN)

    def __del__(self):
        RPIO.cleanup(self.pin)
