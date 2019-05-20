# all cfg params ending with this values, affect the 3D view of the model
CANVAS_KEYS = ["_diam", "_L", "N_pyr_x", "N_pyr_y", "gridSpacingPyr", "sizeY"]

# default values when adding a new evoke proximal input
PROXIMAL = {
    "startTimeMean": 0.,
    "stopTimeStd": 2.5,
    "numberOfSpikes": 1,
    "L2PyrAMPAWeight": 0.,
    "L2PyrNMDAWeight": 0.,
    "L2BasketAMPAWeight": 0.,
    "L2BasketNMDAWeight": 0.,
    "L5PyrAMPAWeight": 0.,
    "L5PyrNMDAWeight": 0.,
    "L5BasketAMPAWeight": 0.,
    "L5BasketNMDAWeight": 0.
}

# default values when adding a new evoke distal input
DISTAL = {
    "startTimeMean": 0.,
    "stopTimeStd": 6.,
    "numberOfSpikes": 1,
    "L2PyrAMPAWeight": 0.,
    "L2PyrNMDAWeight": 0.,
    "L2BasketAMPAWeight": 0.,
    "L2BasketNMDAWeight": 0.,
    "L5PyrAMPAWeight": 0.,
    "L5PyrNMDAWeight": 0.
}
