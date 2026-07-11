import os
import numpy as np
import pydicom
from scipy.ndimage import zoom

from config import GRID


def load_dicom_hu(filepath="slice.dcm"):
    """
    Lê uma imagem CT em formato DICOM e converte os valores armazenados
    para Unidades de Hounsfield (HU).
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
    Redimensiona uma matriz 2D para a grelha definida em config.py.
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