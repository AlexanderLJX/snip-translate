# Snip-Translate
A handy snipping tool with TTS and translation options designed for Windows

Initially designed for Japanese to English translation, but easily adaptable for other languages

## Demo

https://user-images.githubusercontent.com/83382087/237959812-dc56a76a-1155-4413-85b7-1564791f07be.mp4

## Features

- Snipping tool
- Manga OCR (default OCR) ([kha-white/manga-ocr](https://github.com/kha-white/manga-ocr))
- Tesserocr ([sirfz/tesserocr](https://github.com/sirfz/tesserocr))
- Free chatGPT translation using free api (better than DeepL and Google Translate imo) (default translation tts)
- Unlimited Google Translate using multiple proxies ([vitalets/google-translate-api](https://github.com/vitalets/google-translate-api))
- Text to speech powered by Coqui TTS ([coqui-ai/TTS](https://github.com/coqui-ai/TTS))
- Automatically copies scanned text to clipboard
- Editable arguments in the bat file to turn on/off features

## Installation

### Install espeak

1. Download and install espeak from [espeak-ng/espeak-ng/releases](https://github.com/espeak-ng/espeak-ng/releases/).
2. The installation directory should be `C:\Program Files\eSpeak NG\espeak-ng.exe` else you should modify the `run.bat` file accordingly.
Note that espeak is used in the VITS English TTS.

### Install rubberband (Optional)

rubberband allows you to use the `--untranslated_tts_speed` arugment to change the speed of the audio playback.

1. Download the rubberband cli from [rubberband downloads](https://breakfastquay.com/rubberband/index.html) and add the files to your environment path or just copy them into the root directory of this project.

### Install Node.js

Install [Node.js](https://nodejs.org/en)

### Install Anaconda

1. Download and install Anaconda from [anaconda.com/download](https://www.anaconda.com/download/) and add it to your environment path.

### Install packages

1. Double-click `install.bat` to install additional packages.

### Run the application

1. Double-click `run.bat` to start the program.
2. Use `ctrl+shift+s` to snip. Scanned text will be copied to clipboard.
