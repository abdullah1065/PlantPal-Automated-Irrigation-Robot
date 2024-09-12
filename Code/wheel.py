import RPi.GPIO as GPIO
import time

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
    pwm1.start(0)
    pwm2.start(0)

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
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
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

# Main function
if __name__ == '__main__':
    try:
        setup()
        while True:
     
           
            backward(50)  # Turn left at 50% speed
          
           
        # Turn right at 50% speed
            time.sleep(2)
           
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        cleanup()