# Snip-Translate
A handy snipping tool with TTS and translation options designed for Windows

Initially designed for Japanese to English translation, but easily adaptable for other languages

## Demo
No gpu demo

https://user-images.githubusercontent.com/83382087/238321576-61be4b33-d40a-4570-b2e8-1900047a663c.mp4

GUI interface

![image](https://github.com/AlexanderLJX/snip-translate/assets/83382087/5a736e6b-fb82-4240-b182-e3e126a8833e)

## Features

- GUI interface
- Manga OCR (default OCR) ([kha-white/manga-ocr](https://github.com/kha-white/manga-ocr))
- Tesserocr ([sirfz/tesserocr](https://github.com/sirfz/tesserocr))
- Free chatGPT translation using free api (better than DeepL and Google Translate)
- Unlimited Google Translate using multiple proxies ([vitalets/google-translate-api](https://github.com/vitalets/google-translate-api))
- Text to speech powered by Coqui TTS ([coqui-ai/TTS](https://github.com/coqui-ai/TTS))
- Automatically copies scanned text to clipboard
- Editable arguments in the bat file to turn on/off features

## Installation

### Install espeak

1. Download and install espeak from [espeak-ng/espeak-ng/releases](https://github.com/espeak-ng/espeak-ng/releases/).
2. The installation directory should be `C:\Program Files\eSpeak NG\espeak-ng.exe` else you should modify the `run.bat` file accordingly.
Note that espeak is used in the VITS English TTS.

### Install Node.js

Install [Node.js](https://nodejs.org/en)

### Install Anaconda

1. Download and install Anaconda from [anaconda.com/download](https://www.anaconda.com/download/) and add it to your environment path.

### Install packages

1. Double-click `install.bat` to install additional packages.

### Run the application

1. Double-click `run.bat` to start the program.
2. Use `ctrl+shift+s` to snip. Scanned text will be copied to clipboard.
