import numpy as np
from config import GRID


def water_phantom():
    """
    Creates a homogeneous 2D water phantom, represented by
    a relative density matrix with all voxels set to 1.0,
    corresponding to water.

    Returns
    -------
    Phantom matrix.
    """

    lines = GRID["nz"]
    columns = GRID["nx"]

    phantom = np.ones((lines, columns))
    return phantom

def tissue_insert(phantom, zi_cm, zf_cm, xi_cm, xf_cm, density):
    """
    Inserts a rectangular region of constant density into a phantom.

    Parameters
    ----------
    phantom: 2D relative density matrix to be modified.

    x, z: This set of parameters specificate the initial
    and final coordinates of the inserted region in cm.

    density: Relative density assigned to the inserted region.

    Returns
    -------
    Modified phantom matrix.
    """

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
    """
    Creates a water phantom containing a lung-equivalent insertion.

    The lung region extends originally from 5 cm to 15 cm in depth and occupies
    the full lateral width of the phantom.

    Intended to be modified by the user, if needed.

    Returns 
    -------
    Relative density matrix containing a lung region with, originally, density 0.3
    """

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
    """
    Creates a water phantom containing a bone-equivalent insertion.

    The bone region originally extends from 10 cm to 12 cm in depth and occupies
    the full lateral width of the phantom.

    Intended to be modified by the user, if needed.

    Returns
    -------
    Relative density matrix containing a bone region with, originally, density 1.8.
    """
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
    """
    Creates an example phantom containing a high-density material.

    The inserted slab is intended only as a demonstration of how custom
    heterogeneous regions can be introduced into the computational grid.

    Returns
    -------
    Relative density matrix containing, originally, a high-density region with
    density 4.5.
    """
    custom_phantom = water_phantom()
    
    custom_phantom = tissue_insert(
        custom_phantom,
        zi_cm=8.0,
        zf_cm=9.0,
        xi_cm=0.0,
        xf_cm=GRID["nx"] * GRID["dx"],
        density=4.5
    )
    return custom_phantom