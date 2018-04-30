# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Coding\RailwayInfoSys\registerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Register(object):
    def setupUi(self, Register):
        Register.setObjectName("Register")
        Register.resize(400, 300)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        Register.setFont(font)
        Register.setSizeGripEnabled(True)
        self.button_commit = QtWidgets.QPushButton(Register)
        self.button_commit.setGeometry(QtCore.QRect(80, 230, 91, 31))
        self.button_commit.setObjectName("button_commit")
        self.button_cancel = QtWidgets.QPushButton(Register)
        self.button_cancel.setGeometry(QtCore.QRect(210, 230, 91, 31))
        self.button_cancel.setObjectName("button_cancel")
        self.label_4 = QtWidgets.QLabel(Register)
        self.label_4.setGeometry(QtCore.QRect(70, 30, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.line = QtWidgets.QFrame(Register)
        self.line.setGeometry(QtCore.QRect(70, 60, 251, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget = QtWidgets.QWidget(Register)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 80, 250, 131))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineedit_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineedit_name.setText("")
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
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineedit_pwconfirm = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineedit_pwconfirm.setText("")
        self.lineedit_pwconfirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineedit_pwconfirm.setObjectName("lineedit_pwconfirm")
        self.gridLayout.addWidget(self.lineedit_pwconfirm, 2, 1, 1, 1)

        self.retranslateUi(Register)
        self.button_commit.clicked.connect(self.Submit)
        self.button_cancel.clicked.connect(self.Cancel)
        QtCore.QMetaObject.connectSlotsByName(Register)

    def retranslateUi(self, Register):
        _translate = QtCore.QCoreApplication.translate
        Register.setWindowTitle(_translate("Register", "注册 - 铁路信息查询系统"))
        self.button_commit.setText(_translate("Register", "提交"))
        self.button_cancel.setText(_translate("Register", "取消"))
        self.label_4.setText(_translate("Register", "用户注册"))
        self.label.setText(_translate("Register", "用户名："))
        self.label_2.setText(_translate("Register", "密码："))
        self.label_3.setText(_translate("Register", "确认密码："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Register = QtWidgets.QDialog()
    ui = Ui_Register()
    ui.setupUi(Register)
    Register.show()
    sys.exit(app.exec_())

