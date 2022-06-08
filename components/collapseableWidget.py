import random
import sys
from PyQt5 import (
    QtCore as qtc,
    QtGui as qtg,
    QtWidgets as qtw
)



class CollapsibleBox(qtw.QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)
        self.title = title
        
        # Toggle button
        self.toggle_button = qtw.QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setFont(qtg.QFont('Arial', 12))
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        self.toggle_button.setIconSize(qtc.QSize(10, 10))
        self.toggle_button.setToolButtonStyle(qtc.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(qtc.Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.content_area = qtw.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.content_area.setFrameShape(qtw.QFrame.NoFrame | qtw.QFrame.Raised)

        # Vertical layout for collapseable box to contain toggle button and content area
        lay = qtw.QVBoxLayout()
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)
        self.setLayout(lay)

        # Toggle animation for content area
        self.toggle_animation = qtc.QParallelAnimationGroup(self)
        self.toggle_animation.addAnimation(
            qtc.QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            qtc.QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            qtc.QPropertyAnimation(self.content_area, b"maximumHeight")
        )
        
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        
        self.toggle_button.setArrowType(qtc.Qt.DownArrow if not checked else qtc.Qt.RightArrow)
        self.toggle_animation.setDirection(qtc.QAbstractAnimation.Forward if not checked else qtc.QAbstractAnimation.Backward)
        
        self.toggle_animation.start()
        
    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = layout.sizeHint().height()
        
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(50)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(50)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

    def __str__(self):
        return self.title
        
class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()
       
    def initUi(self):
        centralWidget = qtw.QWidget(self)
        
        # Create vertical layout for central widget
        self.verticalLayout = qtw.QVBoxLayout(centralWidget)
        
        # Set main window's central widget to central wdiget
        self.setCentralWidget(centralWidget)
        
        # Create scroll area to contain data
        scroll = qtw.QScrollArea()
        
        # Add scroll area to the central widget's vertical layout
        self.verticalLayout.addWidget(scroll)
        
        # Create contentwidget for scroll area
        scrollContentWidget = qtw.QWidget()
        
        scroll.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)

        scroll.setWidget(scrollContentWidget)
        scroll.setWidgetResizable(True)
        
        # Create vertical layout for scroll area
        self.vlay = qtw.QVBoxLayout(scrollContentWidget)
        
        boxList = []
        # Create 10 CollapsibleBox
        for i in range(10):
            box = CollapsibleBox(f"Collapsible Box Header-{i}")
            self.vlay.addWidget(box)
            
            # Create vertical layout for each collapsible box
            lay = qtw.QVBoxLayout()
            
            # Create x label with random color for each collapseable box
            for j in range(20):
                
                #Create lable widget and apply a random color to it
                label = qtw.QLabel("{}".format(j))
                color = qtg.QColor(*[random.randint(0, 255) for _ in range(3)])
                label.setStyleSheet("background-color: {}; color : white;".format(color.name()))
                label.setAlignment(qtc.Qt.AlignCenter)
                lay.addWidget(label)

            box.setContentLayout(lay)
            boxList.append(box)
            
        self.vlay.addStretch()
        
        toggle_allDropDow_btn = qtw.QPushButton(parent=self, text='Show all')
        toggle_allDropDow_btn.setCheckable(True)
        
        delete_btn = qtw.QPushButton(parent=self, text='Delete all boxes')
        
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

    app = qtw.QApplication(sys.argv)

    # Create main window and show
    mainWindow = MainWindow()
    mainWindow.resize(1980, 1080)
    mainWindow.show()
    
    sys.exit(app.exec_())