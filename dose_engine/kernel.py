import numpy as np
from config import GRID

def generate_kernel_2d(radius_cm = 3.0):


    radius_pixels = int(radius_cm / GRID["dx"])
    kernel_size = (2 * radius_pixels) + 1


    center = radius_pixels
    x = np.arange(kernel_size) - center
    z = np.arange(kernel_size) - center
    xx, zz = np.meshgrid(x, z)

    r = np.sqrt(xx**2 + zz**2) * GRID["dx"]


    A = 1.0
    a = 5.0
    B = 0.1
    b = 0.5

    kernel = A * np.exp(-a * r) + B * np.exp(-b * r)


    kernel = kernel / np.sum(kernel)

    return kernel