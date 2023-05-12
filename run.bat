@echo off

rem Set the environment name and file paths
set env_name=tts

REM Check if the Conda environment is already installed
call conda activate %env_name% 2>NUL
if %ERRORLEVEL% neq 0 (
    REM Create a new Conda environment with Python 3.9
    call conda create -y -n %env_name% python=3.9
    REM Activate the new Conda environment
    call conda activate %env_name%
    REM Install the packages from requirements.txt
    call pip install -r requirements.txt
)

REM Start the eSpeak NG application
start "" /B "C:\Program Files\eSpeak NG\espeak-ng.exe"

REM Run the Python script
start "" /B python test.py

REM Wait for both processes to finish
:wait_loop
tasklist /FI "IMAGENAME eq cmd.exe" /FI "IMAGENAME eq espeak-ng.exe" 2>NUL | find /I /N "cmd.exe" >NUL
if "%ERRORLEVEL%"=="0" goto wait_loop
taskkill /F /IM "cmd.exe" >NUL
taskkill /F /IM "espeak-ng.exe" >NUL

REM Deactivate the Conda environment
call conda deactivate