#!/bin/bash

# Add the chmod command to change file permissions
chmod 600 /home/jovyan/.local/share/jupyter/runtime/jpserver-7.json

# Start Jupyter Notebook
start-notebook.sh --NotebookApp.token='' --NotebookApp.password=''
