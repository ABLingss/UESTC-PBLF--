from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import sys


class SmallGamesWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("小游戏")
        self.setGeometry(100, 100, 426, 300)  # 设置窗口位置和大小
        self.ui = Ui_Form()
        self.ui.setupUi(self)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(426, 300)
        Form.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                border: none;
                border-radius: 4px;
                color: white;
                padding: 10px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #005FAC;
            }
            QPushButton:pressed {
                background-color: #003D79;
            }
        """)

        # 创建垂直布局管理器
        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)

        # 创建 QLabel
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextFormat(QtCore.Qt.MarkdownText)
        self.label.setText("# 小游戏")
        self.mainLayout.addWidget(self.label)

        # 创建游戏按钮布局
        self.gameLayout = QtWidgets.QVBoxLayout()

        # 俄罗斯方块按钮
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setText("俄罗斯方块")
        self.pushButton_2.clicked.connect(self.start_eluosi_game)
        self.gameLayout.addWidget(self.pushButton_2)

        # 贪吃蛇按钮
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setText("贪吃蛇")
        self.pushButton_4.clicked.connect(self.start_snake_game)
        self.gameLayout.addWidget(self.pushButton_4)

        # 飞机大战按钮
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setText("飞机大战")
        self.pushButton.clicked.connect(self.start_plane_fight_game)
        self.gameLayout.addWidget(self.pushButton)

        # 退回主菜单按钮
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setText("退回主菜单")
        self.pushButton_3.clicked.connect(Form.close)  # 关闭当前窗口
        self.gameLayout.addWidget(self.pushButton_3)

        # 将按钮布局添加到主布局
        self.mainLayout.addLayout(self.gameLayout)

        # 将布局应用到窗口
        Form.setLayout(self.mainLayout)

    def start_eluosi_game(self):
        """启动俄罗斯方块游戏"""
        self.start_game("eluosi.exe")

    def start_snake_game(self):
        """启动贪吃蛇游戏"""
        self.start_game("snake.exe")

    def start_plane_fight_game(self):
        """启动飞机大战游戏"""
        self.start_game("planefight.exe")

    def start_game(self, game_exe):
        """通用启动游戏方法"""
        current_directory = sys.path[0]  # 获取当前 Python 脚本的目录
        executable = f"{current_directory}/{game_exe}"  # 游戏exe文件路径

        try:
            # 启动命令提示符并运行游戏
            subprocess.Popen(['cmd', '/C', 'start', 'cmd', '/K', 'chcp 65001 && ' + executable])
            print(f"游戏 {game_exe} 已启动！")
        except Exception as e:
            print(f"无法启动游戏 {game_exe}: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SmallGamesWindow()
    window.show()
    sys.exit(app.exec_())