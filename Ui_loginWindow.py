# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Coding\RailwayInfoSys\loginWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(330, 220)
        Login.setMinimumSize(QtCore.QSize(330, 220))
        Login.setMaximumSize(QtCore.QSize(330, 220))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        Login.setFont(font)
        Login.setSizeGripEnabled(True)
        self.layoutWidget = QtWidgets.QWidget(Login)
        self.layoutWidget.setGeometry(QtCore.QRect(44, 70, 241, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineedit_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineedit_name.setObjectName("lineedit_name")
        self.gridLayout.addWidget(self.lineedit_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineedit_password = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineedit_password.setText("")
        self.lineedit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineedit_password.setObjectName("lineedit_password")
        self.gridLayout.addWidget(self.lineedit_password, 1, 1, 1, 1)
        self.line = QtWidgets.QFrame(Login)
        self.line.setGeometry(QtCore.QRect(40, 50, 251, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_4 = QtWidgets.QLabel(Login)
        self.label_4.setGeometry(QtCore.QRect(40, 20, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.layoutWidget1 = QtWidgets.QWidget(Login)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 160, 251, 30))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 2, 1, 1)

        self.retranslateUi(Login)
        self.pushButton.clicked.connect(self.Login)
        self.pushButton_2.clicked.connect(self.Register)
        self.pushButton_3.clicked.connect(self.Cancel)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "登陆 - 铁路信息查询系统"))
        self.label.setText(_translate("Login", "用户名："))
        self.label_2.setText(_translate("Login", "密码："))
        self.label_4.setText(_translate("Login", "用户登陆"))
        self.pushButton.setText(_translate("Login", "登陆"))
        self.pushButton_2.setText(_translate("Login", "注册"))
        self.pushButton_3.setText(_translate("Login", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QDialog()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())

