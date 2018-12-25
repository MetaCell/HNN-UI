"""
hnn_geppetto.py
Initialise HNN Geppetto, this class contains methods to connect HNN with the Geppetto based UI
"""
import importlib
import json
import logging
import os
import sys
from contextlib import redirect_stdout

from jupyter_geppetto import jupyter_geppetto, synchronization, utils
from netpyne import sim
from pygeppetto.model.model_serializer import GeppettoModelSerializer

import hnn_ui.model_utils as model_utils
from hnn_ui.cellParams import set_cellParams
from hnn_ui.netParams import set_netParams
from hnn_ui.netpyne_model_interpreter import NetPyNEModelInterpreter

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


class HNNGeppetto():

    def __init__(self):
        self.model_interpreter = NetPyNEModelInterpreter()

        self.cfg = self.load_cfg()

        synchronization.startSynchronization(self.__dict__)
        logging.debug("Initializing the original model")

        jupyter_geppetto.context = {'hnn_geppetto': self}

    def getData(self):
        with redirect_stdout(sys.__stdout__):
            return {
                "metadata": model_utils.load_metadata("hnn_ui/metadata"),
                "isDocker": os.path.isfile('/.dockerenv'),
                "currentFolder": os.getcwd()
            }

    def load_cfg(self):
        cfg_module = importlib.import_module("hnn_ui.cfg")
        return getattr(cfg_module, "cfg")

    def instantiateModelInGeppetto(self):
        try:
            with redirect_stdout(sys.__stdout__):
                netpyne_model = self.instantiateModel()
                self.geppetto_model = self.model_interpreter.getGeppettoModel(netpyne_model)

                return json.loads(GeppettoModelSerializer().serialize(self.geppetto_model))
        except:
            return utils.getJSONError("Error while instantiating the NetPyNE model", sys.exc_info())

    def instantiateModel(self):
        with redirect_stdout(sys.__stdout__):
            # netParams_module = importlib.import_module("hnn_ui.netParams")
            # netParams_snapshot = getattr(netParams_module, "netParams")
            netParams_snapshot = set_netParams(self.cfg)
            netParams_snapshot.cellParams = set_cellParams(self.cfg)

            # saveData = sim.allSimData if hasattr(sim, 'allSimData') and 'spkt' in sim.allSimData.keys() and len(sim.allSimData['spkt'])>0 else False
            sim.create(simConfig=self.cfg, netParams=netParams_snapshot)
            # sim.net.defineCellShapes()  # creates 3d pt for cells with stylized geometries
            sim.gatherData(gatherLFP=False)
            # if saveData: sim.allSimData = saveData  # preserve data from previous simulation

        return sim

    def getEvokedInputs(self):
        return list(self.cfg.evoked.keys())

    # waiting for evoked input model (this is tentative)
    def addEvokedInput(self, input_type):
        evoked_indices = [int(key[key.index("_") + 1:]) for key in self.cfg.evoked.keys() if input_type in key]
        index = str(max(evoked_indices) + 1) if len(evoked_indices) > 0 else 1
        self.cfg.evoked[f"{input_type}_{index}"] = DISTAL if input_type == "distal" else PROXIMAL
        return {'inputs': self.getEvokedInputs(), 'selected_input': f'{input_type}_{index}'}

    def removeEvokedInput(self, name):
        del self.cfg.evoked[name]
        return self.getEvokedInputs()

    def getDirList(self, dir=None, onlyDirs=False, filterFiles=False):
        # Get Current dir
        if dir is None or dir == '':
            dir = os.getcwd()
        dir_list = []
        for f in sorted(os.listdir(str(dir)), key=str.lower):
            ff = os.path.join(dir, f)
            if os.path.isdir(ff):
                dir_list.insert(0, {'title': f, 'path': ff, 'load': False, 'children': [{'title': 'Loading...'}]})
            elif not onlyDirs:
                if not filterFiles or os.path.isfile(ff) and ff.endswith(filterFiles):
                    dir_list.append({'title': f, 'path': ff})
        return dir_list


logging.info("Initialising HNN UI")
hnn_geppetto = HNNGeppetto()
logging.info("HNN UI initialised")
