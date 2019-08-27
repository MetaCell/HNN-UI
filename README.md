[![Build Status](https://travis-ci.org/MetaCell/nwb-explorer.svg?branch=development)](https://travis-ci.org/MetaCell/HNN-UI)
[![Twitter Follow](https://img.shields.io/twitter/follow/metacell.svg?label=follow&style=social)](https://twitter.com/metacell)


# HNN Web User Interface

This repository hosts the web-based user interface for [HNN](https://hnn.brown.edu/). HNN is a user-friendly software tool that gives researchers and clinicians the ability to test and develop hypotheses on the circuit mechanism underlying their EEG/MEG data in an easy-to-use environment.
<p align="center">
    <img src="https://hnn.brown.edu/wp-content/uploads/2018/05/mainlogo3.png" height="80"/>
</p>

![](https://raw.githubusercontent.com/MetaCell/HNN-UI/development/docs/wiki6.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

Have a look in the [documentation](https://github.com/MetaCell/HNN-UI/wiki) for notes on how to use the interface.

### Prerequisites 
Before we start make sure you have 
[NEURON installed](https://github.com/MetaCell/NetPyNE-UI/wiki/Installing-NEURON-(version-7.6.2-with-crxd)) in a new python3 virtual environment.

```bash
python3 -m venv new_venv_folder
source new_venv_folder/bin/activate
```

## Install HNN User Interface from sources (for developers)
Step by step instructions to get a development environment running.

First, clone HNN-UI:
```
git clone https://github.com/MetaCell/HNN-UI
```
Second, activate your virtual environment:
```
source new_venv_folder/bin/activate
```
Then run the installation script:
```
cd HNN-UI/utilities
python install.py
```

## How to run

After the installation has completed, run the script:
```bash
cd ..
./HNN-UI
```
If everything worked, the default browser will open on http://localhost:8888/geppetto

### Run with docker
To pull the [docker container](https://hub.docker.com/r/metacell/hnn-ui):
```bash
docker pull metacell/hnn-ui:release 
```
To run the docker container:
```bash
docker run -it -p 8888:8888 metacell/hnn-ui
```
