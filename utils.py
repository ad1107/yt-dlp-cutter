import os
import sys
import time
import tkinter as tk
from tkinter import filedialog

# Global variables
current_dir = os.path.abspath('.') + '\\'
start_time = None

def converttime(time_str):
    parts = time_str.replace(',', '.').split(':')
    return sum(int(x) * 60**(i+1) for i, x in enumerate(reversed(parts[:-1]))) + float(parts[-1])


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

def progress(count, block_size, total_size):
    if count == 0:
        progress.start = time.time()
        return
    elapsed = time.time() - progress.start
    current = count * block_size
    pct = min(current * 100 / total_size, 100)
    speed = current / elapsed if elapsed else 0 
    eta = (total_size - current) / speed if speed else 0
    bar = '#' * int(pct / 2) + '-' * (50 - int(pct / 2))
    sys.stdout.write(f"\r[{bar}] {pct:.0f}% | {current/(1024*1024):.1f} MB | {speed/1024:.1f} KB/s | ETA: {eta:.0f}s")
    sys.stdout.flush()

def check_ext(ext):
    for filename in os.listdir(current_dir):
        if filename.endswith(ext):
            return True
    return False
