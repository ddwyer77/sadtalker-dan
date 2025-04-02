#!/bin/bash

# Script to run SadTalker with a video source file
# Usage: ./run_with_video.sh <video_file> <audio_file> [--cpu]

# Check if the required arguments are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <video_file> <audio_file> [options]"
    echo "Options:"
    echo "  --cpu            Use CPU processing (slower but more compatible)"
    echo "  --no-enhance     Don't use face enhancement"
    echo "  --full-body      Use full body mode"
    exit 1
fi

VIDEO_FILE="$1"
AUDIO_FILE="$2"
shift 2

# Default options
USE_CPU=""
USE_ENHANCER="--enhancer gfpgan"
FULL_BODY=""

# Parse optional arguments
for arg in "$@"; do
    case $arg in
        --cpu)
            USE_CPU="--cpu"
            ;;
        --no-enhance)
            USE_ENHANCER=""
            ;;
        --full-body)
            FULL_BODY="--still"
            ;;
    esac
done

# Activate the virtual environment
if [ -f "sadtalker_env/bin/activate" ]; then
    source sadtalker_env/bin/activate
elif [ -f "../SadTalker/sadtalker_env/bin/activate" ]; then
    source "../SadTalker/sadtalker_env/bin/activate"
else
    echo "Error: Virtual environment not found"
    exit 1
fi

# Check if files exist
if [ ! -f "$VIDEO_FILE" ]; then
    echo "Error: Video file '$VIDEO_FILE' not found"
    exit 1
fi

if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: Audio file '$AUDIO_FILE' not found"
    exit 1
fi

echo "Starting SadTalker with:"
echo "Video: $VIDEO_FILE"
echo "Audio: $AUDIO_FILE"
echo "Options: $USE_CPU $USE_ENHANCER $FULL_BODY"
echo

# Run SadTalker
python inference.py --driven_audio "$AUDIO_FILE" --source_image "$VIDEO_FILE" $USE_CPU $USE_ENHANCER $FULL_BODY

# Check if successful
if [ $? -eq 0 ]; then
    echo "Processing completed successfully!"
    # Attempt to find the output video in the results directory
    LATEST_RESULT=$(ls -t results/ | head -n 1)
    if [[ $LATEST_RESULT == *.mp4 ]]; then
        echo "Output video: $(pwd)/results/$LATEST_RESULT"
    else
        echo "Check the results directory for the output: $(pwd)/results"
    fi
else
    echo "Processing failed"
fi 