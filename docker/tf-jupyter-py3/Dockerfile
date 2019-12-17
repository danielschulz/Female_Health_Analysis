FROM jupyter/tensorflow-notebook
MAINTAINER "Daniel Schulz"

USER 0:0
RUN apt-get update && \
    apt-get install -qq -y curl time sed gcc dkms make cmake bzip2 perl git zip unzip nano bcrypt nmap wget \
    python-setuptools python-jpype iputils-ping netcat htop socat sed r-base

RUN R -e "install.packages(c('methods', 'jsonlite', 'tseries', 'packrat', 'devtools', \
                             'dbscan', 'cluster', 'Holidays', 'forecast', 'VCA', 'svd', 'PCAmixdata', 'stats', \
                             'auto.pca', 'HMM', 'seqHMM', 'xgboost', 'randomForest', 'sparklyr', \
                             'nycflights13', 'Lahman', 'IRkernel', \
                             'tidyverse', 'mangoTraining', 'broom', 'cli', 'crayon', 'dplyr', 'dbplyr', 'forcats', \
                             'ggplot2', 'haven', 'hms', 'httr', 'jsonlite', 'lubridate', 'magrittr', 'modelr', \
                             'purrr', 'readr', 'readxl', 'reprex', 'rlang', 'rstudioapi', 'rvest', 'stringr', \
                             'tibble', 'tidyr', 'xml2', 'backports', 'generics', 'nlme', 'reshape2', 'assertthat', \
                             'DBI', 'glue', 'R6', 'tidyselect', 'pkgconfig', 'Rcpp', 'ellipsis', 'digest', 'gtable', \
                             'lazyeval', 'MASS', 'mgcv', 'plyr', 'scales', 'viridisLite', 'withr', 'curl', 'mime', \
                             'openssl', 'clipr', 'cellranger', 'callr', 'fs', 'markdown', 'whisker', 'selectr', \
                             'stringi', 'fansi', 'pillar', 'processx', 'rematch', 'Matrix', 'lattice', 'askpass', \
                             'utf8', 'knitr', 'yaml', 'htmltools', 'evaluate', 'base64enc', 'tinytex', 'labeling', \
                             'munsell', 'RColorBrewer', 'sys', 'highr', 'markdown', 'xfun', 'colorspace', 'ps'), \
                           dependencies=TRUE, \
                           repos='http://cran.rstudio.com/')"

ARG ACC_GROUP_NAME=datascientists
ARG ACC_GROUP_GID=1024
ARG ACC_USER_NAME=datascientist
ARG ACC_USER_UID=1024
ARG ACC_USER_PASSWORD=password

RUN groupadd -g ${ACC_GROUP_GID} ${ACC_GROUP_NAME} && \
    useradd -g ${ACC_GROUP_NAME} -G ${NB_GID} -u ${ACC_USER_UID} ${ACC_USER_NAME} \
        -m -d /home/${ACC_USER_NAME} -s /bin/bash && \
    sed -i "s|^root\s*ALL=(ALL)\s*ALL$|root ALL=(ALL) ALL \n${ACC_USER_NAME} ALL=(ALL) ALL|g" /etc/sudoers && \
    echo "${ACC_USER_NAME}:${ACC_USER_PASSWORD}" | chpasswd

ARG NB_UID=${ACC_USER_UID}
ARG NB_USER=${ACC_GROUP_NAME}
ARG NB_GID=${ACC_GROUP_GID}

RUN mkdir -p /apps/data /apps/sw/jdbc/oracle/12c /apps/tmp && \
    chmod 775 -R /apps && \
    chmod 755 -R /apps/sw && \
    chmod 777 -R /home/jovyan /apps/tmp && \
    chmod 700 -R ${HOME} && \
    chown ${ACC_USER_UID}:${ACC_GROUP_GID} -R /apps /home/jovyan ${CONDA_DIR} && \
    fix-permissions ${CONDA_DIR} && \
    fix-permissions /home/${ACC_USER_NAME}

COPY srcs/oracle12c/ojdbc7.jar /apps/sw/jdbc/oracle/12c/

RUN chmod 755 -R /apps/sw && \
    chown ${ACC_USER_UID}:${ACC_GROUP_GID} -R /apps/sw

