import numpy as np
from scipy.ndimage import gaussian_filter

from config import GRID


def hu_to_relative_density(hu_matrix):
    """
    Converts Hounsfield Units into relative density using a simplified
    linear calibration.

    The following reference points are assumed:

        HU = -1000  -> relative density = 0.0
        HU = 0      -> relative density = 1.0
        HU = 1000   -> relative density = 2.0

    Parameters
    ----------
    hu_matrix: 2D CT matrix expressed in Hounsfield Units.

    Returns
    -------
    2D relative density matrix.

    Note
    ----
    This conversion is strictly educational and does not represent a
    scanner-specific clinical CT calibration curve.
    """
    density_matrix = (hu_matrix / 1000.0) + 1.0

    # Limita valores extremos ou não físicos para esta demonstração.
    density_matrix = np.clip(density_matrix, 0.0, 3.0)

    return density_matrix


def apply_etar_filter(density_matrix, sigma_cm):
    """
    Applies Gaussian spatial smoothing to the relative density matrix.

    This operator is a heterogeneity correction inspired
    by the use of effective local density in ETAR-related approaches.
    It is not a direct implementation of the ETAR method.

    Parameters
    ----------
    density_matrix: 2D relative density matrix.

    sigma_cm: Standard deviation of the Gaussian filter, in centimeters.

    Returns
    -------
    Spatially smoothed relative density matrix.
    """
    sigma_z_pixels = sigma_cm / GRID["dz"]
    sigma_x_pixels = sigma_cm / GRID["dx"]

    filtered_density = gaussian_filter(
        density_matrix,
        sigma=(sigma_z_pixels, sigma_x_pixels)
    )

    return filtered_density