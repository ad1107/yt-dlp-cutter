import os
import sys
import time
import tkinter as tk
import webbrowser
import zipfile
from tkinter import filedialog
from urllib.request import urlretrieve

current_dir = os.path.abspath('.') + '\\'


def converttime(time_str):
    parts = time_str.replace(",", ".").split(':')  # support both , and . character.
    seconds, milliseconds = map(str, parts[-1].split('.'))
    hours = int(parts[-3]) if len(parts) >= 3 else 0
    minutes = int(parts[-2]) if len(parts) >= 2 else 0
    total_seconds = str(hours * 3600 + minutes * 60 + int(seconds)) + '.' + milliseconds
    return float(total_seconds)


def select_path(title):
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title=title)
    if path:
        return path + '/'
    else:
        return current_dir


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
    work_path = os.path.join(current_dir, name)
    urlretrieve(url, work_path, percentage)
    print('\n')


def download_yt_exe():
    download('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', 'yt-dlp.exe')


def download_ffmpeg_zip():
    download(
        'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
        'ffmpeg.zip')


def extract_ffmpeg():
    print("Extracting ffmpeg.exe...")
    extract_file('ffmpeg.zip', 'ffmpeg.exe', current_dir)
    print("Extraction finished.")


def check_ext(ext):
    for filename in os.listdir(current_dir):
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
os.system("cls")
flag = 0
print("Step 2: Checking ffmpeg...")
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
os.system("cls")
print("Step 3: Remove residual files")

print("Deleting old input and/or output files if exist...")
if check_ext(".mp4"):
    os.system('del *.mp4 /s /q /f')
if check_ext(".webm"):
    os.system('del *.webm /s /q /f')
else:
    print("All input and/or output files has already been cleared.")

print("\nDeleting ffmpeg.zip after extraction (if exists)...")
if os.path.isfile('ffmpeg.zip'):
    os.system('del ffmpeg.zip /s /q /f')
else:
    print("ffmpeg.zip has already been deleted.")
os.system("cls")
video_link = input("Please paste the video link: ")

print("\nDownloading original video: ")
os.system('yt-dlp ' + '"' + video_link + '"' + ' --no-playlist --merge-output-format mp4 -o input.mp4')

if check_ext("input.mp4"):
    os.system("cls")
    print("""Please select between these options:
    1. Save the entire video
    2. Cut the video""")
    a = input("\nInput your number here: ")
    flag = 0
    if a == '1':
        out_name = input("\nType your output name, if blank, the name will be 'output.mp4': ")
        print(
            "Please select the output directory, if you close the window, the video will be saved at the same "
            "directory as input.")
        out_path = select_path("Select the output directory: ")
        print("\nYour path: " + out_path)
        print("\nExporting...")
        os.system('ffmpeg.exe -v quiet -stats -i input.mp4 -c:v libx264 ' + '"' + out_path + convertname(
            out_name) + '.mp4"')
        print("\nFinished exporting.")
        flag = 1
    elif a == '2':
        out_name = input("\nType your output name, if blank, the name will be 'output.mp4': ")
        print(
            "Please select the output directory, if you close the window, the video will be saved at the same "
            "directory as input.")
        out_path = select_path("Select the output directory: ")
        print("\nYour path: " + out_path)
        web = input('\nPress 1 to visualize video for cutting: ')
        if web == "1":
            print("Opening website on your default browser...")
            webbrowser.open("https://ytcutter.com/")
        begin = converttime(input("\nEnter the beginning time to cut: "))
        end = converttime(input("Enter the end time to cut: "))
        os.system(
            'ffmpeg.exe -v quiet -stats -ss ' + str(begin) + ' -t ' + str(
                end - begin) + ' -i input.mp4 -y -c:v libx264 -c copy ' + '"' + out_path + convertname(
                out_name) + '.mp4"')
        print("\nFinished Exporting.")
        flag = 1

    print("\nDeleting leftover input file")
    if check_ext("input.mp4"):
        os.system('del input.mp4 /s /q /f')
    if check_ext(".webm"):
        os.system('del *.webm /s /q /f')

    os.system("cls")
    print("Finished.\n")
    if flag == 1:
        if len(out_path) == 0: out_path = current_dir
        print("Exported video: " + out_path + convertname(out_name) + '.mp4\n')
        if input("Press 1 if you want to open the directory contain the output file: ") == "1":
            print("\nOpening the directory...")
            os.system('explorer ' + out_path.replace("/", "\\"))
        if input("\nPress 1 if you want to play the video using your default video player: ") == "1":
            print("\nOpening video file..")
            os.system(out_path + "'" + convertname(out_name) + '.mp4"')
    else:
        print("Exporting failed. Please try again.\n")
    os.system('pause')
else:
    print("\nCannot download video. Please try again.\n")
    os.system("pause")
