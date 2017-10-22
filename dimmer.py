import time, datetime
import RPi.GPIO as GPIO

t1 = 0.008
t2 = 0.000006
counter = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def zc(channel):
#	global counter
#	counter += 1
#	if (counter == 120):
#		print("ZC 1s", time.ctime())
#		counter = 0
	print(time.ctime())
	time.sleep(t1)
	GPIO.output(16,GPIO.HIGH)
	time.sleep(t2)
	GPIO.output(16, GPIO.LOW)

# Garante que apenas ocorra uma interrupcao a cada 7ms (tempo teorico 8,3ms)
GPIO.add_event_detect(37, GPIO.RISING, callback=zc, bouncetime=8)

try:
    print ("Waiting...\n")
    GPIO.wait_for_edge(15, GPIO.RISING)
    print ("rolouu!\n")

except KeyboardInterrupt:
   GPIO.cleanup()
GPIO.cleanup()
