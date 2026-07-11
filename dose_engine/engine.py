import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter

from config import GRID, ENGINE
import physics
import kernel

class DoseEngine:

    def __init__(self, phantom_matrix, model="pencil_beam"):
        self.phantom_matrix = phantom_matrix
        self.model = model

    def apply_ETAR_filter(self, density_matrix):

        sigma_pixels = ENGINE["etar_sigma"] / GRID["dx"]

        smooth_density = gaussian_filter(density_matrix, sigma=sigma_pixels)
        return smooth_density
    
    def run(self):
        if self.model == "simple":
            d_eff = physics.calculate_radiologic_length(self.phantom_matrix)
            fluence = physics.calculate_primary_fluence(d_eff)

            return physics.calculate_TERMA(fluence)
        
        elif self.model == "pencil_beam":

            self.matrix_calculation = self.phantom_matrix

            d_eff = physics.calculate_radiologic_length(self.matrix_calculation)
            fluence = physics.calculate_primary_fluence(d_eff)
            terma = physics.calculate_TERMA(fluence)

            if ENGINE["apply_etar"]:
                terma = self.apply_ETAR_filter(terma)

            kernel_matrix = kernel.generate_kernel_2d()
            dose = convolve2d(terma, kernel_matrix, mode="same", boundary="fill", fillvalue=0)

            return dose

        elif self.model == "advanced":
            raise NotImplementedError("Algoritmo AAA ainda não foi implementado.")
        
        else:
            raise ValueError(f"Modelo físico {self.model} não reconhecido.")