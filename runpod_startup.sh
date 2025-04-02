#!/bin/bash
set -e

echo "Starting SadTalker on RunPod with GPU Acceleration"

# Create results directory if it doesn't exist
mkdir -p /workspace/results

# Check if the checkpoints are available
if [ ! -f "/workspace/checkpoints/epoch_20.pth" ]; then
    echo "Downloading required model checkpoints..."
    mkdir -p /workspace/checkpoints
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/epoch_20.pth -O /workspace/checkpoints/epoch_20.pth
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/mapping_00109-model.pth.tar -O /workspace/checkpoints/mapping_00109-model.pth.tar
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/mapping_00229-model.pth.tar -O /workspace/checkpoints/mapping_00229-model.pth.tar
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/SadTalker_V0.0.2_256.safetensors -O /workspace/checkpoints/SadTalker_V0.0.2_256.safetensors
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/facevid2vid_00189-model.pth.tar -O /workspace/checkpoints/facevid2vid_00189-model.pth.tar
fi

# Check if GFPGAN weights are available
if [ ! -f "/workspace/gfpgan/weights/GFPGANv1.3.pth" ]; then
    echo "Downloading GFPGAN weights..."
    mkdir -p /workspace/gfpgan/weights
    wget -nc https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth -O /workspace/gfpgan/weights/GFPGANv1.3.pth
fi

# Print CUDA version and GPU info
echo "CUDA version: $(nvcc --version | grep release | awk '{print $6}' | cut -c2-)"
echo "GPU Information:"
nvidia-smi

# Launch the UI with public access on port 7860
cd /workspace
python3 sadtalker_ui.py --share --listen=0.0.0.0 --port=7860 