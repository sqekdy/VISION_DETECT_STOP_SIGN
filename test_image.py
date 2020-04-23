"""
This is the test driver program to test the image after processing it every step
Returns: Image
"""
from PIL import Image
import os
import numpy as np

def convert_2d_3d(input_array):
    """  This only works for the gray-scale images, given that all the RGB values of pixels are same
    :param: 2D or 3D representation of an image
    :return: 3D, or 2D representation of image for 2D and 3D respectively
    """

    dimension_converted_array = None

    if input_array.ndim == 3:
        # Convert into 2 dimensional
        dimension_converted_array = np.zeros((input_array.shape[0], input_array.shape[1]), dtype=np.uint8)
        for i in range(input_array.shape[0]):
            for j in range(input_array.shape[1]):
                dimension_converted_array[i, j] = input_array[i, j, 1]

    else:
        # Convert into 3 dimensional
        dimension_converted_array = np.zeros((input_array.shape[0], input_array.shape[1], 3), dtype=np.uint8)
        for i in range(input_array.shape[0]):
            for j in range(input_array.shape[1]):

                dimension_converted_array[i, j] = [input_array[i, j] for p in range(3)]

    return dimension_converted_array



def test_driver_image(ndarray):


    ndarray = ndarray if ndarray.ndim == 3 else convert_2d_3d(ndarray)

    # Since bitmap images are read in bottom-up fashion, reverse the ndarray
    image_2d_array = ndarray[::-1, :, :]

    img = Image.new( 'RGB', (image_2d_array.shape[1], image_2d_array.shape[0]), "black") # Create a new black image
    pixels = img.load() # Create the pixel map
    for i in range(img.size[0]):    # For every pixel:
        for j in range(img.size[1]):
            pixels[i, j] = tuple(image_2d_array[j, i])  # Set the colour accordingly


    img.show()

    img.save(os.path.join(os.getcwd(),"teste_image.bmp"))
