@echo off
title snip-translate

REM Set the environment name and arguments
set env_name=sniptranslate
set arguments=--untranslated_tts_speed 0.9 --translate --tts_translated --tts_untranslated

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

REM Check if @vitalets/google-translate-api package is already installed
call npm list --depth=0 @vitalets/google-translate-api >nul 2>&1
if %ERRORLEVEL% neq 0 (
    REM Install the @vitalets/google-translate-api package
    call npm install @vitalets/google-translate-api
)

REM Update the package.json file to include "type": "module"
call python update_package_json.py

REM Check if http-proxy-agent package is already installed
call npm list --depth=0 http-proxy-agent >nul 2>&1
if %ERRORLEVEL% neq 0 (
    REM Install the http-proxy-agent package
    call npm install http-proxy-agent
)

REM Set the title back to snip-translate
title snip-translate

REM Start the eSpeak NG application
start "" /B "C:\Program Files\eSpeak NG\espeak-ng.exe"

REM Run the Python script
start "" /B python test.py %arguments%

REM Wait for both processes to finish
:wait_loop
tasklist /FI "IMAGENAME eq cmd.exe" /FI "IMAGENAME eq espeak-ng.exe" 2>NUL | find /I /N "cmd.exe" >NUL
if "%ERRORLEVEL%"=="0" goto wait_loop
taskkill /F /IM "cmd.exe" >NUL
taskkill /F /IM "espeak-ng.exe" >NUL

REM Deactivate the Conda environment
call conda deactivate
