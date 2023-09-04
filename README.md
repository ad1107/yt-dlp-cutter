# yt-dlp-cutter
Automatically cut or save videos from Youtube.
Video will be automatically downloaded in the highest quality and resolution, and converted to ``mp4`` with codec ``H264``.

# Features
Automatically check for missing required files\
``Tkinter`` (gui) is used for selecting folder.\
Improved compatibility using ``libx264`` codec from ffmpeg for output.\
ffmpeg now only shows progress bar.\
``yt-dlp`` now merge input file as ``mp4`` ``(vp90)``.\
Clean up unused files before/after export.\
Option to open directory or video file after export.\
``ytcutter.com`` is used for visualizing timing.

# Using the source code
After download, extract the ``python.zip`` folder.\
You can run the code directly by using the ``run.bat`` file.\
Use ``build.bat`` to release a version, the build file will be located in the root of the directory.
