from dependency import manage_dependencies
from video_processor import VideoProcessor

def main():
    print("*** yt-dlp-cutter - Automatically cut videos from Youtube ***\n")
    print("Checking for dependencies...")
    manage_dependencies()
    processor = VideoProcessor()
    processor.run()

if __name__ == "__main__":
    main()
