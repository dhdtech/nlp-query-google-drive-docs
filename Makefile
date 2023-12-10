# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	RED          := $(shell tput -Txterm setaf 1)
	GREEN        := $(shell tput -Txterm setaf 2)
	BLUE         := $(shell tput -Txterm setaf 6)
	ORANGE 	     := $(shell tput -Txterm setaf 3)
	RESET 		 := $(shell tput -Txterm sgr0)
	PURPLE       := $(shell tput -Txterm setaf 5)
else
	RED          := ""
	GREEN        := ""
	BLUE         := ""
	RESET        := ""
endif

.PHONY: help
help: ## Show this help message
	@echo "${GREEN}############################################### Hudson Dias Makefile ################################################${RESET}"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${BLUE}%-30s${RESET} %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo "${GREEN}#####################################################################################################################${RESET}"

.SILENT: 
lint_and_format: ## Runs flake8, isort and black against the codebase
	isort .
	black --config pyproject.toml .
	flake8 .


configure_devel: validate_local_env clean_devel ## Cleans up the environment and installs the development dependencies
	@bash -c "python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && pre-commit install"
	
clean_devel:
	echo "${PURPLE}2. Doing a fresh install of the development environment${RESET}"
	echo "   ${ORANGE}Checking if within an active virtual environment${RESET}"
	if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "         ${GREEN}Within an active virtual environment. Will deactivate it.${RESET}"; \
		deactivate; \
		echo "         ${GREEN}Virtual environment deactivated.${RESET}"; \
	fi;
	echo "      ${ORANGE}Removing the virtual environment folder (venv) if it exists${RESET}"
	rm -rf venv || true
	

.SILENT:
validate_local_env:
	echo "${PURPLE}1. Validating local environment${RESET}"
	echo "      ${ORANGE}Checking if python3 is installed in the system${RESET}"
	if ! command -v python3 &> /dev/null; then \
		echo "         ${RED}Python3 is not installed in the system. Please install it first.${RESET}"; \
		exit 1; \
	else \
		echo "         ${GREEN}Python3 is installed in the system.${RESET}"; \
	fi;
	echo ""
