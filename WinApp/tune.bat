@echo off
setlocal enabledelayedexpansion

:: Define the paths to check
set "path1=C:\Program Files (x86)\Logitech\LogiTune\LogiTune.exe"
set "path2=C:\Program Files\Logitech\LogiTune\LogiTune.exe"

:: Capture the port number from the command line argument
set "port=%1"

:: Check if the executable exists in the first path
if exist "!path1!" (
    :: Run the existing executable from the first path
    start "" "!path1!" --remote-debugging-port=!port!
) else (
    :: If not found, check the second path
    if exist "!path2!" (
        :: Run the existing executable from the second path
        start "" "!path2!" --remote-debugging-port=!port!
    ) else (
        echo The application is missing. Ensure it is installed and placed in your PATH.
    )
)