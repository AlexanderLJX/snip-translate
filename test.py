import sys
import tesserocr
from manga_ocr import MangaOcr
from PyQt5.QtWidgets import QApplication, QMainWindow, QRubberBand
from PyQt5.QtCore import Qt, QRect, QPoint, QSize, QThread, pyqtSignal
import pyscreenshot as ImageGrab
import keyboard
import pyperclip
import subprocess
from TTS.api import TTS
import pyaudio
import wave
import librosa
import soundfile as sf
import pyrubberband as pyrb
import argparse
import getproxies
from requestgpt import get_translation
import threading


class HotkeyThread(QThread):
    hotkey_pressed = pyqtSignal()

    def run(self):
        while True:
            keyboard.wait('ctrl+shift+s')
            self.hotkey_pressed.emit()

class SnippingTool(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.initUI()
        self.tts_lock = threading.Lock()
        self.ttsjp = TTS(model_name="tts_models/ja/kokoro/tacotron2-DDC", progress_bar=False, gpu=self.args.use_gpu)
        self.ttsen = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False, gpu=self.args.use_gpu)


    def initUI(self):
        self.setWindowTitle('Snipping Tool')
        self.setWindowOpacity(0.5)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showFullScreen()

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.capture()

    def capture(self):
        rect = self.rubber_band.geometry()
        self.close()
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        left, top, right, bottom = min(x, x+w), min(y, y+h), max(x, x+w), max(y, y+h)

        area = (right - left) * (bottom - top)
        if area < 10:
            print("Operation cancelled due to small area")
            return

        img = ImageGrab.grab(bbox=(left, top, right, bottom))

        text = ''
        if self.args.use_manga_ocr:
            mocr = MangaOcr()
            text = mocr(img)
        else:
            # Initialize the tesserocr API with the Japanese language and vertical text mode
            with tesserocr.PyTessBaseAPI(lang='jpn_vert') as api:
                # Set the image for OCR
                print("OCR-ing...")
                api.SetImage(img)
                print("OCR-ed")
                # Get the OCR text
                text = api.GetUTF8Text()
                print("OCR text: "+text)

        if text == '':
            text = 'No text detected'
            self.text_to_speech(text, self.ttsen)
            return
        
        # Remove newlines and brackets
        text = text.replace("\n", " ")
        text = text.replace("]", "")
        text = text.replace("[", "")
        text = text.replace("」", "")
        text = text.replace("「", "")
        text = text.replace("』", "")
        text = text.replace("『", "")

        if self.args.tts_untranslated:
            untranslated_tts_thread = threading.Thread(target=self.text_to_speech, args=(text,self.ttsjp, "untranslated.wav", self.args.untranslated_tts_speed))
            untranslated_tts_thread.start()
        pyperclip.copy(text)
        if self.args.translate:
            print("Text copied to clipboard")
            print("pre-translated text: "+text)
            self.translate_and_copy_to_clipboard(text)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def translate_and_copy_to_clipboard(self, text):
        with open('input.txt', 'w', encoding='utf-8') as f:
            f.write(text)

        # Translate via Google Translate
        google_translate_thread = threading.Thread(target=self.google_translate, args=(text,))
        google_translate_thread.start()

        # Translate via ChatGPT
        chatgpt_thread = threading.Thread(target=self.chatgpt_translate, args=(text,))
        chatgpt_thread.start()

    def google_translate(self, text):
        subprocess.run(['node', 'translate.js', 'input.txt', 'output.txt', str(self.args.proxy_timeout)])
        with open('output.txt', 'r', encoding='utf-8') as f:
            translated_text = f.read()
        print("Google Translate: "+translated_text)
        if translated_text == '':
            translated_text = 'No text detected'
        if self.args.tts_translated:
            self.text_to_speech(translated_text, self.ttsen, "translated.wav")

    def chatgpt_translate(self, text):
        result = get_translation(text)
        # Handle the result of get_translation here
        print("ChatGPT: "+result)
        if result == '':
            result = 'No text detected'
        if self.args.tts_chatgpt:
            self.text_to_speech(result, self.ttsen, "chatgpt.wav")
        print("finished chatgpt")
        

    def text_to_speech(self, text, tts, filename, speed=1.0):
        tts.tts_to_file(text=text, file_path=filename)

        # Load the audio file using librosa
        y, sr = librosa.load(filename, sr=None)

        if speed != 1.0:
            # Time-stretch the audio without changing the pitch using Rubber Band Library
            y_stretched = pyrb.time_stretch(y, sr, speed)  # Slow down by the reciprocal of the speed

            # Save the stretched audio
            sf.write(filename, y_stretched, sr)

        chunk = 1024
        f = wave.open(filename, "rb")
        p = pyaudio.PyAudio()
        self.tts_lock.acquire()
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        data = f.readframes(chunk)

        while data:
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
        self.tts_lock.release()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Snipping Tool with TTS and translation options")
    parser.add_argument("--untranslated_tts_speed", type=float, default=1.0, help="Speed factor for untranslated TTS playback")
    parser.add_argument("--translate", action="store_true", default=False, help="Enable translation")
    parser.add_argument("--tts_translated", action="store_true", default=False, help="Enable text to speech for translated text")
    parser.add_argument("--tts_chatgpt", action="store_true", default=False, help="Enable text to speech for chatgpt output")
    parser.add_argument("--tts_untranslated", action="store_true", default=False, help="Enable text to speech for untranslated text")
    parser.add_argument("--use_manga_ocr", action="store_true", default=False, help="Use manga-ocr instead of tesserocr")
    parser.add_argument("--proxy_timeout", type=int, default=7000, help="Timeout for proxy requests (milliseconds))")
    parser.add_argument("--use-gpu", action="store_true", default=False, help="Use GPU for TTS")
    return parser.parse_args()

def main():
    args = parse_arguments()
    app = QApplication(sys.argv)
    snipping_tool = SnippingTool(args)
    snipping_tool.hide()

    hotkey_thread = HotkeyThread()
    hotkey_thread.hotkey_pressed.connect(snipping_tool.showFullScreen)
    hotkey_thread.start()
    print("Press Ctrl+Shift+S to start snipping")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
