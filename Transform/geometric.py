from .interpolation import interpolation

class Geometric:
    def __init__(self):
        pass

    def forward_rotate(self, image, theta):
        """Computes the forward rotated image by an angle theta
                image: input image
                theta: angle to rotate the image by (in radians)
                return the rotated image"""

        return image

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        """Computes the reverse rotated image by an angle theta
                rotated_image: the rotated image from previous step
                theta: angle to rotate the image by (in radians)
                Origin: origin of the original image with respect to the rotated image
                Original shape: shape of the orginal image
                return the original image"""

        return rotated_image

    def rotate(self, image, theta, interpolation_type):
        """Computes the forward rotated image by an angle theta using interpolation
                image: the input image
                theta: angle to rotate the image by (in radians)
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the original image"""

        return image


