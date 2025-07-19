#!/usr/bin/env bash

set -e

echo "Creating Chrome install dir..."
mkdir -p /tmp/chrome

echo "Downloading Chrome..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip
unzip -q chrome-linux64.zip
mv chrome-linux64 /tmp/chrome/chrome
rm -f chrome-linux64.zip
echo "✅ Chrome installed at /tmp/chrome/chrome"

echo "Downloading ChromeDriver..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chromedriver-linux64.zip
unzip -q chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /tmp/chrome/chromedriver
chmod +x /tmp/chrome/chromedriver
rm -rf chromedriver-linux64.zip chromedriver-linux64
echo "✅ ChromeDriver installed at /tmp/chrome/chromedriver"
