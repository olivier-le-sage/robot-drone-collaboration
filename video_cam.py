import picamera
from time import sleep

camera = picamera.PiCamera()

#  start the camera preview and stop it, after 60 seconds you will be able to
# see the preview
camera.start_preview()
# To record a vedio
camera.start_recording("/home/pi/Desktop/video.h264")
time.sleep(60)
# Stop the recording 
camera.stop_recording()
#stop preview
camera.stop_preview()
camera.close()
print("Stopped")


