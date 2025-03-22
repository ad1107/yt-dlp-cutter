import os
import logging
from downloader import download_yt_exe, download_ffmpeg_zip, extract_ffmpeg
from utils import check_ext

logging.basicConfig(level=logging.INFO, format='%(message)s')

class DependencyManager:
    @staticmethod
    def check_dependencies():
        logging.info("Checking yt-dlp...")
        if not os.path.isfile('yt-dlp.exe'):
            logging.info("Downloading yt-dlp...")
            download_yt_exe()
        else:
            logging.info("yt-dlp already exists.")

        logging.info("Checking ffmpeg...")
        if not os.path.isfile('ffmpeg.exe'):
            if os.path.isfile('ffmpeg.zip'):
                logging.info("Extracting ffmpeg...")
                extract_ffmpeg()
            else:
                logging.info("Downloading ffmpeg...")
                download_ffmpeg_zip()
                extract_ffmpeg()
        else:
            logging.info("ffmpeg already exists.")

    @staticmethod
    def cleanup():
        logging.info("Cleaning up residual files...")
        if check_ext(".mp4"):
            os.system('del *.mp4 /s /q /f')
        if check_ext(".webm"):
            os.system('del *.webm /s /q /f')
        if os.path.isfile('ffmpeg.zip'):
            os.system('del ffmpeg.zip /s /q /f')
        os.system("cls")

def manage_dependencies():
    DependencyManager.check_dependencies()
    os.system("cls")
    DependencyManager.cleanup()
