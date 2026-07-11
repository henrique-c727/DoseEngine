import numpy as np
from config import GRID, BEAM

mu_water = 0.048

def calculate_radiologic_length(phantom):


    d_eff = np.cumsum(phantom * GRID["dz"], axis=0)

    return d_eff

def calculate_primary_fluence(d_eff):

    lines, columns = d_eff.shape
    fluence = np.zeros((lines, columns))

    center_idx = columns // 2
    field_radius_pixels = int((BEAM["field_size_cm"] / 2.0) / GRID["dx"])
    column_i = int(center_idx - field_radius_pixels)
    column_f = int(center_idx + field_radius_pixels)

    z_physical = np.arange(1, lines + 1) * GRID["dz"]
    isl = (BEAM["ssd_cm"] / (BEAM["ssd_cm"] + z_physical)) ** 2

    for z in range(lines):
        attenuation = np.exp(-mu_water * d_eff[z, column_i:column_f])
        fluence[z, column_i:column_f] = 1.0 * attenuation * isl[z]

    return fluence

def calculate_TERMA(fluence):
    return fluence * mu_water