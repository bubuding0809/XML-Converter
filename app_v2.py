import logging
from components.UiMainWindow_v2 import Ui_MainWindow
from components.SummaryDialogWidget import SummaryDialog
from components.TeststepGroupBoxWidget import TeststepGroupBoxWidget
from components.CollapsibleTestcaseWidget import CollapsibleTestcaseWidget
from components.CustomLineEdit import CustomLineEdit
from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
import sys, os, subprocess
import random
import xmlParser
import subprocess
import utils as u
from components.resources import bootstrap_rc
from samples import testFilePaths as testfiles

#* Set up logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
)
logger = logging.getLogger(__name__)



#* Get base directory of application 
baseDir = os.path.dirname(__file__)



class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        #* Initialize UI to main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #* Additional UI setup
        # Create Custom line edit search bar 
        self.ui.mainSearchBar_lineEdit = CustomLineEdit(':/icons/bootstrap-icons-1.8.3/search.svg', 'Search')
        self.ui.mainSearchBar_lineEdit.setMinimumWidth(200)
        self.ui.mainSearchBar_lineEdit.setMaximumWidth(400)
        self.ui.mainSearchBar_lineEdit.setEnabled(False)
        self.ui.dataToolGroup_widget.layout().insertWidget(0, self.ui.mainSearchBar_lineEdit)

        #* QShortcuts
        self.ui.quitSc = qtw.QShortcut(qtg.QKeySequence('Ctrl+W'), self)
        

        #* Signal connectors
        self.ui.setConfigFile_btn.clicked.connect(self.handleXLSXInput)
        self.ui.setXmlFile_btn.clicked.connect(self.handleXMLInput)
        self.ui.setSaveLocation_btn.clicked.connect(self.handleSaveLocation)
        self.ui.xmlATPFileList_widget.itemDoubleClicked.connect(self.handleXMLFileDoubleClick)
        self.ui.xmlATPFileList_widget.itemClicked.connect(self.handleXMLFileClick) 


        self.ui.mainSearchBar_lineEdit.textChanged.connect(self.handleSearchBar)

        # self.ui.xml_loadData_btn.clicked.connect(self.handleXMLLoad)
        # self.ui.xml_clearTeststeps_btn.clicked.connect(self.clearTestStepScrollArea)
        # self.ui.showAll_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        # self.ui.hideAll_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        # self.ui.selectAll_checkBox.pressed.connect(self.handleSelectAllCheckBox)

        
        # self.ui.xml_summary_btn.clicked.connect(self.handleXMLSummary)
        # self.ui.xml_convert_btn.clicked.connect(self.handleXMLConvert)

        self.ui.quitSc.activated.connect(self.handleExitApp)


        #* Global variables
        self.xlsxInFile = testfiles.CONFIG_PATH_WIN32 if sys.platform == 'win32' else testfiles.CONFIG_PATH_DARWIN
        self.xmlInFileList = [testfiles.INPUT_PATH_WIN32 if sys.platform == 'win32' else testfiles.INPUT_PATH_DARWIN,]
        self.xmlOutFileLocation =  testfiles.SAVE_PATH_WIN32 if sys.platform == 'win32' else testfiles.SAVE_PATH_DARWIN

        self.xmlData = {}
        self.filteredTeststepIds = set()
        self.ui.xlsxConfigFilepath_label.setText(self.xlsxInFile)
        self.ui.saveLocationFilepath_label.setText(self.xmlOutFileLocation)
        
        # Initialize conversionMap for testing
        self.conversionMap = xmlParser.handleXlsx(self.xlsxInFile)
        
        
        
    # ************************* Signal Handler methods **************************** #
    def handleXLSXInput(self):
        #* reset conversion map upon clicking config file button
        self.conversionMap.clear()


        #* Retrieve excel config file path from file dialog
        file = qtw.QFileDialog.getOpenFileName(self, 'Input config XLSX file', directory='', filter='Excel files (*.xlsx)')
        if file:
            self.xlsxInFile = file[0]
            self.ui.xlsxConfigFilepath_label.setText(file[0])
        
        
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
                for tag, value in mapping.items():
                    if tag == 'isMatched':
                        continue
                    if not len(value):
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
                f"The following teststeps were found to have empty fields in your config file at {self.xlsxInFile}:\
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
        if len(self.xlsxInFile) and len(self.xmlInFileList):
            self.ui.xml_loadData_btn.setEnabled(True)
        else:
            self.ui.xml_loadData_btn.setEnabled(False)
        self.ui.xml_convert_btn.setEnabled(False)
        self.clearTestStepScrollArea()



    def handleXMLInput(self):
        #* Create fileDialog to choose multiple existing xml files
        fileDialog = qtw.QFileDialog(self)
        fileDialog.setViewMode(qtw.QFileDialog.List)
        fileDialog.setFileMode(qtw.QFileDialog.ExistingFiles)
        fileDialog.setNameFilter('XML files (*.xml)')
        fileDialog.setDirectory('./')

        #* Execute the file dialog and save the selected filepaths to a list
        if fileDialog.exec_():
            selectedFiles = fileDialog.selectedFiles()
            self.xmlInFileList.append(selectedFiles)

            if selectedFiles: self.handlXmlLoadData(selectedFiles)

        

    def handlXmlLoadData(self, selectedFiles):
        #* Create list items based on the selected xml files and add into xmlATPFileList_widget
        for file in selectedFiles:

            #* Initialize testcase obj to contain all testcase items for each file
            testcases = {}
            filteredTeststepIds = set()

            #* Create stacked widget for each xmlFileItem
            xmlFileDataWidget = qtw.QWidget()
            xmlFileDataWidget.setObjectName("xmlFileDataWidget")

            mainVLayout = qtw.QVBoxLayout(xmlFileDataWidget)
            mainVLayout.setContentsMargins(0, 0, 0, 0)

            dataScrollArea = qtw.QScrollArea(xmlFileDataWidget)
            dataScrollArea.setWidgetResizable(True)
            mainVLayout.addWidget(dataScrollArea)

            dataScrollAreaContent_widget = qtw.QWidget()
            scrollContentVLayout = qtw.QVBoxLayout(dataScrollAreaContent_widget)
            
            dataScrollArea.setWidget(dataScrollAreaContent_widget)

            #* Get parsed xml data based on config file and update conversion map
            xmlData, conversionMap = xmlParser.getTestStepData(file, self.conversionMap)

            #* Filter teststeps into their respective testcases
            testCaseList = {}
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

                    #* Create testcase data obj to be passed into the CollapsibleBox widget
                    testcaseData = {
                        'id': testcase,
                        'type': teststeps[0]['parentType'],
                        'teststeps': teststeps
                    }

                    #* Create collapsible box for test case
                    box = CollapsibleTestcaseWidget(
                        title=f"{testcase} <{teststeps[0]['parentType']}>",
                        data=testcaseData
                    )
                    scrollContentVLayout.insertWidget(index, box)
                    
                    #* Create vertical layout for each collapsible box
                    testcaseContentVlayout = qtw.QVBoxLayout()
                    testcaseContentVlayout.setContentsMargins(0, 0, 0, 0)
                    
                    teststepList = []
                    for teststep in teststeps:

                        testStepBox = TeststepGroupBoxWidget(
                            title=f"ID: {teststep['id']} - {teststep['old']['description']}", 
                            data=teststep, 
                            parent=self
                        )

                        testcaseContentVlayout.addWidget(testStepBox)
                        teststepList.append(testStepBox)
                        
                    testcaseContentVlayout.addStretch()
                    box.setContentLayout(testcaseContentVlayout)
                    testcases[box] = teststepList
            else:
                emptyLabel = qtw.QLabel('No test steps matched in XML file')
                scrollContentVLayout.addWidget(emptyLabel)
                
            #* Add stretch to the scroll area content layout to top align the testcases
            scrollContentVLayout.addStretch()


            #* Add Signal handler to each teststep checkbox
            # Iterate over every testStepBoxList
            for teststepList in testcases.values():
                
                # Iterate over every teststep in each teststepBoxList
                for teststep in teststepList:
                    # Add all teststep IDs to the list of filtered teststeps IDs
                    filteredTeststepIds.add(teststep.id)
                    
                    # Get the checkbox object and toggle it
                    checkBox = teststep.hLayout_teststepBox.itemAt(3).widget()
                    checkBox.clicked.connect(lambda _, teststep=teststep: self.handleTestStepCheckbox(teststep))
            
            
            #* Setup autocompleter for search bar to allow for predictive searching of teststeps by description
            # SearchByTeststepDescriptionList = []
            # for teststepList in self.testCaseBoxList.values():
            #     for teststep in teststepList:
            #         SearchByTeststepDescriptionList.append(teststep.title)

            # autoCompleter = qtw.QCompleter(SearchByTeststepDescriptionList, self)
            # autoCompleter.setFilterMode(qtc.Qt.MatchFlag.MatchContains)
            # autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
            # self.ui.mainSearchBar_lineEdit.setCompleter(autoCompleter)


            #* Check if the xml file have already been loaded into the program
            xmlFileData = self.xmlData.get(file, None)

            #* Replace Existing stacked widget with updated data
            if xmlFileData:
                self.ui.stackDataGrids_widget.removeWidget(xmlFileData['widget'])
                self.ui.stackDataGrids_widget.addWidget(xmlFileDataWidget)

                #* Replace xml data with new widget and data objects
                xmlFileData['widget'] = xmlFileDataWidget
                xmlFileData['testcases'] = testcases
                xmlFileData['filteredTeststepIds'] = filteredTeststepIds

            #* Create new data for the xml file
            else:

                #* Create list item for each xmlFile
                baseFileName = os.path.basename(file)
                xmlFileItem = qtw.QListWidgetItem()
                xmlFileItem.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)
                xmlFileItem.setText(baseFileName)
                xmlFileItem.setData(qtc.Qt.UserRole, file)

                #* Add list widget item to the list widget
                self.ui.xmlATPFileList_widget.addItem(xmlFileItem)

                #* Add the newly created datawidget to the stack widget and save the widget and its data to the xmlData object
                self.ui.stackDataGrids_widget.addWidget(xmlFileDataWidget)

                self.xmlData[xmlFileDataWidget] = {
                    'filepath': file,
                    'testcases': testcases,
                    'filteredTeststepIds': filteredTeststepIds
                }





        #* Enable the respective data tool buttons
        self.ui.mainSearchBar_lineEdit.setEnabled(True)
        self.ui.xml_summary_btn.setEnabled(True)
        self.ui.showAll_btn.setEnabled(True)
        self.ui.hideAll_btn.setEnabled(True)
        self.ui.selectAll_checkBox.setEnabled(True)



    def handleSaveLocation(self):
        #* Create fileDialog to choose multiple existing xml files
        fileDialog = qtw.QFileDialog(self)
        fileDialog.setFileMode(qtw.QFileDialog.Directory)
        fileDialog.setDirectory('./')

        #* Execute the file dialog and save the selected filepaths to a list
        if fileDialog.exec_():
            self.xmlOutFileLocation = fileDialog.selectedFiles()
            self.ui.saveLocationFilepath_label.setText(self.xmlOutFileLocation[0] + '/')



    def handleXMLFileDoubleClick(self, item):
        filepath = item.data(qtc.Qt.UserRole)
        print(filepath, 'double clicked')

        for xmlFileWidget, widgetData in self.xmlData.items():
            if filepath == widgetData['filepath']:
                self.ui.stackDataGrids_widget.setCurrentWidget(xmlFileWidget)



    def handleXMLFileClick(self, item):
        #* Display xml file full path at xmlATPFilepath_label 
        self.ui.xmlATPFilepath_label.setText(item.data(qtc.Qt.UserRole))



    def handleExitApp(self):
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle('Exit app')
            msgBox.setText('Confirm with OK to exit the application now')
            msgBox.setIcon(qtw.QMessageBox.Warning)
            msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            msgBox.setDefaultButton(qtw.QMessageBox.Ok)

            msgBox.defaultButton().clicked.connect(qtw.QApplication.instance().quit)

            ret = msgBox.exec_()



    def handleSearchBar(self, text):
        #* Get stacked widget's current widget
        currentStackedWidget = self.ui.stackDataGrids_widget.currentWidget()

        #* Iterate through all the teststeps in the xml file testcase list and show or hide the teststeps based on the search input
        for testcase, teststepList in self.xmlData[currentStackedWidget]['testcases'].items():
            testcase.show()
            isAnyFound = False

            visibleCount = 0
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

            testcase.show() if isAnyFound else testcase.hide()



    def handleTestStepCheckbox(self, teststep):
        #* Get stacked widget's current widget
        currentStackedWidget = self.ui.stackDataGrids_widget.currentWidget()
        widgetData = self.xmlData[currentStackedWidget]
        # Check if the checkbox is checked
        checked = teststep.hLayout_teststepBox.itemAt(3).widget().isChecked()
        
        # if checked, add the teststep id to the filtered set else remove from set
        if checked: 
            widgetData['filteredTeststepIds'].add(teststep.id) 
        else :
            widgetData['filteredTeststepIds'].remove(teststep.id)
        
        print(f"{widgetData['filepath']} Teststep {teststep.id} is checked: {checked}")


        
    #*************************** Utility functions ******************************* #    
    
    def clearTestStepScrollArea(self):
        # Empty global list of testcaseBoxes
        self.xmlData.clear()
        
        # Remove all widgets inside scroll area
        # while self.ui.verticalLayout_3.count():
        #     item = self.ui.verticalLayout_3.takeAt(0)
            
        #     if item.widget():
        #         item.widget().deleteLater()

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

        print(screenGeo, windowGeo)
        xPosition = (screenGeo.width() - windowGeo.width()) / 2 
        yPosition = (screenGeo.height() - windowGeo.height()) / 2 

        self.move(int(xPosition), int(yPosition))


    
    def getUpdatedConversionMap(self):
        #* Create a updated copy of the conversion map based on the latest state of the teststep boxes
        updatedConversionMap = {}
        
        # Iterate through all the teststeps boxes 
        for teststepList in self.testCaseBoxList.values():

            for teststep in teststepList:
                
                # If teststep has been selected
                # Extract the latest text value of the mapping data and update the convsersion map
                if teststep.id in self.filteredTeststepIds:
                    data = teststep.getNewTeststepMap()
                    updatedConversionMap[teststep.title] = {
                        'description': data['description'],
                        'function_library': data['function_library'],
                        'function_name': data['function_name'],
                        'function_parameters': data['function_parameters'],
                    }

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
    app.setWindowIcon(qtg.QIcon(":/icons/bootstrap-icons-1.8.3/tools.svg"))

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