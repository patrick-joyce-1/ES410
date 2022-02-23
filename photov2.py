import cv2  # import the opencv library
filename = 'savedImage.jpg'

# define a video capture object
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Capture the video frame by frame
ret, frame = vid.read()

cv2.imwrite(filename, frame)  # Using cv2.imwrite() method to the image

vid.release()  # After the loop release the cap object

