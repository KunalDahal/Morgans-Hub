#!/usr/bin/env bash
set -e

echo "📁 Creating Chrome install directory..."
sudo mkdir -p /usr/local/bin/chrome

echo "⬇️ Downloading Chrome..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip
unzip -q chrome-linux64.zip
sudo mv chrome-linux64 /usr/local/bin/chrome
rm -f chrome-linux64.zip

echo "🔧 Making Chrome binary executable..."
sudo chmod +x /usr/local/bin/chrome/chrome

echo "⬇️ Downloading ChromeDriver..."
wget -q https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chromedriver-linux64.zip
unzip -q chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
sudo rm -rf chromedriver-linux64.zip chromedriver-linux64

echo "🔧 Making ChromeDriver executable..."
sudo chmod +x /usr/local/bin/chromedriver

echo "✅ Chrome installed at /usr/local/bin/chrome/chrome"
echo "✅ ChromeDriver installed at /usr/local/bin/chromedriver"

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎉 Build complete!"
