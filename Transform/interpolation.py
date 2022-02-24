import math
import numpy as np
class interpolation:

    def linear_interpolation(point, point1, point2, i1, i2):
        """Computes the linear interpolation value at some iD location x between two 1D points (Pt1 and Pt2).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes two 1D points Pt1 and Pt2, and their intensitites I(Pt1), I(Pt2).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for linear interpolation here

        i = ((i1*(point2 - point))/(point2 - point1)) + ((i2*(point - point1))/(point2 - point1))
        return i

    def bilinear_interpolation(point, image):

        """Computes the bi linear interpolation value at some 2D location x between four 2D points (Pt1, Pt2, Pt3, and Pt4).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes four 2D points Pt1, Pt2, Pt3, and Pt4, and their intensitites I(Pt1), I(Pt2), I(Pt3), and I(Pt4).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for bilinear interpolation here
        # Recall that bilinear interpolation performs linear interpolation three times
        # Please reuse or call linear interpolation method three times by passing the appropriate parameters to compute this task
        first_point = np.array((math.floor(point[0]), math.floor(point[1])))
        second_point = np.array((math.floor(point[0]), math.ceil(point[1])))
        third_point = np.array((math.ceil(point[0]), math.floor(point[1])))
        fourth_point = np.array((math.ceil(point[0]), math.ceil(point[1])))
        
        i1 = image[first_point[0]][first_point[1]]
        i2 = image[second_point[0]][second_point[1]]
        i3 = image[third_point[0]][third_point[1]]
        i4 = image[fourth_point[0]][fourth_point[1]]

        iR1 = interpolation.linear_interpolation(point[1],first_point[1], second_point[1], i1, i2)
        iR2 = interpolation.linear_interpolation(point[1],third_point[1], fourth_point[1], i3, i4)
        intensity = interpolation.linear_interpolation(point[0], first_point[0], third_point[0], iR1, iR2)
        return intensity

