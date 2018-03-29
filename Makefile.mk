### Globals
# Project
PROFILE = default
PROJECT_NAME = immigration-sentiment
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Python
PYTHON_INTERPRETER = python3
CONDA_HOME = $(HOME)/anaconda3
CONDA_BIN_DIR = $(CONDA_HOME)/bin
CONDA = $(CONDA_BIN_DIR)/conda
CONDA_INSTALLER = miniconda_linux-x86_64.sh

# Environment
ENV_DIR = $(CONDA_HOME)/envs/$(PROJECT_NAME)
ENV_BIN_DIR = $(ENV_DIR)/bin
ENV_LIB_DIR = $(ENV_DIR)/lib
ENV_PYTHON = $(ENV_BIN_DIR)/python

### Commands

# Install conda, installs quietly with NO path modifications.
conda_install:
    @echo 'installing the latest version of Conda python package manager'
    @echo
    wget --no-use-server-timestamps http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda_linux-x86_64.sh
    bash $(CONDA_INSTALLER) -b -p $(CONDA_HOME)

# Creates a new Conda environment
conda_env_create:
	@echo 'creating the '${PROJECT_NAME}' environment'
	@echo
	$((CONDA) env create --name $(PROJECT_NAME) python=3.6)
	@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
	@echo

# Installs required packages for project
conda_env_requirements: requirements.txt
	@pip install -qU pip setuptools wheel
	@pip install -qr requirements.txt
	touch requirements.txt

 

