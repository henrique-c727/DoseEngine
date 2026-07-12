import numpy as np
from scipy.signal import convolve2d


def convolve_terma(terma_matrix, kernel_matrix):
    """
    Calculates the relative dose distribution through a 2D
    convolution between the TERMA matrix and the dose spread kernel.

    Parameters
    ----------
    terma_matrix: 2D relative TERMA distribution.

    kernel_matrix: 2D normalized dose spread kernel.

    Returns
    -------
    Relative dose matrix with the same shape as terma_matrix.

    Notes
    -----
    The calculation assumes a spatially invariant kernel.
    Values outside
    the computational domain are treated as zero.
    """
    if terma_matrix.ndim != 2 or kernel_matrix.ndim != 2:
        raise ValueError("TERMA and kernel must both be 2D matrices.")

    dose_matrix = convolve2d(
        terma_matrix,
        kernel_matrix,
        mode="same",
        boundary="fill",
        fillvalue=0
    )

    return dose_matrix