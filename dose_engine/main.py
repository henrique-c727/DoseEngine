import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt

from config import GRID
import ct
import density
import phantom as ph
from engine import DoseEngine

import argparse


def plot_results(density_matrix, TERMA_matrix, dose_matrix, water_dose_matrix, phantom_type="lung"):
    width_cm = GRID["nx"] * GRID["dx"]
    depth_cm = GRID["nz"] * GRID["dz"]
    extent = [0, width_cm, depth_cm, 0]

    fig, axs = plt.subplots(2, 2, figsize=(14,10), constrained_layout=True)
    fig.suptitle("DoseEngine v1.0 - Beam analysis (Pencil Beam)", fontsize=16, fontweight="bold")

    # CT
    im1 = axs[0,0].imshow(density_matrix, cmap="bone", extent=extent, vmin=0, vmax=2.5, aspect="auto")
    axs[0,0].set_title("Effective density")
    fig.colorbar(im1, ax=axs[0,0], label="Relative density")

    # TERMA
    im2 = axs[0,1].imshow(TERMA_matrix, cmap="magma", extent=extent, aspect="auto")
    axs[0,1].set_title("TERMA")
    fig.colorbar(im2, ax=axs[0,1], label="Intensity")

    # FINAL DOSE
    im3 = axs[1,0].imshow(dose_matrix, cmap="turbo", extent=extent, aspect="auto")
    axs[1,0].set_title("Final Dose Distribution")
    fig.colorbar(im3, ax=axs[1,0], label="Relative dose")

    # PDD and LATERAL PROFILE
    z_axis = np.arange(GRID["nz"]) * GRID["dz"]
    x_axis=np.arange(GRID["nx"]) * GRID["dx"]

    pdd_lung = dose_matrix[:, GRID["nx"] // 2] # midpoint of the lung
    pdd_water = water_dose_matrix[:, GRID["nx"] // 2]

    lateral_profile = dose_matrix[int(10 / GRID["dz"]), :]

    axs[1,1].plot(z_axis, pdd_lung, color="red", linewidth=2, label="Central-axis depth-dose profile")
    axs[1,1].plot(z_axis, pdd_water, color="black", linewidth=1.5, linestyle="--", alpha=0.5, label="Water baseline depth-dose profile")
    
    if phantom_type == "lung":
        axs[1,1].axvspan(5.0, 15.0, color="gray", alpha=0.2, label="Lung Region (0.3 $g/cm^3$)")
    elif phantom_type == "bone":
        axs[1,1].axvspan(10.0, 12.0, color="gray", alpha=0.2, label="Bone Region (1.8 $g/cm^3$)")


    ax_secondary = axs[1,1].twiny()
    ax_secondary.plot(x_axis, lateral_profile, color="blue", linewidth=2, linestyle="--", label="Lateral Profile (Z = 10 cm)")

    axs[1,1].set_title("Quantitative analysis (PDD and lateral profile)")
    axs[1,1].set_xlabel("Depth Z (cm) [Red line]")
    ax_secondary.set_xlabel("Lateral X (cm) [Blue Line]")
    axs[1,1].grid(True, linestyle="--", alpha=0.6)

    lines1, labels1 = axs[1,1].get_legend_handles_labels()
    lines2, labels2 = ax_secondary.get_legend_handles_labels()
    axs[1,1].legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="DoseEngine")
    parser.add_argument("--phantom", type=str, choices=["lung", "bone", "water", "ct", "custom"], default="lung", 
                        help="Choose anatomic feature (default: lung)")

    parser.add_argument("--ct_path", type=str, default="sample.dcm", 
                        help="DICOM filepath (only used if --phantom is 'ct')")
    
    args = parser.parse_args()

    print(f"Initializing DoseEngine for scenario: {args.phantom.upper()}...")

    print("Generating anatomic phantom...")
    if args.phantom == "lung":
        patient = ph.create_lung()
    elif args.phantom == "bone":
        patient = ph.create_bone()
    elif args.phantom == "water":
        patient = ph.water_phantom()
    elif args.phantom == "ct":
        print(f"Reading DICOM file: {args.ct_path}")
        # DICOM -> HU
        hu_matrix = ct.load_dicom_hu(args.ct_path)
        # Adaptar a imagem à grelha do DoseEngine
        hu_matrix = ct.resize_to_grid(hu_matrix)
        # HU -> densidade relativa
        patient = density.hu_to_relative_density(hu_matrix)
        
    elif args.phantom == "custom":
        patient = ph.create_custom()
    patient_baseline = ph.water_phantom()

    print("Calculating primary transport (TERMA)...")
    engine_terma = DoseEngine(patient, model="simple")
    visual_terma = engine_terma.run()

    print("Calculating secondary transport (Heterogeneous)...")
    engine_dose = DoseEngine(patient, model="pencil_beam")
    final_dose = engine_dose.run()

    print("Calculating baseline transport (Homogeneous Water)...")
    engine_water = DoseEngine(patient_baseline, model="pencil_beam")
    water_dose = engine_water.run()

    print("Generating visualization elements...")
    plot_results(patient, visual_terma, final_dose, water_dose, args.phantom)