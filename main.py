

import sys, asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QFormLayout, QWidget, QComboBox
from PySide6.QtCore import QThread, Signal

from script import speech

EDGE_TTS_VOICE_TYPE = ["en-GB-SoniaNeural", "en-US-GuyNeural", "en-US-JennyNeural"]


class TextToSpeechThread(QThread):
    finished = Signal()

    def __init__(self, text, voice, parent=None):
        super().__init__(parent)
        self.text = text
        self.voice = voice

    def run(self):
        asyncio.run(speech(text=self.text, voice=self.voice))
        print("TextToSpeechThread run " + self.text)
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle("Text to Speech")

        self.voiceCmbBox = QComboBox()
        self.voiceCmbBox.addItems(EDGE_TTS_VOICE_TYPE)

        self.text_area = QTextEdit(self)
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_text)

        lay = QFormLayout()
        lay.addRow('Voice', self.voiceCmbBox)
        lay.addRow(self.text_area)
        lay.addRow(self.play_button)

        container = QWidget()
        container.setLayout(lay)
        self.setCentralWidget(container)

        self.show()

    def play_text(self):
        text = self.text_area.toPlainText()
        if text:
            voice = self.voiceCmbBox.currentText()
            self.thread = TextToSpeechThread(text, voice)
            self.thread.finished.connect(self.on_play_finished)
            self.play_button.setEnabled(False)
            self.thread.start()

    def on_play_finished(self):
        self.play_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
