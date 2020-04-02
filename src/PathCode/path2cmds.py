# Takes path as a list of points in pixels as the input
# Calcuates how many commands need to be issued to satisfy the path

import math

# Constants
MIN_TURN_ANGLE = 10 # degrees
MIN_MOVE_DISTANCE = 10 # cm
ROBOT_DIM_W = 33.5 # cm
ROBOT_DIM_H = 37.0 # cm

def gen_commands_from_path(path, init_pose, robot_size):
    '''
        Generates a list of robot commands based on a list of points in pixels.
        inputs:
            - list of points in an image as (x,y)-coordinate pixel pairs
            - initial euclidian pose of the robot (x,y,theta) in pixels and rad
            - the robot's size in pixels, in (x,y) (used as reference)
        outputs:
            - list of commands to be taken by the robot, in the following format
                Ex: ['move_forward', 'move_forward', 'pivot_turn_right', 'halt']
    '''

    # Helper class for vector math
    class LineVector:
        # LineVector is a line between two points
        #   (origin, direction line)
        # NB: origin is optional.
        def __init__(self, x, y, origin=None):

            self.x = x
            self.y = y

            if origin is not None:
                self.origin = origin
                self.x1 = origin[0]
                self.x2 = origin[0] + self.x
                self.y1 = origin[1]
                self.y2 = origin[1] + self.y

                self.point1 = (self.x1, self.y1)
                self.point2 = (self.x2, self.y2)

        def __repr__(self):
            return "("+str(self.origin)+", ("+str(self.x)+", "+str(self.y)+"))"

        def get_mag(self):
            ''' returns magnitude of the vector '''
            return math.sqrt((self.y)^2 + (self.x)^2)

        def get_unit_vector(self):
            ''' returns a new vector object with normalized lengths '''
            normalized_vector = (self.x/self.get_mag, self.y/self.get_mag)
            return LineVector(self.origin, normalized_vector)

        def dot(self, other):
            ''' dot product between this and another vector '''
            return self.x*other.x + self.y*other.y

        def angle_between(self, other):
            ''' returns the angle between this vector object and another '''
            return math.arccos(self.dot(self, other)/(self.get_mag()*other.get_mag()))

    # private helper function
    def calc_num_moves(vector):
        ''' returns the number of move commands required to move along a vector '''
        num_moves = math.floor(vector.get_mag()/MIN_MOVE_DISTANCE)
        return num_moves
    # private helper function
    def calc_num_turns(angle, point1, point2):
        ''' returns the number of turns required to make a rotation '''
        # /!\ Need to check point positions to determine turn direction /!\
        # TBD!
        num_turns = math.floor(angle/MIN_TURN_ANGLE)
        return num_turns
    # private helper function
    def find_angles(point_list):
        '''
            Loops through a list of points and finds the angle
            between each conneting line.
        '''

        ### Currently not really implemented. TBD! ###

        for i in range(len(angles)-1):
            #obj = AngleCalculator()
            #cb = obj.angle_between(LineVectors[i][1], LineVectors[i+1][1])
            # b= Angles[i].AngleCalculator
            #Angles[i].angle_between((1, 0, 0), (0, 1, 0))

            #Angles[i] = AngleCalculator.angle_between(LineVectors[i][1], LineVectors[i+1][1])
        return
    # private helper function
    def pix2cm(vector_px, robot_size):
        '''
            Converts a LineVector object from pixels to cm
            using the robot size in the picture as reference.
        '''
        ### NOTE: WIP! Needs to be tested. ###
        # Based on the following code:
        #def get_distances(height, distances):
        #   list_of_distances = []
        #   pixel_length = 37/height
        #   for distance in distances:
        #       distanceInCM = float(distance) * pixel_length
        #       list_of_distances.append(distanceInCM)
        #   return list_of_distances

        # calculate cm-to-pixel ratio for further calculations
        # each axis scales by a different factor.
        robot_h_px = robot_size[1]
        robot_w_px = robot_size[0]
        pixel_length_h = ROBOT_DIM_H/robot_h_px
        pixel_length_w = ROBOT_DIM_W/robot_w_px

        # convert x and y distances
        y_cm = float(vector_px.y)*pixel_length_h
        x_cm = float(vector_px.x)*pixel_length_w

        # convert origin if it exists
        origin_cm = None
        if vector_px.origin is not None: # if the vector has a base point
            origin_x_cm = float(vector_px.origin[0])*pixel_length_w
            origin_y_cm = float(vector_px.origin[1])*pixel_length_h
            origin_cm = (origin_x_cm, origin_y_cm)

        # and finally:
        vector_cm = LineVector(x_cm, y_cm, origin=origin_cm)

        return vector_cm

    ### THIS FUCTION IS NOT YET IMPLEMENTED ###

    # Tentative outline:
    # 1. Take list of points and create vector objects
    # 2a. Convert vectors to cm
    # 2b. Loop through the vectors, calculating angles at each step
    # 3. Convert to # of commands
    # 4. Generate list with commands and return it

    #def Generate_Vectors():

        #Generate vectors between all points
       # for i in range(len(Points)-1):

            #LineVectors[i] = LineVector.Generate_Vector(Points[i], Points[i+1])

        #Generate vector between final point and origin point
        #LineVectors[-1] = LineVector.Generate_Vector(Points[-1], Points[0])
        #return