USER ${ACC_USER_UID}:${ACC_GROUP_GID}

ARG NOTEBOOK_DIR=/apps/data
ENV NOTEBOOK_DIR=/apps/data

ARG TFP_WHEEL_URI="https://files.pythonhosted.org/packages/4e/93/191e42ca27786d6875f74e7b756e34ef42f385f6d250bfc28aa48a1d1072/tensorflow_probability-0.6.0-py2.py3-none-any.whl"

ARG MYSQL_CONNECTOR_VERSION="2.2.9"
ARG MYSQL_CONNECTOR_C_VERSION="8.0.13"

RUN ls -alsh /opt/conda && \
    conda install anaconda conda conda-build && \
    conda update -q -y -n root anaconda conda conda-build && \
    conda update -q -y -n base anaconda conda conda-build && \
    conda create -n ds python=3.6.7 anaconda conda conda-build && \
    activate ds && \
    conda info --envs && \
    conda update -q -y -n ds anaconda conda conda-build && \
    conda list -n ds > /apps/tmp/ds-00-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all


# env: DS
RUN conda info --envs && \
    conda init bash && \
    /opt/conda/envs/ds/bin/pip install --user pycallgraph && \
    conda install -q -y -n ds -c conda-forge xgboost scikit-optimize cpu_features lz4-c urllib3 && \
    conda install -q -y -n ds -c anaconda accelerate && \
    conda list -n ds > /apps/tmp/ds-01-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all && \
    cd ${NOTEBOOK_DIR}

# env: DS
RUN conda info --envs && \
    conda install -q -y -n ds -c conda-forge pip && \
    /opt/conda/envs/ds/bin/pip install --user --upgrade pip && \
    /opt/conda/envs/ds/bin/pip install --user mysql-connector==${MYSQL_CONNECTOR_VERSION} PyMySQLdb cowsay fortune \
        shap pgmpy pathlib scipy researchpy statsmodels hdbscan && \
    conda list -n ds > /apps/tmp/ds-02-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all

# env: DS
ARG TFP_VERSION_PIP="0.8.0"
ARG TFDS_VERSION="1.2.0"

RUN conda info --envs && \
    /opt/conda/envs/ds/bin/pip install --user pyfiglet sklearn-pandas && \
    conda install -q -y -n ds -c conda-forge mkl-service cudatoolkit cudnn h5py && \
    conda install -q -y -n ds -c r r-essentials && \
    conda install -q -y -n ds -c conda-forge fastparquet pyarrow dask python-graphviz pip seaborn bokeh \
        pydot pydotplus pyyaml ipython-sql nbstripout matplotlib pyarrow hmmlearn xgboost category_encoders \
        pyarrow arrow-cpp parquet-cpp ipython-sql holidays sqlalchemy jaydebeapi pymssql \
        pymc3 pandas scikit-learn pathlib2 && \
    /opt/conda/envs/ds/bin/pip install --user tensorflow-probability==${TFP_VERSION_PIP} \
        tensorflow-datasets==${TFDS_VERSION} && \
    /opt/conda/envs/ds/bin/pip install --user pyro-ppl edward && \
    conda list -n ds > /apps/tmp/ds-03-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all

# env: DS
# CPU vs GPU vs TPU
ARG COMPUTE_ARCH=CPU
ARG TF_VERSION="2.0.0"
# "2.0.0-alpha0"

RUN conda install -q -y -n ds -c anaconda tensorflow=${TF_VERSION} perf protobuf libprotobuf && \
    conda list -n ds > /apps/tmp/ds-04-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all


# env: DB
ARG TFP_VERSION_CONDA="0.8.0"

RUN conda info --envs && \
    conda create -n db python=3.6.7 anaconda conda conda-build && \
    conda list -n db > /apps/tmp/db-00-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all && \
    /opt/conda/envs/db/bin/pip install --user tensorflow-probability==${TFP_VERSION_PIP} \
        tensorflow-datasets==${TFDS_VERSION} && \
    conda install -q -y -n db -c anaconda mysql-connector-python=${MYSQL_CONNECTOR_C_VERSION} \
        tensorflow=${TF_VERSION} && \
    conda install -q -y -n db -c conda-forge tensorflow-probability=${TFP_VERSION_CONDA} keras \
        ipython-sql ipython-sql holidays sqlalchemy jaydebeapi pymssql && \
    conda list -n db > /apps/tmp/db-01-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all


