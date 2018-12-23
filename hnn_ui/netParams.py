# netParams.py - High-level specifications for network model using NetPyNE

from netpyne import specs

from .cfg import cfg

# try:
#   from __main__ import cfg  # import SimConfig object with params from parent module
# except:
#   from cfg import cfg  # if no simConfig in parent module, import directly from cfg module

import numpy as np


# ----------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
# ----------------------------------------------------------------------------

netParams = specs.NetParams()   # object of class NetParams to store the network parameters
#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.sizeX = cfg.N_pyr_x * cfg.gridSpacing # x-dimension (horizontal length) size in um
netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = cfg.N_pyr_y * cfg.gridSpacing # z-dimension (horizontal depth) size in um
netParams.shape = 'cuboid' 

# ----------------------------------------------------------------------------
# Cell parameters
# ----------------------------------------------------------------------------
from .cellParams import cellParams  # defined in separate module for clarity
netParams.cellParams = cellParams


# ----------------------------------------------------------------------------
# Population parameters
# ----------------------------------------------------------------------------
layersE = {'L5': [0.5*cfg.sizeY, 0.5*cfg.sizeY], 'L2': [0.5*cfg.sizeY, 0.5*cfg.sizeY]}
layersI = {'L5': [0.6*cfg.sizeY, 0.6*cfg.sizeY], 'L2': [1.4*cfg.sizeY, 1.4*cfg.sizeY]}

netParams.popParams['L2Pyr'] = {'cellType': 'L2Pyr',    'cellModel': 'HH_reduced', 'yRange': layersE['L2'], 'gridSpacing': cfg.gridSpacing} # 'numCells': numCellsE}
netParams.popParams['L2Basket'] = {'cellType': 'L2Basket', 'cellModel': 'HH_simple', 'yRange': layersI['L2'], 'gridSpacing': cfg.gridSpacing} # 'numCells': numCellsI}
netParams.popParams['L5Pyr'] = {'cellType': 'L5Pyr',    'cellModel': 'HH_reduced', 'yRange': layersE['L5'], 'gridSpacing': cfg.gridSpacing} #  'numCells': numCellsE}
netParams.popParams['L5Basket'] = {'cellType': 'L5Basket', 'cellModel': 'HH_simple', 'yRange': layersI['L5'], 'gridSpacing': cfg.gridSpacing} #  'numCells': numCellsI}


