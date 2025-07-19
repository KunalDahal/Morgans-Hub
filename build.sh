#!/bin/bash
set -ex  # Exit on error and show commands

# Chrome and Chromedriver version (matched pair)
VERSION="138.0.7204.157"
BASE_URL="https://storage.googleapis.com/chrome-for-testing-public"

# Create a local directory for installation
INSTALL_DIR="$HOME/chrome_install"
mkdir -p "$INSTALL_DIR"

# Install Chrome
echo "Installing Chrome ${VERSION}..."
wget -q "${BASE_URL}/${VERSION}/linux64/chrome-linux64.zip" -O chrome.zip
unzip -q chrome.zip -d chrome-temp
rm chrome.zip
mv chrome-temp/chrome-linux64 "$INSTALL_DIR/chrome"
ln -sf "$INSTALL_DIR/chrome/chrome" "$HOME/.local/bin/google-chrome"

# Install Chromedriver
echo "Installing Chromedriver ${VERSION}..."
wget -q "${BASE_URL}/${VERSION}/linux64/chromedriver-linux64.zip" -O chromedriver.zip
unzip -q chromedriver.zip -d chromedriver-temp
rm chromedriver.zip

# Local installation
LOCAL_DRIVER_DIR="/opt/render/project/src/morgan/edit/language"
mkdir -p "$LOCAL_DRIVER_DIR"
mv chromedriver-temp/chromedriver-linux64/chromedriver "${LOCAL_DRIVER_DIR}/chromedriver"
chmod +x "${LOCAL_DRIVER_DIR}/chromedriver"

# Also add to PATH-accessible location
mkdir -p "$HOME/.local/bin"
mv chromedriver-temp/chromedriver-linux64/chromedriver "$HOME/.local/bin/chromedriver"
chmod +x "$HOME/.local/bin/chromedriver"

# Cleanup
rm -rf chrome-temp chromedriver-temp

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    export PATH="$HOME/.local/bin:$PATH"
fi

# Verify installations
google-chrome --version || { echo "Chrome installation failed"; exit 1; }
chromedriver --version || { echo "Chromedriver installation failed"; exit 1; }

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"