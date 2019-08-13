
New user interface
for `HNN <https://hnn.brown.edu/>`__ based on web
technologies.


The UI connects to
`nrnpython <http://www.neuron.yale.edu/neuron/static/docs/help/neuron/neuron/classes/python.html>`__
through a `Geppetto <http://git.geppetto.org>`__ extension for `Jupyter
Notebook <http://jupyter.org/>`__.

HNN-UI
======

User Interface for HNN.
See the `Repo <https://github.com/MetaCell/HNN-UI>`__
info!

Installation
============

.. code-block:: bash

    pip install hnn_ui
    jupyter nbextension enable --py jupyter_geppetto

Usage
=====

.. code-block:: bash

    HNN-UI

or

.. code-block:: bash

    jupyter notebook --NotebookApp.default_url=/geppetto --NotebookApp.token=''