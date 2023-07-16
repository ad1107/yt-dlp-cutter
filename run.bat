@ECHO OFF
IF EXIST "./python/python.exe" (
    .\python\python.exe main.py
) ELSE (
    ECHO Python folder doesn't exist. Please extract them.
)
