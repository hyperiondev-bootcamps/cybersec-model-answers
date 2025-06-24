#!/bin/bash

# Script to change permissions of all files inside a directory to 644.
# This script uses the find command to list all files and then
# iterates over each file to change its permissions.

# Get a list of all files (excluding directories) inside the current directory.
# The find . -type f command lists all files recursively.
FILES=$(find . -type f)

# Iterate over each file found.
for file in $FILES; do
  # Change the permissions of the file to 644.
  # The `chmod` command is used to change the file permissions.
  # 644 permissions correspond to:
  #   - Owner: read and write (6)
  #   - Group: read-only (4)
  #   - Others: read-only (4)
  chmod 644 "$file"
done
