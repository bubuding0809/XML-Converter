import logging
from components.UiMainWindow import Ui_MainWindow
from components.SummaryDialogWidget import SummaryDialog
from components.TeststepGroupBoxWidget import TeststepGroupBoxWidget
from components.CollapsibleTestcaseWidget import CollapsibleTestcaseWidget
from components.CustomButton import ButtonWithIcon
from components.CustomLineEdit import CustomLineEdit
from components.FileFilterProxyModel import FileFilterProxyModel
from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
import utils
import sys, os, subprocess
import xmlParser
import subprocess
from components.resources import bootstrap_rc
from samples import testFilePaths as testfiles


#* Get base directory of application 
baseDir = os.path.dirname(__file__)


#* Set up logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(baseDir, 'app.log'),
)
logger = logging.getLogger(__name__)



class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        #* Initialize UI to main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #* Additional UI setup
        # Create Custom button for save config button
        pixmap = qtg.QPixmap(":/icons/bootstrap-icons-1.8.3/filetype-xlsx.svg").scaled(20, 20, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        self.ui.configFile_btn = ButtonWithIcon(pixmap, 'Config file', self)
        self.ui.configFile_btn.setStatusTip('Select excel config file from explorer')
        self.ui.configFile_btn.setWhatsThis('Select excel config file from explorer')
        self.ui.configFile_btn.setToolTip('Select excel config file from explorer')
        self.ui.configInput_widget.layout().addWidget(self.ui.configFile_btn)
        
        # Create Custom button for save input button
        pixmap = qtg.QPixmap(":/icons/bootstrap-icons-1.8.3/filetype-xml.svg").scaled(20, 20, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        self.ui.xmlFile_btn = ButtonWithIcon(pixmap , 'XML file', self)
        self.ui.xmlFile_btn.setStatusTip('Select xml ATP file from explorer')
        self.ui.xmlFile_btn.setWhatsThis('Select xml ATP file from explorer')
        self.ui.xmlFile_btn.setToolTip('Select xml ATP file from explorer')
        self.ui.xmlInput_widget.layout().addWidget(self.ui.xmlFile_btn)

        # Create Custom button for save location button
        pixmap = qtg.QPixmap(":/icons/bootstrap-icons-1.8.3/folder2.svg").scaled(20, 20, qtc.Qt.KeepAspectRatio, qtc.Qt.SmoothTransformation)
        self.ui.saveLocation_btn = ButtonWithIcon(pixmap, 'Save', self)
        self.ui.saveLocation_btn.setStatusTip('Set save as location for converted xml file')
        self.ui.saveLocation_btn.setWhatsThis('Set save as location for converted xml file')
        self.ui.saveLocation_btn.setToolTip('Set save as location for converted xml file')
        self.ui.saveLocation_widget.layout().addWidget(self.ui.saveLocation_btn)

        # Create Custom line edit search bar 
        self.ui.mainSearchBar_lineEdit = CustomLineEdit(':/icons/bootstrap-icons-1.8.3/search.svg', 'Search')
        self.ui.mainSearchBar_lineEdit.setMinimumWidth(200)
        self.ui.mainSearchBar_lineEdit.setMaximumWidth(400)
        self.ui.mainSearchBar_lineEdit.setEnabled(False)
        self.ui.scrollAreaSearchBox_widget.layout().insertWidget(0, self.ui.mainSearchBar_lineEdit)

        # Create radio buttons for filter box
        self.filterButtonGroup = qtw.QButtonGroup()
        self.filterButtonGroup.addButton(self.ui.filterTestcaseOnly_btn, 1)
        self.filterButtonGroup.addButton(self.ui.filterBoth_btn, 2)
        self.filterButtonGroup.addButton(self.ui.filterFunctionOnly_btn, 3)


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
        self.ui.selectAll_checkBox.stateChanged.connect(self.handleSelectAllCheckBox)
        self.ui.mainSearchBar_lineEdit.textChanged.connect(self.handleSearchBar)
        self.ui.quitSc.activated.connect(self.handleExitApp)
        self.ui.xml_summary_btn.clicked.connect(self.handleXMLSummary)
        self.filterButtonGroup.buttonClicked.connect(self.handleFilterButtonClicked)


        #* Global variables
        self.xlsxInFile = testfiles.CONFIG_PATH_WIN32 if sys.platform == 'win32' else testfiles.CONFIG_PATH_DARWIN
        self.xmlInFile = testfiles.INPUT_PATH_WIN32 if sys.platform == 'win32' else testfiles.INPUT_PATH_DARWIN
        self.xmlOutFile = testfiles.SAVE_PATH_WIN32 if sys.platform == 'win32' else testfiles.SAVE_PATH_DARWIN


        #* Global flags
        self.testCaseBoxList = {}
        self.filteredTeststepIds = set()
        self.filterDataMap = {
            radioButton.text(): utils.removeWhiteSpace(radioButton.text().lower()) 
            for radioButton in self.filterButtonGroup.buttons()
        }
        self.ui.xlsxConfig_input_label.setText(self.xlsxInFile)
        self.ui.xml_input_label.setText(self.xmlInFile)
        self.ui.fileLocation_input_label.setText(self.xmlOutFile)
        
        # Initialize conversionMap
        self.conversionMap = xmlParser.handleXlsx(self.xlsxInFile)
        self.handleXMLLoad()
        
        
        
    # ************************* Signal Handler methods **************************** #
    
    def handleXLSXInput(self):
        #* reset conversion map upon clicking config file button
        self.conversionMap.clear()

        #* Retrieve excel config file path from file dialog
        fileDialog = qtw.QFileDialog(self)
        fileDialog.setOption(qtw.QFileDialog.DontUseNativeDialog)
        fileDialog.setProxyModel(FileFilterProxyModel())
        fileDialog.setWindowTitle('Input config xlsx file')
        fileDialog.setNameFilter('XLSX files (*.xlsx)')
        fileDialog.setDirectory('./samples')

    
        if fileDialog.exec_():
            selectedFiles = fileDialog.selectedFiles()
            self.xlsxInFile = selectedFiles[0]
            self.ui.xlsxConfig_input_label.setText(selectedFiles[0])


        #* Try to process xlsx file and generate conversion map
        if len(self.xlsxInFile):
            try:
                # Read xlsx file and generate conversion map
                self.conversionMap = xmlParser.handleXlsx(self.xlsxInFile)

            except Exception as ex:
                # Catch exceptions and handle them 
                exception = f"There is an error in the xlsx file.\
                    \n\nPlease try to upload a correct config file or edit the current config file."

                arguments = '\n'.join([f"{index+1}: {arg}" for index, arg in enumerate(list(ex.args))])
                
                # Create message box to display the error
                msgBox = qtw.QMessageBox(self)
                msgBox.setWindowTitle('Error')
                msgBox.setText(exception)
                msgBox.setDetailedText(
                    f"Your excel config at {self.xlsxInFile} are missing these headers:\
                    \n--------------------------------------------------------\
                    \n{arguments}"
                )
                msgBox.setStandardButtons(qtw.QMessageBox.Ok)
                editConfig = msgBox.addButton('Edit config', qtw.QMessageBox.ApplyRole)
                retryBtn = msgBox.addButton('Try again', qtw.QMessageBox.AcceptRole)

                msgBox.setIcon(qtw.QMessageBox.Critical)
                msgBox.setWindowModality(qtc.Qt.WindowModal)
                
                ret = msgBox.exec()

                # If user clicks on retry button, try again
                if msgBox.clickedButton() == retryBtn:
                    self.handleXLSXInput()
                    return
                if msgBox.clickedButton() == editConfig:
                    # macOS
                    if sys.platform == 'darwin':
                        subprocess.call(('open', self.xlsxInFile))
                    # Windows   
                    elif sys.platform == 'win32':
                        os.startfile(self.xlsxInFile)

                    
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
                for tag, value in mapping.items():
                    
                    if tag == 'isMatched' or tag == 'oldDescription':
                        continue
                    
                    if not len(value):
                        teststepEmptyField.append(tag)
                
                # If all fields are not filled, add to list
                if teststepEmptyField: emptyFieldList.append({
                    'description': f"{mapping['oldDescription'] if len(oldDescription) else 'Missing old teststep description'} - [row: {index+2}]",
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
            emptyFieldMessageList = '\n\n'.join(emptyFieldMessageList)
            
            # Add empty fields to message
            emptyFieldMessage = (
                f"The following teststeps were found to have empty fields in your config file at \n{self.xlsxInFile}:\
                \n--------------------------------------------------------\
                \n\n{emptyFieldMessageList}"
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
            
            
        #* Enable load xml data if both xlsx and xml inputs exists
        if len(self.xlsxInFile) and len(self.xmlInFile):
            self.handleXMLLoad()
            self.ui.xml_loadData_btn.setEnabled(True)

        #* If all three required inputs are set, enable conversion button
        if len(self.xmlOutFile) and len(self.xmlInFile) and len(self.xmlOutFile):
            self.ui.xml_convert_btn.setEnabled(True)
        else:
            self.ui.xml_convert_btn.setEnabled(False)
            
            

    def handleXMLInput(self):
        #* Retrieve atp xml file path from file dialog
        fileDialog = qtw.QFileDialog(self)
        fileDialog.setOption(qtw.QFileDialog.DontUseNativeDialog)
        fileDialog.setWindowTitle('Input ATP xml file')
        fileDialog.setNameFilter('XML files (*.xml)')
        fileDialog.setDirectory('./samples')

    
        if fileDialog.exec_():
            selectedFiles = fileDialog.selectedFiles()
            self.xmlInFile = selectedFiles[0]
            self.ui.xml_input_label.setText(selectedFiles[0])


        #* Enable load xml data if both xlsx and xml inputs exists
        if len(self.xlsxInFile) and len(self.xmlInFile):
            self.handleXMLLoad()
            self.ui.xml_loadData_btn.setEnabled(True)

        #* If all three required inputs are set, enable conversion button
        if len(self.xmlOutFile) and len(self.xmlInFile) and len(self.xmlOutFile):
            self.ui.xml_convert_btn.setEnabled(True)
        else:
            self.ui.xml_convert_btn.setEnabled(False)
            


    def handleXMLOutput(self):
        file = qtw.QFileDialog.getSaveFileName(self, 'Save converted ATP XML file', filter='XML files (*.xml)')
        
        if file:
            self.xmlOutFile = file[0]
            self.ui.fileLocation_input_label.setText(file[0])

        #* If all three required inputs are set, enable conversion button
        if len(self.xmlOutFile) and len(self.xmlInFile) and len(self.xmlOutFile):
            self.ui.xml_convert_btn.setEnabled(True)
        else:
            self.ui.xml_convert_btn.setEnabled(False)
        


    def handleXMLLoad(self):
        #* Clear data grid of and old data
        self.clearTestStepScrollArea()
        
        #* Reset all isMatch flags in conversion map to False
        for mapping in self.conversionMap.values():
            mapping['isMatched'] = False
        
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
                \n--------------------------------------------------------\
                \n\n{arguments}"
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
        
        
        #* Create mapped data boxes and insert into the vertical scroll layout area 
        if testCaseList:
            for index, (testcase, teststeps) in enumerate(testCaseList.items()):

                # Create testcase data obj to be passed into the CollapsibleBox widget
                testcaseData = {
                    'id': testcase,
                    'type': teststeps[0]['parentType'],
                    'teststeps': teststeps
                }

                # Create collapsible box for test case
                box = CollapsibleTestcaseWidget(
                    title=f"{testcase} <{teststeps[0]['parentType']}>",
                    data=testcaseData
                )
                self.ui.verticalLayout_3.insertWidget(index, box)
                
                # Create vertical layout for each collapsible box
                vlayout = qtw.QVBoxLayout()
                vlayout.setContentsMargins(0, 0, 0, 0)
                
                teststepBoxList = []
                for teststep in teststeps:

                    teststepBox = TeststepGroupBoxWidget(
                        title=f"ID: {teststep['id']} - {teststep['old']['description']}", 
                        data=teststep, 
                        parent=self
                    )

                    teststepBox.newDataTableWidget.itemChanged.connect(
                        lambda item, teststepBox=teststepBox: 
                        self.handleAbstractItemTextChange(item, teststepBox)
                    )

                    teststepBox.newDataListWidget.itemChanged.connect(
                        lambda item, teststepBox=teststepBox: 
                        self.handleAbstractItemTextChange(item, teststepBox)
                    )

                    teststepBox.newDataListWidget.model().rowsInserted.connect(
                        lambda modelIndex, first, last, teststepBox=teststepBox, listWidget=teststepBox.newDataListWidget:
                        self.handleRowsInserted(modelIndex, first, last, teststepBox, listWidget)
                    )

                    teststepBox.newDataListWidget.model().rowsRemoved.connect(
                        lambda modelIndex, first, last, teststepBox=teststepBox, listWidget=teststepBox.newDataListWidget:
                        self.handleRowsRemoved(modelIndex, first, last, teststepBox, listWidget)
                    )

                    # Add teststep box to vlayout and store in a list
                    vlayout.addWidget(teststepBox)
                    teststepBoxList.append(teststepBox)
                    
                vlayout.addStretch()
                box.setContentLayout(vlayout)
                self.testCaseBoxList[box] = teststepBoxList
        else:

            emptyLabel = qtw.QLabel('No test steps matched in XML file')
            self.ui.verticalLayout_3.addWidget(emptyLabel)

        self.ui.verticalLayout_3.addStretch()
        
        
        #* Alert user if there are unmatched teststeps
        # Create list of unmatched teststeps
        unmatchedTeststeps = []
        for index, (oldDescription, mapping) in enumerate(self.conversionMap.items()):
            if mapping['isMatched'] == False:
                unmatchedTeststeps.append(f"{mapping['oldDescription']} - [row: {index+2}]")
        
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
                \n--------------------------------------------------------\
                \n\n{unmatchedTeststeps}"
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
        # Iterate over every teststepBoxList
        for teststepBoxList in self.testCaseBoxList.values():
            
            # Iterate over every teststep in each teststepBoxList
            for teststep in teststepBoxList:
                # Add all teststep IDs to the list of filtered teststeps IDs
                self.filteredTeststepIds.add(teststep.id)
                
                # Get the checkbox object and toggle it
                checkBox = teststep.hLayout_teststepBox.itemAt(3).widget()
                checkBox.clicked.connect(
                    lambda _, teststep=teststep: 
                    self.handleTestStepCheckbox(teststep)
                )
        
        
        #* Setup autocompleter for search bar to allow for predictive searching of teststeps by description
        SearchByTeststepDescriptionList = []
        for teststepBoxList in self.testCaseBoxList.values():
            for teststep in teststepBoxList:
                SearchByTeststepDescriptionList.append(teststep.title)

        autoCompleter = qtw.QCompleter(SearchByTeststepDescriptionList, self)
        autoCompleter.setFilterMode(qtc.Qt.MatchFlag.MatchContains)
        autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.ui.mainSearchBar_lineEdit.setCompleter(autoCompleter)
        
        #* Enable all tool buttons after succesfully loading XML file
        # Enable search bar 
        self.ui.mainSearchBar_lineEdit.setEnabled(True)
        
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

        # Enable filter radio buttons
        self.ui.scrollAreaFilterBox_widget.setEnabled(True)
        self.ui.filterBoth_btn.setChecked(True)
       
       
    
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
        


    def handleSelectAllCheckBox(self, state): #state == 0: unchecked, state == 2: checked
        #* Get current checked filter radio button
        checkFilterButton = self.filterButtonGroup.checkedButton()
        filterTypeChecked = self.filterDataMap[checkFilterButton.text()]

        #* Get state of select all checkbox 
        isChecked = True if state else False

        #* Iterate over every teststepBoxList and its teststeps 
        for testcase, teststepBoxList in self.testCaseBoxList.items():
            
            for teststep in teststepBoxList:

                # Get the teststepbox checkbox object 
                radioButton = teststep.hLayout_teststepBox.itemAt(3).widget()

                # Check if teststep parent type matches filtertype
                if filterTypeChecked == testcase.type or filterTypeChecked == 'both':

                    # add or remove teststep id to/from filteredIds
                    if isChecked:
                        self.filteredTeststepIds.add(teststep.id)
                    else:
                        self.filteredTeststepIds.discard(teststep.id)                            

                    # Set teststep selection radio box state based on isChecked
                    radioButton.setChecked(isChecked)
                
                else:
                    # Remove teststep id from filteredIds
                    self.filteredTeststepIds.discard(teststep.id)

                    # Set teststep selection radio box state to unchecked
                    radioButton.setChecked(False)
    
    
    
    def handleSearchBar(self, text):
        checkFilterButton = self.filterButtonGroup.checkedButton()
        filterTypeChecked = self.filterDataMap[checkFilterButton.text()]

        for testcase, teststepList in self.testCaseBoxList.items():
            isAnyFound = False
            visibleCount = 0

            testcase.show()

            for teststep in teststepList:
                if text.lower() in teststep.title.lower():
                     teststep.show()
                     isAnyFound = True
                     visibleCount += 1
                else:
                     teststep.hide()

            #* Update testcaseBoxWidget with new title text
            testcase.toggle_button.setText(
                f"{testcase} ({str(visibleCount)}/{len(teststepList)})"
            )

            testcase.show() if isAnyFound and testcase.type == filterTypeChecked else testcase.hide()
        


    def handleTestStepCheckbox(self, teststep):
        # Check if the checkbox is checked
        checked = teststep.hLayout_teststepBox.itemAt(3).widget().isChecked()
        
        # if checked, add the teststep id to the filtered set else remove from set
        if checked: 
            self.filteredTeststepIds.add(teststep.id) 
        else :
            self.filteredTeststepIds.remove(teststep.id)
        
        print(f"Teststep {teststep.id} is checked: {checked}")



    def handleXMLSummary(self):
        #* Create summary dialog widget and show
        summaryDialog = SummaryDialog(
            self, 
            data=self.testCaseBoxList,
            filteredIds=self.filteredTeststepIds
        )
        summaryDialog.show()



    def handleXMLConvert(self):                
        conversionMap = self.getUpdatedConversionMap()

        #* Try to execute Execute XML conversion
        try:
            # To be used in XML_xmlParser to selectively convert old teststeps to new
            xmlParser.convertXml(
                self.filteredTeststepIds,
                self.xmlInFile, 
                self.xmlOutFile, 
                conversionMap
            )

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
    
    

    def handleExitApp(self):
        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle('Exit app')
        msgBox.setText('Confirm with OK to exit the application now')
        msgBox.setIcon(qtw.QMessageBox.Warning)
        msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        msgBox.setDefaultButton(qtw.QMessageBox.Ok)

        msgBox.defaultButton().clicked.connect(qtw.QApplication.instance().quit)

        ret = msgBox.exec_()
    


    def handleFilterButtonClicked(self, button):
        filterTypeChecked = self.filterDataMap[button.text()]
        
        for testcase in self.testCaseBoxList.keys():
            testcase.show()

            if filterTypeChecked != testcase.type and filterTypeChecked != 'both':
                testcase.hide()

        #Check select all checkbox and call handleSelect All checkbox to reset selection for new filtered data
        self.ui.selectAll_checkBox.setChecked(True)
        self.ui.mainSearchBar_lineEdit.clear()
        self.handleSelectAllCheckBox(2)



    def handleAbstractItemTextChange(self, item, teststepBox):
        print('Item change triggered')
        # Check if item edited belongs to table widget 
        isTableWidget = type(item) == type(qtw.QTableWidgetItem())
        
        #* Get item text, parent widget of item, item postion and cleaned description of the teststep box
        changedText = item.text()
        widget = item.tableWidget() if isTableWidget else item.listWidget()
        position = widget.column(item) if isTableWidget else widget.row(item)
        sourceCleanedDescription = teststepBox.data['old']['cleanedDescription']

        #* Iterate through all teststeps with the same classic description and propagate the changed text
        for teststeps in self.testCaseBoxList.values():
            
            for teststep in teststeps:

                # Get the target cleaned description for matching purpose 
                targetCleanedDescription = teststep.data['old']['cleanedDescription']

                #If matched, propagate changes to target 
                if sourceCleanedDescription == targetCleanedDescription:
                    # Get target table widget
                    widget = teststep.newDataTableWidget if isTableWidget else teststep.newDataListWidget

                    # Get target table item
                    item = widget.item(0, position) if isTableWidget else widget.item(position)

                    # Block signals from table widget to prevent repeated calls to table item changed event
                    widget.blockSignals(True)

                    # Propagate change to table item text
                    item.setText(changedText)

                    # Unblock singals from table widget once text has been changed
                    widget.blockSignals(False)



    def handleRowsInserted(self, modelIndex, first, last, teststepBox, listWidget):
        print('Rows inserted triggered')
        item = listWidget.item(first)
        sourceCleanedDescription = teststepBox.data['old']['cleanedDescription']
        sourceId = teststepBox.id

        for teststeps in self.testCaseBoxList.values():
            
            for teststep in teststeps:

                # Get the target cleaned description for matching purpose 
                targetCleanedDescription = teststep.data['old']['cleanedDescription']
                targetId = teststep.id

                #If matched, propagate changes to target 
                if sourceCleanedDescription == targetCleanedDescription and sourceId != targetId:
                    # Get target list widget
                    listWidget = teststep.newDataListWidget

                    # Create new list item
                    newItem = qtw.QListWidgetItem('')
                    newItem.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable| qtc.Qt.ItemIsDragEnabled | qtc.Qt.ItemIsEnabled)

                    # Block signals from table model widget to prevent repeated calls to table item inserted event
                    # Propagate insertion of new item
                    listWidget.model().blockSignals(True)
                    listWidget.insertItem(first, newItem)
                    listWidget.model().blockSignals(False)

                    # Block signals from table widget to prevent repeated calls to table item changed event
                    # Propagate new text of new item
                    listWidget.blockSignals(True)
                    newItem.setText(item.text())
                    listWidget.blockSignals(False)

                    print(targetId)
                    print(listWidget.count())



    def handleRowsRemoved(self, modelIndex, first, last, teststepBox, listWidget):
        print(f"Removed row at {first}")
        sourceCleanedDescription = teststepBox.data['old']['cleanedDescription']
        sourceId = teststepBox.id
        
        for teststeps in self.testCaseBoxList.values():
            
            for teststep in teststeps:

                # Get the target cleaned description for matching purpose 
                targetCleanedDescription = teststep.data['old']['cleanedDescription']
                targetId = teststep.id

                #If matched, propagate changes to target 
                if sourceCleanedDescription == targetCleanedDescription and sourceId != targetId:
                    # Get target list widget
                    listWidget = teststep.newDataListWidget

                    # Block signals from table model widget to prevent repeated calls to table item inserted event
                    # Propagate insertion of new item
                    listWidget.model().blockSignals(True)
                    item = listWidget.takeItem(first)
                    del item
                    listWidget.model().blockSignals(False)

                    print(targetId)
                    print(listWidget.count())
        

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
        self.ui.mainSearchBar_lineEdit.clear()

        #* Disable scroll area tool widgets
        self.ui.xml_convert_btn.setEnabled(False)
        self.ui.xml_clearTeststeps_btn.setEnabled(False)
        self.ui.mainSearchBar_lineEdit.setEnabled(False)

        #* Disable toggle dropdown button and set it to unchecked
        self.ui.showAll_btn.setEnabled(False)
        self.ui.hideAll_btn.setEnabled(False)

        #* Disable select all checkbox and set it to checked
        self.ui.selectAll_checkBox.setEnabled(False)
        self.ui.selectAll_checkBox.setChecked(True)

        #* Disable summary button
        self.ui.xml_summary_btn.setEnabled(False)

    
    
    def centerWindowOnScreen(self):
        screenGeo = qtw.QDesktopWidget().screenGeometry()
        windowGeo = self.geometry()

        logger.info(
            f"Screen resolution:{screenGeo.width()}x{screenGeo.height()}.\
             Applcation window: {windowGeo.width()}x{windowGeo.height()}"
        )

        xPosition = (screenGeo.width() - windowGeo.width()) / 2 
        yPosition = (screenGeo.height() - windowGeo.height()) / 2 

        self.move(int(xPosition), int(yPosition))


    
    def getUpdatedConversionMap(self):
        #* Create a updated copy of the conversion map based on the latest state of the teststep boxes
        updatedConversionMap = {}
        
        # Iterate through each teststepList in testCaseBoxList
        for teststepList in self.testCaseBoxList.values():

            # Iterate through each teststepGroupBox widget in teststepList
            for teststep in teststepList:
                
                # If teststep has been selected
                # Extract the latest text value of the mapping data and update the convsersion map
                if teststep.id in self.filteredTeststepIds:
                    newTeststepMap = teststep.getNewTeststepMap()
                    updatedConversionMap[teststep.title] = newTeststepMap

        return updatedConversionMap



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
    app.setWindowIcon(qtg.QIcon(os.path.join(baseDir, 'icon.ico')))

    # Create main window
    mainWindow = MainWindow()

    # Get and set the main window style sheet
    with open(os.path.join(baseDir, 'static/style.qss'), 'r') as file:
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
    
