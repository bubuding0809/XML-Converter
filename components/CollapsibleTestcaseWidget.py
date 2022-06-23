import random
import sys
from PyQt5 import (
    QtCore as qtc,
    QtGui as qtg,
    QtWidgets as qtw
)



class CollapsibleTestcaseWidget(qtw.QWidget):
    def __init__(self, title="", data=None, parent=None):
        super(CollapsibleTestcaseWidget, self).__init__(parent)

        #* Initialize some meta attributes for the widgt
        self.title = title
        self.data = data
        self.id = data['id']
        self.type = data['type']
        self.teststeps = data['teststeps']
        self.teststepsCount = len(self.teststeps)
        self.isChecked = False
        
        #* Toggle button
        self.toggle_button = qtw.QToolButton(
            text=f"{title} ({self.teststepsCount}/{self.teststepsCount})", 
            checkable=True, 
            checked=False
        )
        self.toggle_button.setFont(qtg.QFont('Arial', 12))
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        self.toggle_button.setIconSize(qtc.QSize(10, 10))
        self.toggle_button.setToolButtonStyle(qtc.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(qtc.Qt.RightArrow)

        self.content_area = qtw.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.content_area.setFrameShape(qtw.QFrame.Panel | qtw.QFrame.Raised)


        #* Vertical layout for collapseable box to contain toggle button and content area
        lay = qtw.QVBoxLayout()
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)
        self.setLayout(lay)

        #* Greate parallel animation group for components of collapsible box
        self.ToggleDropDownAnimationGroup = qtc.QParallelAnimationGroup(self)
        self.ToggleDropDownAnimationGroup.addAnimation(
            qtc.QPropertyAnimation(self, b"minimumHeight")
        )
        self.ToggleDropDownAnimationGroup.addAnimation(
            qtc.QPropertyAnimation(self, b"maximumHeight")
        )
        self.ToggleDropDownAnimationGroup.addAnimation(
            qtc.QPropertyAnimation(self.content_area, b"maximumHeight")
        )
        self.ToggleDropDownAnimationGroup.addAnimation(
            qtc.QPropertyAnimation(self.content_area, b"minimumHeight")
        )

        #* Signal connector
        self.toggle_button.pressed.connect(self.HandleDropDown)
        


    def HandleDropDown(self):
        content_height = self.content_area.layout().sizeHint().height()

        #* Iterate through parallel animation group to set animation parameters
        for i in range(self.ToggleDropDownAnimationGroup.animationCount() - 1):
            animation = self.ToggleDropDownAnimationGroup.animationAt(i)
            animation.setStartValue(26)
            animation.setEndValue(26 + content_height)        

        for i in range(2,4):
            content_animation = self.ToggleDropDownAnimationGroup.animationAt(i)
            content_animation.setDuration(100)
            content_animation.setStartValue(0)
            content_animation.setEndValue(content_height)


        self.toggle_button.setArrowType(qtc.Qt.DownArrow if not self.isChecked else qtc.Qt.RightArrow)
        self.ToggleDropDownAnimationGroup.setDirection(qtc.QAbstractAnimation.Forward if not self.isChecked else qtc.QAbstractAnimation.Backward)
        
        self.ToggleDropDownAnimationGroup.start()

        #* Toggle tool button check status
        self.isChecked = not self.isChecked
        


    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        
        self.content_area.setLayout(layout)
        content_height = layout.sizeHint().height()
        
        #* Iterate through parallel animation group to set animation parameters
        for i in range(self.ToggleDropDownAnimationGroup.animationCount()):
            animation = self.ToggleDropDownAnimationGroup.animationAt(i)
            animation.setDuration(100)
            animation.setStartValue(26 if i < 2 else 0)
            animation.setEndValue(26 + content_height if i < 2 else content_height)


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
            box = CollapsibleTestcaseWidget(f"Collapsible Box Header-{i}")
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