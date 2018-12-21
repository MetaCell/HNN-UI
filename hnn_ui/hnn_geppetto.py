"""
hnn_geppetto.py
Initialise HNN Geppetto, this class contains methods to connect HNN with the Geppetto based UI
"""
import os
import logging

from pygeppetto import ui
from netpyne import specs, sim, analysis
from hnn_ui.netpyne_model_interpreter import NetPyNEModelInterpreter
from pygeppetto.model.model_serializer import GeppettoModelSerializer
from jupyter_geppetto import jupyter_geppetto, synchronization, utils


class HNNGeppetto():

    def __init__(self):
        self.model_interpreter = NetPyNEModelInterpreter()

        self.netParams = specs.NetParams()
        self.simConfig = specs.SimConfig()
        synchronization.startSynchronization(self.__dict__)
        logging.debug("Initializing the original model")

        jupyter_geppetto.context = {'hnn_geppetto': self}

    def getData(self):
        return {"metadata": {},
                "netParams": self.netParams.todict(),
                "simConfig": self.simConfig.todict(),
                "isDocker": os.path.isfile('/.dockerenv'),
                "currentFolder": os.getcwd()
        }


logging.info("Initialising HNN UI")
hnn_geppetto = HNNGeppetto()
logging.info("HNN UI initialised")