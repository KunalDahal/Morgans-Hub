#!/usr/bin/env bash

set -e

echo "Creating Chrome install dir..."
mkdir -p /tmp/chrome

echo "Downloading Chrome..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip
unzip -q chrome-linux64.zip
mv chrome-linux64 /tmp/chrome/chrome

# Clean up
rm -f chrome-linux64.zip

echo "✅ Chrome up in /tmp/chrome"
