"""
hnn_geppetto.py
Initialise HNN Geppetto, this class contains methods to connect HNN with the Geppetto based UI
"""
import os
import sys
import json
import logging
import importlib

from pygeppetto import ui
from netpyne import specs, sim, analysis
from hnn_ui.netpyne_model_interpreter import NetPyNEModelInterpreter
from pygeppetto.model.model_serializer import GeppettoModelSerializer
from jupyter_geppetto import jupyter_geppetto, synchronization, utils

import hnn_ui.cfg as cfg
import hnn_ui.model_utils as model_utils
from contextlib import redirect_stdout, redirect_stderr

from hnn_ui.netParams import set_netParams
from hnn_ui.cellParams import set_cellParams

from hnn_ui.constants import CANVAS_KEYS, PROXIMAL, DISTAL

class HNNGeppetto():

    def __init__(self):
        self.model_interpreter = NetPyNEModelInterpreter()
        self.cfg = self.load_cfg()
        # use to decide wheter or not to update the canvas in the front end
        self.last_cfg_snapshot = self.cfg.__dict__.copy()
        synchronization.startSynchronization(self.__dict__)
        logging.debug("Initializing the original model")

        jupyter_geppetto.context = { 'hnn_geppetto': self }

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
            netParams_snapshot = set_netParams(self.cfg)
            netParams_snapshot.cellParams = set_cellParams(self.cfg)
            sim.create(simConfig=self.cfg, netParams=netParams_snapshot)
            sim.gatherData(gatherLFP=False)
            self.last_cfg_snapshot = self.cfg.__dict__.copy()

        return sim

    def getEvokedInputs(self):
        return list(self.cfg.evoked.keys())

    # waiting for evoked input model (this is tentative)
    def addEvokedInput(self, input_type):
        evoked_indices = [int(key[key.index("_")+1:]) for key in self.cfg.evoked.keys() if input_type in key]
        index = str(max(evoked_indices) + 1) if len(evoked_indices) > 0 else 1
        self.cfg.evoked[f"{input_type}_{index}"] = DISTAL if input_type=="distal" else PROXIMAL
        return { 'inputs': self.getEvokedInputs(), 'selected_input': f'{input_type}_{index}' }
    
    def removeEvokedInput(self, name):
        del self.cfg.evoked[name]
        return self.getEvokedInputs()

    def compare_cfg_to_last_snapshot(self):
        return {
            "canvasUpdateRequired": self._is_canvas_update_required(),
            "simulationUpdateRequired": self._have_params_changed()
        }

    def _is_canvas_update_required(self):
        for key in self.cfg.__dict__:
            for end in CANVAS_KEYS:
                if key.endswith(end) and getattr(self.cfg, key) != self.last_cfg_snapshot[key]:
                    return True
        return False

    def _have_params_changed(self):
        for key in self.cfg.__dict__:
            if getattr(self.cfg, key) != self.last_cfg_snapshot[key]:
                return True
        return False

logging.info("Initialising HNN UI")
hnn_geppetto = HNNGeppetto()
logging.info("HNN UI initialised")