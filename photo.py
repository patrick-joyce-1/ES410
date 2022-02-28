import cv2  # import the opencv library
# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
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

# Define acquired photo file-name
filename = 'photo.jpg'

# Define a video capture object for the photo
vid = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER) # Set flip_method=2 to rotate the image 180 degrees

# Capture the video-output from the camera
ret, frame = vid.read()

# Write the frame into the file-name previously defined
cv2.imwrite(filename, frame)  

# Release the video capture object
vid.release()  
