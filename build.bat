@echo off
REM ============================================================
REM Build Script for yt-dlp-cutter Portable Executable
REM ============================================================

set /p ver="Enter version number: "
cls

echo [INFO] Installing PyInstaller...
pip install pyinstaller || (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)
cls

echo [INFO] Building executable from main.py...
pyinstaller --onefile main.py || (
    echo [ERROR] Build process failed.
    pause
    exit /b 1
)
cls

echo [INFO] Moving built executable to project root...
pushd dist
if exist main.exe (
    move main.exe ..
) else (
    echo [ERROR] main.exe not found in the dist directory.
    popd
    pause
    exit /b 1
)
popd

rmdir /s /q dist

if exist main.exe (
    ren main.exe yt-dlp-cutter-%ver%.exe
) else (
    echo [ERROR] main.exe not found in the project root.
    pause
    exit /b 1
)

:: Remove PyInstaller build artifacts
del /s /q *.spec
rmdir /s /q build

cls
echo [SUCCESS] Build complete: yt-dlp-cutter-%ver%.exe
pause
