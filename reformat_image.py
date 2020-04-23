from test_image import test_driver_image, convert_2d_3d
from parse_bitmap import read_image
import numpy as np
import copy



def perform_formatting():
    """
    :param i2dr: Image represented in two dimensional numpy matrix #TODO REdundant remove later
    :return: reformatted image, after smoothing, contrast management and other formatting operations
    """
    # Get the shape of the image width * height first
    image_3d_array = read_image()

    # Re2, edge_transform_array.shape[0]):
    #     for j in range(edge_transform_array.shape[1]):
    #
    #         edge_transform_duced size of array to perform the edge detection
    edge_transform_array_x = np.zeros(shape=(image_3d_array.shape[0], image_3d_array.shape[1]))
    edge_transform_array_y = np.zeros(shape=(image_3d_array.shape[0], image_3d_array.shape[1]))

    # lapx = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])       # laplacian operator to extract the outward edges
    # lapy = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])    # laplacian operator to extract the inward edges

    # The following is the sobel operator, although the name is lapx and lapy
    lapx = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    lapy = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    # First step is to do  brightness and contrast management

    img_height = image_3d_array.shape[0]
    img_width = image_3d_array.shape[1]

    # Increase the brightness, add constant value to every pixel
    # Increase the contrast, 127 + c*(pixel_value -127), for c > 1.0

    for i in range(img_height):    # For every pixel:
        for j in range(img_width):
            image_3d_array[i, j] = [127 + (((rbg + 20) - 127) * 1.0) for rbg in image_3d_array[i, j]]
    # #

    test_driver_image(image_3d_array)

    # Second step is to reduce the noise in the image, by means of smoothing (replace each pixel with average of itself
    # and the surrounding pixels). Since, the image produced by devices these days, does not have a lot of noise
    # we'll avoid this step for now.

    # Other methods for smoothing can be calculating mean, median, or weighted center (Local Averaging Techniques)

    # The next step is to sharpen the image, using spatial differentiation.

    # We follow to bring out more details in the image using the "Histogram Equalization" technique. This will equalize,
    # non equal distribution of the light intensity across the image

    histogram_buffer = np.zeros((256, 3), dtype=np.int32)  # Initialize histogram buffer to zero

    # Compute the histogram
    for i in range(img_height):
        for j in range(img_width):
            for pix in range(histogram_buffer.shape[1]):
                histogram_buffer[image_3d_array[i, j, pix], pix] += 1

    # print(histogram_buffer)

    # Compute the cumulative histogram
    for i in range(1, histogram_buffer.shape[0]):
        for j in range(0, histogram_buffer.shape[1]):
            histogram_buffer[i, j] = histogram_buffer[i - 1, j] + histogram_buffer[i, j]

    # Normalize the cumulative histogram
    for i in range(histogram_buffer.shape[0]):
        for j in range(histogram_buffer.shape[1]):
            histogram_buffer[i, j] = histogram_buffer[i, j] * 255 / (img_height * img_width)

    # print(histogram_buffer)
    # Update the image to have equalized histogram values


    for i in range(img_height):    # For every pixel:
        for j in range(img_width):
            image_3d_array[i, j] = [histogram_buffer[image_3d_array[i, j, pix], pix] for pix in range(histogram_buffer.shape[1])]


    # test_driver_image(image_3d_array)


    ###########################################   HISTOGRAM WORKS PROPOERLY ##########################################

    # Edge Detection
    # Since , the image that we would want to transform is greyscale image, and all the value of RGB are the same,
    # reducing the array dimension from width* height* 3 to just width * height

    image_2d_array = convert_2d_3d(image_3d_array)

    print(image_2d_array.shape)
    edge_transform_array_x = np.zeros((image_2d_array.shape[0] + 2, image_2d_array.shape[1] + 2))
    edge_transform_array_y = np.zeros((image_2d_array.shape[0] + 2, image_2d_array.shape[1] + 2))

    # padding zeros
    # edge_transform_array_x = np.pad(edge_transform_array_x, ((2, 2), (2, 2)), 'constant')
    # edge_transform_array_y = np.pad(edge_transform_array_y, ((2, 2), (2, 2)), 'constant')


    # Now we slide over the laplacian operator of size 3*3 into the image of window width*height

    for i in range(2, edge_transform_array_x.shape[0] - 2):
        for j in range(2, edge_transform_array_x.shape[1] -2):

            edge_transform_array_x[i, j] = sum(lapx[m, n] * image_2d_array[i - m,  j - n] for m in range(3) for n in range(3))

    # test_driver_image(edge_transform_array_x)

    for i in range(2, edge_transform_array_y.shape[0] - 2):
        for j in range(2, edge_transform_array_y.shape[1]- 2):

            edge_transform_array_y[i, j] = sum(lapy[m, n] * image_2d_array[i - m,  j - n]
                                               for m in range(3) for n in range(3))

    # test_driver_image(edge_transform_array_y)


    dup_eta = np.abs(np.subtract(edge_transform_array_x, edge_transform_array_y))

    dup_eta = dup_eta[2:-2, 2:-2]           # Remove the padded zeros

    for i in range(dup_eta.shape[0]):
        for j in range(dup_eta.shape[1]):
            if dup_eta[i, j] > 100:
                dup_eta[i, j] = 0

            else:
                dup_eta[i, j] = 255

    test_driver_image(dup_eta)
    ####################################### Reducing the noise from the edge image ##################################
    # If number of neighbouring element is greater than, certain threshold then keep edge element
    # else remove it. A better approximation of threshold can be 2 or 3

    threshold_noise = 8  # Total number of neighbouring elements for a pixel to not being identified as noise

    for i in range(2, dup_eta.shape[0] - 2):
        for j in range(2, dup_eta.shape[1] - 2):
            # check if the pixel element in black i.e., it constitutes an edge
            if dup_eta[i, j] != 255:
                # Check neighbouring pixel value in 5*5 window, if set to 0 i.e., black, increase the count
                cur_threshold = sum(1 for m in range(-2, 3) for n in range(-2, 3) if dup_eta[i + m, j + n] == 0)

                if cur_threshold - 1 < threshold_noise:

                    dup_eta[i, j] = 255

    test_driver_image(dup_eta)

    return dup_eta



if __name__=="__main__":
    perform_formatting()
