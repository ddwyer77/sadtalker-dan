#!/bin/bash
# Simple script to set up and run SadTalker on RunPod

# Exit on error
set -e

echo "=== Setting up SadTalker ==="

# Install ffmpeg if not already installed
if ! which ffmpeg >/dev/null 2>&1; then
  echo "Installing ffmpeg..."
  apt-get update && apt-get install -y ffmpeg
else
  echo "ffmpeg already installed."
fi

# Install PyTorch with CUDA support
echo "Installing PyTorch with CUDA support..."
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --no-build-isolation
pip install -r requirements3d.txt --no-build-isolation

# Install Gradio explicitly
echo "Upgrading Gradio..."
pip install gradio --upgrade

# Download model checkpoints if they don't exist
if [ ! -f "checkpoints/SadTalker_V0.0.2_256.safetensors" ] || [ ! -f "checkpoints/SadTalker_V0.0.2_512.safetensors" ]; then
  echo "Downloading model checkpoints..."
  bash scripts/download_models.sh
else
  echo "Model checkpoints already exist."
fi

# Run tests to verify setup
echo "Running test script to verify setup..."
python test_setup.py

# Ask if user wants to run the web UI
echo ""
echo "Setup complete! Run the web UI now? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
  echo "Starting web UI..."
  # Use the updated app_sadtalker.py which has proper binding parameters
  python app_sadtalker.py
else
  echo "You can run the web UI later with:"
  echo "python app_sadtalker.py"
fi 