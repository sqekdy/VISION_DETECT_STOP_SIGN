import reformat_image
import numpy as np
from test_image import test_driver_image
from reformat_image import perform_formatting


def compare():

    edge_image = perform_formatting()

    # We use two image -> 1 . original image pixels
    # 2nd -> final image pixels
    # we loop until original image pixels and final image pixels are not identical
    # Contour points ->  Edge pixel that is bounded in at least one side by non edge element, that is removed

    # create a final image of size corresponding to edge image, initialized with all white pixel value i.e, 255
    final_image = np.full((edge_image.shape[0], edge_image.shape[1]), 255)

    # We maintain 2 set of points Ai and Bi to determine the final points
    # None is the placeholder for the values x and y, which are conditional
    # np.nan is the placeholder for the value, for which the values at corresponding location is not defined
    # Ai are always final and Bi are final depending upon the sub-cycles.

    Ai = []
    Bi = []

    A1 = np.array([[None, None, None], [255, 0, 255], [None, None, None]])
    A2 = np.array([[255, None, None], [None, 0, None], [None, None, 255]])
    A3 = np.array([[None, 255, None], [None, 0, None], [None, 255, None]])
    A4 = np.array([[None, None, 255], [None, 0, None], [255, None, None]])

    Ai.extend([A1, A2, A3, A4])

    B1 = np.array([[None, None, None], [np.NaN, 0, 255], [255, 0, np.NaN]])
    B2 = np.array([[None, np.nan, 255], [None, 0, 0], [None, 255, np.nan ]])
    B3 = np.array([[np.nan, 0, 255], [255, 0, np.nan], [None, None, None]])
    B4 = np.array([[np.nan, 255, None], [0, 0, None], [255, np.nan, None]])

    Bi.extend([B1, B2, B3, B4])

    b_mappings = {0: (1, 2), 1: (3, 4), 2: (1, 4), 3: (2, 3)}

    while edge_image.all() != final_image.all():

        # Each sub-cycle iterates 4 times, to prevent outcome to be non-connected lines while transformation
        # The sub- cycles are pixel with (non-edge element)
        #                                   -> South border set to 255
        #                                   -> North border set to 255
        #                                   -> West border set to 255
        #                                   -> East border set to 255
        for q in range(4):

            ontour_points = np.full((edge_image.shape[0], edge_image.shape[1]), 255)


            # First extract the final points
            for i in range(1, edge_image.shape[0] - 1):
                for j in range(1, edge_image.shape[1] - 1):

                    # This creates a 3*3 test window, by extracting values from the array
                    test_window = np.array([[edge_image[i + m, j + n] for n in range(-1, 2)] for m in range(-1, 2)])

                    outer_res = False
                    # Compare the above test window with Ai adn Bi to detect tge final points

                    for a_window in Ai:
                        res = True

                        for a_window_i in range(a_window.shape[0]):
                            for a_window_j in range(a_window.shape[1]):

                                if a_window[a_window_i, a_window_j] is not None:
                                    if a_window[a_window_i, a_window_j] != test_window [a_window_i, a_window_j]:
                                        res = False

                        if res:  # If after comparing, it is still true, then it's a final point
                            outer_res = True
                            break

                    if outer_res:

                        final_image [i, j] = 0      # Set this index (i,j) in the final element matrix
                        continue
                    else:
                        bs = b_mappings[q]

                        for ind_b in bs:

                            b_window = Bi[ind_b - 1]
                            res = True

                            for b_window_i in range(b_window.shape[0]):
                                for b_window_j in range(b_window.shape[1]):

                                    if b_window[b_window_i, b_window_j] is not None:
                                        if b_window[b_window_i, b_window_j] is not np.nan:
                                            if b_window[b_window_i, b_window_j] != test_window[b_window_i, b_window_j]:
                                                res = False

                            if res:  # If after comparing, it is still true, then it's a final point

                                final_image[i, j] = 0 # Set to black, if this pixel matches any of B's
                                break

            # By this point, it is determined that if any pixels in the whole image array belongs to final point or not

            for i in range(1, edge_image.shape[0] - 1):
                for j in range(1, edge_image.shape[1] - 1):

                    if q == 0:

                        if edge_image[i + 1, j] == 255:

                            edge_image[i, j] = 255  # Remove the contour points


                    elif q == 1:

                        if edge_image[i - 1, j] == 255:
                            edge_image[i, j] = 255


                    elif q == 2:

                        if edge_image[i, j-1] == 255:
                            edge_image[i, j] = 255


                    else:

                        if edge_image[i, j + 1] == 255:
                            edge_image[i, j] = 255


            # After all the contour points is deleted from the original image, add the final points to final image

            for i in range(1, edge_image.shape[0] - 1):
                for j in range(1, edge_image.shape[1] - 1):

                    # Add the final points in the image

                    if final_image[i, j] == 0:

                        edge_image[i, j] = 0

    test_driver_image(final_image)

    return final_image


if __name__ =="__main__":


    compare()