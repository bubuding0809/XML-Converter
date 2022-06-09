from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
from TestStepGroupBox import TestStepGroupBox
from CollapseableWidget import CollapsibleBox
import sys
        
class MainWindow(qtw.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.testdata = {
            'id': 1,
            'parentName': 'testcase1',
            'old': {
                'description': 'testDescription',
                'function_library': 'testLibrary',
                'function_name': 'testname',
                'function_parameters': []
            },
            'new': {
                'description': 'testDescription',
                'function_library': 'testLibrary',
                'function_name': 'testname',
                'function_parameters': []
            }
        }
        self.teststepList = []
        self.collapsibleBoxList = []
        
        self.centralWidget = qtw.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.vLayout_central = qtw.QVBoxLayout(self.centralWidget)
        
        self.searchBar = qtw.QLineEdit()
        self.vLayout_central.addWidget(self.searchBar)
        
        self.scrollArea = qtw.QScrollArea(self.centralWidget)
        self.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = qtw.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.vLayout_scrollArea = qtw.QVBoxLayout(self.scrollAreaWidget)
        
        self.vLayout_central.addWidget(self.scrollArea)
        
        for i in range(10):
            collapsibleBox = CollapsibleBox(title=str(i), parent=self)
            vLayout_collapsibleBox = qtw.QVBoxLayout()

            for i in range(20):
                searchItem = TestStepGroupBox(title=f'testItem_{i}', parent=self, data=self.testdata)
                vLayout_collapsibleBox.addWidget(searchItem)
                self.teststepList.append(searchItem)
                
                collapsibleBox.setContentLayout(vLayout_collapsibleBox)

            vLayout_collapsibleBox.addStretch()
            self.vLayout_scrollArea.addWidget(collapsibleBox)
            self.collapsibleBoxList.append(collapsibleBox)

        self.vLayout_scrollArea.addStretch()
            
        self.autoCompleter = qtw.QCompleter(list({teststep.title for teststep in self.teststepList}))
        self.autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.searchBar.setCompleter(self.autoCompleter)

        # Event signal connectors
        self.searchBar.textChanged.connect(self.handleSearchBar)
        
        
    # Event handler methods
    def handleSearchBar(self, text):
        for teststep in self.teststepList:
            if text.lower() in teststep.title.lower():
                teststep.show()
            else:
                teststep.hide()
                
        for index, box in enumerate(self.collapsibleBoxList):
            print(box.layout().sizeHint(), box.layout().minimumSize())
            print(box.content_area.geometry().height())
        


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1980, 1080)
    mainWindow.show()
    
    sys.exit(app.exec_())