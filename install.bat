@echo off
title snip-translate install

set env_name=sniptranslate

REM Check if the Conda environment is already installed
call conda activate %env_name% 2>NUL
if %ERRORLEVEL% neq 0 (
    REM Create a new Conda environment with Python 3.9
    call conda create -y -n %env_name% python=3.9
) else (
    echo conda env %env_name% already created.
)
REM Activate the new Conda environment
call conda activate %env_name%
REM Install the packages from requirements.txt
call pip install -r requirements.txt
REM Install tesserocr
conda install -c conda-forge tesserocr

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
echo install finish