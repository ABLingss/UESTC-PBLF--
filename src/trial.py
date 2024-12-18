import sys
from PyQt5 import QtWidgets
from login import Ui_MainWindow as LoginUi
from main import Ui_MainInterface as MainUi

class LoginWindow(QtWidgets.QMainWindow, LoginUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        # 假设登录验证通过
        print("登录成功")
        self.main_window = MainInterface()  
        self.main_window.show()  
        self.close()

class MainInterface(QtWidgets.QMainWindow, MainUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
