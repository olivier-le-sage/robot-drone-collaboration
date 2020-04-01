import math
import numpy as np

# Take list of points, with distances, as the input

List_LineVectors = [((4,7),(5,7)), ((6,10),(5,9)), ((1,7),(2,8))]

List_Points = [(3,5), (4,6), (10,8)]

List_Angles= [30.0, 45.6, -135.0]

#Constants

TURN_ANGLE = 10
#degrees

MOVE_DISTANCE = 10
#centimetres


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    print("Unit Vector")
    print(vector / np.linalg.norm(vector))
    return vector / np.linalg.norm(vector)
		
def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    print("angle between vectors")
    print(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

#Test
#angle_between((1, 0, 0), (0, 1, 0))

def Calculate_Length (Point1,Point2):
    x1 = Point1[0]
    y1 = Point1[1]

    x2 = Point2[0]
    y2 = Point2[1]

    Length = math.sqrt((y2 - y1)**2 + (x2-x1)**2)
    print("Length between two points")
    print(Length)

    return Length

#Test
#Calculate_Length ((3,5),(2,1))

def Find_Angles():
    #Loop through list of points and find the angle between each connecting line
    for i in range(len(List_Angles)-1):
        angle = angle_between(List_LineVectors[i][1], List_LineVectors[i+1][1])
        print("The found Angle")
        print(angle)

#Test
#Find_Angles()

#def Move_Robot_Line (LineVector):
    
  
def Turn_Robot (Angle, Point1, Point2):
    
    #Need to check point positions to determine turn direction
    
    Num_Turns = math.floor(Angle / TURN_ANGLE)
    print("Num of turns")
    print(Num_Turns)

#Test   
#Turn_Robot (30, (3,6), (4,1))
