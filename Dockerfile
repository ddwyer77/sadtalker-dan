FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /workspace

# Clone SadTalker repository
COPY . /workspace/

# Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118 && \
    pip3 install -r requirements.txt && \
    pip3 install -r requirements3d.txt && \
    pip3 install opencv-python==4.7.0.72 opencv-contrib-python==4.7.0.72 && \
    pip3 install dlib insightface==0.7.3

# Download checkpoint files (if not already included)
RUN mkdir -p checkpoints
RUN if [ ! -d "checkpoints/epoch_20.pth" ]; then \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/epoch_20.pth -O checkpoints/epoch_20.pth; \
    fi

RUN if [ ! -d "checkpoints/mapping_00109-model.pth.tar" ]; then \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/mapping_00109-model.pth.tar -O checkpoints/mapping_00109-model.pth.tar; \
    fi

RUN if [ ! -d "checkpoints/mapping_00229-model.pth.tar" ]; then \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/mapping_00229-model.pth.tar -O checkpoints/mapping_00229-model.pth.tar; \
    fi

RUN if [ ! -d "checkpoints/SadTalker_V0.0.2_256.safetensors" ]; then \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/SadTalker_V0.0.2_256.safetensors -O checkpoints/SadTalker_V0.0.2_256.safetensors; \
    fi

RUN if [ ! -d "checkpoints/facevid2vid_00189-model.pth.tar" ]; then \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2/facevid2vid_00189-model.pth.tar -O checkpoints/facevid2vid_00189-model.pth.tar; \
    fi

RUN if [ ! -d "gfpgan/weights" ]; then \
    mkdir -p gfpgan/weights && \
    wget -nc https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth -O gfpgan/weights/GFPGANv1.3.pth; \
    fi

# Create runpod startup script
COPY runpod_startup.sh /workspace/runpod_startup.sh
RUN chmod +x /workspace/runpod_startup.sh

# Expose port for Gradio web UI
EXPOSE 7860

# Set entry point
ENTRYPOINT ["/workspace/runpod_startup.sh"] 