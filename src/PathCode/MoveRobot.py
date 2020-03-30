import math

# Take list of points, with distances, as the input

List LineVectors

List Points

List Angles

#Constants

TURN_ANGLE = 10
#degrees

MOVE_DISTANCE = 10
#centimetres

class MoveRobot:


    def __init__(self, Points, LineVectors, Angles):

        self.LineVectors = LineVectors
        self.Angles = Angles
        self.Points = Points


    def Generate_Vectors()

        #Generate vectors between all points
        for i in range(len(Points)-1):

            LineVectors[i] = LineVector.Generate_Vector(Points[i], Points[i+1])

        #Generate vector between final point and origin point
        LineVectors[-1] = LineVector.Generate_Vector(Points[-1], Points[0])
        return

    def Find_Angles()

        #Loop through list of points and find the angle between each connecting line
        for i in range(len(Angles)-1):

            Angles[i] = AngleCalculator.angle_between(LineVectors[i][1], LineVectors[i+1][1])

        return

    #Moves robot along a single line vector
    def Move_Robot_Line (LineVector)

        Num_Moves = math.floor(LineVector.Calculate_Length / MOVE_DISTANCE)

        for i in range(Num_Moves):

            #Make call to servo
        return

    def Turn_Robot (Angle, Point1, Point2)

        #Need to check point positions to determine turn direction

        Num_Turns = math.floor(Angle / TURN_ANGLE)

        for i in range(Num_Turns):
            #Make call to servo
