import numpy as np
from scipy.ndimage import gaussian_filter

from config import GRID


def hu_to_relative_density(hu_matrix):
    """
    Converte Unidades de Hounsfield para densidade relativa através
    de uma calibração linear simplificada.

    Aproximações utilizadas:
        HU = -1000  -> densidade relativa = 0.0
        HU = 0      -> densidade relativa = 1.0
        HU = 1000   -> densidade relativa = 2.0

    Esta relação é estritamente didática e não representa uma curva
    de calibração clínica de um scanner CT.
    """
    density_matrix = (hu_matrix / 1000.0) + 1.0

    # Limita valores extremos ou não físicos para esta demonstração.
    density_matrix = np.clip(density_matrix, 0.0, 3.0)

    return density_matrix


def apply_etar_filter(density_matrix, sigma_cm):
    """
    Aplica uma média espacial gaussiana à matriz de densidade.

    Este operador constitui uma correção qualitativa inspirada no
    princípio ETAR.

    
    Retorna a matriz de densidade suavizada,
    na tentativa de representar melhor os efeitos de dose em
    heterogeneidades. 
    """
    sigma_z_pixels = sigma_cm / GRID["dz"]
    sigma_x_pixels = sigma_cm / GRID["dx"]

    filtered_density = gaussian_filter(
        density_matrix,
        sigma=(sigma_z_pixels, sigma_x_pixels)
    )

    return filtered_density