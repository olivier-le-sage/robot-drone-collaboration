import math
#import numpy as np
import AngleCalculator

# Take list of points, with distances, as the input

LineVectors = [((4,7),(5,7)), ((6,10),(5,9)), ((1,7),(2,8))]

Points = [(3,5), (4,6), (10,8)]

Angles= [30.0, 45.6, -135.0]

#Constants

TURN_ANGLE = 10
#degrees

MOVE_DISTANCE = 10
#centimetres

class MoveRobot:
    
    def __init__(self, Point1, Point2): 
            self.Point1 = Point1
            self.Point2 = Point2

            x1 = Point1[0]
            y1 = Point1[1]

            x2 = Point2[0]
            y2 = Point2[1]

            #Vector = (Original Point) + t * (P2 - P1)

            #Save the vector in tuple format: (Origin, (Line Vector))
            Line_Vector = (Point1, (x2 - x1, y2-y1))
            #return Line_Vector

    def Calculate_Length (Point1,Point2):
        x1 = Point1[0]
        y1 = Point1[1]

        x2 = Point2[0]
        y2 = Point2[1]

        Length = math.sqrt((y2 - y1)^2 + (x2-x1)^2)
        print(Length)

        return Length


#Calculate_Length((3,5), (2,10))
#2.449489742783178

 

    def __init__(self, Points, LineVectors, Angles):

        self.LineVectors = LineVectors
        self.Angles = Angles
        self.Points = Points


    #def Generate_Vectors():

        #Generate vectors between all points
       # for i in range(len(Points)-1):

            #LineVectors[i] = LineVector.Generate_Vector(Points[i], Points[i+1])

        #Generate vector between final point and origin point
        #LineVectors[-1] = LineVector.Generate_Vector(Points[-1], Points[0])
        #return
        
   

    def Find_Angles():

        #Loop through list of points and find the angle between each connecting line
        for i in range(len(Angles)-1):
            
            obj = AngleCalculator()
            cb = obj.angle_between(LineVectors[i][1], LineVectors[i+1][1])
            # b= Angles[i].AngleCalculator
            #Angles[i].angle_between((1, 0, 0), (0, 1, 0))

            #Angles[i] = AngleCalculator.angle_between(LineVectors[i][1], LineVectors[i+1][1])

        return

    #Moves robot along a single line vector
    def Move_Robot_Line (LineVector):

        Num_Moves = math.floor(LineVector.Calculate_Length() / MOVE_DISTANCE)
        print("Num of Moves")
        print(Num_Moves)

        #return Num_Moves

    def Turn_Robot (Angle, Point1, Point2):

        #Need to check point positions to determine turn direction

        Num_Turns = math.floor(Angle / TURN_ANGLE)
        print("Num of turns")
        print(Num_Turns)

   
    Find_Angles() 
    #line = ((4,7),(5,7))
    #Move_Robot_Line (LineVectors[0])
    
