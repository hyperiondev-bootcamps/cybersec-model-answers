#!/bin/bash

# This script performs the following tasks using apt:
# 1. Uninstalls all unused dependencies.
# 2. Updates the software database.
# 3. Updates the entire system.
# It also checks if the script is run with root privileges.

# Check if the script is run by the root user.
account=$(whoami)

if [ "$account" != "root" ]; then
  # Print an error message to stderr if not run as root.
  >&2 echo "This script must be run with superuser privileges."
  exit 1
fi

# Uninstall all unused dependencies.
apt autoremove -y

# Update the software database.
apt update

# Update the entire system.
apt full-upgrade -y

exit 0
