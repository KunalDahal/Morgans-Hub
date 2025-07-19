#!/usr/bin/env bash

set -e

# Create a directory for Chrome and Chromedriver
mkdir -p /tmp/chrome

echo "Installing Chrome to /tmp/chrome..."
wget -q -O /tmp/chrome/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    xdg-utils
dpkg -x /tmp/chrome/chrome.deb /tmp/chrome/
mv /tmp/chrome/opt/google/chrome /tmp/chrome/

# Install matching ChromeDriver
echo "Installing ChromeDriver to /tmp/chrome..."
CHROME_VERSION=$(grep -oP '\d+\.\d+\.\d+\.\d+' /tmp/chrome/chrome/cron | head -1 || echo "114.0.5735.90")
wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"
unzip -q chromedriver-linux64.zip -d /tmp/chrome/
mv /tmp/chrome/chromedriver-linux64/chromedriver /tmp/chrome/
chmod +x /tmp/chrome/chromedriver

# Clean up
rm -rf /tmp/chrome/chrome.deb chromedriver-linux64.zip /tmp/chrome/chromedriver-linux64

echo "Build completed. Chrome and ChromeDriver are in /tmp/chrome"
