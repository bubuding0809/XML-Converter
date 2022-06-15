import logging
from UiMainWindow import Ui_MainWindow
from SummaryDialog import Ui_SummaryDialogWidget
from components.TestStepGroupBox import TestStepGroupBox
from components.CollapseableWidget import CollapsibleBox
from components.CustomButton import ButtonWithIcon
from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
import sys, os, subprocess
import xmlParser
import subprocess
import utils as u
import bootstrap_rc
from testdata import testFilePaths as testfiles

#* Set up logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
)
logger = logging.getLogger(__name__)


#* Get base directory of application 
basedir = os.path.dirname(__file__)


class SummaryDialog(qtw.QDialog):
    def __init__(self, parent, data=[], *args, **kwargs) -> None:
        super(SummaryDialog, self).__init__(parent, *args, **kwargs)
        
        self.ui = Ui_SummaryDialogWidget()
        self.ui.setupUi(self)
        
        #* Additional UI setup
        self.ui.dataTree_Widget.setSortingEnabled(False)
        self.setWindowModality(qtc.Qt.WindowModal)

        # for i in range(10):
        #     TestCaseItem = qtw.QTreeWidgetItem()
        #     TestCaseItem.setText(0, f'Testcase {i+1}')
        #     self.ui.dataTree_Widget.addTopLevelItem(TestCaseItem)
            
        #     for j in range(10):
        #         teststepItem = qtw.QTreeWidgetItem()
        #         teststepItem.setText(0, f'{(i+1)*(j+1)}')
        #         teststepItem.setText(1, f'old')
        #         teststepItem.setText(2, f'new')
        #         TestCaseItem.addChild(teststepItem)
            
        #     TestCaseItem.setExpanded(True)
        
        #* Signal connectors
        self.ui.closeSummary_btn.clicked.connect(self.handleCloseButton)
    
    #* Signal handler functions
    def handleCloseButton(self):
        self.close()
        
        
