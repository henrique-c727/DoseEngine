"""
Global configuration for DoseEngine

Spatial dimensions are expressed in centimeters

Brief description:

GRID
dx and dz: voxel size in their respective dimensions
nx and nz: number of voxels along their respective axis

BEAM
ssd: source to surface distance

ENGINE
apply_etar: Enables the qualitative ETAR-inspired density correction
etar_sigma: Gaussian smoothing scale used by the correction
"""



GRID = {
    "dx": 0.2, 
    "dz": 0.2, 
    "nx": 100, 
    "nz": 200  
}

BEAM = { 
    "energy_mv": 6, # 
    "field_size_cm": 10.0,
    "ssd_cm": 100.0 
}

ENGINE = {
    "model_type": "pencil_beam", 
    "apply_etar": False, # True enables correction
    "etar_sigma": 1.0 
}

