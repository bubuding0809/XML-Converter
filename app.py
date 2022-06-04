from UiMainWindow import Ui_MainWindow
from components.testStepGroupBox import TestStepGroupBox
from components.collapseableWidget import CollapsibleBox

from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)

import sys
import XML_parser
import subprocess
import random


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        #Initialize UI to main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Event connectors
        self.ui.xlsxConfig_input_btn.clicked.connect(self.handleXLSXInput)
        self.ui.xml_input_btn.clicked.connect(self.handleXMLInput)
        self.ui.fileLocation_input_btn.clicked.connect(self.handleXMLOutput)
        self.ui.xml_convert_btn.clicked.connect(self.handleXMLConvert)
        self.ui.xml_loadData_btn.clicked.connect(self.handleXMLLoad)
        
        #Global variables
        self.xlsxInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/config.xlsx'
        self.xmlInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/input.xml'
        self.xmlOutFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/output.xml'

        
        self.ui.xlsxConfig_input_label.setText(self.xmlInFile)
        self.ui.xml_input_label.setText(self.xmlInFile)
        self.ui.fileLocation_input_label.setText(self.xmlOutFile)
        
    #************************* Event Handler methods ****************************#
    def handleXLSXInput(self):
        file = qtw.QFileDialog.getOpenFileName(self, 'Input config XLSX file', directory='', filter='Xlsx files (*.xlsx)')
        if file:
            self.xlsxInFile = file[0]
            
            self.ui.xlsxConfig_input_label.setText(file[0])
            
        
    def handleXMLInput(self):
        file = qtw.QFileDialog.getOpenFileName(self, 'Input ATP XML file', directory='', filter='XML files (*.xml)' )
        
        if file:
            self.xmlInFile = file[0]
            
            self.ui.xml_input_label.setText(file[0])

            
    def handleXMLOutput(self):
        file = qtw.QFileDialog.getSaveFileName(self, 'Save converted ATP XML file', directory='')
        filePath = file[0]
        
        if len(filePath):
            self.xmlOutFile = filePath + '.xml'
            
            self.ui.fileLocation_input_label.setText(filePath + '.xml')
            
            
    def handleXMLConvert(self):
        if not self.xlsxInFile or not self.xmlInFile or not self.xmlOutFile:
            
            #Create error message box
            qtw.QMessageBox.critical(self, 'Error', 'Ensure all required fields are filled')
            return print('Ensure all required fields are filled')

        #Execute XML conversion
        atpMap = XML_parser.handleXlsx(self.xlsxInFile)
        XML_parser.convertXML(self.xmlInFile, self.xmlOutFile, atpMap)
        
        #Create success message box
        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle("Success")
        msgBox.setText("Successfully converted ATP XML file")
        msgBox.setIcon(qtw.QMessageBox.Information)
        checkbox = qtw.QCheckBox('Show file in explorer', msgBox)
        checkbox.setChecked(True)
        msgBox.setCheckBox(checkbox)
        
        ret = msgBox.exec_()
        
        if checkbox.isChecked():
            subprocess.call(["open", "-R", self.xmlOutFile])
        
        
    def handleXMLLoad(self):
        for i in range(10):
            self.createCollapseableBox()
    
            
    def createCollapseableBox(self):
        box = CollapsibleBox(title='testcase')
        self.ui.verticalLayout_3.insertWidget(0, box)
        
        # Create vertical layout for each collapsible box
        vlayout = qtw.QVBoxLayout()
        
        for i in range(10):
            testStepBox = TestStepGroupBox(title='test step')
            vlayout.addWidget(testStepBox)

        box.setContentLayout(vlayout)
        
    
    def testLoadData(self):
        for i in range(20):
            testStepBox = TestStepGroupBox(title=f'teststep {i}')
            self.ui.verticalLayout_3.insertWidget(0, testStepBox)
            
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1980, 1080)
    mainWindow.show()
    
    sys.exit(app.exec_())
