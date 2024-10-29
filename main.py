
import subprocess, time, os, tempfile, psutil
import sys, asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QFormLayout, QWidget, QComboBox
from PySide6.QtCore import QThread, Signal
from script import kill

EDGE_TTS_VOICE_TYPE = ["en-GB-SoniaNeural", "en-US-GuyNeural", "en-US-JennyNeural"]


class TextToSpeechThread(QThread):
    finished = Signal()

    def __init__(self, text, voice, parent=None):
        super().__init__(parent)
        self.text = text
        self.voice = voice
        self.__stop = False

    def stop(self):
        self.__stop = True

    def run(self):
        media = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        media.close()
        mp3_fname = media.name

        subtitle = tempfile.NamedTemporaryFile(suffix=".vtt", delete=False)
        subtitle.close()
        vtt_fname = subtitle.name

        print(f"Media file: {mp3_fname}")
        print(f"Subtitle file: {vtt_fname}\n")
        with subprocess.Popen(
                [
                    "edge-tts",
                    f"--write-media={mp3_fname}",
                    f"--write-subtitles={vtt_fname}",
                    f"--voice={self.voice}",
                    f"--text={self.text}",
                ]
        ) as process:
            process.communicate()

        proc = subprocess.Popen(
                [
                    "mpv",
                    f"--sub-file={vtt_fname}",
                    mp3_fname,
                ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        while proc.poll() is None:
            time.sleep(0.1)
            if self.__stop:
                kill(proc.pid)
                break
        if mp3_fname is not None and os.path.exists(mp3_fname):
            os.unlink(mp3_fname)
        if vtt_fname is not None and os.path.exists(vtt_fname):
            os.unlink(vtt_fname)
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

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_text)

        lay = QFormLayout()
        lay.addRow('Voice', self.voiceCmbBox)
        lay.addRow(self.text_area)
        lay.addRow(self.play_button)
        lay.addRow(self.stop_button)

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

    def stop_text(self):
        self.thread.stop()

    def on_play_finished(self):
        self.play_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
