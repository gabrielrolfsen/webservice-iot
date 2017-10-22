import time
import RPi.GPIO as GPIO

t1 = 0.0 #max  0.0055
t2 = 0.000024 #0.000006
counter = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def zc(channel):
    global counter
    counter += 1
    if (counter == 120):
        print("1s: ", time.clock())
        counter = 0

    milli_sec = int(round(time.time() * 1000))
    print(milli_sec)
    time.sleep(t1)
    GPIO.output(16,GPIO.HIGH)
    time.sleep(t2)
    GPIO.output(16, GPIO.LOW)

GPIO.add_event_detect(37, GPIO.RISING, callback=zc, bouncetime = 7)

try:
    print ("Waiting...\n")
    GPIO.wait_for_edge(15, GPIO.RISING)
    print ("rolouu!\n")

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
