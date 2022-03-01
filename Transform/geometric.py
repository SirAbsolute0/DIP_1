from threading import local
from .interpolation import interpolation
import numpy as np
import math 
class Geometric:
    def __init__(self):
        pass

    def forward_rotate(self, image, theta):
        """Computes the forward rotated image by an angle theta
                image: input image
                theta: angle to rotate the image by (in radians)
                return the rotated image"""

        #Get local copy of the image and theta        
        local_image = image.copy()
        local_theta = theta

        #Rotation matrix
        rotation = np.array(( (np.cos(local_theta), -np.sin(local_theta)), 
                                (np.sin(local_theta), np.cos(local_theta))))

        #Four corners rotated
        top_left = np.array((0,0)) * rotation
        top_right = np.array((0, local_image.shape[1])) * rotation
        bottom_left = np.array((local_image.shape[0], 0)) * rotation
        bottom_right = np.array((local_image.shape[0], local_image.shape[1])) * rotation

        first_point = top_left.sum(axis = 1)
        second_point = top_right.sum(axis = 1)
        third_point = bottom_left.sum(axis = 1)
        fourth_point = bottom_right.sum(axis = 1)

        #Get the max, min for x, y
        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0

        four_points = [first_point, second_point, third_point, fourth_point]
        for point in four_points:
            if (point[0] < min_x):
                min_x = point[0]
            if (point[0] > max_x):
                max_x = point[0]
            if (point[1] < min_y):
                min_y = point[1]
            if (point[1] > max_y):
                max_y = point[1]
        
        #Creating new image baed on the rows and columns found
        rows = math.ceil(max_x - min_x)
        cols = math.ceil(max_y - min_y)

        new_image = np.zeros((rows, cols))

        #Get new image
        for y in range(0, local_image.shape[1]):
            for x in range(0, local_image.shape[0]):
                point = np.array((x, y)) * rotation
                coordinate = point.sum(axis = 1)

                new_image[int(coordinate[0] - min_x), int(coordinate[1] - min_y)] = local_image[x, y]

        return new_image

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        """Computes the reverse rotated image by an angle theta
                rotated_image: the rotated image from previous step
                theta: angle to rotate the image by (in radians)
                Origin: origin of the original image with respect to the rotated image
                Original shape: shape of the orginal image
                return the original image"""

        #Get local copy of the input
        local_image = rotated_image.copy()
        local_theta = theta * -1

        #Rotation matrix with -theta
        rotation = np.array(( (np.cos(local_theta), -np.sin(local_theta)), 
                                (np.sin(local_theta), np.cos(local_theta))))

        #Create new image with the original shape parameter
        new_image = np.zeros(original_shape)
        
        #Get new image
        for y in range(0, local_image.shape[1]):
            for x in range (0, local_image.shape[0]):
                temp = np.array((x, y)) - origin
                point = temp * rotation
                coordinate = point.sum(axis = 1)

                if( (0 <= coordinate[0] < original_shape[0]) and (0 <= coordinate[1] < original_shape[1]) ):
                    new_image[int(coordinate[0]), int(coordinate[1])] = local_image[x, y]

        return new_image

    def rotate(self, image, theta, interpolation_type):
        """Computes the forward rotated image by an angle theta using interpolation
                image: the input image
                theta: angle to rotate the image by (in radians)
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the original image"""

        #Get local copy of the input
        local_image = image.copy()
        local_theta = theta
        reverse_theta = local_theta * -1

        #Rotation Matricies
        rotation = np.array(( (np.cos(local_theta), -np.sin(local_theta)), 
                                (np.sin(local_theta), np.cos(local_theta))))
        
        reverse_rotation = np.array(( (np.cos(reverse_theta), -np.sin(reverse_theta)), 
                                        (np.sin(reverse_theta), np.cos(reverse_theta))))

        #Four corners rotated
        top_left = np.array((0,0)) * rotation
        top_right = np.array((0, local_image.shape[1])) * rotation
        bottom_left = np.array((local_image.shape[0], 0)) * rotation
        bottom_right = np.array((local_image.shape[0], local_image.shape[1])) * rotation

        first_point = top_left.sum(axis = 1)
        second_point = top_right.sum(axis = 1)
        third_point = bottom_left.sum(axis = 1)
        fourth_point = bottom_right.sum(axis = 1)

        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0

        four_points = [first_point, second_point, third_point, fourth_point]
        for point in four_points:
            if (point[0] < min_x):
                min_x = point[0]
            if (point[0] > max_x):
                max_x = point[0]
            if (point[1] < min_y):
                min_y = point[1]
            if (point[1] > max_y):
                max_y = point[1]
        
        rows = math.ceil(max_x - min_x)
        cols = math.ceil(max_y - min_y)

        #Set origin and created new image
        origin = np.array((-min_x, -min_y))
        
        new_image = np.zeros((rows, cols))

        for y in range(0, local_image.shape[1]):
            for x in range(0, local_image.shape[0]):
                point = np.array((x, y)) * rotation
                coordinate = point.sum(axis = 1)

                new_image[int(coordinate[0] - min_x), int(coordinate[1] - min_y)] = local_image[x, y]

        #Interpolation based on input parameter
        for y in range(0, new_image.shape[1]):
            for x in range(0, new_image.shape[0]):
                coordinate = np.array((x, y))
                location_origin = np.array(coordinate - origin)

                inverse_location = location_origin * reverse_rotation
                inverse_coordinate = inverse_location.sum(axis = 1)

                if (interpolation_type == "nearest_neighbor"):
                    neighbor = np.array((round(inverse_coordinate[0], 0), round(inverse_coordinate[1], 0)))

                    if ( (0 <= neighbor[0] < local_image.shape[0]) and (0 <= neighbor[1] < local_image.shape[1]) ):
                        new_image[x, y] = local_image[int(neighbor[0]), int(neighbor[1])]

                elif (interpolation_type == "bilinear"):
                    if ( 0 < inverse_coordinate[0] < local_image.shape[0] - 1 and 0 < inverse_coordinate[1] < local_image.shape[1] - 1):
                        intensity = interpolation.bilinear_interpolation(inverse_coordinate, local_image)

                        new_image[x, y] = intensity
                    else:
                        new_image[x, y] = 0
                    
        return new_image


