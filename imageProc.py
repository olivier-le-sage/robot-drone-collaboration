from imgproc import *

#open camera
pi_cam = Camera(320,240)

#grab an image from the camera
image= pi_cam.grabImage()

#set the view size to the size of the image
view = Viewer( image.width, image.hight," image processing")

#display image
view.displayImage(my_image)

waitTime(10000)



#https://maker.pro/raspberry-pi/tutorial/how-to-do-basic-image-processing-with-raspberry-pi?fbclid=IwAR1FeKjw3ms7eE-ohFLig4KSIa5HmPSw5Yf7oE0ljkW0gfAjnhnUMdvUkwk
