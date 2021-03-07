FROM arm64v8/python:3.8

RUN pip install jupyterlab && jupyter-lab --generate-config

COPY ./jupyter_lab_config.py /root/.jupyter/jupyter_lab_config.py

ENTRYPOINT ["/bin/bash"]
# CMD ["jupyter-lab --allow-root"]