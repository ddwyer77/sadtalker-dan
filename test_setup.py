#!/usr/bin/env python3
"""
Simple test script to verify SadTalker dependencies and core functionality
"""
import os
import sys
import torch
import numpy as np
import cv2
import subprocess

# Test basic imports
print("=== Testing basic imports ===")
print(f"Python version: {sys.version}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# Test OpenCV
print("\n=== Testing OpenCV ===")
print(f"OpenCV version: {cv2.__version__}")

# Test ffmpeg
print("\n=== Testing ffmpeg ===")
try:
    result = subprocess.run(["ffmpeg", "-version"], 
                           capture_output=True, 
                           text=True, 
                           check=True)
    print("ffmpeg is installed and working")
    first_line = result.stdout.split('\n')[0]
    print(f"Version: {first_line}")
except subprocess.CalledProcessError:
    print("⚠️ ffmpeg test failed")
except FileNotFoundError:
    print("⚠️ ffmpeg not found, please install it")

# Check for model files
print("\n=== Checking model files ===")
models = [
    "checkpoints/mapping_00229-model.pth.tar",
    "checkpoints/SadTalker_V0.0.2_256.safetensors",
    "checkpoints/SadTalker_V0.0.2_512.safetensors",
    "gfpgan/weights/detection_Resnet50_Final.pth",
    "gfpgan/weights/parsing_parsenet.pth",
    "gfpgan/weights/alignment_WFLW_4HG.pth",
]

for model in models:
    if os.path.exists(model):
        size_mb = os.path.getsize(model) / (1024 * 1024)
        print(f"✓ {model} ({size_mb:.2f} MB)")
    else:
        print(f"✗ {model} not found")

print("\nIf all tests pass, your setup is ready to run SadTalker!")
print("Run the web UI with: python app_sadtalker.py --listen=0.0.0.0 --port=7860") 