#!/bin/bash

# Install Chrome
wget https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
rm chrome-linux64.zip
mv chrome-linux64 /opt/google/chrome
ln -s /opt/google/chrome/chrome /usr/bin/google-chrome

# Install matching Chromedriver
wget https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
rm chromedriver-linux64.zip
mv chromedriver-linux64 /opt/google/chromedriver
ln -s /opt/google/chromedriver/chromedriver /usr/bin/chromedriver
chmod +x /opt/google/chromedriver/chromedriver

# Install dependencies
pip install -r requirements.txt