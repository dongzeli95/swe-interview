#!/bin/bash

gitbook build

# Get current datetime
version=$(date "+%Y%m%d%H%M%S")

# Navigate to the parent directory
cd ..

# If it does exist, navigate into it
cd swe-interview-book

# Remove old _book content if exists
rm -rf ./*

# Copy _book directory into swe-interview-book
cp -r ../swe-interview/_book/* .

# Add all new files to git
git add .

# Commit the changes
git commit -m "Update _book content version: $version"

# Push changes to origin main
git push origin main

# Go back to the original directory
cd ../swe-interview
