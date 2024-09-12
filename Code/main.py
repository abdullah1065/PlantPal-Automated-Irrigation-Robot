import RPi.GPIO as GPIO
import time
import cv2
import serial

from objectIdent import getObjects

GPIO.cleanup()
# For different object detected image window
a = 0
# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)
# For servo motor used for soil moisture sensor
# Set GPIO 19 as an output, and set servol as GPIO 17 as PWM
GPIO.setup(19,GPIO.OUT)
servo1 = GPIO.PWM(19,50) # Note 11 is pin, 50 = 50Hz pulse
#start PUM running, but with value of o (pulse off)
servo1.start(0)

# Declaring constant pin for ultrasonic senson
TRIG=21
ECHO=20
#GPIO.setwarnings(False)
# Front
# Right Wheel Motor pin declaration
in1 = 17
in2 = 27
en_a = 25
# Left Wheel Motor pin declaration
in3 = 18
in4 = 23
en_b = 24


GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en_a, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en_b, GPIO.OUT)
q = GPIO.PWM(en_a, 100)
p = GPIO.PWM(en_b, 100)
p.start(75)
q.start(75)
# setting all the gpio connections low
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
# Wrap main content in a try block so we can catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent the user seeing lots of unnecessary error messages.
servo1.ChangeDutyCycle(12)
time.sleep(0.5)

ser = serial.Serial('/dev/ttyACM0', 9600)

def test(param):
    last_pump_state = False
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            parts = line.split(", ")
            if len(parts) == 2:
                moisture_level = int(parts[0].split(": ")[1])
                water_level = int(parts[1].split(": ")[1])
                # Control pump based on soil moisture
                if moisture_level > param and not last_pump_state:  # Dry soil threshold
                    ser.write("TURN_ON_PUMP\n".encode())
                    last_pump_state = True
                elif moisture_level < param and last_pump_state:  # Wet soil threshold
                    ser.write("TURN_OFF_PUMP\n".encode())
                    last_pump_state = False
                    return
        time.sleep(1)


try:
# Create Infinite loop to read user input
    cap = cv2.VideoCapture(0)            
    cap.set(3, 640)
    cap.set(4, 480)
    target = 'potted plant'
    #target = 'bottle'
    while True:
        success, img = cap.read()
        #img = cv2.resize(img, None, fx=0.4, fy=0.4)
        result, objectInfo = getObjects(img, 0.35, 0.2, objects=[target])
        if len(objectInfo) > 0:
            detection, name = objectInfo[0]
            print(detection)
            height, width, channels = img.shape
            x = int(detection[0] * width)
            y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            
            # For ultrasonic distance detection
            print("distance measurement in progress")
            GPIO.setup(TRIG, GPIO.OUT)
            GPIO.setup(ECHO, GPIO.IN)
            GPIO.output(TRIG, False)
            print("waiting for sensor to settle")
            time.sleep(0.2)
            GPIO.output(TRIG, True)
            time.sleep (0.00001)
            GPIO.output(TRIG, False)
            while GPIO.input(ECHO)==0:
                pulse_start=time.time()
            while GPIO.input(ECHO)==1:
                pulse_end=time.time()
            pulse_duration=pulse_end-pulse_start
            distance=pulse_duration*17150
            distance=round(distance, 2)
            print("distance:", distance, "cm")
            print(x,y,w,h)
            # Controlling movement of model
            # Here x,y coordinate are taken left topmost corner of image to left topmost corner of object detected
            # here w,h are width and heigth of object detected
            # if distance between model and obstacle is less than 20 cm stop the model
            if distance < 10:
                inp = 'stop'
            # otherwise check if no object is detected move backward
            elif w == 0 or h == 0:
                inp = 'back'
            else:
                #if x < 45:
                    #inp = 'right'
                # otherwise check if x coordinate + width of object is greater than 82.3 percent of the width i.e. 210px to move left
                #elif x+w > 210:
                    #inp = 'left'
                # otherwise check it detected obnect area is less than 31515 ox to move the model forward
                #else:
                inp = 'forward'

            input = inp
            if input == 'forward':
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
                time.sleep(0.4)
                GPIO.output(in1, GPIO.LOW)
                GPIO.output (in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.LOW)
                print("Forward")
     
            elif input == 'back':
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
                time.sleep (0.1)
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.LOW)
                print('Back')
      
            elif input == "right":
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
                time.sleep (0.08)
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.LOW)
                print ("Right")
                
            elif input == "left":
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
                time.sleep (0.08)
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.LOW)
                print ("Left")

            elif input ==  "stop":
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.LOW)
                print('Stop')
                # Turn back to 180 degrees
                print ("Turning back to 180(12) degrees")
                servo1.ChangeDutyCycle (12)
                time.sleep(0.5)
                servo1.ChangeDutyCycle(0)
                time.sleep(1.5)
                #turn back to 54 degrees
                print("Turning back to 54 degrees")
                servo1.ChangeDutyCycle(7)
                test(600)
                servo1.ChangeDutyCycle(0)
        cv2.imshow("Output",img)
        cv2.waitKey(1)
    # If user press CTRL-C
except KeyboardInterrupt:
    servo1.ChangeDutyCycle(12)
    time.sleep(0.5)
    GPIO.cleanup()
    print("GPIO Clean up")


