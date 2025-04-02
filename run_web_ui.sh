#!/bin/bash
# Simple script to set up and run SadTalker on RunPod

# Install ffmpeg if not already installed
which ffmpeg >/dev/null 2>&1 || sudo apt-get update && sudo apt-get install -y ffmpeg

# Install PyTorch with CUDA support
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

# Install dependencies
pip install -r requirements.txt --no-build-isolation
pip install -r requirements3d.txt --no-build-isolation

# Install Gradio explicitly
pip install gradio --upgrade

# Download model checkpoints if they don't exist
if [ ! -d "checkpoints/SadTalker_V0.0.2_256.safetensors" ]; then
  bash scripts/download_models.sh
fi

# Run the web UI
python app_sadtalker.py --listen=0.0.0.0 --port=7860 