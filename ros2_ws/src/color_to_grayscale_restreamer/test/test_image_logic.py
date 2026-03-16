import pytest
import numpy as np
import cv2
from color_to_grayscale_restreamer.py_color2grayscale import ImageProcessor


def test_grayscale_conversion_dimensions():
    node = ImageProcessor()
    input_img = np.zeros((100, 100, 3), dtype=np.uint8)
    input_img[:, :] = [255, 0, 0]
    output_img = node.process_image(input_img)
    assert (output_img.shape == (100, 100))
    assert len(output_img.shape) == 2
