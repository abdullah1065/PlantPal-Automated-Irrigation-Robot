import RPi.GPIO as GPIO
import time
import cv2
import serial

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
servo1 = GPIO.PWM(19,50) # Note 11 is pin, 50 = 50Hz pulse
#start PUM running, but with value of o (pulse off)
servo1.start(0)

while True:
    servo1.ChangeDutyCycle (12)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    time.sleep(1.5)
    servo1.ChangeDutyCycle(7)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

