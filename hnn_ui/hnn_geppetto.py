"""
hnn_geppetto.py
Initialise HNN Geppetto, this class contains methods to connect HNN with the Geppetto based UI
"""
import importlib
import io
import json
import logging
import os
import re
import sys
import hnn_ui.holoviews_plots as holoviews_plots

import jsonpickle
from jupyter_geppetto import jupyter_geppetto, synchronization, utils
from netpyne import sim
from pygeppetto.model.model_serializer import GeppettoModelSerializer

import hnn_ui.model_utils as model_utils
from hnn_ui.cellParams import set_cellParams
from hnn_ui.constants import CANVAS_KEYS, PROXIMAL, DISTAL
from hnn_ui.netParams import set_netParams
from hnn_ui.netpyne_model_interpreter import NetPyNEModelInterpreter
from hnn_ui.utils import set_cfg_from_params, set_cfg_from_file


class HNNGeppetto:

    def __init__(self):
        """

        Initializes HNN Geppetto
        Loads initial cfg
        Loads initial .param file
        Gets all the evoked information
        Loads initial experimental data
        Takes snapshot
        Starts synchronization on cfg

        """
        self.model_interpreter = NetPyNEModelInterpreter()
        # loads the param file on top of the cfg contained in cfg.py
        self.cfg = set_cfg_from_file('load_examples/ERPYes100Trials.param', self.load_cfg())
        self.evoked_dict = self.get_evoked_dict(self.cfg)
        self.experimental_data = self.load_experimental_from_file()
        # use to decide whether or not to update the canvas in the front end
        self.last_cfg_snapshot = self.cfg.__dict__.copy()
        synchronization.startSynchronization(self.__dict__)
        logging.debug("Initializing the original model")

        jupyter_geppetto.context = {'hnn_geppetto': self}

    def getData(self):
        """

        Gets the information needed to display the UI correctly

        Returns
        -------
        dict
            metadata
            isDocker
            currentFolder

        """
        return {
            "metadata": model_utils.load_metadata("hnn_ui/metadata"),
            "isDocker": os.path.isfile('/.dockerenv'),
            "currentFolder": os.getcwd()
        }

    def load_cfg(self):
        """

        Creates a cfg SimConfig from cfg.py file

        Returns
        -------
        SimConfg
            cfg SimConfig

        """
        cfg_module = importlib.import_module("hnn_ui.cfg")
        cfg = getattr(cfg_module, "cfg")
        return cfg

    def load_cfg_from_json(self, file):
        """

        Creates a cfg SimConfig from .json file

        Parameters
        ----------
        file : json object of bytes
            bytes of a .json file wrapped in json

        """
        file_list = json.loads(file)
        file_bytes = bytes(file_list)
        self.cfg = jsonpickle.decode(json.loads(file_bytes.decode('utf-8')))
        self.evoked_dict = self.get_evoked_dict(self.cfg)

    def load_cfg_from_param(self, file):
        """

        Creates a cfg SimConfig from .param file

        Parameters
        ----------
        file : json object of bytes
            bytes of a .param file wrapped in json

        """
        file_list = json.loads(file)
        file_bytes = bytes(file_list)
        self.cfg = set_cfg_from_params(file_bytes, self.cfg)
        self.evoked_dict = self.get_evoked_dict(self.cfg)

    def load_experimental_from_file(self):
        """

        Creates an initial experimental data dict from .txt file

        Parameters
        ----------

        Returns
        -------
        dict
            experimental data dict

        """
        d = {'x': [], 'y': [], 'label': 'Experiment'}
        with open("load_examples/hnn_test.txt") as f:
            for line in f:
                x, y = line.split()
                d['x'].append(float(x))
                d['y'].append(float(y))
        return d

    def load_experimental(self, file):
        """

        Creates an experimental data dict from .txt file

        Parameters
        ----------
        file : json object of bytes
            bytes of a .txt file wrapped in json

        Returns
        -------
        dict
            experimental data dict

        """
        file_list = json.loads(file)
        file_bytes = bytes(file_list)
        d = {'x': [], 'y': [], 'label': 'Experiment'}
        with io.BytesIO(file_bytes) as fp:
            ln = fp.readlines()
            for l in ln:
                x, y = l.split()
                d['x'].append(float(x.decode("utf-8")))
                d['y'].append(float(y.decode("utf-8")))
        self.experimental_data = d

    def save_model(self):
        """

        Serializes the cfg SimConfig to JSON

        Returns
        -------
        JSON
            serialized cfg SimConfig

        """
        return jsonpickle.encode(self.cfg)

    def instantiateModelInGeppetto(self):
        """

        Instantiates model in geppetto
        Runs simulation

        Returns
        -------
        JSON
            serialized geppetto model

        """
        try:
            netpyne_model = self.instantiateModel()
            self.geppetto_model = self.model_interpreter.getGeppettoModel(netpyne_model)
            logging.debug('Running single thread simulation')
            self.simulateModel()

            return json.loads(GeppettoModelSerializer().serialize(self.geppetto_model))
        except:
            return utils.getJSONError("Error while instantiating the NetPyNE model", sys.exc_info())

    def instantiateModel(self):
        """

        Instantiates model
        Sets netParams and cellParams given cfg values
        Takes snapshot of cfg

        Returns
        -------
        SimConfig
            generated SimConfig

        """
        netParams_snapshot = set_netParams(self.cfg)
        netParams_snapshot.cellParams = set_cellParams(self.cfg)
        sim.create(simConfig=self.cfg, netParams=netParams_snapshot)
        sim.gatherData(gatherLFP=False)
        self.last_cfg_snapshot = self.cfg.__dict__.copy()
        return sim


    def getModelInGeppetto(self):
        """

        Gets model in geppetto

        Returns
        -------
        JSON
            serialized geppetto model

        """
        return json.loads(GeppettoModelSerializer().serialize(self.geppetto_model))

    def simulateModel(self):
        """

        Simulates model

        Returns
        -------
        SimConfig
            generated SimConfig

        """
        sim.setupRecording()
        sim.simulate()
        sim.saveData()
        return sim

    @staticmethod
    def get_evoked_dict_aux(str_, word):
        """

        Returns both the evoked key and inner key from cfg an attribute:
        Assumes @word with the following format: {inner_key-begin}{str_}_id{inner_key-end}

        Parameters
        ----------
        str_ : str
            evdist_ or evprost_
        word : str
            cfg attribute

        Returns
        -------
        str, str
            given f.e. evdist_, gbar_evdist_1_L2Basket_ampa
            returns evdist_1, gbar_L2Basket_ampa

        """
        if str_ in word:
            ev_index = word.index(str_)
            len_str = len(str_)
            ev_id = re.findall(r'(?<=_)\d+', word)[0]
            key = str_ + ev_id
            inner_key = word[0:ev_index - 1] + word[ev_index + len_str + 1:]
            return key, inner_key

    def get_evoked_dict(self, cfg):
        """

        Creates a dictionary of evoked inputs

        Parameters
        ----------
        cfg : dict
            the cfg SimConfig

        Returns
        -------
        dict
            Returns a dictionary of evoked inputs as follow:
                evdist_1:
                    gbar_L2Basket_ampa: 0.001229
                    gbar_L2Basket_nmda: 0.002043
                evprox_1:
                    gbar_L2Basket_ampa: 0.001229
                    gbar_L2Basket_nmda: 0.002043
        """

        cfg_dict = {}
        for att in dir(cfg):
            if "evprox_" in att:
                key, inner_key = self.get_evoked_dict_aux("evprox_", att)
                if key in cfg_dict.keys():
                    cfg_dict[key][inner_key] = getattr(cfg, att)
                else:
                    cfg_dict[key] = {inner_key: getattr(cfg, att)}
            elif "evdist_" in att:
                key, inner_key = self.get_evoked_dict_aux("evdist_", att)
                if key in cfg_dict.keys():
                    cfg_dict[key][inner_key] = getattr(cfg, att)
                else:
                    cfg_dict[key] = {inner_key: getattr(cfg, att)}

        return self.filter_evoked_dict(cfg_dict)

    def filter_evoked_dict(self, cfg_dict):
        """

        Returns a dictionary of valid evoked inputs

        Parameters
        ----------
        cfg_dict : dict
            the cfg_dict dictionary

        Returns
        -------
        dict
            Returns a dictionary of valid evoked inputs as follow:
                evdist_1:
                    gbar_L2Basket_ampa: 0.001229
                    gbar_L2Basket_nmda: 0.002043
                evprox_1:
                    gbar_L2Basket_ampa: 0.001229
                    gbar_L2Basket_nmda: 0.002043
        """
        keys_to_delete = []
        for ev_input in cfg_dict:
            if 'evdist' in ev_input:
                if bool(DISTAL.keys() - cfg_dict[ev_input].keys()):
                    keys_to_delete.append(ev_input)
            elif 'evprox' in ev_input:
                if bool(PROXIMAL.keys() - cfg_dict[ev_input].keys()):
                    keys_to_delete.append(ev_input)

        for key in keys_to_delete:
            del cfg_dict[key]

        return cfg_dict

    def getEvokedInputs(self):

        """

        Creates a list of all the evoked inputs present in evoked_dict.
        Used for display purposes only

        Returns
        -------
        list
            list of all the evoked inputs present in evoked_dict

        """
        return list(self.evoked_dict.keys())

    def addEvokedInput(self, input_type):
        """

        Adds an evoked input both to flat and dict representations.

        Parameters
        ----------
        input_type : str
            distal or proximal

        Returns
        -------
        dict
            { list of evoked inputs, added input as selected input }

        """
        evoked_indices = [int(key[key.index("_") + 1:]) for key in self.evoked_dict.keys() if input_type in key]
        index = str(max(evoked_indices) + 1) if len(evoked_indices) > 0 else 1
        dict_attributes = DISTAL if input_type == "distal" else PROXIMAL
        key = f"{input_type}_{index}"
        self.evoked_dict[key] = dict_attributes
        self.add_to_cfg(key, dict_attributes)
        return {'inputs': self.getEvokedInputs(), 'selected_input': f'{input_type}_{index}'}

    def add_to_cfg(self, key, attributes):
        """

        Adds to cfg dictionary the evoked input following naming conventions.

        Parameters
        ----------
        key : str
            evprox or evdist + _index
        attributes : dict
            cfg attributes associated with key

        """
        for att in attributes:
            if 'gbar' in att:
                setattr(self.cfg, 'gbar_' + key + att.replace('gbar', ''), attributes[att])
            else:
                setattr(self.cfg, att + '_' + key, attributes[att])

    def removeEvokedInput(self, key):
        """

        Removes an evoked input both from flat and dict representations.

        Parameters
        ----------
        key : str
            evprox or evdist + _index

        Returns
        -------
        list
            list of all the evoked inputs present in evoked_dict

        """
        del self.evoked_dict[key]
        self.delete_from_cfg(key)
        return self.getEvokedInputs()

    def delete_from_cfg(self, key):
        """

        Removes from cfg flat representation all the entries related to the evoked input

        Parameters
        ----------
        key : str
            evprox or evdist + _index

        """
        to_del = []
        for item in self.cfg.__dict__.items():
            att = item[0]
            if key in att:
                to_del.append(att)
        for att in to_del:
            delattr(self.cfg, att)

    def compare_cfg_to_last_snapshot(self):
        """

        Checks if an update is required.

        Returns
        -------
        dict
            dict with boolean information about the need of an update for each of the attributes (canvas and simulation)

        """
        return {
            "canvasUpdateRequired": self._is_canvas_update_required(),
            "simulationUpdateRequired": self._have_params_changed()
        }

    def _is_canvas_update_required(self):
        """

        Checks if an update is required for canvas
        Attributes that affect canvas are stored in CANVAS_KEYS

        Returns
        -------
        bool
            boolean information about the need of an update for canvas

        """
        for key in self.cfg.__dict__:
            for end in CANVAS_KEYS:
                if key.endswith(end) and getattr(self.cfg, key) != self.last_cfg_snapshot[key]:
                    return True
        return False

    def _have_params_changed(self):
        """

        Checks if an update is required for simulation
        by comparing snapshots

        Returns
        -------
        bool
            boolean information about the need of an update for simulation

        """
        for key in self.cfg.__dict__:
            if getattr(self.cfg, key) != self.last_cfg_snapshot[key]:
                return True
        return False

    def get_dipole_plot(self):
        """

        Gets the html with the dipole plot given the simulation values and experimental data
        or only the experimental data on failure (typically due to lack of simulation data)

        Returns
        -------
        html str
            html str with the dipole plot and/or experimental data plot

        """
        plot_html = sim.analysis.iplotDipole(self.experimental_data)
        if plot_html != -1:
            return plot_html
        return holoviews_plots.get_experimental_plot(self.experimental_data)

    def get_traces_plot(self):
        """

        Gets the html with the traces plot given the simulation values

        Returns
        -------
        html str
            html str with the traces plot

        """
        plot_html = sim.analysis.iplotTraces(**self.cfg.analysis['iplotTraces'])
        if plot_html != -1:
            return plot_html
        return ""

    def get_psd_plot(self):
        """

        Gets the html with the psd plot given the simulation values

        Returns
        -------
        html str
            html str with the psd plot

        """
        plot_html = sim.analysis.iplotRatePSD(**self.cfg.analysis['iplotRatePSD'])
        if plot_html != -1:
            return plot_html
        return ""

    def get_raster_plot(self):
        """

        Gets the html with the raster plot given the simulation values

        Returns
        -------
        html str
            html str with the raster plot

        """
        plot_html = sim.analysis.iplotRaster(**self.cfg.analysis['iplotRaster'])
        if plot_html != -1:
            return plot_html
        return ""

    def get_spectrogram_plot(self):
        """

        Gets the html with the spectrogram plot given the simulation values

        Returns
        -------
        html str
            html str with the spectrogram plot

        """
        plot_html = sim.analysis.iplotLFP(plots=['spectrogram'])
        if plot_html != -1:
            return plot_html
        return ""

    def get_spikehistogram_plot(self):
        """

        Gets the html with the spike histogram plot given the simulation values

        Returns
        -------
        html str
            html str with the spike histogram plot

        """
        plot_html = sim.analysis.iplotSpikeHist(**self.cfg.analysis['iplotSpikeHist'])
        if plot_html != -1:
            return plot_html
        return ""

    def getDirList(self, dir=None, onlyDirs=False, filterFiles=""):
        """

        Deprecated
        Lists information about the files in the current directory

        Parameters
        ----------
        dir : str
            Directory to iterate over
        onlyDirs : bool
            Show only directories
        filterFiles : str
            Accepted extensions

        Returns
        -------
        list
            Lists information about the files in the current directory

        """
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

