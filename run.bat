@echo off

set env_name=sniptranslate
set arguments=--untranslated_tts_speed 1.0 --translate --tts_chatgpt --tts_untranslated --proxy_timeout 4000

REM Set the title back to snip-translate
title snip-translate

REM Start the eSpeak NG application
start "" /B "C:\Program Files\eSpeak NG\espeak-ng.exe"

REM Activate the new Conda environment
call conda activate %env_name%
REM Run the Python script
echo Launch arguments: %arguments%
start "" /B python test.py %arguments%

REM Wait for both processes to finish
:wait_loop
tasklist /FI "IMAGENAME eq cmd.exe" /FI "IMAGENAME eq espeak-ng.exe" 2>NUL | find /I /N "cmd.exe" >NUL
if "%ERRORLEVEL%"=="0" goto wait_loop
taskkill /F /IM "cmd.exe" >NUL
taskkill /F /IM "espeak-ng.exe" >NUL

REM Deactivate the Conda environment
call conda deactivate
