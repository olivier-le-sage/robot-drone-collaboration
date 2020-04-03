#-------------------
# Imports
#-------------------

import tkinter as tk
from PIL import ImageTk, Image
import subprocess
from src.Trash_Detection import TrashDetector as Trash
from PIL import Image
from PIL import ImageTk
import pathlib
import os



#--------------------------------------------------------------------------
# MAC address of Pi
#
# Change this to the MAC (physical) address of the raspberry Pi being used
#--------------------------------------------------------------------------
piPhysicalAddr = 'dc-a6-32-2e-b9-a8'


# This section inputs command1 into the terminal in order to retrieve the
# IP address of the Hotspot created. It may need to be changed if the
# hotspot is not created through Windows settings.
command1 = 'netsh interface ip show addresses "Local Area Connection* 12"'
process1 = subprocess.Popen(command1, stdout=subprocess.PIPE, stderr=None, shell=True)
output1 = process1.communicate()
netsh = output1[0].decode("utf-8") 
netstring = netsh.split()
ipaddr = netstring[12]

# Takes the retrieved IP address and adds it to the "arp" command which
# retrieves all IP addresses connected to ipaddr
maincom = 'arp -a -N ' + ipaddr



# Inputs the arp command into the terminal to get the list of connected 
# devices and IP addresses and then searches through them to find the
# one associated with piPhysicalAddr (MAC address of pi)
command2 = 'arp -a -N ' + ipaddr
process2 = subprocess.Popen(command2, stdout=subprocess.PIPE, stderr=None, shell=True)
output2 = process2.communicate()
arpdecoded = output2[0].decode("utf-8")
arpstring = arpdecoded.split()
for i in range(len(arpstring)):
    if arpstring[i] == piPhysicalAddr:
        rtmpip = arpstring[i-1]


images = "src/Trash_Detection/images2" # relative to this file
td = Trash.TrashDetector(images_dir=images)







#--------------------------------------------------------------------------
# GUI section
#--------------------------------------------------------------------------


win = tk.Tk()	#initialize a window for the GUI
runDisplayed = False
ROOT_DIR = str(pathlib.Path(__file__).parent.absolute())
print(ROOT_DIR)

# command3 is the terminal command that connects to the RTMP stream and
# then captures and image from it. See onClick function for more.
command3 = r'ffmpeg -y -i rtmp://' +rtmpip+ \
		   r'/live/test -vframes 1 "'+ROOT_DIR+'/images2/img%03d.jpg"'
print(command3)


# Function that is called when the "Capture" button is clicked. The function
# passes command3 to the terminal which captures a picture from the stream.
# The function then opens this picture, resizes it, and adds it to the GUI
# so that the user can verify it before running the detection. It also adds
# the button to start detection to the GUI at this time.
def onClick(label):
    process = subprocess.Popen(command3, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    img = Image.open("src/Trash_Detection/images2/img001.jpg")
    img = img.resize((500,281), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)
    #CLabel = tk.Label(win, image=photoImg)
    label.configure(image=photoImg)
    label.img = photoImg
    label.pack()
    global runDisplayed
    if not runDisplayed:
        runDetectionText = tk.Label(win, text="Click to perform detection on image")
        runDetectionText.pack()
        detectionButton = tk.Button(win, text="Run", fg="green", command=onClick2)
        detectionButton.pack()
        runDisplayed = True

def onClick1(label):
    img = Image.open(ROOT_DIR + "/src/Trash_Detection/images2/demo_pic.jpg")
    img = img.resize((281,500), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)
    #CLabel = tk.Label(win, image=photoImg)
    label.configure(image=photoImg)
    label.img = photoImg
    label.pack()
    global runDisplayed
    if not runDisplayed:
        runDetectionText = tk.Label(win, text="Click to perform detection on image")
        runDetectionText.pack()
        detectionButton = tk.Button(win, text="Run", fg="green", command=onClick2)
        detectionButton.pack()
        runDisplayed = True

# Function that is run when the "Run" button is clicked. This starts the 
# trash detection on the picture stored in the directory after the "Capture"
# button was clicked.
def onClick2():
	point_list, pose, size = td.run_single(images+"/demo_pic.jpg",quiet_mode=False)
    

# The following code initializes the GUI window

win.title("Robot-Drone-App")	#Set title of the window
win.geometry("700x700")		#Set window dimensions to 500x500
win.resizable(False, False)		#Don't make window resizable in x or y

tk.Label(win, text="Ensure mobile hotspot is turned on and camera is streaming before starting!",\
		 background='red').pack() 	#Warning message to user

CLabel = tk.Label(win)

tk.Label(win, text="Click to capture image").pack()		#Button label	
tk.Button(win, text="Capture", fg="red", command= lambda: onClick1(CLabel)).pack()	#"Capture" button



win.mainloop()

