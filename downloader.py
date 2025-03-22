import os
import zipfile
from urllib.request import urlretrieve
from utils import current_dir, percentage

def extract_file(zip_path, file_name, output_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_name in file_info.filename:
                extracted_filename = os.path.basename(file_info.filename)
                extracted_path = os.path.join(output_path, extracted_filename)
                with open(extracted_path, 'wb') as extracted_file:
                    extracted_file.write(zip_ref.read(file_info.filename))
                return True
    return False

def download(url, name):
    print("Downloading " + name + ":")
    work_path = os.path.join(current_dir, name)
    urlretrieve(url, work_path, percentage)
    print('\n')

def download_yt_exe():
    download('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', 'yt-dlp.exe')

def download_ffmpeg_zip():
    download('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip', 'ffmpeg.zip')

def extract_ffmpeg():
    print("Extracting ffmpeg.exe...")
    extract_file('ffmpeg.zip', 'ffmpeg.exe', current_dir)
    print("Extraction finished.")
