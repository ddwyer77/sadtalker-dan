#!/bin/bash

# Change to the SadTalker directory
cd "$(dirname "$0")"

# Check if the virtual environment exists in the current directory
if [ -f "sadtalker_env/bin/activate" ]; then
    echo "Activating local virtual environment"
    source sadtalker_env/bin/activate
# If it doesn't exist in this directory, try the parent directory (for the case where we're in SadTalker-main)
elif [ -f "../SadTalker/sadtalker_env/bin/activate" ]; then
    echo "Activating parent directory virtual environment"
    source "../SadTalker/sadtalker_env/bin/activate"
else
    echo "Error: Virtual environment not found"
    exit 1
fi

# Check if PyQt5 is installed
if ! python -c "import PyQt5" &> /dev/null; then
    echo "Installing PyQt5..."
    pip install PyQt5
fi

# Run the UI
python sadtalker_ui.py

# Keep the terminal open if there's an error
if [ $? -ne 0 ]; then
    echo -e "\nAn error occurred. Press Enter to exit..."
    read
fi 