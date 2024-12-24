# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutUsWindow(object):
    def setupUi(self, AboutUsWindow):
        AboutUsWindow.setObjectName("AboutUsWindow")
        AboutUsWindow.resize(800, 602)
        self.centralwidget = QtWidgets.QWidget(AboutUsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")

        # 设置标题标签
        self.aboutUsTitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.aboutUsTitleLabel.setObjectName("aboutUsTitleLabel")
        self.verticalLayout.addWidget(self.aboutUsTitleLabel)

        # 设置滚动区域
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        # 滚动区域内容
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 750, 500))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(750, 500))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setObjectName("scrollAreaLayout")

        # 添加团队成员标签
        self.teamMemberLabel1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.teamMemberLabel1.setObjectName("teamMemberLabel1")
        self.scrollAreaLayout.addWidget(self.teamMemberLabel1)

        self.teamMemberLabel2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.teamMemberLabel2.setObjectName("teamMemberLabel2")
        self.scrollAreaLayout.addWidget(self.teamMemberLabel2)

        self.teamMemberLabel3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.teamMemberLabel3.setObjectName("teamMemberLabel3")
        self.scrollAreaLayout.addWidget(self.teamMemberLabel3)

        self.teamMemberLabel4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.teamMemberLabel4.setObjectName("teamMemberLabel4")
        self.scrollAreaLayout.addWidget(self.teamMemberLabel4)

        self.teamMemberLabel5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.teamMemberLabel5.setObjectName("teamMemberLabel5")
        self.scrollAreaLayout.addWidget(self.teamMemberLabel5)

        self.teamMemberLabel6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.teamMemberLabel6.setObjectName("teamMemberLabel6")
        self.scrollAreaLayout.addWidget(self.teamMemberLabel6)

        self.teamMemberLabel7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.teamMemberLabel7.setObjectName("teamMemberLabel7")
        self.scrollAreaLayout.addWidget(self.teamMemberLabel7)

        self.teamMemberLabel8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.teamMemberLabel8.setObjectName("teamMemberLabel8")
        self.scrollAreaLayout.addWidget(self.teamMemberLabel8)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # 设置返回按钮
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setObjectName("backButton")
        self.buttonLayout.addWidget(self.backButton)
        self.verticalLayout.addLayout(self.buttonLayout)

        AboutUsWindow.setCentralWidget(self.centralwidget)

        # 设置样式表
        AboutUsWindow.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
                font-family: 'Segoe UI', sans-serif;
                background-image: 
                    url("D:/python/pythonProject1/frontend/assets/D315856FD459A2B52B8D781C3CFCC3D2.png")
                    url("D:/python/pythonProject1/frontend/assets/0D0F18143C6225D0B9868C8044758203.png")
                    url("D:/python/pythonProject1/frontend/assets/0D0F18143C6225D0B9868C8044758203.png");
                    
                background-position: top left, top right, bottom left;
                background-repeat: no-repeat, no-repeat, no-repeat;
                background-size: contain;
            }

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

            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }

            QScrollArea {
                border: none;
            }

            QTextEdit {
                border: 1px solid #ccc;
                font-size: 14px;
                color: #333;
                padding: 10px;
                background-color: #F5F5F5;
            }
        """)

        self.retranslateUi(AboutUsWindow)
        QtCore.QMetaObject.connectSlotsByName(AboutUsWindow)

    def retranslateUi(self, AboutUsWindow):
        _translate = QtCore.QCoreApplication.translate
        AboutUsWindow.setWindowTitle(_translate("AboutUsWindow", "关于我们"))

        # 设置团队成员信息
        self.aboutUsTitleLabel.setText(_translate("AboutUsWindow", "关于我们"))
        self.teamMemberLabel1.setText(_translate("AboutUsWindow", "张三 - 项目经理"))
        self.teamMemberLabel2.setText(_translate("AboutUsWindow", "李四 - 后端开发"))
        self.teamMemberLabel3.setText(_translate("AboutUsWindow", "王五 - 前端开发"))
        self.teamMemberLabel4.setText(_translate("AboutUsWindow", "赵六 - 测试工程师"))
        self.teamMemberLabel5.setText(_translate("AboutUsWindow", "孙七 - UI设计师"))
        self.teamMemberLabel6.setText(_translate("AboutUsWindow", "周八 - 数据分析师"))
        self.teamMemberLabel7.setText(_translate("AboutUsWindow", "吴九 - 系统架构师"))
        self.teamMemberLabel8.setText(_translate("AboutUsWindow", "郑十 - 流程优化专家"))

        # 设置返回按钮文本
        self.backButton.setText(_translate("AboutUsWindow", "返回主菜单"))


def main():
    # 初始化应用
    app = QtWidgets.QApplication(sys.argv)

    # 创建主窗口对象
    AboutUsWindow = QtWidgets.QMainWindow()

    # 设置UI
    ui = Ui_AboutUsWindow()
    ui.setupUi(AboutUsWindow)

    # 显示窗口
    AboutUsWindow.show()

    # 运行应用
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
