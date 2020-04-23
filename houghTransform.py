from thin_edges import compare
import numpy as np
import math

def line_transform():
    """ This function uses the hough Transform algorithm to detect lines in the edge image/ or thinned edge image
    :param: None, in the phase of development, may change later
    :return: An image with the lines
    """

    thinned_edge_image = compare()

    # This is the threshold value above which the pixels values will be considered the part of line
    line_threshold = 150

    # This is the size of local window for which the line_threshold will be calculated for

    local_wd = 20

    theta_max = math.pi
    theta_min = 0.0

    # Minimum and Maximum distance for our image size
    d_min = 0.0
    d_max = math.hypot(thinned_edge_image.shape[0], thinned_edge_image.shape[1])

    # This is the dimension of our graph of perpendicular distance(d) versus the angle to the pp(theta threshold)
    d_threshold = 200
    theta_threshold = 300

    accumulator_array = np.zeros((d_threshold, theta_threshold))

    for x in range(thinned_edge_image.shape[0]):
        for y in range(thinned_edge_image.shape[1]):

            if thinned_edge_image[x, y] == 255:
                continue
            for i_theta in range(theta_threshold):
                theta = i_theta * theta_max / theta_threshold
                d = x * math.cos(theta) + y * math.sin(theta)

                i_d = int(d_threshold * d / d_max)
                accumulator_array[i_d, i_theta] = accumulator_array[i_d, i_theta] + 1


    return accumulator_array








if __name__ =="__main__":
    line_transform()