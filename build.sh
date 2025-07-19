#!/bin/bash
set -ex  # Exit on error and show commands

# Chrome and Chromedriver version (matched pair)
VERSION="138.0.7204.157"
BASE_URL="https://storage.googleapis.com/chrome-for-testing-public"

# Install Chrome
echo "Installing Chrome ${VERSION}..."
wget -q "${BASE_URL}/${VERSION}/linux64/chrome-linux64.zip" -O chrome.zip
unzip -q chrome.zip -d chrome-temp
rm chrome.zip
mkdir -p /opt/google/chrome
mv chrome-temp/chrome-linux64/* /opt/google/chrome
ln -sf /opt/google/chrome/chrome /usr/bin/google-chrome

# Install Chromedriver (local + system-wide fallback)
echo "Installing Chromedriver ${VERSION}..."
wget -q "${BASE_URL}/${VERSION}/linux64/chromedriver-linux64.zip" -O chromedriver.zip
unzip -q chromedriver.zip -d chromedriver-temp
rm chromedriver.zip

# 1. Local installation (priority)
LOCAL_DRIVER_DIR="/opt/render/project/src/morgan/edit/language"
mkdir -p $LOCAL_DRIVER_DIR
mv chromedriver-temp/chromedriver-linux64/chromedriver "${LOCAL_DRIVER_DIR}/chromedriver"
chmod +x "${LOCAL_DRIVER_DIR}/chromedriver"

# 2. System-wide installation (fallback)
mv chromedriver-temp/chromedriver-linux64/chromedriver /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

# Cleanup
rm -rf chrome-temp chromedriver-temp

# Verify installations
google-chrome --version || { echo "Chrome installation failed"; exit 1; }
chromedriver --version || { echo "Chromedriver installation failed"; exit 1; }

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"