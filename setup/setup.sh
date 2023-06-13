#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Configure Git username and email
git config --local user.name "hungdhv97"
git config --local user.email "hungdhv97@gmail.com"

# Install dependencies using Poetry
poetry install
