import numpy as np
from config import GRID

import pydicom
from scipy.ndimage import zoom
import os

def water_phantom():

    lines = GRID["nz"]
    columns = GRID["nx"]

    phantom = np.ones((lines, columns))
    return phantom

def tissue_insert(phantom, zi_cm, zf_cm, xi_cm, xf_cm, density):


    line_i = int(zi_cm / GRID["dz"])
    line_f = int(zf_cm / GRID["dz"])

    column_i = int(xi_cm / GRID["dx"])
    column_f = int(xf_cm / GRID["dx"])

    line_i = max(0, line_i)
    line_f = min(GRID["nz"], line_f)

    column_i = max(0, column_i)
    column_f = min(GRID["nx"], column_f)

    phantom[line_i : line_f, column_i: column_f] = density

    return phantom


def load_dicom_ct(filepath="slice.dcm"):
    # Verificar se existe o ficheiro
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"DICOM file not found: {filepath}, please insert a valid filepath.")

    # Ler o ficheiro
    dicom_file = pydicom.dcmread(filepath)
    pixels = dicom_file.pixel_array

    # Convertercada pixel para Unidades de Hounsfield (HU)
    intercept = dicom_file.RescaleIntercept
    slope = dicom_file.RescaleSlope
    hu_matrix = (pixels * slope) + intercept

    # Calibração CT (HU -> densidade relativa) [água:0 -> 1.0; ar:-1000.0 -> 0.0; osso:1000.0 -> 2.0]
    density_matrix = (hu_matrix/1000.0) + 1.0
    density_matrix = np.clip(density_matrix, 0.0, 3.0) # valores sempre entre 0 e 3

    # Redimensionar CT para a grelha configurada
    lines_og, columns_og = density_matrix.shape
    z_scale = GRID["nz"] / lines_og
    x_scale = GRID["nx"] / columns_og

    phantom_ct = zoom(density_matrix, (z_scale, x_scale))

    return phantom_ct



# Testes

def create_lung():

    phantom_lung = water_phantom()
    phantom_lung = tissue_insert(
        phantom_lung,
        zi_cm = 5.0,
        zf_cm = 15.0,
        xi_cm = 0.0,
        xf_cm = GRID["nx"] * GRID["dx"],
        density=0.3
        )
    
    return phantom_lung


def create_bone():
    phantom_bone = water_phantom()
    phantom_bone = tissue_insert(
        phantom_bone,
        zi_cm = 10.0,
        zf_cm = 12.0,
        xi_cm = 0.0,
        xf_cm = GRID["nx"] * GRID["dx"],
        density=1.8
        )
    
    return phantom_bone