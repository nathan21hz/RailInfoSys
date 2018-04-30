# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Coding\RailwayInfoSys\loginWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(330, 220)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        Login.setFont(font)
        Login.setSizeGripEnabled(True)
        self.pushButton = QtWidgets.QPushButton(Login)
        self.pushButton.setGeometry(QtCore.QRect(40, 140, 71, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Login)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 140, 71, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Login)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 140, 71, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.layoutWidget = QtWidgets.QWidget(Login)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 40, 235, 81))
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

        self.retranslateUi(Login)
        self.pushButton.clicked.connect(self.Login)
        self.pushButton_2.clicked.connect(self.Register)
        self.pushButton_3.clicked.connect(self.Cancel)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "登陆"))
        self.pushButton.setText(_translate("Login", "登陆"))
        self.pushButton_2.setText(_translate("Login", "注册"))
        self.pushButton_3.setText(_translate("Login", "取消"))
        self.label.setText(_translate("Login", "用户名："))
        self.label_2.setText(_translate("Login", "密码："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QDialog()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())

