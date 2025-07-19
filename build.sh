#!/usr/bin/env bash

# Fail on error
set -e

echo "Starting build script..."

# Install dependencies
apt-get update
apt-get install -y wget unzip gnupg ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils

# Download and install latest Google Chrome
echo "Installing Chrome..."
mkdir -p /opt/google/chrome
wget -O chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
mv chrome-linux64/* /opt/google/chrome/
chmod +x /opt/google/chrome/chrome
rm -rf chrome-linux64 chrome-linux64.zip

# Confirm installation
/opt/google/chrome/chrome --version

echo "Chrome installed."

# You should also place your chromedriver manually in:
# /opt/render/project/src/morgan/edit/language/chromedriver
# Make sure it's executable:
chmod +x /opt/render/project/src/morgan/edit/language/chromedriver

echo "Build script completed."
