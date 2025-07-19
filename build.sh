#!/bin/bash

# build.sh - Script to install dependencies for Render deployment
# Installs:
# 1. Chrome and ChromeDriver
# 2. Python packages from requirements.txt

set -e  # Exit immediately if any command fails

# Define installation directories
CHROME_DIR="/opt/google/chrome"
CHROMEDRIVER_LOCAL_DIR="/opt/render/project/src/morgan/edit/language"
CHROMEDRIVER_SYSTEM_DIR="/usr/bin"

# URLs for Chrome and ChromeDriver (version 138.0.7204.157)
CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip"
CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chromedriver-linux64.zip"

# Create directories if they don't exist
sudo mkdir -p $CHROME_DIR
sudo mkdir -p $CHROMEDRIVER_LOCAL_DIR
sudo mkdir -p $CHROMEDRIVER_SYSTEM_DIR

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y unzip python3-pip

# Download and install Chrome
echo "Downloading Chrome..."
wget -O /tmp/chrome.zip $CHROME_URL
unzip /tmp/chrome.zip -d /tmp
sudo mv /tmp/chrome-linux64/* $CHROME_DIR
sudo ln -sf $CHROME_DIR/chrome /usr/bin/chrome

# Download and install ChromeDriver (local copy)
echo "Downloading ChromeDriver..."
wget -O /tmp/chromedriver.zip $CHROMEDRIVER_URL
unzip /tmp/chromedriver.zip -d /tmp
sudo mv /tmp/chromedriver-linux64/chromedriver $CHROMEDRIVER_LOCAL_DIR/chromedriver
sudo chmod +x $CHROMEDRIVER_LOCAL_DIR/chromedriver

# Install ChromeDriver system-wide (fallback)
sudo mv /tmp/chromedriver-linux64/chromedriver $CHROMEDRIVER_SYSTEM_DIR/chromedriver
sudo chmod +x $CHROMEDRIVER_SYSTEM_DIR/chromedriver

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Clean up
rm -rf /tmp/chrome-linux64 /tmp/chromedriver-linux64 /tmp/chrome.zip /tmp/chromedriver.zip

echo "All dependencies installed successfully."