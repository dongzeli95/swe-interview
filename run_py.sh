#!/bin/bash

# Default values
file_name="main.py"

# Handle command-line options using getopts
while getopts ":f:" opt; do
    case $opt in
        f)
            file_name="$OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

# Shift the option index so that $1 points to the first non-option argument (directory path)
shift "$((OPTIND-1))"

# Check if the directory exists
dir_path=$(dirname "$1")
if [ ! -d "$dir_path" ]; then
    echo "Error: Directory not found."
    exit 1
fi

# Change the current directory to the user-provided directory
cd "$dir_path"

# Check if the main.py file exists in the directory
if [ ! -f "$file_name" ]; then
    echo "Error: $file_name not found in the directory."
    exit 1
fi

# Run the Python script
python3 "$file_name"

# Check if the execution was successful
if [ $? -eq 0 ]; then
    echo "Execution successful."
else
    echo "Execution failed."
fi
