# SadTalker on RunPod with GPU Acceleration

This guide provides detailed instructions for deploying SadTalker on RunPod with GPU acceleration for significantly faster processing of talking face animations.

## Why RunPod?

RunPod offers several advantages for running SadTalker:

1. **GPU Acceleration**: Access to powerful NVIDIA GPUs (up to A100, H100) for much faster processing
2. **On-demand Resources**: Pay only for the time you use
3. **Persistent Storage**: Your models and results are saved between sessions
4. **Web UI Access**: Access SadTalker through a web interface from anywhere
5. **Scalability**: Easily scale up or down based on your processing needs

## Deployment Options

### Option 1: One-Click Deployment (Recommended)

The easiest way to deploy SadTalker on RunPod:

1. Visit [RunPod.io](https://runpod.io) and create an account
2. Navigate to the RunPod Templates section
3. Search for "SadTalker GPU" or use the direct template link (coming soon)
4. Select your preferred GPU type:
   - For basic use: RTX 3080/3090 (16-24GB VRAM)
   - For faster processing: A5000/A6000 (24-48GB VRAM)
5. Click "Deploy" and wait for your pod to start (usually takes 2-3 minutes)
6. Once started, click on the provided URL to access the SadTalker web UI

### Option 2: Manual Deployment

For advanced users who want more control:

1. Create a new pod on RunPod:
   - Select a GPU template (NVIDIA with CUDA support)
   - Set the Docker image to: `nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04`
   - Add ports: `7860:7860` (for the web UI)
   - Start the pod

2. After the pod starts, open a terminal session and run:

```bash
# Clone the repository
git clone https://github.com/ddwyer77/sadtalker-dan.git
cd sadtalker-dan/SadTalker

# Build the Docker image
docker build -t sadtalker-runpod .

# Run the container
docker run --gpus all -p 7860:7860 -v $(pwd)/checkpoints:/workspace/checkpoints -v $(pwd)/results:/workspace/results sadtalker-runpod
```

3. Access the web UI through the URL provided in your RunPod dashboard

## Expected Performance

Benchmark comparisons between CPU and GPU processing:

| Platform | Hardware | 10-second video generation | 60-second video generation |
|----------|----------|----------------------------|---------------------------|
| Laptop CPU | Intel i7, 16GB RAM | ~5-8 minutes | ~30-45 minutes |
| RunPod | RTX 3080, 16GB VRAM | ~30-45 seconds | ~3-4 minutes |
| RunPod | A100, 40GB VRAM | ~15-20 seconds | ~1-2 minutes |

## Volume Persistence

Models and generated results are stored in persistent volumes:

- `/workspace/checkpoints`: Contains model checkpoints
- `/workspace/results`: Contains generated videos

This ensures your models and results are saved even if you stop and restart your pod. You can download generated videos directly from the web UI or via the RunPod file browser.

## Cost Considerations

RunPod pricing varies based on the GPU type. As of 2023-2024:

- RTX 3080 (10GB): ~$0.25-0.35/hour
- RTX 3090 (24GB): ~$0.39-0.49/hour
- A5000 (24GB): ~$0.59-0.69/hour
- A100 (40-80GB): ~$1.99-2.99/hour

For most SadTalker use cases, an RTX 3080/3090 provides excellent price/performance ratio.

## Troubleshooting

If you encounter issues with your RunPod deployment:

1. **Web UI Not Loading**:
   - Check if the pod is fully initialized (can take 2-3 minutes)
   - Verify port 7860 is exposed in your pod configuration
   - Check the pod logs for any error messages

2. **Model Download Issues**:
   - The startup script should automatically download models
   - If they fail to download, you can manually upload them via the RunPod file browser

3. **CUDA/GPU Not Detected**:
   - Verify you selected a GPU-enabled pod
   - Check nvidia-smi output in the terminal
   - Ensure CUDA drivers match the PyTorch version

## Advanced Configuration

To customize your RunPod deployment:

1. **Custom Checkpoint Path**: 
   Edit `runpod_startup.sh` to set custom model paths

2. **Higher Resolution Output**:
   Edit `runpod_startup.sh` to add resolution parameters 

3. **Auto-shutdown after Inactivity**:
   Use RunPod's auto-shutdown feature to save costs

4. **API Integration**:
   RunPod supports API access for automation

For additional support, join our [Discord community](https://discord.gg/rrayYqZ4tf) or open an issue on GitHub. 