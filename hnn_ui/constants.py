# all cfg params ending with this values, affect the 3D view of the model
CANVAS_KEYS = ["_diam", "_L", "N_pyr_x", "N_pyr_y", "gridSpacingBasket", "gridSpacingPyr", "sizeY", 'xzScaling']

# default values when adding a new evoke proximal input
PROXIMAL = {
    "t": 0.,
    "sigma_t": 2.5,
    "numspikes": 1,
    "gbar_L2Basket_ampa": 0.,
    "gbar_L2Basket_nmda": 0.,
    "gbar_L2Pyr_ampa": 0.,
    "gbar_L2Pyr_nmda": 0.,
    "gbar_L5Basket_ampa": 0.,
    "gbar_L5Basket_nmda": 0.,
    "gbar_L5Pyr_ampa": 0.,
    "gbar_L5Pyr_nmda": 0.
}

# default values when adding a new evoke distal input
DISTAL = {
    "t": 0.,
    "sigma_t": 6.,
    "numspikes": 1,
    "gbar_L2Basket_ampa": 0.,
    "gbar_L2Basket_nmda": 0.,
    "gbar_L2Pyr_ampa": 0.,
    "gbar_L2Pyr_nmda": 0.,
    "gbar_L5Pyr_ampa": 0.,
    "gbar_L5Pyr_nmda": 0.
}
