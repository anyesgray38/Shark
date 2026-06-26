#!/bin/bash
set -e

# Install and enable OpenSSH server on Debian/Ubuntu-based systems
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
echo "OpenSSH server installed and running."
