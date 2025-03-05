# Snip-Translate
A handy snipping tool with TTS and translation options designed for Windows

Designed for reading Manga

## Demo
GUI interface

![image](https://github.com/AlexanderLJX/snip-translate/assets/83382087/5a736e6b-fb82-4240-b182-e3e126a8833e)

## Features

- GUI interface
- Manga OCR (default OCR) ([kha-white/manga-ocr](https://github.com/kha-white/manga-ocr))
- Tesserocr ([sirfz/tesserocr](https://github.com/sirfz/tesserocr))
- Free gemini API, requires api key
- Unlimited Google Translate using multiple proxies ([vitalets/google-translate-api](https://github.com/vitalets/google-translate-api))
- Automatically copies scanned text to clipboard
- Editable arguments in the bat file to turn on/off features

## Installation

### Install Node.js

Install [Node.js](https://nodejs.org/en)

### Install Anaconda

1. Download and install Anaconda from [anaconda.com/download](https://www.anaconda.com/download/) and add it to your environment path.

### Setup

1. Double-click `install.bat` to install additional packages.
2. Create a file .env with the contents `GEMINI_API_KEY=your_api_key'
3. Download the repo from [here](https://huggingface.co/kha-white/manga-ocr-base/tree/main) into the root of this repo


### Run the application

1. Double-click `run.bat` to start the program.
2. Use `ctrl+shift+s` to snip. Scanned text will be copied to clipboard.
