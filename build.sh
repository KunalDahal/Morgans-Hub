#!/bin/bash

# build.sh - Optimized for Render's environment

set -e  # Exit on error

# Install system dependencies
echo "Installing system dependencies..."
apt-get update -y
apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    unzip \
    wget

# Install Python dependencies
echo "Installing Python packages..."
pip install --upgrade pip
pip install selenium==4.9.1 webdriver-manager==3.8.6

echo "Build completed successfully."