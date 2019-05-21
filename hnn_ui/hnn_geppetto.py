"""
hnn_geppetto.py
Initialise HNN Geppetto, this class contains methods to connect HNN with the Geppetto based UI
"""
import copy
import importlib
import io
import json
import logging
import os
import re
import sys
from contextlib import redirect_stdout
import hnn_ui.holoviews_plots as holoviews_plots

import jsonpickle
from jupyter_geppetto import jupyter_geppetto, synchronization, utils
from netpyne import sim
from netpyne import specs
from pygeppetto.model.model_serializer import GeppettoModelSerializer

import hnn_ui.model_utils as model_utils
from hnn_ui.cellParams import set_cellParams
from hnn_ui.constants import CANVAS_KEYS, PROXIMAL, DISTAL
from hnn_ui.netParams import set_netParams
from hnn_ui.netpyne_model_interpreter import NetPyNEModelInterpreter
from hnn_ui.utils import set_cfg_from_params


class HNNGeppetto:

    def __init__(self):
        self.model_interpreter = NetPyNEModelInterpreter()
        self.cfg = self.load_cfg()
        self.load_cfg_from_param_debug("load_examples/ERPYes100Trials.param")
        self.experimental_data = self.load_experimental_from_file()
        # use to decide whether or not to update the canvas in the front end
        self.last_cfg_snapshot = self.cfg.__dict__.copy()
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
        cfg = getattr(cfg_module, "cfg")
        return self.get_evoked_dict(cfg)

    def load_cfg_from_json(self, file):
        file_list = json.loads(file)
        file_bytes = bytes(file_list)
        cfg = jsonpickle.decode(json.loads(file_bytes.decode('utf-8')))
        self.cfg = self.get_evoked_dict(cfg)

    def load_cfg_from_param(self, file):
        file_list = json.loads(file)
        file_bytes = bytes(file_list)
        cfg = set_cfg_from_params(file_bytes, self.cfg)
        self.cfg = self.get_evoked_dict(cfg)

    def load_cfg_from_param_debug(self, file):
        fh = open(file, 'rb')
        file_bytes = bytearray(fh.read())
        cfg = set_cfg_from_params(file_bytes, self.cfg)
        self.cfg = self.get_evoked_dict(cfg)


    def load_experimental_from_file(self):
        d = {'x': [], 'y': [], 'label': 'Experiment'}
        with open("load_examples/hnn_test.txt") as f:
            for line in f:
                x, y = line.split()
                d['x'].append(float(x))
                d['y'].append(float(y))
        return d

    def load_experimental(self, file):
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

    def dict_to_flat(self):
        flat_cfg = copy.copy(self.cfg)
        for evk in flat_cfg.evoked:
            for key in flat_cfg.evoked[evk]:
                if 'gbar' in key:
                    setattr(flat_cfg, 'gbar_' + evk + key.replace('gbar', ''), self.cfg.evoked[evk][key])
                else:
                    setattr(flat_cfg, key + '_' + evk, self.cfg.evoked[evk][key])
        delattr(flat_cfg, 'evoked')
        return flat_cfg

    def save_model(self):
        flat_cfg = self.dict_to_flat()
        return jsonpickle.encode(flat_cfg)

    def instantiateModelInGeppetto(self):
        try:
            with redirect_stdout(sys.__stdout__):
                netpyne_model = self.instantiateModel()
                self.geppetto_model = self.model_interpreter.getGeppettoModel(netpyne_model)
                logging.debug('Running single thread simulation')
                self.simulateModel()

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

    def simulateModel(self):
        with redirect_stdout(sys.__stdout__):
            sim.setupRecording()
            sim.simulate()
            sim.saveData()
        return sim

    @staticmethod
    def get_evoked_dict_aux(str_, word):
        if str_ in word:
            ev_index = word.index(str_)
            len_str = len(str_)
            ev_id = re.findall(r'(?<=_)\d+', word)[0]
            key = str_ + ev_id
            inner_key = word[0:ev_index - 1] + word[ev_index + len_str + 1:]
            return key, inner_key

    def get_evoked_dict(self, cfg):
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

        setattr(cfg, "evoked", cfg_dict)
        return cfg

    def getEvokedInputs(self):
        return list(self.cfg.evoked.keys())

    def addEvokedInput(self, input_type):
        evoked_indices = [int(key[key.index("_") + 1:]) for key in self.cfg.evoked.keys() if input_type in key]
        index = str(max(evoked_indices) + 1) if len(evoked_indices) > 0 else 1
        self.cfg.evoked[f"{input_type}_{index}"] = DISTAL if input_type == "distal" else PROXIMAL
        return {'inputs': self.getEvokedInputs(), 'selected_input': f'{input_type}_{index}'}

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

    def get_dipole_plot(self):
        plot_html = sim.analysis.iplotDipole(self.experimental_data)
        if plot_html != -1:
            return plot_html
        return holoviews_plots.get_experimental_plot(self.experimental_data)

    def get_traces_plot(self):
        plot_html = sim.analysis.iplotTraces()
        if plot_html != -1:
            return plot_html
        return ""

    def get_psd_plot(self):
        plot_html = sim.analysis.iplotRatePSD()
        if plot_html != -1:
            return plot_html
        return ""

    def get_raster_plot(self):
        plot_html = sim.analysis.iplotRaster()
        if plot_html != -1:
            return plot_html
        return ""

    def get_spectrogram_plot(self):
        plot_html = sim.analysis.iplotLFP(plots=['spectrogram'])
        if plot_html != -1:
            return plot_html
        return ""

    def get_spikehistogram_plot(self):
        plot_html = sim.analysis.iplotSpikeHist()
        if plot_html != -1:
            return plot_html
        return ""

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


