"""
netParams.py

High-level specifications for HNN network model using NetPyNE

Contributors: salvadordura@gmail.com
"""

from netpyne import specs

import numpy as np
import itertools as it


def set_netParams(cfg):


    # ----------------------------------------------------------------------------
    #
    # NETWORK PARAMETERS
    #
    # ----------------------------------------------------------------------------

    netParams = specs.NetParams()  # object of class NetParams to store the network parameters

    #------------------------------------------------------------------------------
    # General network parameters
    #------------------------------------------------------------------------------
    netParams.sizeX = (cfg.N_pyr_x * cfg.gridSpacingPyr) - 1  # x-dimension (horizontal length) size in um
    netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth) size in um
    netParams.sizeZ = (cfg.N_pyr_y * cfg.gridSpacingPyr) - 1 # z-dimension (horizontal depth) size in um
    netParams.shape = 'cuboid'


    # ----------------------------------------------------------------------------
    # Cell parameters
    # ----------------------------------------------------------------------------
    # from cellParams import cellParams  # defined in separate module for clarity
    # netParams.cellParams = cellParams


    # ----------------------------------------------------------------------------
    # Population parameters
    # ----------------------------------------------------------------------------
    layersE = {'L2': [0.0*cfg.sizeY, 0.0*cfg.sizeY], 'L5': [0.654*cfg.sizeY, 0.654*cfg.sizeY]} # 0.654 = 1308/2000
    layersI = {'L2': [0.0*cfg.sizeY, 0.0*cfg.sizeY], 'L5': [0.654*cfg.sizeY, 0.654*cfg.sizeY]}

    # Create list of locations for Basket cells based on original ad hoc rules
    # define relevant x spacings for basket cells
    xzero = np.arange(0, cfg.N_pyr_x, 3)
    xone = np.arange(1, cfg.N_pyr_x, 3)
    yeven = np.arange(0, cfg.N_pyr_y, 2)
    yodd = np.arange(1, cfg.N_pyr_y, 2)
    coords = [pos for pos in it.product(xzero, yeven)] + [pos for pos in it.product(xone, yodd)]
    coords_sorted = sorted(coords, key=lambda pos: pos[1])
    BasketLocs = [{'x': coord[0], 'z': coord[1]} for coord in coords_sorted]

    netParams.popParams['L2Basket'] = {'cellType':  'L2Basket', 'cellModel': 'HH_simple',   'yRange': layersI['L2'], 'numCells': len(BasketLocs), 'cellsList': BasketLocs}
    netParams.popParams['L2Pyr'] =    {'cellType':  'L2Pyr',    'cellModel': 'HH_reduced',  'yRange': layersE['L2'],  'gridSpacing': cfg.gridSpacingPyr}
    netParams.popParams['L5Basket'] = {'cellType':  'L5Basket', 'cellModel': 'HH_simple',   'yRange': layersI['L5'],  'numCells': len(BasketLocs), 'cellsList': BasketLocs}
    netParams.popParams['L5Pyr'] =    {'cellType':  'L5Pyr',    'cellModel': 'HH_reduced',  'yRange': layersE['L5'],  'gridSpacing': cfg.gridSpacingPyr}

    pops = list(netParams.popParams.keys())
    cellsPerPop = {}
    cellsPerPop['L2Pyr'] = cellsPerPop['L5Pyr'] = int(cfg.N_pyr_x * cfg.N_pyr_x)
    cellsPerPop['L2Basket'] = cellsPerPop['L5Basket'] = int(np.ceil(cfg.N_pyr_x * cfg.N_pyr_x / cfg.gridSpacingBasket[2]) + 1)


    #------------------------------------------------------------------------------
    # Synaptic mechanism parameters
    #------------------------------------------------------------------------------

    netParams.synMechParams['L2Pyr_AMPA'] = {'mod':'Exp2Syn', 'tau1': cfg.L2Pyr_ampa_tau1, 'tau2': cfg.L2Pyr_ampa_tau2, 'e': cfg.L2Pyr_ampa_e}
    netParams.synMechParams['L2Pyr_NMDA'] = {'mod': 'Exp2Syn', 'tau1': cfg.L2Pyr_nmda_tau1, 'tau2': cfg.L2Pyr_nmda_tau2, 'e': cfg.L2Pyr_nmda_e}
    netParams.synMechParams['L2Pyr_GABAA'] = {'mod':'Exp2Syn', 'tau1': cfg.L2Pyr_gabaa_tau1, 'tau2': cfg.L2Pyr_gabaa_tau2, 'e': cfg.L2Pyr_gabaa_e}
    netParams.synMechParams['L2Pyr_GABAB'] = {'mod':'Exp2Syn', 'tau1': cfg.L2Pyr_gabab_tau1, 'tau2': cfg.L2Pyr_gabab_tau2, 'e': cfg.L2Pyr_gabab_e}

    netParams.synMechParams['L5Pyr_AMPA'] = {'mod':'Exp2Syn', 'tau1': cfg.L5Pyr_ampa_tau1, 'tau2': cfg.L5Pyr_ampa_tau2, 'e': cfg.L5Pyr_ampa_e}
    netParams.synMechParams['L5Pyr_NMDA'] = {'mod': 'Exp2Syn', 'tau1': cfg.L5Pyr_nmda_tau1, 'tau2': cfg.L5Pyr_nmda_tau2, 'e': cfg.L5Pyr_nmda_e}
    netParams.synMechParams['L5Pyr_GABAA'] = {'mod':'Exp2Syn', 'tau1': cfg.L5Pyr_gabaa_tau1, 'tau2': cfg.L5Pyr_gabaa_tau2, 'e': cfg.L5Pyr_gabaa_e}
    netParams.synMechParams['L5Pyr_GABAB'] = {'mod':'Exp2Syn', 'tau1': cfg.L5Pyr_gabab_tau1, 'tau2': cfg.L5Pyr_gabab_tau2, 'e': cfg.L5Pyr_gabab_e}

    netParams.synMechParams['AMPA'] = {'mod':'Exp2Syn', 'tau1': 0.5, 'tau2': 5.0, 'e': 0}
    netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 1, 'tau2': 20, 'e': 0}
    netParams.synMechParams['GABAA'] = {'mod':'Exp2Syn', 'tau1': 0.5, 'tau2': 5, 'e': -80}
    netParams.synMechParams['GABAB'] = {'mod':'Exp2Syn', 'tau1': 1, 'tau2': 20, 'e': -80}


    #------------------------------------------------------------------------------
    # Local connectivity parameters
    #------------------------------------------------------------------------------

    # Weight and delay distance-dependent functions (as strings) to use in conn rules
    weightDistFunc = '{A_weight} * exp(-(dist_2D**2) / ({lamtha}**2))'
    delayDistFunc = '{A_delay} / exp(-(dist_2D**2) / ({lamtha}**2))'

    if cfg.localConn:

        # L2 Pyr -> L2 Pyr
        synParamsList = [{'synMech': 'L2Pyr_AMPA',
                          'A_weight': cfg.EEgain * cfg.gbar_L2Pyr_L2Pyr_ampa,
                          'A_delay': 1.,
                          'lamtha': 3.},

                         {'synMech': 'L2Pyr_NMDA',
                          'A_weight': cfg.EEgain * cfg.gbar_L2Pyr_L2Pyr_nmda,
                          'A_delay': 1.,
                          'lamtha': 3.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['L2Pyr->L2Pyr_%d'%(i)] = {
                'preConds': {'pop': 'L2Pyr'},
                'postConds': {'pop': 'L2Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams), # equivalent to weightDistFunc.format(A_weight=cfg.gbar_L2Pyr_L2Pyr_ampa, lamtha=1.)
                'delay': delayDistFunc.format(**synParams),
                'synsPerConn': 3,
                'sec': ['basal_2', 'basal_3','apical_oblique', ]}


        # L2 Basket -> L2 Pyr
        synParamsList = [{'synMech': 'L2Pyr_GABAA',
                          'A_weight': cfg.IEgain * cfg.gbar_L2Basket_L2Pyr_gabaa,
                          'A_delay': 1.,
                          'lamtha': 50.},

                         {'synMech': 'L2Pyr_GABAB',
                          'A_weight': cfg.IEgain * cfg.gbar_L2Basket_L2Pyr_gabab,
                          'A_delay': 1.,
                          'lamtha': 50.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['L2Basket->L2Pyr_%d'%(i)] = {
                'preConds': {'pop': 'L2Basket'},
                'postConds': {'pop': 'L2Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'synsPerConn': 1,
                'sec': ['soma']}


        # L2 Pyr -> L2 Basket
        synParams = {'synMech': 'AMPA',
                     'A_weight': cfg.EIgain * cfg.gbar_L2Pyr_L2Basket,
                     'A_delay': 1.,
                     'lamtha': 3.}

        netParams.connParams['L2Pyr->L2Basket_%s'%(synParams['synMech'])] = {
            'preConds': {'pop': 'L2Pyr'},
            'postConds': {'pop': 'L2Basket'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 1,
            'sec': ['soma']}


        # L2 Basket -> L2 Basket
        synParams = {'synMech': 'GABAA',
                     'A_weight': cfg.IIgain * cfg.gbar_L2Basket_L2Basket,
                     'A_delay': 1.,
                     'lamtha': 20.}

        netParams.connParams['L2Basket->L2Basket'] = {
            'preConds': {'pop': 'L2Basket'},
            'postConds': {'pop': 'L2Basket'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 1,
            'sec': ['soma']}


        # L5 Pyr -> L5 Pyr
        synParamsList = [{'synMech': 'L5Pyr_AMPA',
                          'A_weight': cfg.EEgain * cfg.gbar_L5Pyr_L5Pyr_ampa,
                          'A_delay': 1.,
                          'lamtha': 3.},

                         {'synMech': 'L5Pyr_NMDA',
                          'A_weight': cfg.EEgain * cfg.gbar_L5Pyr_L5Pyr_nmda,
                          'A_delay': 1.,
                          'lamtha': 3.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['L5Pyr->L5Pyr_%d'%(i)] = {
                'preConds': {'pop': 'L5Pyr'},
                'postConds': {'pop': 'L5Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'synsPerConn': 3,
                'sec': ['basal_2', 'basal_3', 'apical_oblique']}


        # L5 Basket -> L5 Pyr
        synParamsList = [{'synMech': 'L5Pyr_GABAA',
                          'A_weight': cfg.IEgain * cfg.gbar_L5Basket_L5Pyr_gabaa,
                          'A_delay': 1.,
                          'lamtha': 70.},

                         {'synMech': 'L5Pyr_GABAB',
                          'A_weight': cfg.IEgain * cfg.gbar_L5Basket_L5Pyr_gabab,
                          'A_delay': 1.,
                          'lamtha': 70.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['L5Basket->L5Pyr_%d'%(i)] = {
                'preConds': {'pop': 'L5Basket'},
                'postConds': {'pop': 'L5Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'synsPerConn': 1,
                'sec': ['soma']}


        # L2 Pyr -> L5 Pyr
        synParams = {'synMech': 'L5Pyr_AMPA',
                     'A_weight': cfg.EEgain * cfg.gbar_L2Pyr_L5Pyr,
                     'A_delay': 1.,
                     'lamtha': 3.}

        netParams.connParams['L2Pyr->L5Pyr'] = {
            'preConds': {'pop': 'L2Pyr'},
            'postConds': {'pop': 'L5Pyr'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 4,
            'sec': ['basal_2', 'basal_3', 'apical_tuft', 'apical_oblique']}


        # L2 Basket -> L5 Pyr
        synParams = {'synMech': 'L5Pyr_GABAA',
                     'A_weight': cfg.IEgain * cfg.gbar_L2Basket_L5Pyr,
                     'A_delay': 1.,
                     'lamtha': 50.}

        netParams.connParams['L2Basket->L5Pyr'] = {
            'preConds': {'pop': 'L2Basket'},
            'postConds': {'pop': 'L5Pyr'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 1,
            'sec': ['apical_tuft']}


        # L5 Pyr -> L5 Basket
        synParams = {'synMech': 'AMPA',
                     'A_weight': cfg.EIgain * cfg.gbar_L5Pyr_L5Basket,
                     'A_delay': 1.,
                     'lamtha': 3.}

        netParams.connParams['L5Pyr->L5Basket'] = {
            'preConds': {'pop': 'L5Pyr'},
            'postConds': {'pop': 'L5Basket'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 1,
            'sec': ['soma']}


        # L2 Pyr -> L5 Basket
        synParams = {'synMech': 'AMPA',
                     'A_weight': cfg.EIgain * cfg.gbar_L2Pyr_L5Basket,
                     'A_delay': 1.,
                     'lamtha': 3.}

        netParams.connParams['L2Pyr->L5Basket'] = {
            'preConds': {'pop': 'L2Pyr'},
            'postConds': {'pop': 'L5Basket'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 1,
            'sec': ['soma']}


        # L5 Basket -> L5 Basket
        synParams = {'synMech': 'GABAA',
                     'A_weight': cfg.IIgain * cfg.gbar_L5Basket_L5Basket,
                     'A_delay': 1.,
                     'lamtha': 20.}

        netParams.connParams['L5Basket->L5Basket'] = {
            'preConds': {'pop': 'L5Basket'},
            'postConds': {'pop': 'L5Basket'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 1,
            'sec': ['soma']}


    #------------------------------------------------------------------------------
    # Rhythmic proximal and distal inputs parameters
    #------------------------------------------------------------------------------

    # Location of external inputs
    xrange = np.arange(cfg.N_pyr_x)
    extLocX = xrange[int((len(xrange) - 1) // 2)]
    zrange = np.arange(cfg.N_pyr_y)
    extLocZ = xrange[int((len(zrange) - 1) // 2)]
    extLocY = 650 # positive depth of L5 relative to L2; doesn't affect weight/delay calculations

    conn1to1Pyr = np.array([range(0,cellsPerPop['L2Pyr']), range(0,cellsPerPop['L2Pyr'])]).T
    conn1to1Basket = np.array([range(0,cellsPerPop['L2Basket']), range(0,cellsPerPop['L2Basket'])]).T

    if cfg.rhythmicInputs:

        # Ad hoc rules copied from original code (need to improve!! -- maybe add to .param files?)

        ## "if stdev is zero, increase synaptic weights 5 fold to make"
        ## "single input equivalent to 5 simultaneous input to prevent spiking <<---- SN: WHAT IS THIS RULE!?!?!?"
        if cfg.t0_input_stdev_prox == 0.0 and cfg.distribution_prox != 'uniform':
            for key in [k for k in cfg.__dict__ if k.startswith('input_prox_A_weight')]:
                cfg.__dict__[key] *= 5.0

        if cfg.t0_input_stdev_dist == 0.0 and cfg.distribution_dist != 'uniform':
            for key in [k for k in cfg.__dict__ if k.startswith('input_dist_A_weight')]:
                cfg.__dict__[key] *= 5.0

        ## "if L5 delay is -1, use same delays as L2 unless L2 delay is 0.1 in which case use 1. <<---- SN: WHAT IS THIS RULE!?!?!?"
        if cfg.input_prox_A_delay_L5 == -1:
            if cfg.input_prox_A_delay_L2 != 0.1:
                cfg.input_prox_A_delay_L5 = cfg.input_prox_A_delay_L2
            else:
                cfg.input_prox_A_delay_L5 = 1.0

        if cfg.input_dist_A_delay_L5 == -1:
            if cfg.input_dist_A_delay_L2 != 0.1:
                cfg.input_dist_A_delay_L5 = cfg.input_dist_A_delay_L2
            else:
                cfg.input_dist_A_delay_L5 = 1.0

        # External Rhythmic proximal inputs (1 VecStim per cell for each cell population)
        for pop in pops:
            netParams.popParams['extRhythmicProximal_%s'%(pop)] = {
                'cellModel': 'VecStim',
                'numCells': cellsPerPop[pop],
                'xRange': [extLocX, extLocX],
                'yRange': [extLocY, extLocY],
                'zRange': [extLocZ, extLocZ],
                'seed': int(cfg.prng_seedcore_input_prox),
                'spikePattern': {
                    'type': 'rhythmic',
                    'start': cfg.t0_input_prox,
                    'startStd': cfg.t0_input_stdev_prox,
                    'stop': cfg.tstop_input_prox,
                    'freq': cfg.f_input_prox,
                    'freqStd': cfg.f_stdev_prox,
                    'eventsPerCycle': cfg.events_per_cycle_prox,
                    'distribution': cfg.distribution_prox,
                    'repeats': cfg.repeats_prox}}


            # External Rhythmic distal inputs (population of 1 VecStim)
            netParams.popParams['extRhythmicDistal_%s'%(pop)] = {
                'cellModel': 'VecStim',
                'numCells': cellsPerPop[pop],
                'xRange': [extLocX, extLocX],
                'yRange': [extLocY, extLocY],
                'zRange': [extLocZ, extLocZ],
                'seed': int(cfg.prng_seedcore_input_dist),
                'spikePattern': {
                    'type': 'rhythmic',
                    'start': cfg.t0_input_dist,
                    'startStd': cfg.t0_input_stdev_dist,
                    'stop': cfg.tstop_input_dist,
                    'freq': cfg.f_input_dist,
                    'freqStd': cfg.f_stdev_dist,
                    'eventsPerCycle': cfg.events_per_cycle_dist,
                    'distribution': cfg.distribution_dist,
                    'repeats': cfg.repeats_dist}}


        # Rhytmic proximal -> L2 Pyr
        synParamsList = [{'synMech': 'L2Pyr_AMPA',
                          'A_weight': cfg.input_prox_A_weight_L2Pyr_ampa,
                          'A_delay': cfg.input_prox_A_delay_L2,
                          'lamtha': 100.},

                         {'synMech': 'L2Pyr_NMDA',
                          'A_weight': cfg.input_prox_A_weight_L2Pyr_nmda,
                          'A_delay': cfg.input_prox_A_delay_L2,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extRhythmicProx->L2Pyr_%d'%(i)] = {
                'preConds': {'pop': 'extRhythmicProximal_L2Pyr'},
                'postConds': {'pop': 'L2Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'connList': conn1to1Pyr,  # 1-to-1 mapping
                'synsPerConn': 3,
                'sec': ['basal_2', 'basal_3','apical_oblique']}


        # Rhythmic distal -> L2 Pyr
        synParamsList = [{'synMech': 'L2Pyr_AMPA',
                          'A_weight': cfg.input_dist_A_weight_L2Pyr_ampa,
                          'A_delay': cfg.input_dist_A_delay_L2,
                          'lamtha': 100.},

                         {'synMech': 'L2Pyr_NMDA',
                          'A_weight': cfg.input_dist_A_weight_L2Pyr_nmda,
                          'A_delay': cfg.input_dist_A_delay_L2,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extRhythmicDistal->L2Pyr_%d'%(i)] = {
                'preConds': {'pop': 'extRhythmicDistal_L2Pyr'},
                'postConds': {'pop': 'L2Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'connList': conn1to1Pyr,  # 1-to-1 mapping
                'synsPerConn': 1,
                'sec': ['apical_tuft']}


        # Rhythmic proximal -> L5 Pyr
        synParamsList = [{'synMech': 'L5Pyr_AMPA',
                          'A_weight': cfg.input_prox_A_weight_L5Pyr_ampa,
                          'A_delay': cfg.input_prox_A_delay_L5,
                          'lamtha': 100.},

                         {'synMech': 'L5Pyr_NMDA',
                          'A_weight': cfg.input_prox_A_weight_L5Pyr_nmda,
                          'A_delay': cfg.input_prox_A_delay_L5,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extRhythmicProx->L5Pyr_%d'%(i)] = {
                'preConds': {'pop': 'extRhythmicProximal_L5Pyr'},
                'postConds': {'pop': 'L5Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'connList': conn1to1Pyr,  # 1-to-1 mapping
                'synsPerConn': 3,
                'sec': ['basal_2', 'basal_3','apical_oblique']}


        # Rhythmic distal -> L5 Pyr
        synParamsList = [{'synMech': 'L5Pyr_AMPA',
                          'A_weight': cfg.input_dist_A_weight_L5Pyr_ampa,
                          'A_delay': cfg.input_dist_A_delay_L5,
                          'lamtha': 100.},

                         {'synMech': 'L5Pyr_NMDA',
                          'A_weight': cfg.input_dist_A_weight_L5Pyr_nmda,
                          'A_delay': cfg.input_dist_A_delay_L5,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extRhythmicDistal->L5Pyr_%d'%(i)] = {
                'preConds': {'pop': 'extRhythmicDistal_L5Pyr'},
                'postConds': {'pop': 'L5Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'connList': conn1to1Basket,  # 1-to-1 mapping
                'synsPerConn': 1,
                'sec': ['apical_tuft']}


        # Rhytmic proximal -> L2 Basket
        synParamsList = [{'synMech': 'AMPA',
                          'A_weight': cfg.input_prox_A_weight_L2Basket_ampa,
                          'A_delay': cfg.input_prox_A_delay_L2,
                          'lamtha': 100.},

                         {'synMech': 'NMDA',
                          'A_weight': cfg.input_prox_A_weight_L2Basket_nmda,
                          'A_delay': cfg.input_prox_A_delay_L2,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extRhythmicProx->L2Basket_%d'%(i)] = {
                'preConds': {'pop': 'extRhythmicProximal_L5Pyr'},
                'postConds': {'pop': 'L2Basket'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'connList': conn1to1Basket,  # 1-to-1 mapping
                'synsPerConn': 1,
                'sec': 'soma'}


        # Rhytmic proximal -> L5 Basket
        synParamsList = [{'synMech': 'AMPA',
                          'A_weight': cfg.input_prox_A_weight_L5Basket_ampa,
                          'A_delay': cfg.input_prox_A_delay_L5,
                          'lamtha': 100.},

                         {'synMech': 'NMDA',
                          'A_weight': cfg.input_prox_A_weight_L5Basket_nmda,
                          'A_delay': cfg.input_prox_A_delay_L5,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extRhythmicProx->L5Basket_%d'%(i)] = {
                'preConds': {'pop': 'extRhythmicProximal_L5Pyr'},
                'postConds': {'pop': 'L5Basket'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'connList': conn1to1Basket,  # 1-to-1 mapping
                'synsPerConn': 1,
                'sec': 'soma'}


    #------------------------------------------------------------------------------
    # Evoked proximal and distal inputs parameters
    #------------------------------------------------------------------------------

    if cfg.evokedInputs:

        # Evoked proximal inputs (population of 1 VecStim)
        nprox = len([k for k in cfg.__dict__ if k.startswith('t_evprox')])
        ndist = len([k for k in cfg.__dict__ if k.startswith('t_evdist')])

        # TEMPORARY CODE TO HARD CODE SAME SPIKE TIMES AS IN ORIGINAL MODEL (ERP TUT)
        # import json
        # with open('../input_spikes.json', 'r') as f:
        #     input_spikes = json.load(f)
        # ev_gids = {'L2Basket': [0,35], 'L2Pyr': [35,135], 'L5Basket': [135,170], 'L5Pyr': [170,270]}

        # Evoked proximal inputs (population of 1 VecStim)
        for iprox in range(nprox):
            for pop in pops:
                skey = 'evprox_%d'%(iprox+1)
                netParams.popParams['evokedProximal_%d_%s'%(iprox+1, pop)] = {
                    'cellModel': 'VecStim',
                    'numCells': cellsPerPop[pop],
                    'xRange': [extLocX, extLocX],
                    'yRange': [extLocY, extLocY],
                    'zRange': [extLocZ, extLocZ],
                    'seed': int(getattr(cfg, 'prng_seedcore_' + skey)),
                    #'spkTimes': input_spikes['evprox'+str(iprox+1)][ev_gids[pop][0]:ev_gids[pop][1]]}
                    'spikePattern': {
                        'type': 'evoked',
                        'start': getattr(cfg, 't_' + skey),
                        'startStd': getattr(cfg, 'sigma_t_' + skey),
                        'numspikes': getattr(cfg, 'numspikes_' + skey),
                        'sync': getattr(cfg, 'sync_evinput')}}


            # Evoked proximal -> L2 Pyr
            synParamsList = [{'synMech': 'L2Pyr_AMPA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L2Pyr_ampa'),
                              'A_delay': 0.1,
                              'lamtha': 3.},

                             {'synMech': 'L2Pyr_NMDA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L2Pyr_nmda'),
                              'A_delay': 0.1,
                              'lamtha': 3.}]

            for i,synParams in enumerate(synParamsList):
                netParams.connParams['evokedProx_%d->L2Pyr_%d'%(iprox+1, i)] = {
                    'preConds': {'pop': 'evokedProximal_%d_L2Pyr'%(iprox+1)},
                    'postConds': {'pop': 'L2Pyr'},
                    'synMech': synParams['synMech'],
                    'weight': weightDistFunc.format(**synParams),
                    'delay': delayDistFunc.format(**synParams),
                    'connList': conn1to1Pyr,
                    'synsPerConn': 3,
                    'sec': ['basal_2', 'basal_3','apical_oblique']}

            # Evoked proximal -> L5 Pyr
            synParamsList = [{'synMech': 'L5Pyr_AMPA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L5Pyr_ampa'),
                              'A_delay': 1.0,
                              'lamtha': 3.},

                             {'synMech': 'L5Pyr_NMDA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L5Pyr_nmda'),
                              'A_delay': 1.0,
                              'lamtha': 3.}]

            for i,synParams in enumerate(synParamsList):
                netParams.connParams['evokedProx_%d->L5Pyr_%d'%(iprox+1, i)] = {
                    'preConds': {'pop': 'evokedProximal_%d_L5Pyr'%(iprox+1)},
                    'postConds': {'pop': 'L5Pyr'},
                    'synMech': synParams['synMech'],
                    'weight': weightDistFunc.format(**synParams),
                    'delay': delayDistFunc.format(**synParams),
                    'connList': conn1to1Pyr,
                    'synsPerConn': 3,
                    'sec': ['basal_2', 'basal_3','apical_oblique']}

            # Evoked proximal -> L2 Basket
            synParamsList = [{'synMech': 'AMPA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L2Basket_ampa'),
                              'A_delay': 0.1,
                              'lamtha': 3.},

                             {'synMech': 'NMDA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L2Basket_nmda'),
                              'A_delay': 0.1,
                              'lamtha': 3.}]

            for i,synParams in enumerate(synParamsList):
                netParams.connParams['evokedProx_%d->L2Basket_%d'%(iprox+1, i)] = {
                    'preConds': {'pop': 'evokedProximal_%d_L2Basket'%(iprox+1)},
                    'postConds': {'pop': 'L2Basket'},
                    'synMech': synParams['synMech'],
                    'weight': weightDistFunc.format(**synParams),
                    'delay': delayDistFunc.format(**synParams),
                    'connList': conn1to1Basket,
                    'synsPerConn': 1,
                    'sec': 'soma'}

            # Evoked proximal -> L5 Basket
            synParamsList = [{'synMech': 'AMPA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L5Basket_ampa'),
                              'A_delay': 1.0,
                              'lamtha': 3.},

                             {'synMech': 'NMDA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L5Basket_nmda'),
                              'A_delay': 1.0,
                              'lamtha': 3.}]

            for i,synParams in enumerate(synParamsList):
                netParams.connParams['evokedProx_%d->L5Basket_%d'%(iprox+1, i)] = {
                    'preConds': {'pop': 'evokedProximal_%d_L5Basket'%(iprox+1)},
                    'postConds': {'pop': 'L5Basket'},
                    'synMech': synParams['synMech'],
                    'weight': weightDistFunc.format(**synParams),
                    'delay': delayDistFunc.format(**synParams),
                    'connList': conn1to1Basket,
                    'synsPerConn': 1,
                    'sec': 'soma'}


        # Evoked distal inputs (population of 1 VecStim)
        for idist in range(ndist):
            for pop in pops:
                skey = 'evdist_%d'%(idist+1)
                netParams.popParams['evokedDistal_%d_%s'%(idist+1, pop)] = {
                    'cellModel': 'VecStim',
                    'numCells': cellsPerPop[pop],
                    'xRange': [extLocX, extLocX],
                    'yRange': [extLocY, extLocY],
                    'zRange': [extLocZ, extLocZ],
                    'seed': int(getattr(cfg, 'prng_seedcore_' + skey)),
                    #'spkTimes': input_spikes['evdist'+str(idist+1)][ev_gids[pop][0]:ev_gids[pop][1]]}
                    'spikePattern': {
                        'type': 'evoked',
                        'start': getattr(cfg, 't_' + skey),
                        'startStd': getattr(cfg, 'sigma_t_' + skey),
                        'numspikes': getattr(cfg, 'numspikes_' + skey),
                        'sync': getattr(cfg, 'sync_evinput')}}


            # Evoked Distal -> L2 Pyr
            synParamsList = [{'synMech': 'L2Pyr_AMPA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L2Pyr_ampa'),
                              'A_delay': 0.1,
                              'lamtha': 3.},

                             {'synMech': 'L2Pyr_NMDA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L2Pyr_nmda'),
                              'A_delay': 0.1,
                              'lamtha': 3.}]

            for i,synParams in enumerate(synParamsList):
                netParams.connParams['evokedDistal_%d->L2Pyr_%d'%(idist+1, i)] = {
                    'preConds': {'pop': 'evokedDistal_%d_L2Pyr'%(idist+1)},
                    'postConds': {'pop': 'L2Pyr'},
                    'synMech': synParams['synMech'],
                    'weight': weightDistFunc.format(**synParams),
                    'delay': delayDistFunc.format(**synParams),
                    'connList': conn1to1Pyr,
                    'synsPerConn': 1,
                    'sec': 'apical_tuft'}

            # Evoked Distal -> L5 Pyr
            synParamsList = [{'synMech': 'L5Pyr_AMPA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L5Pyr_ampa'),
                              'A_delay': 0.1,
                              'lamtha': 3.},

                             {'synMech': 'L5Pyr_NMDA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L5Pyr_nmda'),
                              'A_delay': 0.1,
                              'lamtha': 3.}]

            for i,synParams in enumerate(synParamsList):
                netParams.connParams['evokedDistal_%d->L5Pyr_%d'%(idist+1, i)] = {
                    'preConds': {'pop': 'evokedDistal_%d_L5Pyr'%(idist+1)},
                    'postConds': {'pop': 'L5Pyr'},
                    'synMech': synParams['synMech'],
                    'weight': weightDistFunc.format(**synParams),
                    'delay': delayDistFunc.format(**synParams),
                    'connList': conn1to1Pyr,
                    'synsPerConn': 1,
                    'sec': 'apical_tuft'}

            # Evoked Distal -> L2 Basket
            synParamsList = [{'synMech': 'AMPA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L2Basket_ampa'),
                              'A_delay': 0.1,
                              'lamtha': 3.},

                             {'synMech': 'NMDA',
                              'A_weight': getattr(cfg, 'gbar_'+skey+'_L2Basket_nmda'),
                              'A_delay': 0.1,
                              'lamtha': 3.}]

            for i,synParams in enumerate(synParamsList):
                netParams.connParams['evokedDistal_%d->L2Basket_%d'%(idist+1, i)] = {
                    'preConds': {'pop': 'evokedDistal_%d_L2Basket'%(idist+1)},
                    'postConds': {'pop': 'L2Basket'},
                    'synMech': synParams['synMech'],
                    'weight': weightDistFunc.format(**synParams),
                    'delay': delayDistFunc.format(**synParams),
                    'connList': conn1to1Basket,
                    'synsPerConn': 1,
                    'sec': 'soma'}


    #------------------------------------------------------------------------------
    # Tonic input parameters
    #------------------------------------------------------------------------------

    if cfg.tonicInputs:

        # Tonic inputs (IClamp) -> L2Pyr
        if cfg.Itonic_T_L2Pyr_soma == -1:
            t_dur = cfg.duration - cfg.Itonic_t0_L2Pyr_soma
        else:
            t_dur = cfg.Itonic_T_L2Pyr_soma - cfg.Itonic_t0_L2Pyr_soma

        netParams.stimSourceParams['ITonic_L2Pyr'] = {'type': 'IClamp', 'del': cfg.Itonic_t0_L2Pyr_soma, 'dur': t_dur, 'amp': cfg.Itonic_A_L2Pyr_soma}
        netParams.stimTargetParams['ITonic->L2Pyr'] = {'source': 'ITonic_L2Pyr', 'sec':'soma', 'loc': 0.5, 'conds': {'pop': 'L2Pyr'}}


        # Tonic inputs (IClamp) -> L5Pyr
        if cfg.Itonic_T_L5Pyr_soma == -1:
            t_dur = cfg.duration - cfg.Itonic_t0_L5Pyr_soma
        else:
            t_dur = cfg.Itonic_T_L5Pyr_soma - cfg.Itonic_t0_L5Pyr_soma

        netParams.stimSourceParams['ITonic_L5Pyr'] = {'type': 'IClamp', 'del': cfg.Itonic_t0_L5Pyr_soma, 'dur': t_dur, 'amp': cfg.Itonic_A_L5Pyr_soma}
        netParams.stimTargetParams['ITonic->L5Pyr'] = {'source': 'ITonic_L5Pyr', 'sec':'soma', 'loc': 0.5, 'conds': {'pop': 'L5Pyr'}}


        # Tonic inputs (IClamp) -> L2Basket
        if cfg.Itonic_T_L2Basket == -1:
            t_dur = cfg.duration - cfg.Itonic_t0_L2Basket
        else:
            t_dur = cfg.Itonic_T_L2Basket - cfg.Itonic_t0_L2Basket

        netParams.stimSourceParams['ITonic_L2Basket'] = {'type': 'IClamp', 'del': cfg.Itonic_t0_L2Basket, 'dur': t_dur, 'amp': cfg.Itonic_A_L2Basket}
        netParams.stimTargetParams['ITonic->L2Basket'] = {'source': 'ITonic_L2Basket', 'sec':'soma', 'loc': 0.5, 'conds': {'pop': 'L2Basket'}}


        # Tonic inputs (IClamp) -> L5Basket
        if cfg.Itonic_T_L5Basket == -1:
            t_dur = cfg.duration - cfg.Itonic_t0_L5Basket
        else:
            t_dur = cfg.Itonic_T_L5Basket - cfg.Itonic_t0_L5Basket

        netParams.stimSourceParams['ITonic_L5Basket'] = {'type': 'IClamp', 'del': cfg.Itonic_t0_L5Basket, 'dur': t_dur, 'amp': cfg.Itonic_A_L5Basket}
        netParams.stimTargetParams['ITonic->L5Basket'] = {'source': 'ITonic_L5Basket', 'sec':'soma', 'loc': 0.5, 'conds': {'pop': 'L5Basket'}}


    #------------------------------------------------------------------------------
    # Poisson-distributed input parameters
    #------------------------------------------------------------------------------

    if cfg.poissonInputs:

        # Poisson inputs -> L2 Pyr
        netParams.popParams['extPoisson_L2Pyr'] = {
            'cellModel': 'VecStim',
            'numCells': 1,
            'xRange': [extLocX, extLocX],
            'yRange': [extLocY, extLocY],
            'zRange': [extLocZ, extLocZ],
            'seed': int(getattr(cfg, 'prng_seedcore_extpois')),
            'spikePattern': {
                'type': 'poisson',
                'start': getattr(cfg, 't0_pois'),
                'interval': getattr(cfg, 'T_pois'),
                'frequency': getattr(cfg, 'L2Pyr_Pois_lamtha')}}

        synParamsList = [{'synMech': 'L2Pyr_AMPA',
                          'A_weight': getattr(cfg, 'L2Pyr_Pois_A_weight_ampa'),
                          'A_delay': 0.1,
                          'lamtha': 100.},

                         {'synMech': 'L2Pyr_NMDA',
                          'A_weight': getattr(cfg, 'L2Pyr_Pois_A_weight_nmda'),
                          'A_delay': 0.1,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extPoisson->L2Pyr_%d'%(i)] = {
                'preConds': {'pop': 'extPoisson_L2Pyr'},
                'postConds': {'pop': 'L2Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'synsPerConn': 3,
                'sec': ['basal_2', 'basal_3','apical_oblique']}


        # Poisson inputs -> L5 Pyr
        netParams.popParams['extPoisson_L5Pyr'] = {
            'cellModel': 'VecStim',
            'numCells': 1,
            'xRange': [extLocX, extLocX],
            'yRange': [extLocY, extLocY],
            'zRange': [extLocZ, extLocZ],
            'seed': int(getattr(cfg, 'prng_seedcore_extpois')),
            'spikePattern': {
                'type': 'poisson',
                'start': getattr(cfg, 't0_pois'),
                'interval': getattr(cfg, 'T_pois'),
                'frequency': getattr(cfg, 'L5Pyr_Pois_lamtha')}}

        synParamsList = [{'synMech': 'L5Pyr_AMPA',
                          'A_weight': getattr(cfg, 'L5Pyr_Pois_A_weight_ampa'),
                          'A_delay': 0.1,
                          'lamtha': 100.},

                         {'synMech': 'L5Pyr_NMDA',
                          'A_weight': getattr(cfg, 'L5Pyr_Pois_A_weight_nmda'),
                          'A_delay': 0.1,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extPoisson->L5Pyr_%d'%(i)] = {
                'preConds': {'pop': 'extPoisson_L5Pyr'},
                'postConds': {'pop': 'L5Pyr'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'synsPerConn': 3,
                'sec': ['basal_2', 'basal_3','apical_oblique']}


        # Poisson inputs -> L2 Basket
        netParams.popParams['extPoisson_L2Basket'] = {
            'cellModel': 'VecStim',
            'numCells': 1,
            'xRange': [extLocX, extLocX],
            'yRange': [extLocY, extLocY],
            'zRange': [extLocZ, extLocZ],
            'seed': int(getattr(cfg, 'prng_seedcore_extpois')),
            'spikePattern': {
                'type': 'poisson',
                'start': getattr(cfg, 't0_pois'),
                'interval': getattr(cfg, 'T_pois'),
                'frequency': getattr(cfg, 'L2Basket_Pois_lamtha')}}

        synParamsList = [{'synMech': 'AMPA',
                          'A_weight': getattr(cfg, 'L2Basket_Pois_A_weight_ampa'),
                          'A_delay': 1.0,
                          'lamtha': 100.},

                         {'synMech': 'NMDA',
                          'A_weight': getattr(cfg, 'L2Basket_Pois_A_weight_nmda'),
                          'A_delay': 1.0,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extPoisson->L2Basket_%d'%(i)] = {
                'preConds': {'pop': 'extPoisson_L2Basket'},
                'postConds': {'pop': 'L2Basket'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'synsPerConn': 1,
                'sec': ['soma']}


        # Poisson inputs -> L5 Basket
        netParams.popParams['extPoisson_L5Basket'] = {
            'cellModel': 'VecStim',
            'numCells': 1,
            'xRange': [extLocX, extLocX],
            'yRange': [extLocY, extLocY],
            'zRange': [extLocZ, extLocZ],
            'seed': int(getattr(cfg, 'prng_seedcore_extpois')),
            'spikePattern': {
                'type': 'poisson',
                'start': getattr(cfg, 't0_pois'),
                'interval': getattr(cfg, 'T_pois'),
                'frequency': getattr(cfg, 'L5Basket_Pois_lamtha')}}

        synParamsList = [{'synMech': 'AMPA',
                          'A_weight': getattr(cfg, 'L5Basket_Pois_A_weight_ampa'),
                          'A_delay': 1.0,
                          'lamtha': 100.},

                         {'synMech': 'NMDA',
                          'A_weight': getattr(cfg, 'L5Basket_Pois_A_weight_nmda'),
                          'A_delay': 1.0,
                          'lamtha': 100.}]

        for i,synParams in enumerate(synParamsList):
            netParams.connParams['extPoisson->L5Basket_%d'%(i)] = {
                'preConds': {'pop': 'extPoisson_L5Basket'},
                'postConds': {'pop': 'L5Basket'},
                'synMech': synParams['synMech'],
                'weight': weightDistFunc.format(**synParams),
                'delay': delayDistFunc.format(**synParams),
                'synsPerConn': 1,
                'sec': ['soma']}


    #------------------------------------------------------------------------------
    # Gaussian-distributed inputs parameters
    #------------------------------------------------------------------------------

    if cfg.gaussInputs:

        # Gaussian inputs -> L2 Pyr
        netParams.popParams['extGauss_L2Pyr'] = {
            'cellModel': 'VecStim',
            'numCells': 1,
            'xRange': [extLocX, extLocX],
            'yRange': [extLocY, extLocY],
            'zRange': [extLocZ, extLocZ],
            'seed': int(getattr(cfg, 'prng_seedcore_extgauss')),
            'spikePattern': {
                'type': 'gauss',
                'mu': getattr(cfg, 'L2Pyr_Gauss_mu'),
                'sigma': getattr(cfg, 'L2Pyr_Gauss_sigma')}}

        synParams = {'synMech': 'L2Pyr_AMPA',
                     'A_weight': getattr(cfg, 'L2Pyr_Gauss_A_weight'),
                     'A_delay': 0.1,
                     'lamtha': 100.}

        netParams.connParams['extGauss->L2Pyr'] = {
            'preConds': {'pop': 'extGauss_L2Pyr'},
            'postConds': {'pop': 'L2Pyr'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 3,
            'sec': ['basal_2', 'basal_3','apical_oblique']}


        # Gaussian inputs -> L5 Pyr
        netParams.popParams['extGauss_L5Pyr'] = {
            'cellModel': 'VecStim',
            'numCells': 1,
            'xRange': [extLocX, extLocX],
            'yRange': [extLocY, extLocY],
            'zRange': [extLocZ, extLocZ],
            'seed': int(getattr(cfg, 'prng_seedcore_extgauss')),
            'spikePattern': {
                'type': 'gauss',
                'mu': getattr(cfg, 'L5Pyr_Gauss_mu'),
                'sigma': getattr(cfg, 'L5Pyr_Gauss_sigma')}}

        synParams = {'synMech': 'L5Pyr_AMPA',
                     'A_weight': getattr(cfg, 'L5Pyr_Gauss_A_weight'),
                     'A_delay': 0.1,
                     'lamtha': 100.}

        netParams.connParams['extGauss->L5Pyr'] = {
            'preConds': {'pop': 'extGauss_L5Pyr'},
            'postConds': {'pop': 'L5Pyr'},
            'synMech': synParams['synMech'],
            'weight': weightDistFunc.format(**synParams),
            'delay': delayDistFunc.format(**synParams),
            'synsPerConn': 3,
            'sec': ['basal_2', 'basal_3','apical_oblique']}

        return netParams