#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
'''
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
# Connectivity parameters 
#------------------------------------------------------------------------------

# Weight and delay distance-dependent functions (as strings) to use in conn rules
weightDistFunc = '{A_weight} * exp(-(dist_2D**2) / ({lamtha}**2))'
delayDistFunc = '{A_weight} / exp(-(dist_2D**2) / ({lamtha}**2))'


# L2 Pyr -> L2 Pyr
synParamsList = [{'synMech': 'L2Pyr_AMPA',
            'A_weight': cfg.gbar_L2Pyr_L2Pyr_ampa,
            'A_delay': 1.,
            'lamtha': 3.},

            {'synMech': 'L2Pyr_NMDA',
            'A_weight': cfg.gbar_L2Pyr_L2Pyr_nmda,
            'A_delay': 1.,
            'lamtha': 3.}]

for synParams in synParamsList:
    netParams.connParams['L2Pyr->L2Pyr'] = { 
        'preConds': {'pop': 'L2Pyr'}, 
        'postConds': {'pop': 'L2Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': ['basal_2', 'basal_3','apical_oblique', ]}
                

# L2 Basket -> L2 Pyr
synParamsList = [{'synMech': 'L2Pyr_GABAA',
            'A_weight': cfg.gbar_L2Basket_L2Pyr_gabaa,
            'A_delay': 1.,
            'lamtha': 50.},

            {'synMech': 'L2Pyr_GABAB',
            'A_weight': cfg.gbar_L2Basket_L2Pyr_gabab,
            'A_delay': 1.,
            'lamtha': 50.}]

for synParams in synParamsList:
    netParams.connParams['L2Basket->L2Pyr'] = { 
        'preConds': {'pop': 'L2Basket'}, 
        'postConds': {'pop': 'L2Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 1,
        'sec': ['soma']}


# L2 Pyr -> L2 Basket 
synParams = {'synMech': 'AMPA',
            'A_weight': cfg.gbar_L2Pyr_L2Basket,
            'A_delay': 1.,
            'lamtha': 3.}

netParams.connParams['L2Pyr->L2Basket'] = { 
    'preConds': {'pop': 'L2Pyr'}, 
    'postConds': {'pop': 'L2Basket'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 1,
    'sec': ['soma']}


# L2 Basket -> L2 Basket 
synParams = {'synMech': 'GABAA',
            'A_weight': cfg.gbar_L2Basket_L2Basket,
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
            'A_weight': cfg.gbar_L5Pyr_L5Pyr_ampa,
            'A_delay': 1.,
            'lamtha': 3.},

            {'synMech': 'L5Pyr_NMDA',
            'A_weight': cfg.gbar_L5Pyr_L5Pyr_nmda,
            'A_delay': 1.,
            'lamtha': 3.}]

for synParams in synParamsList:
    netParams.connParams['L5Pyr->L5Pyr'] = { 
        'preConds': {'pop': 'L5Pyr'}, 
        'postConds': {'pop': 'L5Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 3,
        'sec': ['basal_2', 'basal_3', 'apical_oblique']}
              

# L5 Basket -> L5 Pyr
synParamsList = [{'synMech': 'L5Pyr_GABAA',
            'A_weight': cfg.gbar_L5Basket_L5Pyr_gabaa,
            'A_delay': 1.,
            'lamtha': 70.},

            {'synMech': 'L5Pyr_GABAB',
            'A_weight': cfg.gbar_L5Basket_L5Pyr_gabab,
            'A_delay': 1.,
            'lamtha': 70.}]

for synParams in synParamsList:
    netParams.connParams['L5Basket->L5Pyr'] = { 
        'preConds': {'pop': 'L5Basket'}, 
        'postConds': {'pop': 'L5Pyr'},
        'synMech': synParams['synMech'],
        'weight': weightDistFunc.format(**synParams),
        'delay': delayDistFunc.format(**synParams),
        'synsPerConn': 1,
        'sec': ['soma']}


# L2 Pyr -> L5 Pyr
synParams = {'synMech': 'L5Pyr_AMPA',
            'A_weight': cfg.gbar_L2Pyr_L5Pyr,
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
            'A_weight': cfg.gbar_L2Basket_L5Pyr,
            'A_delay': 1.,
            'lamtha': 50.}

netParams.connParams['L2Basket->L5Pyr'] = { 
    'preConds': {'pop': 'L2Basket'}, 
    'postConds': {'pop': 'L5Pyr'},
    'synMech': synParams['synMech'],
    'weight': weightDistFunc.format(**synParams),
    'delay': delayDistFunc.format(**synParams),
    'synsPerConn': 4,
    'sec': ['apical_tuft']}
       

# L5 Pyr -> L5 Basket 
synParams = {'synMech': 'AMPA',
            'A_weight': cfg.gbar_L5Pyr_L5Basket,
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
            'A_weight': cfg.gbar_L2Pyr_L5Basket,
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
            'A_weight': cfg.gbar_L5Basket_L5Basket,
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

'''


"""
# ----------------------------------------------------------------------------
# Current inputs (IClamp)
# ----------------------------------------------------------------------------
if cfg.addIClamp:   
    for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
        ic = getattr(cfg, iclabel, None)  # get dict with params

        # add stim source
        netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'delay': ic['start'], 'dur': ic['dur'], 'amp': ic['amp']}
        
        # connect stim source to target
        netParams.stimTargetParams[iclabel+'_'+ic['pop']] = \
            {'source': iclabel, 'conds': {'pop': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}


# ----------------------------------------------------------------------------
# NetStim inputs
# ----------------------------------------------------------------------------
if cfg.addNetStim:
    for nslabel in [k for k in dir(cfg) if k.startswith('NetStim')]:
        ns = getattr(cfg, nslabel, None)

        # add stim source
        netParams.stimSourceParams[nslabel] = {'type': 'NetStim', 'start': ns['start'], 'interval': ns['interval'], 
                                               'noise': ns['noise'], 'number': ns['number']}

        # connect stim source to target
        netParams.stimTargetParams[nslabel+'_'+ns['pop']] = \
            {'source': nslabel, 'conds': {'pop': ns['pop']}, 'sec': ns['sec'], 'loc': ns['loc'],
             'synMech': ns['synMech'], 'weight': ns['weight'], 'delay': ns['delay']}
"""
