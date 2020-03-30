import math

#A line Vector object, which consits of a line between two points

#Assume points are given as tuples with x, y

class LineVector

    #LineVector is represented as a tuple of size 2
    #Origin point in first element, direction line in second element


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
            return Line_Vector


    def Calculate_Length ()

        Length = math.srqt ((y2 - y1)^2 (x2-x1)^2)

        return Length
