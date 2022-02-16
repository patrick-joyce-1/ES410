import time
import cv2
import os
import RPi.GPIO as GPIO
import sleep

## Added a for loop within the if statements

# Pin Definitions
motor_pin_a = 18  # BOARD pin 18
motor_pin_b = 12  # BOARD pin 12


def main():
    try:
        # Pin Setup
        # Board pin-numbering scheme
        GPIO.setmode(GPIO.BCM)
        # Set both pins to LOW
        GPIO.setup(motor_pin_a, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(motor_pin_b, GPIO.OUT, initial=GPIO.LOW)

        # Initialise variables
        camerafov = 60  # FOV (degrees)
        camerares = [1920, 1080]  # Resolution
        app = camerafov / camerares[0]  # Angle per pixel
        motorposition = 0  # Motor angle

        while True:
            # Apriltag position system
            # determine position of apriltag
            # script about detecting apriltag position
            # corners = [[#,#],[#,#],[#,#],[#,#]]
            # pixel = (corners[0,1]+corners[1,1]+corners[2,1]+corners[3,1])/4 # average apriltag position in x direction

            #pixel = input("Enter measured value")
            #pixelangle = (pixel - 540) * app
            pixelangle = input("Enter measured value")
            print("Measured angle is: ", pixelangle)
            # middle is 540

            # Alignment system
            if abs(motorposition - pixelangle) > 0.9:  # if greater than highest precision
                if motorposition > pixelangle:  # i.e. angle is less than current motor position
                    # Set GPIO pin anti-clockwise
                    GPIO.output(motor_pin_b, 0)
                    print("anticlockwise")
                elif motorposition < pixelangle:
                    # Set GPIO pin clockwise
                    GPIO.output(motor_pin_b, 1)
                    print("clockwise")
                for i in range(1, round(abs(motorposition - pixelangle) / 1.8) + 1):
                    # Set GPIO pin signal high-low
                    GPIO.output(motor_pin_a, 1)
                    GPIO.output(motor_pin_a, 0)
                    motorposition += 1.8
                print("Motor position is: ", motorposition)

            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
