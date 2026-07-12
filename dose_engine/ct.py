import os
import numpy as np
import pydicom
from scipy.ndimage import zoom

from config import GRID


def load_dicom_hu(filepath="slice.dcm"):
    """
    Reads a CT image in DICOM format and convert the stored pixel values
    into Hounsfield Units (HU).

    Parameters
    ----------
    filepath: Path to the DICOM file.

    Returns
    -------
    2D CT matrix expressed in Hounsfield Units.
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"DICOM file not found: {filepath}. "
            "Please provide a valid filepath."
        )

    dicom_file = pydicom.dcmread(filepath)
    pixels = dicom_file.pixel_array.astype(np.float64)

    slope = float(getattr(dicom_file, "RescaleSlope", 1.0))
    intercept = float(getattr(dicom_file, "RescaleIntercept", 0.0))

    hu_matrix = pixels * slope + intercept

    return hu_matrix


def resize_to_grid(matrix):
    """
    Resamples a 2D matrix to the computational grid defined
    in config.py.

    Linear interpolation estimates new voxel values from neighbouring values
    in the original image.

    Parameters
    ----------
    matrix: 2D matrix to be resampled.

    Returns
    -------
    Resampled matrix with shape (GRID["nz"], GRID["nx"]).
    """
    original_lines, original_columns = matrix.shape

    z_scale = GRID["nz"] / original_lines
    x_scale = GRID["nx"] / original_columns

    resized_matrix = zoom(
        matrix,
        (z_scale, x_scale),
        order=1
    )

    return resized_matrix