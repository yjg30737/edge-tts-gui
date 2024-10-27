from main_3_edge_playback_background import speech
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal

import sys, asyncio

class TextToSpeechThread(QThread):
    finished = Signal()  # 재생 완료 시 신호를 보냅니다.

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text

    def run(self):
        asyncio.run(speech(text=self.text, voice="en-US-AndrewMultilingualNeural"))
        print("TextToSpeechThread run " + self.text)
        self.finished.emit()  # 재생이 완료되었음을 알립니다.


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle("Text to Speech")
        self.setGeometry(100, 100, 800, 600)

        # Text area 및 버튼 설정
        self.text_area = QTextEdit(self)
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_text)  # 버튼 클릭 시 재생 함수 연결

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.play_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()

    def play_text(self):
        """Play 버튼이 눌렸을 때 호출되는 함수입니다."""
        text = self.text_area.toPlainText()
        if text:
            # 새로운 스레드를 생성하여 텍스트 재생을 시작합니다.
            self.thread = TextToSpeechThread(text)
            self.thread.finished.connect(self.on_play_finished)
            self.play_button.setEnabled(False)  # 재생 중에는 버튼을 비활성화합니다.
            self.thread.start()

    def on_play_finished(self):
        """재생이 완료되었을 때 호출됩니다."""
        self.play_button.setEnabled(True)  # 재생 완료 후 버튼을 다시 활성화합니다.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
