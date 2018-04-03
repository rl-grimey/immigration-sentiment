#################################################################################
# GLOBALS                                                                       #
#################################################################################

# Project
PROFILE = default
PROJECT_NAME = immigration-sentiment
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Python
PYTHON_INTERPRETER = python3
CONDA_HOME = $(HOME)/minicond3
CONDA_BIN_DIR = $(CONDA_HOME)/bin
CONDA = $(CONDA_BIN_DIR)/conda
CONDA_INSTALLER = miniconda_linux-x86_64.sh

# Environment
ENV_DIR = $(CONDA_HOME)/envs/$(PROJECT_NAME)
ENV_BIN_DIR = $(ENV_DIR)/bin
ENV_LIB_DIR = $(ENV_DIR)/lib
ENV_PYTHON = $(ENV_BIN_DIR)/python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Sets up our project for a new user.
00-environment: install-conda install-environment update-environment .env

## Creates database and uploads csvs.
01-data: create-database reports/pipeline.import.log reports/pipeline.filter.log

## Expose a port for remote Jupyter SSH session
jupyter-serve:
	jupyter notebook --no-browser --port 8889
	@echo 

## Connects to remote Jupyter session
jupyter-connect:
	@echo 'Replace the following with your information'
	@echo 'ssh -N -L localhost:8889:localhost:8889 remote_user@remote_host'
	@echo 

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".ipynb_checkpoints" -exec rm -r "{}" \;
	@echo

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

variables:
	@echo 'PROFILE: ' $(PROFILE)
	@echo 'PROJECT_NAME: ' $(PROJECT_NAME)
	@echo 'PROJECT_DIR: ' $(PROJECT_DIR)
	@echo
	@echo 'PYTHON_INTERPRETER: ' $(PYTHON_INTERPRETER)
	@echo 'CONDA_HOME: ' $(CONDA_HOME)
	@echo 'CONDA_BIN_DIR: ' $(CONDA_BIN_DIR)
	@echo 'CONDA: ' $(CONDA)
	@echo 'CONDA_INSTALLER: ' $(CONDA_INSTALLER)
	@echo
	@echo 'ENV_DIR: ' $(ENV_DIR)
	@echo 'ENV_BIN_DIR: ' $(ENV_BIN_DIR)
	@echo 'ENV_LIB_DIR: ' $(ENV_LIB_DIR)
	@echo 'ENV_PYTHON: ' $(ENV_PYTHON)

install-conda:
ifeq (,$(shell which conda))
	@echo '>>> Downloading Conda python package manager'
	@wget -q --no-use-server-timestamps http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $(CONDA_INSTALLER)
	@echo '>>> Installing Conda'
	@bash $(CONDA_INSTALLER) -b -p $(CONDA_HOME)
	@echo '>>> Making a backup of .bashrc and adding Conda to PATH'
	@cp ~/.bashrc ~/.bashrc.bak
	@printf '\n\n# Anaconda Python Distribution' >> ~/.bashrc
	@printf '\nexport PATH='$(CONDA_BIN_DIR)':$$PATH' >> ~/.bashrc
	@rm $(CONDA_INSTALLER)
else
	@echo '>>> Found Conda installation.'
endif

uninstall-conda:
	@echo 'Uninstalling conda'
	@rm ~/.bashrc
	@mv ~/.bashrc.bak ~/.bashrc
	@rm -rf $(CONDA_HOME)

install-environment:
	@echo '>>> Creating new Python project environment'
	@${CONDA} env create --name $(PROJECT_NAME) python=3.6

update-environment: environment.yml
	@echo '>>> Updating Python environment'
	@echo $(PROJECT_NAME)
	@${CONDA} env update --name $(PROJECT_NAME) -f $<

.env: src/utils/make_environment.py
	@echo '>>> Creating environment configuration file'
	@$(ENV_PYTHON) src/utils/make_environment.py

create-database: src/data/database.py src/data/createdb.sql .env
	@echo '>>> Creating database tables'
	@${ENV_PYTHON} $< src/data/createdb.sql

reset-database: src/data/database.py src/data/dropdb.sql .env
	@echo '>>> Dropping database tables'
	@${ENV_PYTHON} $< src/data/dropdb.sql
	@rm reports/pipeline.*.log

reports/pipeline.import.log: src/data/make_dataset.py .env
	@echo '>>> Uploading CSVs to database.'
	@$(ENV_PYTHON) $<

reports/pipeline.filter.log: src/data/make_filtered.py reports/pipeline.import.log .env
	@echo '>>> Filtering raw tweets from database'
	@$(ENV_PYTHON) $<


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help install-conda install-environment 00-environment 01-data
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
