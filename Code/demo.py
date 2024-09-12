from objectIdent import getObjects
from ultrasonic import distance
from servoSetup import start_motor

import RPi.GPIO as GPIO
import time

import cv2

# GPIO pins for motor driver input
IN1 = 17
IN2 = 27
IN3 = 18
IN4 = 23
ENA = 25
ENB = 24

# Declare PWM channels as global variables
pwm1 = None
pwm2 = None

# Initialize GPIO
def setup():
    global pwm1, pwm2  # Declare as global to access outside the function
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
   
    # Set PWM instance and frequency
    pwm1 = GPIO.PWM(ENA, 100)
    pwm2 = GPIO.PWM(ENB, 100)
    pwm1.start(75)
    pwm2.start(75)

# Move forward
def forward(speed):
    if pwm1 is not None and pwm2 is not None:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm1.ChangeDutyCycle(speed)
        pwm2.ChangeDutyCycle(speed)

# Move backward
def backward(speed):
    if pwm1 is not None and pwm2 is not None:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm1.ChangeDutyCycle(speed)
        pwm2.ChangeDutyCycle(speed)

# Turn left
def left(speed):
    if pwm1 is not None and pwm2 is not None:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        pwm1.ChangeDutyCycle(speed)
        pwm2.ChangeDutyCycle(speed)

# Turn right
def right(speed):
    if pwm1 is not None and pwm2 is not None:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm1.ChangeDutyCycle(speed)
        pwm2.ChangeDutyCycle(speed)

# Stop
def stop():
    if pwm1 is not None and pwm2 is not None:
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)

# Clean up GPIO
def cleanup():
    stop()
    GPIO.cleanup()
    

MIN_SPEED = 70  # Adjust this value based on your testing

def adjust_speed(distance):
    """ Adjust the speed based on distance, with a minimum speed limit. """
    if distance > 30:
        # Increase speed as distance increases with a max cap at 100
        speed = max(MIN_SPEED, min(100, 70 * (distance / 100)))
    else:
        # Close to the object, slow down but not below the minimum speed
        speed = MIN_SPEED
    return speed

def main():
    cap = cv2.VideoCapture(0)            
    cap.set(3, 640)
    cap.set(4, 480)
    setup()
    target = 'potted plant'
    
    try:
        while True:
            success, img = cap.read()
            result, objectInfo = getObjects(img, 0.45, 0.2, objects=[target])
            if len(objectInfo) > 0:
                axis, name = objectInfo[0]
                dist = distance()
                center_x = img.shape[1] // 2
                tolerance = 50
                print(dist)
                if dist > 10:
                    if axis[0] < center_x - tolerance:
                        left(adjust_speed(dist))
                    elif axis[0] > center_x + tolerance:
                        right(adjust_speed(dist))
                    else:
                        forward(adjust_speed(dist))
                else:
                    stop()
                    if len(objectInfo) > 0:
                        start_motor()
            else:
                stop()
            
            cv2.imshow("Output", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cleanup()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
