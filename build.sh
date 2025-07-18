#!/usr/bin/env bash
# Install Chrome (headless-friendly)
apt-get update
apt-get install -y wget unzip curl gnupg

# Add Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# (Optional: verify Chrome path)
which google-chrome
