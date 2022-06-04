import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)
        self.title = title
        #Toggle button
        self.toggle_button = QtWidgets.QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(
            maximumHeight=0, minimumHeight=0
        )
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
        )
        
    @QtCore.pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        
        self.toggle_button.setArrowType(QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow)
        self.toggle_animation.setDirection(QtCore.QAbstractAnimation.Forward if not checked else QtCore.QAbstractAnimation.Backward)
        
        self.toggle_animation.start()
        
    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

    def __str__(self):
        return self.title
        
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()

            
    def initUi(self):
        centralWidget = QtWidgets.QWidget(self)
        
        # Create vertical layout for central widget
        self.verticalLayout = QtWidgets.QVBoxLayout(centralWidget)
        
        # Set main window's central widget to central wdiget
        self.setCentralWidget(centralWidget)
        
        # Create scroll area to contain data
        scroll = QtWidgets.QScrollArea()
        
        # Add scroll area to the central widget's vertical layout
        self.verticalLayout.addWidget(scroll)
        
        # Create contentwidget for scroll area
        scrollContentWidget = QtWidgets.QWidget()
        
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        scroll.setWidget(scrollContentWidget)
        scroll.setWidgetResizable(True)
        
        # Create vertical layout for scroll area
        self.vlay = QtWidgets.QVBoxLayout(scrollContentWidget)
        
        boxList = []
        # Create 10 CollapsibleBox
        for i in range(10):
            box = CollapsibleBox("Collapsible Box Header-{}".format(i))
            self.vlay.addWidget(box)
            
            # Create vertical layout for each collapsible box
            lay = QtWidgets.QVBoxLayout()
            
            # Create x label with random color for each collapseable box
            for j in range(20):
                
                #Create lable widget and apply a random color to it
                label = QtWidgets.QLabel("{}".format(j))
                color = QtGui.QColor(*[random.randint(0, 255) for _ in range(3)])
                label.setStyleSheet("background-color: {}; color : white;".format(color.name()))
                label.setAlignment(QtCore.Qt.AlignCenter)
                lay.addWidget(label)

            box.setContentLayout(lay)
            boxList.append(box)
            
        self.vlay.addStretch()
        
        toggle_allDropDow_btn = QtWidgets.QPushButton(parent=self, text='Show all')
        toggle_allDropDow_btn.setCheckable(True)
        
        delete_btn = QtWidgets.QPushButton(parent=self, text='Delete all boxes')
        
        self.verticalLayout.insertWidget(0, toggle_allDropDow_btn)
        self.verticalLayout.insertWidget(0, delete_btn)
        
        #Initialize event connectors
        toggle_allDropDow_btn.pressed.connect(lambda: self.HandleToggleAllDropDownBtn(boxList))
        delete_btn.clicked.connect(self.handleDeleteAllBoxes)
        
    def HandleToggleAllDropDownBtn(self, boxList):
        eventSender = self.sender()
        isChecked = eventSender.isChecked()
        
        eventSender.setText('Hide all' if not isChecked else 'Show all')
        for box in boxList:
            box.toggle_button.setChecked(isChecked)
            box.on_pressed()
            box.toggle_button.setChecked(not isChecked)
    
    def handleDeleteAllBoxes(self):
        while self.vlay.count():
            item = self.vlay.takeAt(0)
            print(item.widget())
            if item.widget():
                item.widget().deleteLater()
        

        
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    # Create main window and show
    mainWindow = MainWindow()
    mainWindow.resize(1980, 1080)
    mainWindow.show()
    
    sys.exit(app.exec_())