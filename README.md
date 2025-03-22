# yt-dlp-cutter

Automatically cut videos from YouTube using yt-dlp and ffmpeg.
Now with improved/maintainable script!

## Overview

This project downloads a YouTube video and either saves the entire video or cuts out a specific segment based on user input. It uses:
- **yt-dlp** for downloading YouTube videos.
- **ffmpeg** for processing the video.
- **tkinter** for GUI-based directory selection.
- **requests** and **tqdm** for enhanced download progress display.

## Usage
1. Install the required libraries:
    ```
    pip install -r requirements.txt
    ```
2. Run the script:
    ```
    python main.py
    ```
3. Follow the on-screen instructions.
