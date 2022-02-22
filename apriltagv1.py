import apriltag
import cv2
path = r'/Home/lib-dt-apriltags/dt_apriltags/photo.png'
img = cv2.imread(path,0)
detector = apriltag.Detector()
result = detector.detect(img)

print(result)
