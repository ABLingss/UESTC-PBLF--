# 这是aboutus的页面，为了简洁我们采用了滚动条设计
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys

class ScrollingTextWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口
        self.setWindowTitle("关于我们")
        self.setGeometry(100, 100, 800, 600)

        # 创建中央小部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建布局
        layout = QVBoxLayout(central_widget)

        # 创建 QLabel 用于显示滚动文本
        self.scroll_label = QLabel(self)
        text = "张三 - 项目经理\n李四 - 后端开发\n王五 - 前端开发\n赵六 - 测试工程师\n孙七 - UI设计师\n周八 - 数据分析师\n吴九 - 系统架构师\n郑十 - 流程优化专家"
        self.scroll_label.setText(text)
        self.scroll_label.setAlignment(Qt.AlignTop)  # 从顶部开始滚动
        layout.addWidget(self.scroll_label)

        # 设置字体和样式
        self.scroll_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        # 创建定时器来定时更新文字位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(10)  # 每50毫秒更新一次

        # 初始文本位置
        self.y_pos = self.height()

    def scroll_text(self):
        # 获取 QLabel 当前的文本位置
        rect = self.scroll_label.geometry()

        # 设置新的垂直位置
        self.y_pos -= 5  # 每次向上移动2个像素

        # 如果文字完全离开窗口，就将其重置到上方重新开始
        if self.y_pos + rect.height() < 0:
            self.y_pos = self.height()

        # 更新位置
        self.scroll_label.move(rect.x(), self.y_pos)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollingTextWindow()
    window.show()
    sys.exit(app.exec_())
