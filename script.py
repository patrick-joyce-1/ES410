# Imports from main
import time
import cv2
import os
import RPi.GPIO as GPIO

# Imports from photov2 (import cv2)

# Imports from apriltagv1 (import cv2)
import apriltag
from PIL import Image
from numpy import asarray

# Pin Definitions
motor_pin_a = 18  # BOARD pin 18
motor_pin_b = 12  # BOARD pin 12

def gstreamer_pipeline(
    capture_width=1920,
    capture_height=1080,
    display_width=1920,
    display_height=1080,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def main():
    try:
        # Pin Setup
        # Board pin-numbering scheme
        GPIO.setmode(GPIO.BOARD)
        # Set both pins to LOW
        GPIO.setup(motor_pin_a, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(motor_pin_b, GPIO.OUT, initial=GPIO.LOW)
        
        curr_value_pin_a = GPIO.LOW
        curr_value_pin_b = GPIO.LOW
                
        # Initialise variables
        camerafov = 60  # FOV (degrees)
        camerares = [1920, 1080]  # Resolution
        app = camerafov / camerares[0]  # Angle per pixel
        motorposition = 0  # Motor angle

        while True:
            ## Take picture
            filename = 'photo.jpg'
            # define a video capture object
            vid = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
            # Capture the video frame by frame
            ret, frame = vid.read()
            cv2.imwrite(filename, frame)  # Using cv2.imwrite() method to the image
            
            # Apriltag position system
            img = Image.open('photo.jpeg')
            imggrey = img.convert('L')
            data = asarray(imggrey)
            detector = apriltag.Detector()
            result = detector.detect(data)
            pixel = result[0][6][0]
            pixelangle = (pixel - 960) * app
            
            # Alignment system
            if abs(motorposition - pixelangle) > 0.9:  # if greater than highest precision
                if motorposition > pixelangle:  # Set GPIO pin anti-clockwise
                    curr_value_pin_b = GPIO.LOW
                    GPIO.output(motor_pin_b, 0)
                    print("anticlockwise")
                elif motorposition < pixelangle:  # Set GPIO pin clockwise
                    curr_value_pin_b = GPIO.HIGH
                    GPIO.output(motor_pin_b, curr_value_pin_b)
                    print("clockwise")
                for i in range(1, int(round(abs(motorposition - pixelangle) / 1.8) + 1)):
                    # Set GPIO pin signal high-low
                    curr_value_pin_a ^= GPIO.HIGH
                    GPIO.output(motor_pin_a, curr_value_pin_a)
                    curr_value_pin_a ^= GPIO.LOW
                    GPIO.output(motor_pin_a, curr_value_pin_a)
                    time.sleep(0.05)
                    curr_value_pin_a ^= GPIO.HIGH
                    GPIO.output(motor_pin_a, curr_value_pin_a)
                    curr_value_pin_a ^= GPIO.LOW
                    GPIO.output(motor_pin_a, curr_value_pin_a)
                    if curr_value_pin_b == GPIO.LOW:  # Anti-clockwise
                        motorposition -= 1.8
                    elif curr_value_pin_b == GPIO.HIGH:  # Clockwise
                        motorposition += 1.8
                    #time.sleep(1)
                    print("Motor position is: ", motorposition)
            vid.release()  # After the loop release the cap object        

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    main()