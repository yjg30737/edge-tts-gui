from main_5_exec_mpv_background import speech
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal

import sys, asyncio


class TextToSpeechThread(QThread):
    finished = Signal()

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text

    def run(self):
        asyncio.run(speech(text=self.text, voice="en-US-AndrewMultilingualNeural"))
        print("TextToSpeechThread run " + self.text)
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle("Text to Speech")

        self.text_area = QTextEdit(self)
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_text)

        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.play_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()

    def play_text(self):
        text = self.text_area.toPlainText()
        if text:
            self.thread = TextToSpeechThread(text)
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
