import time
import RPi.GPIO as GPIO

t1 = 0.000 #max  0.0055
# 55 -> 30-40V , 45 -> 50-60V, 35 -> 60-80, 25 -> 80-95, 15 -> 95-110
# 05 -> 105-120, 00-> 110-127 
t2 = 0.000006 #0.000006
#counter = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def zc(channel):
#    global counter
#    counter += 1
#    if (counter == 120):
#        print("1s: ", time.clock())
#        counter = 0

    milli_sec = int(round(time.time() * 1000))
    print(milli_sec)
    time.sleep(t1)
    GPIO.output(16,GPIO.HIGH)
    time.sleep(t2)
    GPIO.output(16, GPIO.LOW)

GPIO.add_event_detect(15, GPIO.RISING, callback=zc, bouncetime = 7)

try:
    print ("Waiting...\n")
    GPIO.wait_for_edge(37, GPIO.RISING)
    print ("rolouu!\n")

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
