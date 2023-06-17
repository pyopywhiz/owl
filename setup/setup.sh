#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Configure Git username and email
git config --local user.name "pyopywhiz"
git config --local user.email "acc0568074190@gmail.com"

# Install dependencies using Poetry
poetry install
