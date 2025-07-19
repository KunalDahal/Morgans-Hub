#!/usr/bin/env bash

set -e

echo "Creating Chrome install dir..."
mkdir -p /tmp/chrome

echo "Downloading Chrome..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip
unzip -q chrome-linux64.zip
mv chrome-linux64 /tmp/chrome/chrome
rm -f chrome-linux64.zip

# ✅ Make Chrome binary executable
chmod +x /tmp/chrome/chrome/chrome
echo "✅ Chrome installed at /tmp/chrome/chrome/chrome and made executable"

echo "Downloading ChromeDriver..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chromedriver-linux64.zip
unzip -q chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /tmp/chrome/chromedriver

# ✅ Make ChromeDriver executable
chmod +x /tmp/chrome/chromedriver

# Cleanup
rm -rf chromedriver-linux64.zip chromedriver-linux64
echo "✅ ChromeDriver installed at /tmp/chrome/chromedriver and made executable"
