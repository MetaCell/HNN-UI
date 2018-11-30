# The purpose of this Dockerfile is to serve as skeleton for a future production version.
# Therefore currently it is NOT functional

FROM metacell/jupyter-neuron:latest
USER $NB_USER

ARG hnnuiBranch=development
ENV hnnuiBranch=${hnnuiBranch}
RUN echo "$hnnuiBranch";

ARG INCUBATOR_VER=unknown
RUN /bin/bash -c "INCUBATOR_VER=${INCUBATOR_VER} source activate snakes && pip install netpyne_ui"
RUN /bin/bash -c "source activate snakes && jupyter nbextension enable --py jupyter_geppetto"
RUN /bin/bash -c "source activate snakes &&  jupyter serverextension enable --py jupyter_geppetto"
RUN /bin/bash -c "source activate snakes && jupyter nbextension enable --py widgetsnbextension"

WORKDIR /home/jovyan/work
RUN wget https://github.com/MetaCell/HNN-UI/archive/$hnnuiBranch.zip -q
RUN unzip $hnnuiBranch.zip
WORKDIR /home/jovyan/work/HNN-UI-$hnnuiBranch/utilities
CMD /bin/bash -c "exec jupyter notebook --NotebookApp.default_url=/geppetto --NotebookApp.token='' --library=hnn_ui"