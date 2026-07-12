from config import ENGINE

import convolution
import density
import kernel
import physics


class DoseEngine:
    """
    Coordinates the physical dose-calculation pipeline.

    The engine receives a 2D relative density matrix and
    applies the selected calculation model. The current implementation
    supports:

    "simple": primary transport only, returning a relative TERMA matrix;
    "pencil_beam": primary transport followed by convolution with a
      spatially invariant dose spread kernel.

    Parameters
    ----------
    phantom_matrix: 2D relative density matrix representing the phantom
    or resampled CT slice.

    model: Physical calculation model to use. Default is "pencil_beam".
    """
    def __init__(self, phantom_matrix, model="pencil_beam"):
        self.phantom_matrix = phantom_matrix
        self.model = model

        # Stores the density matrix used in the calculation
        self.matrix_calculation = phantom_matrix

    def run(self):
        """
        Executes the selected physical model.

        Returns
        -------
        Two-dimensional relative TERMA or dose matrix, depending on
        the selected model.
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

           # Applies the optional qualitative ETAR-inspired correction
            if ENGINE["apply_etar"]:
                self.matrix_calculation = density.apply_etar_filter(
                    self.phantom_matrix,
                    sigma_cm=ENGINE["etar_sigma"]
                )

            # Primary photon transport
            d_eff = physics.calculate_radiologic_length(
                self.matrix_calculation
            )

            fluence = physics.calculate_primary_fluence(d_eff)
            terma = physics.calculate_TERMA(fluence)

            # Secondary energy transport through kernel convolution
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