import sys
from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidgetLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 780, 539))
        self.scrollAreaWidgetLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
        self.scrollAreaWidgetLayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.buttonWidget = QtWidgets.QWidget(self.centralwidget)
        self.buttonAddGroupBox = QtWidgets.QPushButton('Add GroupBox', self.buttonWidget)
        self.buttonDeleteLaterGroupBox = QtWidgets.QPushButton('DeleteLater GroupBox', self.buttonWidget)
        self.buttonRemoveItemGroupBox = QtWidgets.QPushButton('RemoveItem GroupBox', self.buttonWidget)
        self.buttonRemoveWidgetGroupBox = QtWidgets.QPushButton('RemoveWidget GroupBox', self.buttonWidget)
        self.buttonLayout = QtWidgets.QGridLayout(self.buttonWidget)
        self.buttonLayout.addWidget(self.buttonAddGroupBox,          0, 0, 1, 1)
        self.buttonLayout.addWidget(self.buttonDeleteLaterGroupBox,  0, 1, 1, 1)
        self.buttonLayout.addWidget(self.buttonRemoveItemGroupBox,   1, 0, 1, 1)
        self.buttonLayout.addWidget(self.buttonRemoveWidgetGroupBox, 1, 1, 1, 1)
        
        self.centralwidgetLayout.addWidget(self.buttonWidget)
        self.centralwidgetLayout.addWidget(self.scrollArea)
        self.setCentralWidget(self.centralwidget)

        self.buttonAddGroupBox.clicked.connect(self.addGroupBox)
        self.buttonDeleteLaterGroupBox.clicked.connect(self.deleteLaterGroupBox)
        self.buttonRemoveItemGroupBox.clicked.connect(self.removeItemGroupBox)
        self.buttonRemoveWidgetGroupBox.clicked.connect(self.removeWidgetGroupBox)

    def addGroupBox(self):
        count = self.scrollAreaWidgetLayout.count() - 1
        groupBox = QtWidgets.QGroupBox('GroupBox ' + str(count), self.scrollAreaWidget)
        self.scrollAreaWidgetLayout.insertWidget(count, groupBox)

        comboBox = QtWidgets.QComboBox(groupBox)
        comboBox.addItems(['val1', 'val2', 'val3'])

        gridLayout = QtWidgets.QGridLayout(groupBox)
        gridLayout.addWidget(QtWidgets.QLabel('Label ' + str(count), groupBox),       0, 0, 1, 1)
        gridLayout.addWidget(QtWidgets.QLineEdit('LineEdit ' + str(count), groupBox), 0, 1, 1, 1)
        gridLayout.addWidget(comboBox,                                                1, 0, 1, 1)
        gridLayout.addWidget(QtWidgets.QSlider(QtCore.Qt.Horizontal, groupBox),       1, 1, 1, 1)

    def deleteLaterGroupBox(self):
        count = self.scrollAreaWidgetLayout.count()
        if count == 1:
            return
        item = self.scrollAreaWidgetLayout.itemAt(count - 2)
        widget = item.widget()
        widget.deleteLater()

    def removeItemGroupBox(self):
        count = self.scrollAreaWidgetLayout.count()
        if count == 1:
            return
        item = self.scrollAreaWidgetLayout.itemAt(count - 2)
        self.scrollAreaWidgetLayout.removeItem(item)

    def removeWidgetGroupBox(self):
        count = self.scrollAreaWidgetLayout.count()
        if count == 1:
            return
        item = self.scrollAreaWidgetLayout.itemAt(count - 2)
        widget = item.widget()
        self.scrollAreaWidgetLayout.removeWidget(widget)

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec()

if __name__ == '__main__':
    main()