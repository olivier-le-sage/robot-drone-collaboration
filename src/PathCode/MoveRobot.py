import math

# Take list of points with distances as input

List LineVectors
List Points
List Angles

#Constants

TURN_ANGLE = 10
#degrees

MOVE_DISTANCE = 10
#centimetres

class MoveRobot:


    def __init__(self, LineVectors, Angles):

        self.LineVectors = LineVectors
        self.Angles = Angles

    def Find_Angles (Angles)

        #Loop through list of points and find the angle between each connecting line
        for i in range(len(Angles)-1):

            AngleCalculator.angle_between(LineVectors[i], LineVectors[i+1])

    def Move_Along_Line (?)


    def Turn_Robot ()
