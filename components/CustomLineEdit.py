from PyQt5 import QtGui, QtCore, QtWidgets
from .resources import bootstrap_rc
import sys, os, subprocess



baseDir = os.path.dirname(__file__)



class CustomLineEdit(QtWidgets.QLineEdit):
    def __init__(self, icon_file, placeholderText='', parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.setObjectName('CustomLineEdit')

        self.setClearButtonEnabled(True)
        self.setPlaceholderText(placeholderText)

        #*Create left aligned QLabel Icon
        self.icon = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(icon_file).scaled(15, 15, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.icon.setPixmap(pixmap)
        self.icon.setStyleSheet('border: 0px; padding: 0px;')



    def resizeEvent(self, event):
        iconSize = self.icon.sizeHint()
        self.icon.move(
            self.rect().left() + 5,
            int((self.rect().bottom()-iconSize.height()+1) / 2)
        )
        super(CustomLineEdit, self).resizeEvent(event)



    def handleClearLineEdit(self):
        self.setText('')




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = CustomLineEdit(':/icons/bootstrap-icons-1.8.3/search.svg', 'Search')
    with open(os.path.join(baseDir, '../static/style.qss'), 'r') as file:
        stylesheet = file.read()
    main.setStyleSheet(stylesheet)
    main.show()

    sys.exit(app.exec_())