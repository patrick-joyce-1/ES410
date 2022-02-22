import apriltag
import cv2
img = cv2.imread('photo.png')
detector = apriltag.Detector()
result = detector.detect(img)

print(result)
