# Taken from: https://github.com/dusty-nv/jetson-containers/blob/master/Dockerfile.tensorflow

FROM ros_base_nvidia

ENV DEBIAN_FRONTEND=noninteractive
ARG HDF5_DIR="/usr/lib/aarch64-linux-gnu/hdf5/serial/"
ARG MAKEFLAGS=-j6

RUN printenv

#
# install prerequisites - https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html#prereqs
#
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
          python3-pip \
		  python3-dev \
		  gfortran \
		  build-essential \
		  liblapack-dev \ 
		  libblas-dev \
		  libhdf5-serial-dev \
		  hdf5-tools \
		  libhdf5-dev \
		  zlib1g-dev \
		  zip \
		  libjpeg8-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install setuptools Cython wheel
RUN pip3 install numpy --verbose
RUN pip3 install h5py==2.10.0 --verbose
RUN pip3 install future==0.18.2 mock==3.0.5 h5py==2.10.0 keras_preprocessing==1.1.1 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11 --verbose

#
# TensorFlow 
#
ARG TENSORFLOW_URL=https://developer.download.nvidia.com/compute/redist/jp/v44/tensorflow/tensorflow-1.15.3+nv20.9-cp36-cp36m-linux_aarch64.whl
ARG TENSORFLOW_WHL=tensorflow-1.15.3+nv20.9-cp36-cp36m-linux_aarch64.whl

RUN wget --quiet --show-progress --progress=bar:force:noscroll --no-check-certificate ${TENSORFLOW_URL} -O ${TENSORFLOW_WHL} && \
    pip3 install ${TENSORFLOW_WHL} --verbose && \
    rm ${TENSORFLOW_WHL}

# 
# PyCUDA
#
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"
RUN echo "$PATH" && echo "$LD_LIBRARY_PATH"

RUN pip3 install pycuda six --verbose

# COPY ./autostart.sh /
# RUN chmod +x /autostart.sh
# ENTRYPOINT /autostart.sh
ENTRYPOINT /bin/bash