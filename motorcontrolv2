import RPi.GPIO as GPIO
import time

# Pin Definitions
output_pin = 18 # BOARD pin 12, BCM pin 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(output_pin, GPIO.OUT, initial = GPIO.HIGH)
print("Press CTRL+C to exit")

while True:
  time.sleep(1)
  GPIO.output(output_pin,GPIO.HIGH)
  time.sleep(1)
  GPIO.output(output_pin,GPIO.LOW)
