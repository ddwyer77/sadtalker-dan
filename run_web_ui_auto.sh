#!/bin/bash
# Non-interactive script to set up and run SadTalker on RunPod
# Useful for automated startup

# Exit on error
set -e

echo "=== Setting up SadTalker (Automated Mode) ==="

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

# Start the web UI automatically
echo "Starting web UI..."
python app_sadtalker.py --listen=0.0.0.0 --port=7860 