#-------------------
# Imports
#-------------------
import os
import sys
import random
import math
import re
import time
import glob
import skimage
import skimage.segmentation as seg
import skimage.color as color
import imutils
import cv2
from imutils import perspective
from imutils import contours
from skimage.feature import canny
from skimage.morphology import remove_small_objects
from skimage.measure import label
from skimage.color import rgb2gray
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import distance
from scipy import ndimage as ndi
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log
from trash import trash
from Path import get_distances
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Root directory of the project.
# Change in case you want to put the code somewhere else.

ROOT_DIR = os.getcwd()

# Path to Trash trained weights
TRASH_WEIGHTS_PATH = "weights/mask_rcnn_trash_0200_030519_large.h5" #the best

# Device to load the neural network on.
# Useful if you're training a model on the same
# machine, in which case use CPU and leave the
# GPU for training.
DEVICE = "/cpu:0"  # /cpu:0 or /gpu:0

# Inspect the model in training or inference modes
# values: 'inference' or 'training'
# TODO: code for 'training' test mode not ready yet
TEST_MODE = "inference"

class TrashDetector:
    def __init__(self):

        print(ROOT_DIR)
        # Import Mask RCNN
        sys.path.append(ROOT_DIR)  # To find local version of the library

        # Directory to save logs and trained model
        MODEL_DIR = os.path.join(ROOT_DIR, "logs")

        # Configurations
        config = trash.TrashConfig()
        TRASH_DIR = 'trash'

        # Get images from the directory of all the test images
        # TODO: This should be changed to the directory where the desired images are stored

        self.jpg = glob.glob("images2/*.jpg")
        self.jpeg = glob.glob("images2/*.jpeg")
        self.jpg.extend(self.jpeg)

        # Override the training configurations with a few
        # changes for inferencing.
        class InferenceConfig(config.__class__):
            # Run detection on one image at a time
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1

        # Load validation dataset
        dataset = trash.TrashDataset()
        dataset.load_trash(TRASH_DIR, "val")

        # Must call before using the dataset
        dataset.prepare()

        # Create model in inference mode
        with tf.device(DEVICE):
            self.model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,config=config)

        # Load the weights you trained
        weights_path = os.path.join(ROOT_DIR, TRASH_WEIGHTS_PATH)
        self.model.load_weights(weights_path, by_name=True)

    def get_init_pose(self, image):
        '''
            Determines the initial position and size of the robot from the same
            picture as the path calculation (using openCV edge detection).

            Assumes the robot is present in the picture.

            Returns a euclidean pose (x, y, angle) in pixels.
        '''

        # Private helper functions
        def midpoint(a, b):
            # returns (a_x+b_x)/2 and (a_y+b_y)/2
	        return ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5)
        def calculate_pose(x, y):
            # Calculate euclidean pose from rectangle size (in pixels)
            return (x, y, angle)
        def resize_with_ratio(image,width=None,height=None,inter=cv2.INTER_AREA):
            dim = None
            (h, w) = image.shape[:2]

            if width is None and height is None:
                return image
            if width is None:
                r = height / float(h)
                dim = (int(w * r), height)
            else:
                r = width / float(w)
                dim = (width, int(h * r))

            return cv2.resize(image, dim, interpolation=inter)


        def find_post_it(list_of_contours, robot_contour):
            '''
                    Finds the post-it note on the robot by locating all contours that have an
                    area within 4.5%-5.5% of the robots area (the post it should be right around 5%).

                    Assumes the robot is present in the picture.

                    Returns the post-it contour.
            '''

            # TODO: add a second verification that checks to make sure the contours that pass the size test are located
            #  within the robot's area
            post_it_list = []
            i = 0

            for contour in list_of_contours:
                robot_area = cv2.contourArea(robot_contour)
                min_area = robot_area * 0.045
                max_area = robot_area * 0.055
                area = cv2.contourArea(contour)
                if min_area < area < max_area:
                    post_it_list.append(contour)
                i += 1


            post_it = max(post_it_list, key = cv2.contourArea)
            return post_it #check to make sure this is returning the right thing

        x,y,angle,width,height = 0,0,0,0,0

        # load the image, convert it to grayscale, and blur it slightly
        image = cv2.imread(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # perform edge detection, then perform a dilation + erosion to
        # close gaps in between object edges
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        # find contours in the edge map
        cnts, contour_hierarchy = cv2.findContours(edged.copy(), cv2.RETR_CCOMP,
            cv2.CHAIN_APPROX_SIMPLE)
        #cnts = imutils.grab_contours(cnts)
        # sort the contours from left-to-right and initialize the
        # 'pixels per metric' calibration variable
        (cntrs, _) = contours.sort_contours(cnts)


        ## Next we take the largest contour
        # For now we'll just take the biggest cluster to be the robot.
        # In the future better ways of identifying the robot in the picture
        # will be required.
        cntrs = list(cntrs)
        c = max(cntrs, key = cv2.contourArea)



        # compute the rotated bounding box of the contour
        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)
        print(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
        # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # unpack the ordered bounding box
        (tl, tr, br, bl) = box

        # find the post-it box and then repeat same steps
        # TODO: add some error handling to both this and the part that calls it. For now it just exits if it can't find
        #  the post-it.
        try:
            c2 = find_post_it(cnts, c)
        except ValueError:
            print("Unable to find post-it")
            exit()

        box2 = cv2.minAreaRect(c2)
        box2 = cv2.cv.BoxPoints(box2) if imutils.is_cv2() else cv2.boxPoints(box2)
        box2 = np.array(box2, dtype="int")
        print(box2)
        cv2.drawContours(orig, [box2.astype("int")], -1, (0, 255, 0), 2)
        # loop over the original points and draw them
        for (x, y) in box2:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # unpack the post-it box
        (tl2, tr2, br2, bl2) = box2

        # compute the midpoint between the top-left and top-right coordinates,
        # followed by the midpoint between bottom-left and bottom-right
        # coordinates
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tltrX2, tltrY2) = midpoint(tl2, tr2)
        (blbrX2, blbrY2) = midpoint(bl2, br2)

        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        (tlblX2, tlblY2) = midpoint(tl2, bl2)
        (trbrX2, trbrY2) = midpoint(tr2, br2)

        # draw the midpoints on the image
        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tltrX2), int(tltrY2)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX2), int(blbrY2)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX2), int(tlblY2)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX2), int(trbrY2)), 5, (255, 0, 0), -1)
        # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
        (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
        (255, 0, 255), 2)

        cv2.line(orig, (int(tltrX2), int(tltrY2)), (int(blbrX2), int(blbrY2)),
                 (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX2), int(tlblY2)), (int(trbrX2), int(trbrY2)),
                 (255, 0, 255), 2)
        # compute the Euclidean distance between the midpoints
        height = distance.euclidean((tltrX, tltrY), (blbrX, blbrY))
        width  = distance.euclidean((tlblX, tlblY), (trbrX, trbrY))
        height2 = distance.euclidean((tltrX2, tltrY2), (blbrX2, blbrY2))
        width2 = distance.euclidean((tlblX2, tlblY2), (trbrX2, trbrY2))
        # compute the center by computing the midpoints' midpoints
        # use both ways then compute the average to smooth out error
        robot_center_1 = midpoint( (tlblX, tlblY), (trbrX, trbrY) )
        robot_center_2 = midpoint( (tltrX, tltrY), (blbrX, blbrY) )
        rx = (robot_center_1[0] + robot_center_2[0])/2
        ry = (robot_center_1[1] + robot_center_2[1])/2

        postit_center_1 = midpoint((tlblX2, tlblY2), (trbrX2, trbrY2))
        postit_center_2 = midpoint((tltrX2, tltrY2), (blbrX2, blbrY2))
        px = (postit_center_1[0] + postit_center_2[0]) / 2
        py = (postit_center_1[1] + postit_center_2[1]) / 2
        # draw the center on the image
        cv2.circle(orig, (int(rx), int(ry)), 10, (0, 255, 255), -1)
        cv2.circle(orig, (int(px), int(py)), 10, (0, 255, 255), -1)

        # TODO: Figure out which lines are front/back vs sides of robot. Use the average of their lengths,
        #  shorter ones are front/back. Find the angle of the sides with respect to y axis (?). Create a vector
        #  starting at the robots midpoint and ending at the post-its midpoint. This vector points toward the back of
        #  the robot, so the front should be the opposite direction.

        # compute the angle/orientation of the box in radians
        # use both sides separately then take the average (to smooth out error)
        angle_rad_1 = math.atan( (tl[0]-bl[0]) / (tl[1]-bl[1]) )
        angle_rad_2 = math.atan( (tr[0]-br[0]) / (tr[1]-br[1]) )
        angle_rad = (angle_rad_1 + angle_rad_2)/2
        print(angle_rad)
        angle = angle_rad * (180/math.pi)
        print(rx, ry)
        print(angle)

        # draw the object sizes on the image
        cv2.putText(orig, "{:.1f}px".format(height),
            (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.1f}px".format(width),
            (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)
        # show the output image
        resized = resize_with_ratio(orig, height=720)
        cv2.imshow("Image", resized)
        cv2.waitKey(0)

        #edges = canny(rgb2gray(image), sigma=1)
        #fill_clusters = ndi.binary_fill_holes(edges)
        #test = ndi.label(remove_small_objects(fill_clusters, 21))[0]
        #fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14,14))
        #ax.imshow(test)
        #ax.axis('off')

        # Run algorithm to get segmentation masks
        # higher scale parameter --> bigger clusters
        #image_felz = seg.felzenszwalb(image,scale=5000.0,sigma=0.95,min_size=100)
        #print("Felzenszwalb'ed with ", np.unique(image_felz).size, " regions")
        # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14,14))
        # ax.imshow(image_felz)
        # ax.axis('off')

        # apply to original image and display the result
        #image_felz_colored = color.label2rgb(image_felz, image, kind='avg')
        #print("Done applying felzenszwalb to coloured image. Displaying result.")
        #fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14,14))
        #ax.imshow(image_felz_colored)
        #ax.axis('off')

        return rx, ry, angle, width, height

    def run(self):
        # RUN COLLECTION
		# This runs the detection on all images in the directory.

        for image in self.jpg:

            # Save a temporary variable for image so that we can reread it after and then
            # import the image with imread.
            image_temp = image
            image = skimage.io.imread('{}'.format(image))


            listOfPoints = [] 	#	list of points that will make up the path
            listOfDistances = []

            def f(x,y):
                    return (x+y)*np.exp(-5.0*(x**2+y**2))

            # Run object detection
            results = self.model.detect([image], verbose=1)

            # Save results as r
            r = results[0]

            mask = r['masks']
            mask = mask.astype(int)

            #--------------------------------------------------------------------------
            # STARTING POINT OF ROBOT
            #--------------------------------------------------------------------------
            rbt_x,rbt_y,rbt_angle,rbt_width,rbt_height = self.get_init_pose(image_temp)
            print("Robot found at: (",rbt_x,"px,",rbt_y,"px,",rbt_angle,"deg)")
            currentPoint = [(rbt_y, rbt_x)]
            listOfPoints.append(currentPoint[0])

            # Loop through all the detected objects. For each object, store the point determined to
            # be closest to currentPoint
            while(mask.shape[2] != 0):
                listOfShortest = []

                for i in range(mask.shape[2]):
                    diffMaskNewArray = np.transpose(np.nonzero(mask[:,:,i] == 1)) # Changes the array so that we have an array of points were the mask is.
                    shortestPoint = diffMaskNewArray[distance.cdist(currentPoint, diffMaskNewArray, 'euclidean').argmin()] # Finds the closest point in the mask to a given point and stores that point.
                    distanceToPoint = distance.cdist(currentPoint, [shortestPoint], 'euclidean') # Stores the distance of that point. Currently stores it in a 2D array. Need to find a fix for this later
                    distanceToPoint = distanceToPoint[0][0] #The value is currently written in a 2D array, this takes the value from that 2D array and stores it.
                    listOfShortest.append([shortestPoint,distanceToPoint,i]) # Add the point to a list of shortest. This can be changed later to just replace the stored value if the new one is closer.
                    image = image_temp
                    temp = skimage.io.imread('{}'.format(image))


                # Print the list of points for each object, calulcate which object is closest to
                # currentPoint, add it to the listOfPoints and then set it as the new currentPoint

                currentPoint
                print(listOfShortest)
                absoluteShortest = min(listOfShortest, key=lambda x: x[1])
                print("Shortest point is " + str(absoluteShortest[0]) + " and the distance to it is: " + str(absoluteShortest[1])) ##Print the distance to the shortest point.
                print(absoluteShortest[2])
                mask = np.delete(mask,absoluteShortest[2], 2)
                currentPoint = [(absoluteShortest[0][0],absoluteShortest[0][1])]
                listOfPoints.append(currentPoint[0])
                listOfDistances.append(absoluteShortest[1])

            # Display final results
            print(listOfPoints)
            distanceCM = get_distances(rbt_height, listOfDistances)
            print("Distance between points is" + str(distanceCM))
            image = image_temp
            temp = skimage.io.imread('{}'.format(image))
            plt.figure(figsize=(8,8))
            plt.imshow(temp)
            x,y = zip(*listOfPoints)
            plt.scatter(y, x)
            plt.plot(y,x,linewidth=3)
            plt.show()

        #return listOfPoints, listOfDistances

if __name__ == '__main__':
    trash_detector = TrashDetector()
    trash_detector.run()
