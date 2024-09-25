#!/usr/bin/env bash

# Update and install system dependencies
apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpython3-dev \
    build-essential

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt
