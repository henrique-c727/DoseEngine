import numpy as np
from scipy.signal import convolve2d


def convolve_terma(terma_matrix, kernel_matrix):
    """
    Calcula a distribuição relativa de dose através da convolução
    bidimensional entre o TERMA e o Dose Spread Kernel.

    Retorna a matriz de dose relativa com as mesmas dimensões do TERMA.
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