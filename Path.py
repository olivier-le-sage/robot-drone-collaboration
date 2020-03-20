import math
#List of pixcels where there is trash ( Randomly choosen Number )
List_of_pixcels = [(10,100), (30,103), (50,200),(70,205), (80,300), (88,400),(100,450), (110,500)]

Pixels_for_robot= [(0,1322)]


# To convert Pixcels to cm 

#There are 2.54 cm per inch. assum pixels_per_Inch = 96
pixel_per_inch = 96
List_of_Pixcles_in_CM = [(x[0]* 2.54/pixel_per_inch, x[1]* 2.54/pixel_per_inch) for x in List_of_pixcels]

print("The points in pixcels coverted to CM")
print(List_of_Pixcles_in_CM)
print()

Pixcels_TO_CM_For_robot= [(y[0]* 2.54/pixel_per_inch, y[1] * 2.54/pixel_per_inch) for y in Pixels_for_robot]

print("For the robot points in pixcels coverted to CM")
print(Pixcels_TO_CM_For_robot)
print()

#calculate the diatance from the robot to each tash point              
def calculateDistance(p1,p2):
        dist= math.sqrt((p1[0])**2 + (p2[0])**2)
        print(dist)
        return dist
          
for i in range (8):
        print("Distance between the robot and trash " + str(i))
        calculateDistance(Pixcels_TO_CM_For_robot[0], List_of_Pixcles_in_CM[i])


#Compare the distance between the robot and each trash point,
#see the smallest then move toward this point 
