import numpy as np
from config import GRID

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
    line_f = max(GRID["nz"], line_f)

    column_i = max(0, column_i)
    column_f = max(GRID["nx"], column_f)

    phantom[line_i : line_f, column_i: column_f] = density

    return phantom

