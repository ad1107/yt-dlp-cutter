import os
import sys
import time
import tkinter as tk
from tkinter import filedialog

# Global variables
current_dir = os.path.abspath('.') + '\\'
start_time = None

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

def check_ext(ext):
    for filename in os.listdir(current_dir):
        if filename.endswith(ext):
            return True
    return False
