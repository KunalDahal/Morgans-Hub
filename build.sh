#!/bin/bash

# build.sh - Works within Render's read-only filesystem constraints

set -e  # Exit immediately if any command fails

# Use Render's recommended locations (within the project directory)
INSTALL_DIR="$HOME/.local"
CHROME_DIR="$INSTALL_DIR/chrome"
CHROMEDRIVER_DIR="$INSTALL_DIR/bin"

# URLs for Chrome and ChromeDriver
CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip"
CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chromedriver-linux64.zip"

# Create directories in writable space
mkdir -p $CHROME_DIR
mkdir -p $CHROMEDRIVER_DIR

# Install dependencies available in Render's environment
echo "Installing system dependencies..."
apt-get update -y
apt-get install -y --no-install-recommends unzip python3-pip

# Download and install Chrome
echo "Downloading Chrome..."
wget -O /tmp/chrome.zip $CHROME_URL
unzip /tmp/chrome.zip -d /tmp
mv /tmp/chrome-linux64/chrome $CHROME_DIR/
chmod +x $CHROME_DIR/chrome

# Download and install ChromeDriver
echo "Downloading ChromeDriver..."
wget -O /tmp/chromedriver.zip $CHROMEDRIVER_URL
unzip /tmp/chromedriver.zip -d /tmp
mv /tmp/chromedriver-linux64/chromedriver $CHROMEDRIVER_DIR/
chmod +x $CHROMEDRIVER_DIR/chromedriver

# Add to PATH
export PATH="$CHROMEDRIVER_DIR:$CHROME_DIR:$PATH"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Clean up
rm -rf /tmp/chrome-linux64 /tmp/chromedriver-linux64 /tmp/chrome.zip /tmp/chromedriver.zip

echo "Installation completed successfully."