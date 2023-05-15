import sys
import tesserocr
from manga_ocr import MangaOcr
from PyQt5.QtWidgets import QApplication, QMainWindow, QRubberBand
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QCheckBox, QGroupBox, QHBoxLayout, QSpinBox, QTextEdit, QComboBox, QRadioButton
from PyQt5.QtGui import QFont
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
import argparse
import getproxies
from requestgpt import get_gpt_translation
import threading

def initialize_tts(use_gpu):
    ttsjp = TTS(model_name="tts_models/ja/kokoro/tacotron2-DDC", progress_bar=False, gpu=use_gpu)
    ttsen = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False, gpu=use_gpu)
    return ttsjp, ttsen

class MainWindow(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('sniptranslate')

        layout = QVBoxLayout()

        # Create a QHBoxLayout for TTS Options
        self.tts_options_layout = QHBoxLayout()

        self.tts_untranslated_checkbox = QCheckBox("TTS Scanned Text")
        self.tts_untranslated_checkbox.setChecked(self.args.tts_untranslated)
        self.tts_options_layout.addWidget(self.tts_untranslated_checkbox)

        self.untranslated_speed_label = QLabel("TTS Speed % (Not Working)")
        self.tts_options_layout.addWidget(self.untranslated_speed_label)

        self.untranslated_speed_spinbox = QSpinBox()
        self.untranslated_speed_spinbox.setMinimum(0)
        self.untranslated_speed_spinbox.setMaximum(200)
        self.untranslated_speed_spinbox.setValue(int(self.args.untranslated_tts_speed * 100))
        self.tts_options_layout.addWidget(self.untranslated_speed_spinbox)
        # Align to left
        self.tts_options_layout.addStretch(1)

        self.tts_options_group = QGroupBox("TTS Options")
        self.tts_options_group.setLayout(self.tts_options_layout)
        layout.addWidget(self.tts_options_group)

        # Create a QVBoxLayout for Translation Options (2 rows)
        self.translation_options_layout = QVBoxLayout()

        # First Row
        translation_options_row1 = QHBoxLayout()
        self.translate_checkbox = QCheckBox("Translate")
        self.translate_checkbox.setChecked(self.args.translate)
        translation_options_row1.addWidget(self.translate_checkbox)
        self.tts_translated_checkbox = QCheckBox("TTS Google Translate")
        self.tts_translated_checkbox.setChecked(self.args.tts_translated)
        translation_options_row1.addWidget(self.tts_translated_checkbox)
        self.translation_options_layout.addLayout(translation_options_row1)
        self.tts_chatgpt_checkbox = QCheckBox("TTS ChatGPT")
        self.tts_chatgpt_checkbox.setChecked(self.args.tts_chatgpt)
        translation_options_row1.addWidget(self.tts_chatgpt_checkbox)
        # Align to left
        translation_options_row1.addStretch(1)

        # Second Row
        translation_options_row2 = QHBoxLayout()
        self.proxy_timeout_label = QLabel("Proxy Timeout (ms)")
        translation_options_row2.addWidget(self.proxy_timeout_label)
        self.proxy_timeout = QSpinBox()
        self.proxy_timeout.setMinimum(1000)
        self.proxy_timeout.setMaximum(20000)
        self.proxy_timeout.setSingleStep(1000)
        self.proxy_timeout.setValue(self.args.proxy_timeout)
        translation_options_row2.addWidget(self.proxy_timeout)
        self.manga_ocr_checkbox = QCheckBox("Use Manga OCR")
        self.manga_ocr_checkbox.setChecked(self.args.use_manga_ocr)
        translation_options_row2.addWidget(self.manga_ocr_checkbox)
        self.translation_options_layout.addLayout(translation_options_row2)
        # Align to left
        translation_options_row2.addStretch(1)

        self.translation_options_group = QGroupBox("Translation Options")
        self.translation_options_group.setLayout(self.translation_options_layout)
        layout.addWidget(self.translation_options_group)

        # groupbox for font size adjustment
        self.font_options_group = QGroupBox("Font Options")

        # QHBox for font size adjustment
        self.font_layout = QHBoxLayout()
        self.font_size_label = QLabel("Font Size")
        self.font_layout.addWidget(self.font_size_label)
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setMinimum(1)
        self.font_size_spinbox.setMaximum(100)
        # check current font size of window
        self.font_size_spinbox.setValue(self.font().pointSize())
        self.font_layout.addWidget(self.font_size_spinbox)
        # QHBox for font size of textedit
        self.font_size_textedit_layout = QHBoxLayout()
        self.font_size_textedit_label = QLabel("Console Font Size")
        self.font_layout.addWidget(self.font_size_textedit_label)
        self.font_size_textedit_spinbox = QSpinBox()
        self.font_size_textedit_spinbox.setMinimum(1)
        self.font_size_textedit_spinbox.setMaximum(100)
        # check current font size of textedit
        self.font_size_textedit_spinbox.setValue(self.font().pointSize())
        self.font_layout.addWidget(self.font_size_textedit_spinbox)
        # align to left
        self.font_layout.addStretch(1)

        self.font_options_group = QGroupBox("Font Options")
        self.font_options_group.setLayout(self.font_layout)
        layout.addWidget(self.font_options_group)

        # Add the console-like QTextEdit widget
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        # add placeholder text
        self.console.setPlaceholderText("Press Ctrl+Shift+S to start snipping")
        layout.addWidget(self.console)

        # Connect font size adjustment
        self.font_size_spinbox.valueChanged.connect(self.update_font_size)
        
        # Connect Console font size adjustment
        self.font_size_textedit_spinbox.valueChanged.connect(self.update_console_font_size)

        self.chatgpt_translation_length_group = QGroupBox("ChatGPT Translation Length")
        chatgpt_translation_length_layout = QHBoxLayout()
        self.chatgpt_translation_length_short = QRadioButton("Short")
        self.chatgpt_translation_length_medium = QRadioButton("Medium")
        self.chatgpt_translation_length_medium.setChecked(True) # Default to medium
        self.chatgpt_translation_length_long = QRadioButton("Long")
        chatgpt_translation_length_layout.addWidget(self.chatgpt_translation_length_short)
        chatgpt_translation_length_layout.addWidget(self.chatgpt_translation_length_medium)
        chatgpt_translation_length_layout.addWidget(self.chatgpt_translation_length_long)
        # Align to left
        chatgpt_translation_length_layout.addStretch(1)
        self.chatgpt_translation_length_group.setLayout(chatgpt_translation_length_layout)
        layout.addWidget(self.chatgpt_translation_length_group)

        self.setLayout(layout)

    def append_console_text(self, text):
        self.console.append(text)

    def update_font_size(self, font_size):
        # get current font
        font = self.font()
        font.setPointSize(font_size)
        
        # Set the font for the entire window
        self.setFont(font)

    def update_console_font_size(self, font_size):
        # get current font
        font = self.console.font()
        font.setPointSize(font_size)

        # Set the font for the entire window
        self.console.setFont(font)

class HotkeyThread(QThread):
    hotkey_pressed = pyqtSignal()

    def run(self):
        while True:
            keyboard.wait('ctrl+shift+s')
            self.hotkey_pressed.emit()

class SnippingTool(QMainWindow):
    def __init__(self, main_window, ttsjp, ttsen):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.tts_lock = threading.Lock()

        self.ttsjp, self.ttsen = ttsjp, ttsen

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
        if self.main_window.manga_ocr_checkbox.isChecked():
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
            self.text_to_speech(text, self.ttsen, "notext.wav")
            return
        
        # Remove newlines and brackets
        text = text.replace("\n", " ")
        text = text.replace("]", "")
        text = text.replace("[", "")
        text = text.replace("」", "")
        text = text.replace("「", "")
        text = text.replace("』", "")
        text = text.replace("『", "")

        if self.main_window.tts_untranslated_checkbox.isChecked():
            untranslated_tts_thread = threading.Thread(target=self.text_to_speech, args=(text,self.ttsjp, "untranslated.wav"))
            untranslated_tts_thread.start()
        pyperclip.copy(text)
        print("Text copied to clipboard")
        if self.main_window.translate_checkbox.isChecked():
            print("Pre-translated text: "+text)
            # add a divider
            self.main_window.append_console_text("=========================")
            self.main_window.append_console_text("Pre-translated text: "+text)
            self.translate_and_copy_to_clipboard(text)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def translate_and_copy_to_clipboard(self, text):

        # Translate via Google Translate
        google_translate_thread = threading.Thread(target=self.google_translate, args=(text,))
        google_translate_thread.start()

        # Translate via ChatGPT
        chatgpt_thread = threading.Thread(target=self.chatgpt_translate, args=(text,))
        chatgpt_thread.start()

    def google_translate(self, text):
        with open('input.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        subprocess.run(['node', 'translate.js', 'input.txt', 'output.txt', str(self.main_window.proxy_timeout.value())])
        with open('output.txt', 'r', encoding='utf-8') as f:
            translated_text = f.read()
        print("Google Translate: "+translated_text)
        self.main_window.append_console_text("Google Translate: "+translated_text)
        if translated_text == '':
            translated_text = 'No text detected'
        if self.main_window.tts_translated_checkbox.isChecked():
            self.text_to_speech(translated_text, self.ttsen, "translated.wav")

    def chatgpt_translate(self, text):
        translation_length = ""
        if self.main_window.chatgpt_translation_length_short.isChecked():
            translation_length = "short"
        elif self.main_window.chatgpt_translation_length_medium.isChecked():
            translation_length = "medium"
        elif self.main_window.chatgpt_translation_length_long.isChecked():
            translation_length = "long"
        result = get_gpt_translation(text, translation_length, self.main_window.proxy_timeout.value())
        print("ChatGPT: "+result)
        self.main_window.append_console_text("ChatGPT: "+result)
        if result == '':
            result = 'No text detected'
        result = result.split("Full explanation:")[0]
        if self.main_window.tts_chatgpt_checkbox.isChecked():
            self.text_to_speech(result, self.ttsen, "chatgpt.wav")
        

    def text_to_speech(self, text, tts, filename):
        tts.tts_to_file(text=text, file_path=filename, speed=self.main_window.untranslated_speed_spinbox.value()/100.0)
        print("speed: " + str(self.main_window.untranslated_speed_spinbox.value()/100.0))

        # Load the audio file using librosa
        y, sr = librosa.load(filename, sr=None)

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
    parser.add_argument("--use_gpu", action="store_true", default=False, help="Use GPU for TTS")
    return parser.parse_args()

def main():
    args = parse_arguments()
    ttsjp, ttsen = initialize_tts(args.use_gpu)
    app = QApplication(sys.argv)

    main_window = MainWindow(args)
    main_window.show()

    snipping_tool = SnippingTool(main_window, ttsjp, ttsen)
    snipping_tool.hide()

    hotkey_thread = HotkeyThread()
    hotkey_thread.hotkey_pressed.connect(snipping_tool.showFullScreen)
    hotkey_thread.start()
    print("Press Ctrl+Shift+S to start snipping")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
