#!/usr/bin/env bash
set -e

echo "Setting permissions for Chrome and ChromeDriver..."

# Ensure Chrome and Chromedriver are executable
chmod +x /opt/google/chrome/chrome
chmod +x /opt/render/project/src/morgan/edit/language/chromedriver

echo "Done with setup."