# env: DS
RUN conda info --envs && \
    conda info --envs && \
    conda install -q -y -n ds -c conda-forge tensorflow-probability=${TFP_VERSION_CONDA} && \
    conda install -q -y -n ds -c conda-forge keras pyro4 protobuf libprotobuf thrift-cpp thrift thriftpy && \
    conda list -n ds > /apps/tmp/ds-05-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all

# env: DS
RUN conda info --envs && \
    mkdir -p /apps/tmp/git && \
    cd /apps/tmp/git && \
    /opt/conda/envs/ds/bin/pip install --user ${TFP_WHEEL_URI} && \
    /opt/conda/envs/ds/bin/pip install --user --upgrade git+https://github.com/jpmml/sklearn2pmml.git && \
    /opt/conda/envs/ds/bin/pip install --user git+https://github.com/thu-ml/zhusuan && \
    git clone --single-branch --branch master https://github.com/wmyw96/ZhuSuan.git && \
    /opt/conda/envs/ds/bin/pip install --user /apps/tmp/git/ZhuSuan && \
    git clone --single-branch --branch dev https://github.com/pgmpy/pgmpy.git && \
    /opt/conda/envs/ds/bin/pip install --user -r /apps/tmp/git/pgmpy/requirements.txt && \
    /opt/conda/envs/ds/bin/python /apps/tmp/git/pgmpy/setup.py install && \
    conda list -n db > /apps/tmp/db-02-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all && \
    cd ${NOTEBOOK_DIR}


ARG TFHUB_VERSION_CONDA="0.7.0"

# env: DS
RUN conda info --envs && \
    conda install -q -y -n ds -c sbu-hpc glove && \
    conda install -q -y -n ds -c dimazest stanford-corenlp-python && \
    /opt/conda/envs/ds/bin/pip install --user stanford-corenlp && \
    /opt/conda/envs/ds/bin/pip install --user glove_python && \
    conda install -q -y -n ds -c bioconda pomegranate && \
    conda install -q -y -n ds -c omnia hmmlearn && \
    conda install -q -y -n ds -c jaikumarm hyperopt && \
    conda install -q -y -n ds -c anaconda mkl pymc3 nltk && \
    conda install -q -y -n ds -c conda-forge nb_conda_kernels shap fasttext gensim cassandra-driver pyspark \
        scikit-optimize tensorflow-probability=${TFP_VERSION_CONDA} tensorflow-hub=${TFHUB_VERSION_CONDA} && \
    conda install -q -y -n root -c conda-forge nb_conda_kernels && \
    conda install -q -y -n base -c conda-forge nb_conda_kernels && \
    conda install -q -y -c conda-forge nb_conda_kernels && \
    python -m ipykernel install --user --name db --display-name "Databases (db)" && \
    python -m ipykernel install --user --name ds --display-name "Data Science (ds)" && \
    conda list -n db > /apps/tmp/db-03-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all && \
    conda list -n ds > /apps/tmp/ds-06-$( date -u +%Y%m%d_%H%M ).txt && conda info --envs && conda build purge-all && \
    cd ${NOTEBOOK_DIR}

USER ${ACC_GROUP_NAME}

COPY ./srcs/nltk-download-any.py /apps/tmp/

# RUN chmod 775 /apps/tmp/nltk-download-any.py && \
#     chown ${ACC_USER_UID}:${ACC_GROUP_GID} /apps/tmp/nltk-download-any.py && \
#     source /home/jovyan/.bashrc && \
#     source /home/datascientist/.bashrc && \
#     conda activate ds && \
#    /opt/conda/envs/ds/bin/python3.6 /apps/tmp/nltk-download-any.py

ARG NB_UID=${ACC_USER_UID}
ARG NB_USER=${ACC_GROUP_NAME}
ARG NB_GID=${ACC_GROUP_GID}

ENV CLASSPATH=/apps/sw/jdbc/oracle/12c/ojdbc7.jar

WORKDIR ${NOTEBOOK_DIR}

EXPOSE 8888
