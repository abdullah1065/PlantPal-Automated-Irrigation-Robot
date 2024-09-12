import RPi.GPIO as GPIO
import time

# Pin Definitions
moisture_sensor_pin = 16  # GPIO pin 18

def setup():
    # Set up the GPIO channel
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(moisture_sensor_pin, GPIO.IN)  # Set GPIO pin as an input

def read_moisture():
    # Read from the moisture sensor
    if GPIO.input(moisture_sensor_pin):
        print("Soil is dry")
    else:
        print("Soil is moist")

def cleanup():
    GPIO.cleanup()  # Clean up GPIO to reset GPIO pins

def main():
    setup()
    try:
        while True:
            read_moisture()
            time.sleep(1)  # Delay for 1 second
    finally:
        cleanup()  # Ensure GPIOs are cleaned up even if an error occurs

if __name__ == '__main__':
    main()
