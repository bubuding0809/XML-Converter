from components.UiMainWindow import Ui_MainWindow
from components.TestStepGroupBox import TestStepGroupBox
from components.CollapseableWidget import CollapsibleBox
from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
import sys
import XML_parser
import subprocess


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
        self.ui.toggle_dropdown_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        self.ui.xml_clearTeststeps_btn.clicked.connect(self.clearTestStepScrollArea)
        self.ui.selectAll_checkBox.pressed.connect(self.handleSelectAllCheckBox)
        
        #Global variables
        self.xlsxInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/config.xlsx'
        self.xmlInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/input.xml'
        self.xmlOutFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/output.xml'

        #Global flags
        self.testCaseBoxList = {}
        self.ui.xlsxConfig_input_label.setText(self.xmlInFile)
        self.ui.xml_input_label.setText(self.xmlInFile)
        self.ui.fileLocation_input_label.setText(self.xmlOutFile)
        
        
        
    # ************************* Event Handler methods **************************** #
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
        # Clear data grid of and old data
        self.clearTestStepScrollArea()
        
        # Enable toggle drop down button and set it to unchecked
        self.ui.toggle_dropdown_btn.setEnabled(True)
        self.ui.toggle_dropdown_btn.setChecked(False)
        self.ui.toggle_dropdown_btn.setText('Show all')
        
        # Enable select all checkbox and set it to checked
        self.ui.selectAll_checkBox.setEnabled(True)
        self.ui.selectAll_checkBox.setChecked(True)
        
        atpMap = XML_parser.handleXlsx(self.xlsxInFile)
        dataList = XML_parser.getTestStepData(self.xmlInFile, atpMap)

        # Filter teststeps into their respective testcases
        testCaseList = {}
        for dataPair in dataList:
            if dataPair['parentId'] not in testCaseList:
                testCaseList[dataPair['parentId']] = [{
                    'parentName': dataPair['parentName'],
                    'old': dataPair['old'],
                    'new': dataPair['new']
                }]
            else:
                testCaseList[dataPair['parentId']].append({
                    'old': dataPair['old'],
                    'new': dataPair['new']
                })
            
        
        for index, (testcase, teststeps) in enumerate(testCaseList.items()):
            # Create collapsible box for test case
            box = CollapsibleBox(title=f"name: {teststeps[0]['parentName']}\nid: {testcase}")
            self.ui.verticalLayout_3.insertWidget(index, box)
            
            # Create vertical layout for each collapsible box
            vlayout = qtw.QVBoxLayout()
            
            testStepBoxList = []
            for teststep in teststeps:
                testStepBox = TestStepGroupBox(data=teststep)
                vlayout.addWidget(testStepBox)
                testStepBoxList.append(testStepBox)

            box.setContentLayout(vlayout)
            self.testCaseBoxList[box] = testStepBoxList
        
        self.ui.verticalLayout_3.addStretch()
        
        
        for testCaseBox, testStepBoxList in self.testCaseBoxList.items():
            print(testCaseBox)
       
       
    def handleToggleAllDropDownBtn(self):
        eventSender = self.sender()
        isChecked = eventSender.isChecked()
        
        eventSender.setText('Hide all' if not isChecked else 'Show all')
        
        
        for box in self.testCaseBoxList:
            box.toggle_button.setChecked(isChecked)
            box.on_pressed()
            box.toggle_button.setChecked(not isChecked) 
            
            
    def handleSelectAllCheckBox(self):
        for teststepBoxList in self.testCaseBoxList.values():
            for teststep in teststepBoxList:
                checkBox = teststep.hLayout_teststepBox.itemAt(3).widget()
                checkBox.setChecked(False if self.ui.selectAll_checkBox.isChecked() else True)

            
    #*************************** Utility functions ******************************* #             
    def clearTestStepScrollArea(self):
        # Empty global list of testcaseBoxes
        self.testCaseBoxList.clear()
        
        # Disable toggle dropdown button and set it to unchecked
        self.ui.toggle_dropdown_btn.setEnabled(False)
        self.ui.toggle_dropdown_btn.setChecked(False)
        self.ui.toggle_dropdown_btn.setText('Show all')
        
        # Disable select all checkbox and set it to checked
        self.ui.selectAll_checkBox.setEnabled(False)
        self.ui.selectAll_checkBox.setChecked(True)
        
        while self.ui.verticalLayout_3.count():
            item = self.ui.verticalLayout_3.takeAt(0)
            
            if item.widget():
                item.widget().deleteLater()

              
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1980, 1080)
    mainWindow.show()
    
    sys.exit(app.exec_())