class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        #* Initialize UI to main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #* Additional UI setup
        pixmap = qtg.QPixmap(":/icons/bootstrap-icons-1.8.3/filetype-xlsx.svg").scaled(20, 20, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        self.ui.configFile_btn = ButtonWithIcon(pixmap, 'Config file', self)
        self.ui.configInput_widget.layout().addWidget(self.ui.configFile_btn)

        pixmap = qtg.QPixmap(":/icons/bootstrap-icons-1.8.3/filetype-xml.svg").scaled(20, 20, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        self.ui.xmlFile_btn = ButtonWithIcon(pixmap , 'XML file', self)
        self.ui.xmlInput_widget.layout().addWidget(self.ui.xmlFile_btn)

        pixmap = qtg.QPixmap(":/icons/bootstrap-icons-1.8.3/folder2.svg").scaled(20, 20, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        self.ui.saveLocation_btn = ButtonWithIcon(pixmap, 'Save', self)
        self.ui.saveLocation_widget.layout().addWidget(self.ui.saveLocation_btn)


        #* QShortcuts
        self.ui.quitSc = qtw.QShortcut(qtg.QKeySequence('Ctrl+W'), self)
        
        #* Signal connectors
        self.ui.configFile_btn.clicked.connect(self.handleXLSXInput)
        self.ui.xmlFile_btn.clicked.connect(self.handleXMLInput)
        self.ui.saveLocation_btn.clicked.connect(self.handleXMLOutput)
        self.ui.xml_convert_btn.clicked.connect(self.handleXMLConvert)
        self.ui.xml_loadData_btn.clicked.connect(self.handleXMLLoad)
        self.ui.showAll_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        self.ui.hideAll_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        self.ui.xml_clearTeststeps_btn.clicked.connect(self.clearTestStepScrollArea)
        self.ui.selectAll_checkBox.pressed.connect(self.handleSelectAllCheckBox)
        self.ui.xmlData_searchBar.textChanged.connect(self.handleSearchBar)
        self.ui.quitSc.activated.connect(self.handleExitApp)
        self.ui.xml_summary_btn.clicked.connect(self.handleXMLSummary)


        #* Global variables
        self.xlsxInFile = testfiles.CONFIG_PATH_WIN32 if sys.platform == 'win32' else testfiles.CONFIG_PATH_DARWIN
        self.xmlInFile = testfiles.INPUT_PATH_WIN32 if sys.platform == 'win32' else testfiles.INPUT_PATH_DARWIN
        self.xmlOutFile =  testfiles.SAVE_PATH_WIN32 if sys.platform == 'win32' else testfiles.SAVE_PATH_DARWIN

        #* Global flags
        self.testCaseBoxList = {}
        self.filteredTeststepIds = set()
        self.ui.xlsxConfig_input_label.setText(self.xlsxInFile)
        self.ui.xml_input_label.setText(self.xmlInFile)
        self.ui.fileLocation_input_label.setText(self.xmlOutFile)
        
        # Initialize conversionMap for testing
        self.conversionMap = xmlParser.handleXlsx(self.xlsxInFile)
        
        
        
    # ************************* Event Handler methods **************************** #
    def handleXLSXInput(self):
        file = qtw.QFileDialog.getOpenFileName(self, 'Input config XLSX file', directory='', filter='Excel files (*.xlsx)')
        if file:
            self.xlsxInFile = file[0]
            self.ui.xlsxConfig_input_label.setText(file[0])
        
        
        #* Try to process xlsx file and generate conversion map
        if len(self.xlsxInFile):
            try:
                # Read xlsx file and generate conversion map
                self.conversionMap = xmlParser.handleXlsx(self.xlsxInFile)

            except Exception as ex:
                # Catch exceptions and handle them 
                exception = f"There is an error in the xlsx file.\nPlease check the file and try again."
                arguments = '\n'.join([f"{index+1}: {arg}" for index, arg in enumerate(list(ex.args))])
                
                # Create message box to display the error
                msgBox = qtw.QMessageBox(self)
                msgBox.setWindowTitle('Error')
                msgBox.setText(exception)
                msgBox.setDetailedText(
                    f"Your excel config at {self.xlsxInFile} are missing these headers:\
                    \n-----------------------------------------------------------------\
                    \n{arguments}"
                )
                msgBox.setStandardButtons(qtw.QMessageBox.Ok)
                retryBtn = msgBox.addButton('Try again', qtw.QMessageBox.AcceptRole)
                msgBox.setIcon(qtw.QMessageBox.Critical)
                msgBox.setWindowModality(qtc.Qt.WindowModal)
                
                ret = msgBox.exec()

                # If user clicks on retry button, try again
                if msgBox.clickedButton() == retryBtn:
                    self.handleXLSXInput()
                    return
                    
                # Disable load data button
                self.ui.xml_loadData_btn.setEnabled(False)
                
                # Clear xml data in scroll area
                self.clearTestStepScrollArea()
                
                return
        
        
        #* Filter list of teststeps with empty fields
        emptyFieldList = []
        if self.conversionMap:
            for index, (oldDescription, mapping) in enumerate(self.conversionMap.items()):
                teststepEmptyField = []
                
                # Check if old description is empty
                if not len(oldDescription):
                    teststepEmptyField.append('old teststep description')
                    
                # Check if there are any empty fields in the teststep
                for tag, text in mapping.items():
                    if not len(str(text)):
                        teststepEmptyField.append(tag)
                
                # If all fields are not filled, add to list
                if teststepEmptyField: emptyFieldList.append({
                    'description': f"{oldDescription if len(oldDescription) else 'Missing old teststep description'} - [row: {index+2}]",
                    'emptyFields': teststepEmptyField
                })
            
            
        #* If there are empty fields, display message box to warn user
        if emptyFieldList:
            #Create message box to display the error
            msgBox = qtw.QMessageBox(self)
            msgBox.setWindowTitle('Warning')
            msgBox.setText('There are empty fields in your config file.')
            
            #* Create string list of empty fields and add to message
            emptyFieldMessageList = []
            for index, item in enumerate(emptyFieldList):
                # Create string of description and empty fields
                descriptionWithEmptyFields = f"{index+1}: {item['description']:}"
                emptyFields = '\n'.join([f"   - {field}" for field in item['emptyFields']])
                emptyFieldMessageList.append(f"{descriptionWithEmptyFields}\n{emptyFields}")
            
            # Join all empty fields into one string
            emptyFieldMessageList = '\n'.join(emptyFieldMessageList)
            
            # Add empty fields to message
            emptyFieldMessage = (
                f"The following teststeps were found to have empty fields in your config file at {self.xmlInFile}:\
                \n-----------------------------------------------------------------\
                \n{emptyFieldMessageList}"
            )
            
            #* Add message to message box detailed text
            msgBox.setDetailedText(emptyFieldMessage)
            
            #* Add buttons and icons to message box
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            editConfig_btn = msgBox.addButton('Edit config', qtw.QMessageBox.AcceptRole)
            msgBox.setIcon(qtw.QMessageBox.Warning)
            msgBox.setWindowModality(qtc.Qt.WindowModal)   
            
            #* execute message box
            ret = msgBox.exec()
            
            #* If user clicks edit config button, open config file in default program
            if msgBox.clickedButton() == editConfig_btn:
                # macOS
                if sys.platform == 'darwin':
                    subprocess.call(('open', self.xlsxInFile))
                # Windows   
                elif sys.platform == 'win32':
                    os.startfile(self.xlsxInFile)
            
            
        #* Enable load data button if both xlsx and xml inputs exists and xlsx input is valid
        if len(self.xlsxInFile) and len(self.xmlInFile):
            self.ui.xml_loadData_btn.setEnabled(True)
        else:
            self.ui.xml_loadData_btn.setEnabled(False)
        self.ui.xml_convert_btn.setEnabled(False)
        self.clearTestStepScrollArea()
            
            
        
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
        
        # disable convert button if both xlsx and xml inputs exists
        if len(self.xmlOutFile):
            self.ui.xml_convert_btn.setEnabled(True)
        else:
            self.ui.xml_convert_btn.setEnabled(False)
        


    def handleXMLLoad(self):
        #* Clear data grid of and old data
        self.clearTestStepScrollArea()
        
        #* Reset all isMatch flags in conversion map to False
        for fields in self.conversionMap.values():
            fields['isMatched'] = False
        
        #* Get parsed xml data and updated conversion map
        try:
            # Catch errors thrown from xml processing
            xmlData, self.conversionMap = xmlParser.getTestStepData(self.xmlInFile, self.conversionMap)
            
        except Exception as ex:
            # Catch exceptions and handle them 
            exception = f"An exception of type {type(ex)} occurred."
            arguments = '\n'.join([f"{index+1}: {arg}" for index, arg in enumerate(list(ex.args))])
            
            # Create message box to display the error
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle('Error')
            msgBox.setText(exception)
            msgBox.setDetailedText(
                f"Here are the error arguments:\
                \n-----------------------------------------------------------------\
                \n{arguments}"
            )
            msgBox.setIcon(qtw.QMessageBox.Critical)
            ret = msgBox.exec()

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
        if testCaseList:
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
        else:
            emptyLabel = qtw.QLabel('No test steps matched in XML file')
            self.ui.verticalLayout_3.addWidget(emptyLabel)
        self.ui.verticalLayout_3.addStretch()
        
        
        #* Alert user if there are unmatched teststeps
        # Create list of unmatched teststeps
        unmatchedTeststeps = []
        for index, (oldDescription, fields) in enumerate(self.conversionMap.items()):
            if fields['isMatched'] == False:
                unmatchedTeststeps.append(f"{oldDescription} - [row: {index+2}]")
        
        # If there are unmatched teststeps, alert user with a message box with the list of unmatched teststeps
        if unmatchedTeststeps:
            
            # Create message box to display the warning
            msgBox= qtw.QMessageBox(self)
            msgBox.setWindowTitle('Warning')
            msgBox.setText(f"There are unmatched teststeps descriptions in your config file.")
            
            # Create string list of unmatched teststeps and to message
            unmatchedTeststeps = '\n'.join(
                [f"{index+1}: {teststep}" for index, teststep in enumerate(unmatchedTeststeps)]
            )
            noMatchMessage = (
                f"The following teststeps descriptions at {self.xlsxInFile} had no match in the xml file:\
                \n-----------------------------------------------------------------\
                \n{unmatchedTeststeps}"
            )

            # Merge message and set message box detailed text
            msgBox.setDetailedText(noMatchMessage)
            
            # Set message buttons and icons
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            editConfig_btn = msgBox.addButton('Edit config', qtw.QMessageBox.AcceptRole)
            msgBox.setIcon(qtw.QMessageBox.Warning)
            msgBox.setWindowModality(qtc.Qt.WindowModal)   
            
            # execute message box
            ret = msgBox.exec_()
            
            # If user clicks edit config button, open config file in default program
            if msgBox.clickedButton() == editConfig_btn:
                # macOS
                if sys.platform == 'darwin':
                    subprocess.call(('open', self.xlsxInFile))
                # Windows   
                elif sys.platform == 'win32':
                    os.startfile(self.xlsxInFile)


        #* Add Signal handler to each teststep checkbox
        # Iterate over every testStepBoxList
        for teststepBoxList in self.testCaseBoxList.values():
            
            # Iterate over every teststep in each teststepBoxList
            for teststep in teststepBoxList:
                # Add all teststep IDs to the list of filtered teststeps IDs
                self.filteredTeststepIds.add(teststep.id)
                
                # Get the checkbox object and toggle it
                checkBox = teststep.hLayout_teststepBox.itemAt(3).widget()
                checkBox.clicked.connect(lambda _, teststep=teststep: self.handleTestStepCheckbox(teststep))
        
        
        #* Setup autocompleter for search bar to allow for predictive searching of teststeps by description
        self.autoCompleter = qtw.QCompleter(list({teststep.title for teststepBoxList in self.testCaseBoxList.values() for teststep in teststepBoxList}))
        self.autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.ui.xmlData_searchBar.setCompleter(self.autoCompleter)
        
        #* Enable all tool buttons after succesfully loading XML file
        # Enable search bar 
        self.ui.xmlData_searchBar.setEnabled(True)
        
        # Enable toggle drop down button and set it to unchecked
        self.ui.showAll_btn.setEnabled(True)
        self.ui.hideAll_btn.setEnabled(True)
        
        # Enable select all checkbox and set it to checked
        self.ui.selectAll_checkBox.setEnabled(True)
        self.ui.selectAll_checkBox.setChecked(True)
        
        # Enable clear data function
        self.ui.xml_clearTeststeps_btn.setEnabled(True)
        
        # Enable summary button
        self.ui.xml_summary_btn.setEnabled(True)

        # Enable convert button
        self.ui.xml_convert_btn.setEnabled(True)
       
       
    
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
                
                # If select all checkbox is checked, check all teststeps and add the ID to the list of filtered teststeps
                if not self.ui.selectAll_checkBox.isChecked():
                    self.filteredTeststepIds.add(teststep.id)
                    checkBox.setChecked(True)
                # Else, uncheck all teststeps and remove the ID from the list of filtered teststeps
                else:
                    self.filteredTeststepIds.clear()
                    checkBox.setChecked(False)
        
        print(self.filteredTeststepIds)
    
    
    
    def handleSearchBar(self, text):
        for teststep in [teststep for teststepBoxList in self.testCaseBoxList.values() for teststep in teststepBoxList]:
             if text.lower() in teststep.title.lower():
                 teststep.show()
             else:
                 teststep.hide()

        for testcase in self.testCaseBoxList:
            testcase.show()

            isAnyFound = False

            # Get layout of collapsible test case box
            layout = testcase.layout().itemAt(1).widget().layout()
            
            # Iterate through each widget instead of the layout and check if it contains any matched teststep
            for widget in u.getLayoutWidgets(layout):
                if widget.isVisible():
                    isAnyFound = True
            
            testcase.show() if isAnyFound else testcase.hide()

                   
                    
    def handleXMLConvert(self):                
        #* Try to execute Execute XML conversion
        try:
            # To be used in XML_xmlParser to selectively convert old teststeps to new
            xmlParser.convertTeststepData(self.filteredTeststepIds ,self.xmlInFile, self.xmlOutFile, self.conversionMap)

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

        #* Clear search bar
        self.ui.xmlData_searchBar.clear()

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

    
    
    def centerWindowOnScreen(self):
        screenGeo = qtw.QDesktopWidget().screenGeometry()
        windowGeo = self.geometry()

        print(screenGeo, windowGeo)
        xPosition = (screenGeo.width() - windowGeo.width()) / 2 
        yPosition = (screenGeo.height() - windowGeo.height()) / 2 

        self.move(int(xPosition), int(yPosition))



    def handleExitApp(self):
        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle('Exit app')
        msgBox.setText('Confirm with OK to exit the application now')
        msgBox.setIcon(qtw.QMessageBox.Warning)
        msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        msgBox.setDefaultButton(qtw.QMessageBox.Ok)

        msgBox.defaultButton().clicked.connect(qtw.QApplication.instance().quit)

        ret = msgBox.exec_()



    def handleCopyToClipboard(self):
        clipBoard = qtw.QApplication.clipboard()
        clipBoard.clear(clipBoard.Clipboard)
        clipBoard.setText()



    def handleXMLSummary(self):
        # Iterate through testcaseBoxList and filter out the teststeps that are in the filteredTeststepIds list
        summaryDialog = SummaryDialog(self)
        
        for testcase, testcaseBoxList in self.testCaseBoxList.items():
            
            testcaseItem = qtw.QTreeWidgetItem(summaryDialog.ui.dataTree_Widget)
            testcaseItem.setText(1, testcase.title)
            summaryDialog.ui.dataTree_Widget.addTopLevelItem(testcaseItem)
            
            for teststep in testcaseBoxList:
                
                if teststep.id in self.filteredTeststepIds:
                    teststepItem = qtw.QTreeWidgetItem(testcaseItem)
                    teststepItem.setText(0, str(teststep.id))
                    teststepItem.setText(1, testcase.title)
                    teststepItem.setText(2, teststep.data['old']['description'])
                    teststepItem.setText(3, teststep.data['new']['description'])
                    testcaseItem.addChild(teststepItem)

        summaryDialog.show()



    def handleTestStepCheckbox(self, teststep):
        # Check if the checkbox is checked
        checked = teststep.hLayout_teststepBox.itemAt(3).widget().isChecked()
        
        # if checked, add the teststep id to the filtered set else remove from set
        self.filteredTeststepIds.add(teststep.id) if checked else self.filteredTeststepIds.remove(teststep.id)
        
        print(f"Teststep {teststep.id} is checked: {checked}")
        print(self.filteredTeststepIds)
        
        
        
#* Configure windows to identify the application as a custom application
if sys.platform == 'win32':
    try:
        from ctypes import windll  # Only exists on Windows.
        myappid = 'mycompany.myproduct.subproduct.version'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass



if __name__ == '__main__':
    # Create application and set application icon
    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(qtg.QIcon(":/icons/bootstrap-icons-1.8.3/tools.svg"))

    # Create main window
    mainWindow = MainWindow()

    # Get and set the main window style sheet
    with open(os.path.join(basedir, 'static/style.qss'), 'r') as file:
        stylesheet = file.read()
    mainWindow.setStyleSheet(stylesheet)

    # Customize window settings
    mainWindow.setWindowTitle('ATP XML-Converter')
    mainWindow.resize(1600, 900)
    mainWindow.centerWindowOnScreen()
    mainWindow.show()
    logger.info('App started')
    
    
    # Execute application
    sys.exit(app.exec_())
    
