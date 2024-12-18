# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comment.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CommentManagementWindow(object):
    def setupUi(self, CommentManagementWindow):
        CommentManagementWindow.setObjectName("CommentManagementWindow")
        CommentManagementWindow.resize(800, 602)
        self.centralwidget = QtWidgets.QWidget(CommentManagementWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.commentLabel = QtWidgets.QLabel(self.centralwidget)
        self.commentLabel.setObjectName("commentLabel")
        self.verticalLayout.addWidget(self.commentLabel)
        self.commentTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.commentTextEdit.setObjectName("commentTextEdit")
        self.verticalLayout.addWidget(self.commentTextEdit)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setObjectName("buttonLayout")
        self.submitCommentButton = QtWidgets.QPushButton(self.centralwidget)
        self.submitCommentButton.setObjectName("submitCommentButton")
        self.buttonLayout.addWidget(self.submitCommentButton)
        self.backToMainButton = QtWidgets.QPushButton(self.centralwidget)
        self.backToMainButton.setObjectName("backToMainButton")
        self.buttonLayout.addWidget(self.backToMainButton)
        self.verticalLayout.addLayout(self.buttonLayout)
        CommentManagementWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CommentManagementWindow)
        QtCore.QMetaObject.connectSlotsByName(CommentManagementWindow)

    def retranslateUi(self, CommentManagementWindow):
        _translate = QtCore.QCoreApplication.translate
        CommentManagementWindow.setStyleSheet(_translate("CommentManagementWindow", "QMainWindow {\n"
"    background-color: #F5F5F5;\n"
"    font-family: \'Segoe UI\', sans-serif;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #0078D7;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    color: white;\n"
"    padding: 10px;\n"
"    min-width: 150px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #005FAC;\n"
"}\n"
"\n"
"QTextEdit {\n"
"    border: 1px solid #ccc;\n"
"    font-size: 14px;\n"
"    color: #333;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel {\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    color: #333;\n"
"}"))
        self.commentLabel.setText(_translate("CommentManagementWindow", "添加评论"))
        self.commentTextEdit.setPlaceholderText(_translate("CommentManagementWindow", "请输入您的评论..."))
        self.submitCommentButton.setText(_translate("CommentManagementWindow", "提交评论"))
        self.backToMainButton.setText(_translate("CommentManagementWindow", "返回主界面"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CommentManagementWindow = QtWidgets.QMainWindow()
    ui = Ui_CommentManagementWindow()
    ui.setupUi(CommentManagementWindow)
    CommentManagementWindow.show()
    sys.exit(app.exec_())
    CommentManagementWindow.close()
    sys.exit(0)
