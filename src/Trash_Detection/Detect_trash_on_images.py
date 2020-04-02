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
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# This function sets up and runs the object detection
def main():

	# Root directory of the project.
	# Change in case you want to put the notebook somewhere else.
	ROOT_DIR = os.getcwd()
	print(ROOT_DIR)

	# Import Mask RCNN
	sys.path.append(ROOT_DIR)  # To find local version of the library
	from mrcnn import utils
	from mrcnn import visualize
	from mrcnn.visualize import display_images
	import mrcnn.model as modellib
	from mrcnn.model import log
	from scipy.spatial import distance

	from trash import trash


	# Directory to save logs and trained model
	MODEL_DIR = os.path.join(ROOT_DIR, "logs")

	# Path to Trash trained weights
	TRASH_WEIGHTS_PATH = "weights/mask_rcnn_trash_0200_030519_large.h5" #the best

	# Configurations
	config = trash.TrashConfig()
	TRASH_DIR = 'trash'

	# Override the training configurations with a few
	# changes for inferencing.
	class InferenceConfig(config.__class__):
	    # Run detection on one image at a time
	    GPU_COUNT = 1
	    IMAGES_PER_GPU = 1

	# Device to load the neural network on.
	# Useful if you're training a model on the same
	# machine, in which case use CPU and leave the
	# GPU for training.
	DEVICE = "/cpu:0"  # /cpu:0 or /gpu:0

	# Inspect the model in training or inference modes
	# values: 'inference' or 'training'
	# TODO: code for 'training' test mode not ready yet
	TEST_MODE = "inference"

	# Load validation dataset
	dataset = trash.TrashDataset()
	dataset.load_trash(TRASH_DIR, "val")

	# Must call before using the dataset
	dataset.prepare()

	# Create model in inference mode
	with tf.device(DEVICE):
	    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,config=config)

	# Load the weights you trained
	weights_path = os.path.join(ROOT_DIR, TRASH_WEIGHTS_PATH)
	model.load_weights(weights_path, by_name=True)

	# Get images from the directory of all the test images
	#TODO: This should be changed to the directory where the desired images are stored

	jpg = glob.glob("images2/*.jpg")
	jpeg = glob.glob("images2/*.jpeg")
	jpg.extend(jpeg)


	# RUN COLLECTION
	# This runs the detection on all images in the directory.

	for image in jpg:

		# Save a temporary variable for image so that we can reread it after and then
		# import the image with imread.
	    image_temp = image
	    image = skimage.io.imread('{}'.format(image))


	    listOfPoints = [] 	#	list of points that will make up the path

	    def f(x,y):
	        return (x+y)*np.exp(-5.0*(x**2+y**2))

	    # Run object detection
	    results = model.detect([image], verbose=1)

	    # Save results as r
	    r = results[0]

	    mask = r['masks']
	    mask = mask.astype(int)

	    #--------------------------------------------------------------------------
		# STARTING POINT OF ROBOT
		#--------------------------------------------------------------------------
	    currentPoint = [(550,2000)]
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

	    # Display final results
	    print(listOfPoints)
	    image = image_temp
	    temp = skimage.io.imread('{}'.format(image))
	    plt.figure(figsize=(8,8))
	    plt.imshow(temp)
	    x,y = zip(*listOfPoints)
	    plt.scatter(y, x)
	    plt.plot(y,x,linewidth=3)
	    plt.show()

if __name__ == '__main__':
	main()
