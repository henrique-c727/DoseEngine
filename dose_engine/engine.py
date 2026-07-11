from config import ENGINE

import convolution
import density
import kernel
import physics


class DoseEngine:

    def __init__(self, phantom_matrix, model="pencil_beam"):
        self.phantom_matrix = phantom_matrix
        self.model = model

        # Guarda a matriz efetivamente utilizada no cálculo.
        self.matrix_calculation = phantom_matrix

    def run(self):
        """
        Executa o modelo físico selecionado e devolve uma matriz
        bidimensional de TERMA ou dose relativa.
        """
        if self.model == "simple":
            self.matrix_calculation = self.phantom_matrix

            d_eff = physics.calculate_radiologic_length(
                self.matrix_calculation
            )

            fluence = physics.calculate_primary_fluence(d_eff)

            return physics.calculate_TERMA(fluence)

        elif self.model == "pencil_beam":
            self.matrix_calculation = self.phantom_matrix

            # Correção qualitativa de heterogeneidade aplicada à densidade
            if ENGINE["apply_etar"]:
                self.matrix_calculation = density.apply_etar_filter(
                    self.phantom_matrix,
                    sigma_cm=ENGINE["etar_sigma"]
                )

            # Transporte primário
            d_eff = physics.calculate_radiologic_length(
                self.matrix_calculation
            )

            fluence = physics.calculate_primary_fluence(d_eff)
            terma = physics.calculate_TERMA(fluence)

            # Transporte secundário
            kernel_matrix = kernel.generate_kernel_2d()

            dose = convolution.convolve_terma(
                terma,
                kernel_matrix
            )

            return dose

        elif self.model == "advanced":
            raise NotImplementedError(
                "O modelo avançado ainda não foi implementado."
            )

        else:
            raise ValueError(
                f"Modelo físico '{self.model}' não reconhecido."
            )