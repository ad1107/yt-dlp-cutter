@ECHO OFF
IF EXIST "./python/python.exe" (
    START ./python/python.exe main.py
) ELSE (
    ECHO Python folder doesn't exist.
)
