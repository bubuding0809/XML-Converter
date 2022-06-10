from PyQt5 import QtCore, QtGui, QtWidgets

class ButtonWithIcon(QtWidgets.QPushButton):
    def __init__(self, pixmap, text='', parent=None):
        super(ButtonWithIcon, self).__init__(parent)
        self.setPixmap(pixmap)
        self.setText(text)
        self.setObjectName('CustomButton')

    def setPixmap(self, pixmap):
        self.pixmap = pixmap

    def sizeHint(self):
        parent_size = QtWidgets.QPushButton.sizeHint(self)
        return QtCore.QSize(parent_size.width() + self.pixmap.width(), max(parent_size.height(), self.pixmap.height()))

    def paintEvent(self, event):
        QtWidgets.QPushButton.paintEvent(self, event)

        # hardcoded left padding for pixmap
        pos_x = 4
        pos_y = (self.height() - self.pixmap.height()) / 2

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

        #
        painter.drawPixmap(int(pos_x), int(pos_y), self.pixmap)


    