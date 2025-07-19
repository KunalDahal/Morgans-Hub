#!/bin/bash

set -e

echo "Downloading Chrome..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip -O chrome.zip

echo "Unzipping Chrome..."
unzip -q chrome.zip -d chrome

echo "Making Chrome executable..."
chmod +x chrome/chrome-linux64/chrome

# Ensure local chromedriver is executable, if it exists
if [ -f "morgan/edit/language/chromedriver" ]; then
  echo "Making local ChromeDriver executable..."
  chmod +x morgan/edit/language/chromedriver
else
  echo "Local ChromeDriver not found. Will use undetected-chromedriver fallback."
fi

echo "Installing Python packages..."
pip install -r requirements.txt
