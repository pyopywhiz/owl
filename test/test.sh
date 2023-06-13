#!/bin/bash

# check for required tools
command -v black >/dev/null 2>&1 || { echo >&2 "Black is not installed. Aborting."; exit 1; }
command -v isort >/dev/null 2>&1 || { echo >&2 "Isort is not installed. Aborting."; exit 1; }
command -v mypy >/dev/null 2>&1 || { echo >&2 "Mypy is not installed. Aborting."; exit 1; }
command -v flake8 >/dev/null 2>&1 || { echo >&2 "Flake8 is not installed. Aborting."; exit 1; }
command -v pylint >/dev/null 2>&1 || { echo >&2 "Pylint is not installed. Aborting."; exit 1; }

# run black
echo "Running Black..."
black .
echo "Black finished."
echo "--------------------------------------"

# run isort
echo "Running Isort..."
isort .
echo "Isort finished."
echo "--------------------------------------"

# run mypy
echo "Running Mypy..."
mypy .
echo "Mypy finished."
echo "--------------------------------------"

# run flake8
echo "Running Flake8..."
flake8
echo "Flake8 finished."
echo "--------------------------------------"

# run pylint
echo "Running Pylint..."
pylint .
echo "Pylint finished."
echo "--------------------------------------"

# print message when each job is done
echo "All linting and formatting jobs completed."
