import os
import sys
import time
import zipfile
from urllib.request import urlretrieve

dir = os.path.abspath('.')


def convertpath(path):
    if len(path.strip()) == 0:
        return path
    elif path[-1] != '/' and '/' in path:
        return path + '/'
    elif path[-1] != '\\' and '\\' in path:
        return path + "\\"
    else:
        return path


def convertname(name):
    if len(name) == 0:
        return "output"
    else:
        return name


def percentage(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration)) if duration > 0 else 0
    percent = min(int(count * block_size * 100 / total_size), 100)
    time_remaining = ((total_size - progress_size) / 1024) / speed if speed > 0 else 0
    sys.stdout.write("\r%d%%, %d MB, %d KB/s, ETA: %d seconds" % (
        percent, progress_size / (1024 * 1024), speed, time_remaining))
    sys.stdout.flush()


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
    work_path = os.path.join(dir, name)
    urlretrieve(url, work_path, percentage)
    print('\n')


def download_yt_exe():
    download('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', 'yt-dlp.exe')


def download_ffmpeg_zip():
    download(
        'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip',
        'ffmpeg.zip')


def extract_ffmpeg():
    print("Extracting ffmpeg.exe...")
    extract_file('ffmpeg.zip', 'ffmpeg.exe', dir)
    print("Extraction finished.")


def check_ext(ext):
    for filename in os.listdir(dir):
        if filename.endswith(ext): return True
    return False


print("*** yt-dlp-cutter - Automatically cut videos from Youtube ***\n")

print("Checking for dependencies...")

print("\nStep 1: Checking yt-dlp...")
if os.path.isfile('yt-dlp.exe'):
    print("yt-dlp has been already downloaded.")
else:
    print("yt-dlp hasn't been downloaded.\n")
    download_yt_exe()
flag = 0
print("\nStep 2: Checking ffmpeg...")
if os.path.isfile('ffmpeg.exe'):
    print("ffmpeg has already been downloaded.")
    flag = 1
elif os.path.isfile('ffmpeg.zip'):
    print("ffmpeg.zip has already been downloaded, but hasn't been extracted.\n")
    extract_ffmpeg()
else:
    print("ffmpeg hasn't been downloaded.\n")
    download_ffmpeg_zip()
    extract_ffmpeg()

print("\nStep 3: Remove residual files")

print("Deleting old input files if exist...")
if check_ext(".webm"):
    os.system('del *.webm /s /q /f')
else:
    print("All input files has already been cleared.")

print("\nDeleting old output files if exist...")
if check_ext(".mp4"):
    os.system('del *.mp4 /s /q /f')
else:
    print("All output files has already been cleared.")

print("\nDeleting ffmpeg.zip after extraction (if exists)...")
if os.path.isfile('ffmpeg.zip'):
    os.system('del ffmpeg.zip /s /q /f')
else:
    print("ffmpeg.zip has already been deleted.")

print('\n')
video_link = input("Please paste the video link: ")
print("Downloading original video: ")
os.system('yt-dlp ' + '"' + video_link + '"' + ' --no-playlist -o input.webm')

if check_ext(".webm"):
    print("""\nPlease select between these options:
    1. Save the entire video
    2. Cut the video""")
    a = int(input("Input your number here: "))
    flag = 0
    if a == 1:
        out_name = input("\nType your output name, if blank, the name will be 'output.mp4': ")
        out_path = input("Type your output path, if blank, the video will be kept at the same folder as input: ")
        print("\nExporting...")
        print('ffmpeg.exe -i input.webm ' + convertpath(out_path) + convertname(out_name) + '.mp4')
        os.system('ffmpeg.exe -i input.webm ' + convertpath(out_path) + convertname(out_name) + '.mp4')
        print("\nFinished exporting.")
        flag = 1
    elif a == 2:
        out_name = input("\nType your output name, if blank, the name will be 'output.mp4': ")
        out_path = input("Type your output path, if blank, the video will be kept at the same folder as input: ")
        begin = str(input("Enter the beginning time to cut (seconds): "))
        end = str(input("Enter the end time to cut (seconds): "))
        os.system(
            'ffmpeg.exe -ss ' + begin + ' -t ' + end + ' -i input.webm -y -c copy ' + convertpath(
                out_path) + convertname(out_name) + '.mp4')
        print("\nFinished Exporting.")
        flag = 1
    print("\nDeleting leftover input file")
    os.system('del *.webm /s /q /f')
    print("\nFinished.\n")
    if flag == 1:
        if len(out_path) == 0:
            out_path = dir
        print("Exported video: " + convertpath(out_path) + convertname(out_name) + '.mp4\n')
    else:
        print("Exporting failed. Please try again.")
    os.system('pause')
