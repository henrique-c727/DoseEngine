GRID = {
    "dx": 0.2, # pixel horizontal length in cm 
    "dz": 0.2, # pixel vertical length in cm
    "nx": 100, # total number of pixels horizontally
    "nz": 200 # total number of pixels vertically
}

BEAM = { 
    "energy_mv": 6,
    "field_size_cm": 10.0, 
    "ssd_cm": 100.0 # source to surface distance in cm
}

ENGINE = {
    "model_type": "pencil_beam", 
    "apply_etar": False, 
    "etar_sigma": 1.0
}

