import RPIO
RPIO.cleanup()
RPIO.setmode(RPIO.BOARD)
RPIO.setupwarnings(False)

from door_lock import Lock
from light_bulb import Bulb


lock = Lock(40)
lock.set_gpio_interrupt(35)
lock.set_tcp_interrupt(8080)

bulb = Bulb(16)
bulb.set_gpio_interrupt(15)
bulb.set_tcp_interrupt(8181)

try:
    RPIO.wait_for_interrupts()

except KeyboardInterrupt:
    RPIO.cleanup()