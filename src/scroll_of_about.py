from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys
import os
import pygame

class ScrollingTextWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("关于我们")
        self.setGeometry(100, 100, 800, 600)

        current_directory = os.path.dirname(os.path.abspath(__file__))

        # 背景图片路径
        image_path_1 = os.path.join(current_directory, "..", "assets", "D315856FD459A2B52B8D781C3CFCC3D2.png")
        image_path_2 = os.path.join(current_directory, "..", "assets", "0D0F18143C6225D0B9868C8044758203.png")
        image_path_3 = os.path.join(current_directory, "..", "assets", "A5A3EB0508816E38D3D2BF9F34AD7170.png")

        image_path_1 = image_path_1.replace(os.sep, '/')
        image_path_2 = image_path_2.replace(os.sep, '/')
        image_path_3 = image_path_3.replace(os.sep, '/')

        # 播放背景音乐
        pygame.mixer.init()
        # 播放音乐
        pygame.mixer.music.load('../assets/NaiLong.wav')
        pygame.mixer.music.play(-1)  # -1 表示循环播放

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #F5F5F5;
                font-family: 'Segoe UI', sans-serif;
                background-image: 
                    url("{image_path_1}"), 
                    url("{image_path_2}"),
                    url("{image_path_3}");
                background-position: top left, top right, bottom left;
                background-repeat: no-repeat, no-repeat, no-repeat;
                background-size: contain;
            }}
        """)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.setFixedSize(800, 600)  # 固定窗口大小为800x600

        self.scroll_label = QLabel(self)
        text = """无敌极巨化虫洞吞噬者超级奶龙 - 马英哲
奶小龙 - 王梓
奶白雪龙 - 杨潇
界-唐龙 - 杨杰翔
库奶龙 - 王俊豪
"""
        self.scroll_label.setText(text)
        self.scroll_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # 垂直居上，水平居中
        layout.addWidget(self.scroll_label)

        self.scroll_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(20)  # 延长定时器间隔以提升性能

        self.y_pos = self.height()

    def scroll_text(self):
        rect = self.scroll_label.geometry()
        self.y_pos -= 2  # 每次向上移动5个像素
        if self.y_pos + rect.height() < 0:
            self.y_pos = self.height()

        # 更新 QLabel 的位置，水平保持居中，垂直滚动
        self.scroll_label.move((self.width() - rect.width()) // 2, self.y_pos)

    def play_music(self):
        # 播放背景音乐
        music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "NaiLong.wav")
        music_path = music_path.replace(os.sep, '/')
        os.system(f"start {music_path}")

    def closeEvent(self, event):
        # 重写 closeEvent 方法，在窗口关闭时停止音乐播放
        pygame.mixer.music.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollingTextWindow()
    window.show()
    sys.exit(app.exec_())
