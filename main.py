from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 150, 600, 450))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 361, 31))
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 50, 361, 31))
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(490, 40, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(490, 10, 101, 22))
        self.comboBox.addItem("Схема")
        self.comboBox.addItem("Спутник")
        self.comboBox.addItem("Гибрид")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setGeometry(QtCore.QRect(380, 90, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)

        self.retranslateUi()

    def retranslateUi(self):
        self.pushButton.setText("Search")
        self.pushButton_2.setText("Reset")
        self.checkBox.setText("PostIndex")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())
