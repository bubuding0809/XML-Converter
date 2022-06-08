from components.UiMainWindow import Ui_MainWindow
from components.TestStepGroupBox import TestStepGroupBox
from components.CollapseableWidget import CollapsibleBox
from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
import sys
import xmlParser
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
        self.ui.showAll_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        self.ui.hideAll_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        self.ui.xml_clearTeststeps_btn.clicked.connect(self.clearTestStepScrollArea)
        self.ui.selectAll_checkBox.pressed.connect(self.handleSelectAllCheckBox)
        self.ui.xmlData_searchBar.textChanged.connect(self.handleSearchBar)

        #Global variables
        self.xlsxInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/config.xlsx'
        self.xmlInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/input.xml'
        self.xmlOutFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/output.xml'

        #Global flags
        self.testCaseBoxList = {}
        self.ui.xlsxConfig_input_label.setText(self.xlsxInFile)
        self.ui.xml_input_label.setText(self.xmlInFile)
        self.ui.fileLocation_input_label.setText(self.xmlOutFile)
        
        
        
    # ************************* Event Handler methods **************************** #
    def handleXLSXInput(self):
        file = qtw.QFileDialog.getOpenFileName(self, 'Input config XLSX file', directory='', filter='Xlsx files (*.xlsx)')
        if file:
            self.xlsxInFile = file[0]
            self.ui.xlsxConfig_input_label.setText(file[0])
            
        if len(self.xlsxInFile) and len(self.xmlInFile):
            self.ui.xml_loadData_btn.setEnabled(True)
        else:
            self.ui.xml_loadData_btn.setEnabled(False)
        self.ui.xml_convert_btn.setEnabled(False)
            
            
        
    def handleXMLInput(self):
        file = qtw.QFileDialog.getOpenFileName(self, 'Input ATP XML file', directory='', filter='XML files (*.xml)' )
        
        if file:
            self.xmlInFile = file[0]
            self.ui.xml_input_label.setText(file[0])
            
        # Enable load data button if both xlsx and xml inputs exists
        if len(self.xlsxInFile) and len(self.xmlInFile):
            self.ui.xml_loadData_btn.setEnabled(True)
        else:
            self.ui.xml_loadData_btn.setEnabled(False)
        self.ui.xml_convert_btn.setEnabled(False)
            


    def handleXMLOutput(self):
        file = qtw.QFileDialog.getSaveFileName(self, 'Save converted ATP XML file', directory='', filter='XML files (*.xml)')
        
        if file:
            self.xmlOutFile = file[0]
            self.ui.fileLocation_input_label.setText(file[0])
        
        
        
    def handleXMLLoad(self):
        # Clear data grid of and old data
        self.clearTestStepScrollArea()
        
        try:
            # Catch errors thrown from xml processing
            conversionMap = xmlParser.handleXlsx(self.xlsxInFile)
            xmlData = xmlParser.getTestStepData(self.xmlInFile, conversionMap)
            
        except Exception as ex:
            #Catch exceptions and handle them 
            exception = f"An exception of type {type(ex)} occurred."
            arguments = f"Arguments:{ex.args}"
            
            msgBox = qtw.QMessageBox.critical(self, 'Error', exception)
            
            print(f'{exception}\n{arguments}')
            return
            
        #* Filter teststeps into their respective testcases
        testCaseList = {}
        if xmlData:
            
            # Filter each teststep into their respect testcases
            for teststep in xmlData:
                if teststep['parentId'] not in testCaseList:
                    testCaseList[teststep['parentId']] = [{
                        'id': teststep['id'],
                        'parentType': teststep['parentType'],
                        'parentName': teststep['parentName'],
                        'old': teststep['old'],
                        'new': teststep['new']
                    }]
                else:
                    testCaseList[teststep['parentId']].append({
                        'id': teststep['id'],
                        'parentType': teststep['parentType'],
                        'parentName': teststep['parentName'],
                        'old': teststep['old'],
                        'new': teststep['new']
                    })
        

        #* Create filtered data boxes and insert into the vertical scroll layout area 
        for index, (testcase, teststeps) in enumerate(testCaseList.items()):
            # Create collapsible box for test case
            box = CollapsibleBox(title=f"{testcase} <{teststeps[0]['parentType']}>")
            self.ui.verticalLayout_3.insertWidget(index, box)
            
            # Create vertical layout for each collapsible box
            vlayout = qtw.QVBoxLayout()
            
            testStepBoxList = []
            for teststep in teststeps:
                testStepBox = TestStepGroupBox(title=teststep['old']['description'], data=teststep, parent=self)
                vlayout.addWidget(testStepBox)
                testStepBoxList.append(testStepBox)
                
            vlayout.addStretch()
            box.setContentLayout(vlayout)
            self.testCaseBoxList[box] = testStepBoxList
        self.ui.verticalLayout_3.addStretch()
        
        # Setup autocompleter for search bar to allow for predictive searching of teststeps by description
        self.autoCompleter = qtw.QCompleter(list({teststep.title for teststepBoxList in self.testCaseBoxList.values() for teststep in teststepBoxList}))
        self.autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.ui.xmlData_searchBar.setCompleter(self.autoCompleter)
        

        #* Enable search bar 
        self.ui.xmlData_searchBar.setEnabled(True)
        
        #* Enable convert button
        self.ui.xml_convert_btn.setEnabled(True)
        
        #* Enable toggle drop down button and set it to unchecked
        self.ui.showAll_btn.setEnabled(True)
        self.ui.hideAll_btn.setEnabled(True)
        
        #* Enable select all checkbox and set it to checked
        self.ui.selectAll_checkBox.setEnabled(True)
        self.ui.selectAll_checkBox.setChecked(True)
        
        #* Enable clear data function
        self.ui.xml_clearTeststeps_btn.setEnabled(True)
       
       
    
    def handleToggleAllDropDownBtn(self):
        eventSender = self.sender()
        if eventSender == self.ui.showAll_btn:
            #Show all testcases
            for box in self.testCaseBoxList:
                box.toggle_button.setChecked(False)
                box.on_pressed()
                box.toggle_button.setChecked(True) 
        else:
            #Hide all testcases
            for box in self.testCaseBoxList:
                box.toggle_button.setChecked(True)
                box.on_pressed()
                box.toggle_button.setChecked(False) 
        


    def handleSelectAllCheckBox(self):
        # Iterate over every testStepBoxList
        for teststepBoxList in self.testCaseBoxList.values():
            
            # Iterate over every teststep in each teststepBoxList
            for teststep in teststepBoxList:
                
                # Get the checkbox object and toggle it
                checkBox = teststep.hLayout_teststepBox.itemAt(3).widget()
                checkBox.setChecked(False if self.ui.selectAll_checkBox.isChecked() else True)

    
    
    def handleSearchBar(self, text):
        for teststep in [teststep for teststepBoxList in self.testCaseBoxList.values() for teststep in teststepBoxList]:
             if text.lower() in teststep.title.lower():
                 teststep.show()
             else:
                 teststep.hide()
                
                
                    
    def handleXMLConvert(self):
        # Create a filtered set of teststeps ids based on the selected radio box.
        filteredIds = set()
        
        # Iterate over every testStepBoxList
        for teststepBoxList in self.testCaseBoxList.values():
            
            # Iterate over every teststep in each teststepBoxList
            for teststep in teststepBoxList:
                checkBox = teststep.hLayout_teststepBox.itemAt(3).widget()
                if checkBox.isChecked(): filteredIds.add(teststep.id)
                
        # Try to execute Execute XML conversion
        try:
            # Create conversion map based on xlsx config file
            conversionMap = xmlParser.handleXlsx(self.xlsxInFile)
            
            # To be used in XML_xmlParser to selectively convert old teststeps to new
            xmlParser.convertXML(filteredIds ,self.xmlInFile, self.xmlOutFile, conversionMap)
        except Exception as ex:
            # Catch exceptions and handle them 
            exception = f"An exception of type {type(ex)} occurred."
            arguments = f"Arguments:{ex.args}"
            
            msgBox = qtw.QMessageBox.critical(self, 'Error', exception)
            
            print(f'{exception}\n{arguments}')
            return
        
        #* Create success message box
        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle("Success")
        msgBox.setText("Successfully converted ATP XML file")
        msgBox.setIcon(qtw.QMessageBox.Information)
        checkbox = qtw.QCheckBox('Show file in explorer', msgBox)
        checkbox.setChecked(True)
        msgBox.setCheckBox(checkbox)
        ret = msgBox.exec_()
        
        #* Open file in explorer/finder if option is checked
        if checkbox.isChecked():
            if sys.platform == 'win32':
                self.xmlOutFile = self.xmlOutFile.replace('/', '\\')
                subprocess.Popen(f'explorer /select,{self.xmlOutFile}')
                
            elif sys.platform == 'darwin':
                subprocess.call(['open', '-R', self.xmlOutFile])
    
    
    
    #*************************** Utility functions ******************************* #             
    def clearTestStepScrollArea(self):
        # Empty global list of testcaseBoxes
        self.testCaseBoxList.clear()
        
        # Remove all widgets inside scroll area
        while self.ui.verticalLayout_3.count():
            item = self.ui.verticalLayout_3.takeAt(0)
            
            if item.widget():
                item.widget().deleteLater()
        
        #* Disable scroll area tool widgets
        self.ui.xml_convert_btn.setEnabled(False)
        self.ui.xml_clearTeststeps_btn.setEnabled(False)
        self.ui.xmlData_searchBar.setEnabled(False)

        #* Disable toggle dropdown button and set it to unchecked
        self.ui.showAll_btn.setEnabled(False)
        self.ui.hideAll_btn.setEnabled(False)

        #* Disable select all checkbox and set it to checked
        self.ui.selectAll_checkBox.setEnabled(False)
        self.ui.selectAll_checkBox.setChecked(True)



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1980, 1080)
    mainWindow.show()
    
    sys.exit(app.exec_())
