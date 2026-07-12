import numpy as np
from config import GRID, BEAM

# Effective linear attenuation coefficient used by the simplified model.
mu_water = 0.048 # cm^-1

def calculate_radiologic_length(phantom):
    """
    Calculates the accumulated radiological depth along the beam axis.

    The current implementation assumes that the photon beam enters at
    the top of the matrix and propagates along the positive z-axis.

    Each voxel thickness is weighted by its relative density, producing
    a water-equivalent path length.

    Parameters
    ----------
    phantom: 2D relative density matrix with shape (nz, nx).

    Returns
    -------
    Accumulated radiological depth matrix, in centimeters, with the
    same shape as the input phantom.
    """

    d_eff = np.cumsum(phantom * GRID["dz"], axis=0)

    return d_eff

def calculate_primary_fluence(d_eff):
    """
    Calculates the relative primary photon fluence inside the phantom.

    The calculation combines:

    - exponential attenuation through the radiological depth;
    - inverse-square reduction with distance from the source;
    - a centered rectangular field defined by the configured field size.

    The fluence at the phantom surface is treated as a relative value
    of 1.0 before attenuation and geometrical corrections.

    Parameters
    ----------
    d_eff: Accumulated radiological depth matrix, in centimeters.

    Returns
    -------
    Relative primary fluence matrix with the same shape as d_eff.
    Voxels outside the radiation field are assigned zero fluence.
    """

    lines, columns = d_eff.shape
    fluence = np.zeros((lines, columns))


    # Lateral limits of the centered radiation field.
    center_idx = columns // 2
    field_radius_pixels = int((BEAM["field_size_cm"] / 2.0) / GRID["dx"])
    column_i = int(center_idx - field_radius_pixels)
    column_f = int(center_idx + field_radius_pixels)

    # Physical depth of each row, measured from the phantom surface.
    z_physical = np.arange(1, lines + 1) * GRID["dz"]

    # Inverse-square correction relative to the phantom surface.
    isl = (BEAM["ssd_cm"] / (BEAM["ssd_cm"] + z_physical)) ** 2


    for z in range(lines):
        attenuation = np.exp(-mu_water * d_eff[z, column_i:column_f])
        fluence[z, column_i:column_f] = 1.0 * attenuation * isl[z] # relative, value on surface 1.0 as a reference

    return fluence

def calculate_TERMA(fluence):
    """
    Estimates a relative TERMA distribution from the primary fluence.

    In this educational model, TERMA is represented by a relative
    quantity proportional to the attenuated primary fluence and the
    adopted water-equivalent attenuation coefficient.

    Parameters
    ----------
    fluence: Relative primary photon fluence matrix.

    Returns
    -------
    Relative TERMA matrix with the same shape as the input fluence.
    """
    return fluence * mu_water