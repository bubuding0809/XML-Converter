from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
from sqlalchemy import true
from TestStepGroupBox import TestStepGroupBox
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
        
        for i in range(100):
            searchItem = TestStepGroupBox(title=f'testItem_{i}', parent=self, data=self.testdata)
            self.teststepList.append(searchItem)
            self.vLayout_scrollArea.addWidget(searchItem)
        
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

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1980, 1080)
    mainWindow.show()
    
    sys.exit(app.exec_())