import numpy as np
from config import GRID


def water_phantom():

    lines = GRID["nz"]
    columns = GRID["nx"]

    phantom = np.ones((lines, columns))
    return phantom

def tissue_insert(phantom, zi_cm, zf_cm, xi_cm, xf_cm, density):


    line_i = int(np.round(zi_cm / GRID["dz"]))
    line_f = int(np.round(zf_cm / GRID["dz"]))

    column_i = int(np.round(xi_cm / GRID["dx"]))
    column_f = int(np.round(xf_cm / GRID["dx"]))

    line_i = max(0, line_i)
    line_f = min(GRID["nz"], line_f)

    column_i = max(0, column_i)
    column_f = min(GRID["nx"], column_f)

    phantom[line_i : line_f, column_i: column_f] = density

    return phantom



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

def create_custom():
    custom_phantom = water_phantom()
    
    # For example, a titanium mass
    custom_phantom = tissue_insert(
        custom_phantom,
        zi_cm=8.0,
        zf_cm=9.0,
        xi_cm=0.0,
        xf_cm=GRID["nx"] * GRID["dx"],
        density=4.5
    )
    return custom_phantom