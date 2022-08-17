import collections
import logging
from components.pyqtui.UiMainWindow import Ui_MainWindow
from components.FunctionDefinitionDialogWidget import FunctionDefinitionDialog
from components.WarningDialogWidget import WarningDialog
from components.SummaryDialogWidget import SummaryDialog
from components.TeststepGroupBoxWidget import TeststepGroupBoxWidget
from components.TestcaseGroupBoxWidget import CollapsibleTestcaseWidget
from components.CustomLineEdit import CustomLineEdit
from components.FileFilterProxyModel import FileFilterProxyModel
from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
from deepdiff import DeepDiff
import utils
import sys
import os
import subprocess
import data_processor
import copy


# * Get base directory of application
baseDir = os.path.dirname(__file__)


# * Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(baseDir, 'app.log'),
)
logger = logging.getLogger(__name__)

    
# * Configure windows to identify the application as a custom application to display icon
if sys.platform == 'win32':
    try:
        from ctypes import windll  # Only exists on Windows.
        myappid = 'mycompany.myproduct.subproduct.version'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass


# * Create application entry point
class MainWindow(qtw.QMainWindow):
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # * Initialize main window UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # * Additional UI setup
        # Custom button with icon
        self.ui.configFileUpload_btn.setObjectName('IconOnlyButton')
        self.ui.configFileUpload_btn.setIconSize(qtc.QSize(25, 25))
        self.ui.xmlFileUpload_btn.setObjectName('IconOnlyButton')
        self.ui.xmlFileUpload_btn.setIconSize(qtc.QSize(25, 25))

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
        
        # Map button display text to filter type for quick access
        self.filterButtonGroupMap = {
            radioButton.text(): utils.removeWhiteSpace(radioButton.text().lower())
            for radioButton in self.filterButtonGroup.buttons()
        }

        # * QShortcuts
        # Ctrl + w to quit application
        self.ui.quitSc = qtw.QShortcut(qtg.QKeySequence('Ctrl+W'), self)

        # * Signal event connectors
        self.ui.configFileUpload_btn.clicked.connect(self.handleConfigUpload)
        self.ui.xmlFileUpload_btn.clicked.connect(self.handleXMLUpload)
        self.ui.refreshData_btn.clicked.connect(self.handleRefreshData)
        self.ui.showAll_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        self.ui.hideAll_btn.pressed.connect(self.handleToggleAllDropDownBtn)
        self.ui.xmlSummary_btn.clicked.connect(self.handleXMLSummary)
        self.ui.xmlConvert_btn.clicked.connect(self.handleXMLConvert)
        self.ui.selectAll_checkBox.stateChanged.connect(self.handleSelectAllCheckBox)
        self.ui.mainSearchBar_lineEdit.textChanged.connect(self.handleSearchBar)
        self.ui.configFileUpdate_btn.clicked.connect(self.handleConfigUpdate)
        self.filterButtonGroup.buttonClicked.connect(self.handleFilterButtonClicked)
        self.ui.functionDefinition_action.triggered.connect(self.handleFunctionDefinitionView)
        self.ui.quitSc.activated.connect(self.close)

        # * Initialize excel config attributes
        self.referenceMap = {}
        self.functionDefinitionMap = collections.defaultdict(lambda: {})
        self.duplicateFunctionNames = {'data': {}}
        self.conversionMap = {}
        self.keywordMap = {}

        # * Initialize xml data attributes
        self.xmlInFile = ''
        self.xlsxInFile = ''
        self.testCaseBoxList = {}
        self.filteredTeststepIds = set()
        
        # * Load function definition database and initialize function defintion data
        self.functionDefintionInFile = os.path.join(baseDir, '__ATPFunctionDefinitions.xlsx')
        try:
            self.functionDefinitionMap, self.duplicateFunctionNames = data_processor.handleFunctionDefinitionData(self.functionDefintionInFile)
        except FileNotFoundError:
            message = f'{self.functionDefintionInFile}\ncould not be found.\n\nFunction definitions will not be available for edit.'
            qtw.QMessageBox.warning(self, 'Missing file', message, qtw.QMessageBox.Ok)
        else:
            self.ui.functionDefinition_action.setEnabled(True)

    # ************************* Event Handler methods **************************** #

    # * Handle config excel file upload
    def handleConfigUpload(self):
        # * Retrieve excel config file path from file dialog
        fileDialog = qtw.QFileDialog(self)
        fileDialog.setOption(qtw.QFileDialog.DontUseNativeDialog)
        fileDialog.setProxyModel(FileFilterProxyModel(regex=r'^(?!~\$).+'))
        fileDialog.setWindowTitle('Input config xlsx file')
        fileDialog.setNameFilter('XLSX files (*.xlsx)')
        fileDialog.setDirectory('./samples')

        if fileDialog.exec_():
            # * Save excel config file path and update UI
            selectedFiles = fileDialog.selectedFiles()
            self.xlsxInFile = selectedFiles[0]
            self.ui.configFilePath_display.setText(selectedFiles[0])
        else:
            return

        # * Try to process xlsx file and generate conversion map
        self.handleDataProcessing()

    # * Handle ATP xml file upload
    def handleXMLUpload(self):
        # * Retrieve atp xml file path from file dialog
        fileDialog = qtw.QFileDialog(self)
        fileDialog.setOption(qtw.QFileDialog.DontUseNativeDialog)
        fileDialog.setWindowTitle('Input ATP xml file')
        fileDialog.setNameFilter('XML files (*.xml)')
        fileDialog.setDirectory('./samples')

        if fileDialog.exec_():
            selectedFiles = fileDialog.selectedFiles()
            self.xmlInFile = selectedFiles[0]
            self.ui.xmlFilePath_display.setText(selectedFiles[0])
        else:
            return

        # * Enable load xml data if both xlsx and xml inputs exists
        if self.conversionMap and self.xmlInFile:
            self.handleDataLoad()

    # * handle processing of config excel file data
    def handleDataProcessing(self):
        # * Clear all mappings and duplicate warning data
        self.referenceMap.clear()
        self.conversionMap.clear()
        self.keywordMap.clear()
        
        try:
            # * Parse config excel to generate conversion mapping and warning data
            # Generate reference map and duplicate reference warnings from the parameter reference sheet
            self.referenceMap, duplicateReferences = data_processor.handleReferenceData(self.xlsxInFile)
            
            # Generate mapping data from the mapping sheet
            self.conversionMap, self.keywordMap, self.warningData = data_processor.handleMappingData(self.xlsxInFile, self.referenceMap, self.functionDefinitionMap)
            
            # Append warnings to the warning data object
            self.warningData.append(duplicateReferences)
            
            # By any chance the function defintion data base has been altered manually and there are duplicate function names,
            # update the duplicate function names warning data
            self.warningData.append(self.duplicateFunctionNames)
        
        except Exception as ex:
            # Catch exceptions and handle them
            exception = f"There is an error with the xlsx config file.\
                \n\nPlease try to upload a correct config file or edit the current config file."
          
            # parse exception arguments for display
            arguments = '\n'.join(
                [f"{index+1}: {arg}" for index, arg in enumerate(list(ex.args))])

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
            editConfig = msgBox.addButton(
                'Edit config', qtw.QMessageBox.ApplyRole)
            retryBtn = msgBox.addButton(
                'Try again', qtw.QMessageBox.AcceptRole)

            msgBox.setIcon(qtw.QMessageBox.Critical)
            msgBox.setWindowModality(qtc.Qt.WindowModal)

            ret = msgBox.exec()

            # If user clicks on retry button, open file dialog for user to select config file again
            if msgBox.clickedButton() == retryBtn:
                self.handleConfigUpload()
                return

            # IF user clicks on edit config, open up config file in Excel for user to edit
            if msgBox.clickedButton() == editConfig:
                # macOS
                if sys.platform == 'darwin':
                    subprocess.call(('open', self.xlsxInFile))
                # Windows
                elif sys.platform == 'win32':
                    os.startfile(self.xlsxInFile)
            
            # Reset application to default state if there is an error with the config file
            self.resetAllXmlData()
    
        else:
            def loadData():
                # Enable update config button
                self.ui.configFileUpdate_btn.setEnabled(True)
                
                # If xml file is uploaded, parse xml data with conversion map then display in UI
                if self.xmlInFile: self.handleDataLoad()
                
            # If there are any warning data generated from checking the config file
            # Create and show a warning dialog widget to display the warning information
            # Once error message is closed, load data
            if any(True if warning['data'] else False for warning in self.warningData):
                warningDialog = WarningDialog(self, self.xlsxInFile, self.warningData)
                warningDialog.finished.connect(loadData)
                warningDialog.open()
                
            # If there are no warnings, load data if xml file is uploaded
            else:
                loadData()

    # * handle loading of xml data grid into UI
    def handleDataLoad(self):
        # * Reset all xml data
        self.resetAllXmlData()

        # * Reset all isMatch flags in conversion map to False
        for mapping in self.conversionMap.values():
            mapping['isMatched'] = False

        # * Get parsed xml data and updated conversion map
        try:
            # Catch errors thrown from xml processing
            testcaseSortedXmlData, self.conversionMap = data_processor.handleTranslateXmlData(
                self.xmlInFile, self.conversionMap, self.keywordMap)
        except Exception as ex:
            # Catch exceptions and handle them
            exception = f"An exception of type {type(ex)} occurred."
            arguments = '\n'.join(
                [f"{index+1}: {arg}" for index, arg in enumerate(list(ex.args))])

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

        # * Create mapped data boxes and insert into the vertical scroll layout area
        if testcaseSortedXmlData:
            for index, (testcase, teststeps) in enumerate(testcaseSortedXmlData.items()):

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

                    # * Connect teststep box data modification signals to callbacks
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
                        self.handleRowsInserted(
                            modelIndex, first, last, teststepBox, listWidget)
                    )

                    teststepBox.newDataListWidget.model().rowsRemoved.connect(
                        lambda modelIndex, first, last, teststepBox=teststepBox, listWidget=teststepBox.newDataListWidget:
                        self.handleRowsRemoved(
                            modelIndex, first, last, teststepBox, listWidget)
                    )

                    # Add teststep box to vlayout and store in a list
                    vlayout.addWidget(teststepBox)
                    teststepBoxList.append(teststepBox)

                vlayout.addStretch()
                box.setContentLayout(vlayout)
                box.setVisible(True)
                self.testCaseBoxList[box] = teststepBoxList
        else:
            emptyLabel = qtw.QLabel('No test steps matched in XML file')
            self.ui.verticalLayout_3.addWidget(emptyLabel)
        self.ui.verticalLayout_3.addStretch()

        # * Alert user if there are unmatched teststeps
        # get list of unmatched classic description keys
        unmatchedClassicDescriptions = data_processor.getUnmatchedClassicDescriptions(self.conversionMap)

        # If there are unmatched teststeps, alert user with a message box with the list of unmatched teststeps
        if unmatchedClassicDescriptions:

            # Create message box to display the warning
            msgBox = qtw.QMessageBox(self)
            msgBox.setWindowTitle('Warning')
            msgBox.setText(
                f"There are unmatched teststeps descriptions in your config file.")

            # Create string list of unmatched teststeps and to message
            unmatchedClassicDescriptions = '\n'.join(
                [f"{index+1}: {teststep}" for index,
                    teststep in enumerate(unmatchedClassicDescriptions)]
            )
            noMatchMessage = (
                f"The following teststeps descriptions at {self.xlsxInFile} had no match in the xml file:\
                \n--------------------------------------------------------\
                \n\n{unmatchedClassicDescriptions}"
            )

            # Merge message and set message box detailed text
            msgBox.setDetailedText(noMatchMessage)

            # Set message buttons and icons
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            editConfig_btn = msgBox.addButton(
                'Edit config', qtw.QMessageBox.AcceptRole)
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

        # * Add Signal handler to each teststep checkbox
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
                    self.handleTestStepSelection(teststep)
                )

        # * Setup autocompleter for search bar to allow for predictive searching of teststeps by description
        teststepDescriptionSet = set()

        # Append title of visible teststeps to autocomplete list
        for teststepBoxList in self.testCaseBoxList.values():
            for teststep in teststepBoxList:
                teststepDescriptionSet.add(teststep.searchKey)

        autoCompleter = qtw.QCompleter(teststepDescriptionSet, self)
        autoCompleter.setFilterMode(qtc.Qt.MatchFlag.MatchContains)
        autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.ui.mainSearchBar_lineEdit.setCompleter(autoCompleter)

        # * Enable all tool buttons after succesfully loading XML file
        # Enable search bar
        self.ui.mainSearchBar_lineEdit.setEnabled(True)

        # Enable toggle drop down button and set it to unchecked
        self.ui.showAll_btn.setEnabled(True)
        self.ui.hideAll_btn.setEnabled(True)

        # Enable select all checkbox and set it to checked
        self.ui.selectAll_checkBox.setEnabled(True)
        self.ui.selectAll_checkBox.setChecked(True)

        # Enable update config button
        self.ui.configFileUpdate_btn.setEnabled(True)

        # Enable summary button
        self.ui.xmlSummary_btn.setEnabled(True)

        # Enable convert button
        self.ui.xmlConvert_btn.setEnabled(True)

        # Enable filter radio buttons
        self.ui.scrollAreaFilterBox_widget.setEnabled(True)
        self.ui.filterBoth_btn.setChecked(True)

        # Enable refresh data button
        self.ui.refreshData_btn.setEnabled(True)

    # * handle toggling of testcase dropdown expand/collapse
    def handleToggleAllDropDownBtn(self):
        # Get the dropdown button object
        eventSender = self.sender()
        
        # * If button clicked is the expand button, expand all dropdown boxes
        # * If button clicked is the collapse button, collapse all dropdown boxes
        if eventSender == self.ui.showAll_btn:
            # Show all testcases
            for testcaseBox in self.testCaseBoxList:
                if not testcaseBox.isChecked:
                    testcaseBox.toggle_button.click()

        else:
            # Hide all testcases
            for testcaseBox in self.testCaseBoxList:
                if testcaseBox.isChecked:
                    testcaseBox.toggle_button.click()

    # * handle toggling of select all checkbox
    def handleSelectAllCheckBox(self, state):
        # * Get current checked filter radio button
        checkFilterButton = self.filterButtonGroup.checkedButton()
        filterTypeChecked = self.filterButtonGroupMap[checkFilterButton.text()]

        # * Get state of select all checkbox state == 0: unchecked, state == 2: checked
        isChecked = True if state else False

        # * Iterate over every teststepBoxList and its teststeps
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

    # * handle teststep search operation in search bar
    def handleSearchBar(self, text):
        checkFilterButton = self.filterButtonGroup.checkedButton()
        filterTypeChecked = self.filterButtonGroupMap[checkFilterButton.text()]

        for testcase, teststepList in self.testCaseBoxList.items():
            isAnyFound = False
            visibleCount = 0

            testcase.show()

            # * Show teststeps that matches the search keywords, else hide them
            for teststep in teststepList:
                if text.lower() in teststep.title.lower():
                    teststep.show()
                    isAnyFound = True
                    visibleCount += 1
                else:
                    teststep.hide()

            # * Update testcaseBoxWidget with new visibility count
            testcase.toggle_button.setText(
                f"{testcase} ({str(visibleCount)}/{len(teststepList)})"
            )

            # * Only show the testcases with teststeps that matches the search
            if isAnyFound and (filterTypeChecked == testcase.type or filterTypeChecked == 'both'):
                testcase.show()
            else:
                testcase.hide()

            # * Resize collapsible box height to fit to newly visibile contents
            if testcase.isVisible():
                # Get content height of visible teststeps
                content_height = testcase.content_area.layout().sizeHint().height()

                # Reisize testcase box
                testcase.setMinimumHeight(
                    26 + content_height if testcase.isChecked else 26)
                testcase.setMaximumHeight(
                    26 + content_height if testcase.isChecked else 26)

                # Resize testcase box content area
                testcase.content_area.setMinimumHeight(
                    content_height if testcase.isChecked else 0)
                testcase.content_area.setMaximumHeight(
                    content_height if testcase.isChecked else 0)

    # * handle teststep radio button selection for filtering teststeps for conversion
    def handleTestStepSelection(self, teststep):
        # * Check if the checkbox is checked
        checked = teststep.hLayout_teststepBox.itemAt(3).widget().isChecked()

        # * if checked, add the teststep id to the filtered set else remove from set
        if checked:
            self.filteredTeststepIds.add(teststep.id)
        else:
            self.filteredTeststepIds.remove(teststep.id)

    # * handle generation of conversion summary and showing of summary dialog box
    def handleXMLSummary(self):
        # * Create summary dialog widget and show
        summaryDialog = SummaryDialog(
            self,
            data=self.testCaseBoxList,
            filteredIds=self.filteredTeststepIds
        )
        summaryDialog.open()

    # * handle conversion of XML file to DD2.0 capable version
    def handleXMLConvert(self):
        # * Open file dialog and get save file path
        file = qtw.QFileDialog.getSaveFileName(
            self, 'Save converted ATP XML file', filter='XML files (*.xml)')

        # * If user defines save as file, save filepath to variable
        if file[0]:
            xmlOutFile = file[0]
        else:
            return

        conversionMap = self.getFinalConversionMap()

        # * Try to execute Execute XML conversion
        try:
            data_processor.handleConvertXml(
                self.filteredTeststepIds, self.xmlInFile,
                xmlOutFile, conversionMap
            )

        except Exception as ex:
            # If exception caught is Permission Error set specific exception text
            if type(ex) == PermissionError:
                exception = f"The action can't be completed because the file is open.\
                \n\nClose the file and try again."

            # Else create generic exception text
            else:
                exception = f"An exception of type {type(ex)} occurred."

            arguments = '\n'.join(
                [f"{index+1}: {arg}" for index,
                    arg in enumerate(list(ex.args))]
            )

            # Create message box to display the error
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle('Error')
            msgBox.setText(exception)
            msgBox.setIcon(qtw.QMessageBox.Critical)
            msgBox.setDetailedText(
                f"Here are the error arguments:\
                \n--------------------------------------------------------\
                \n\n{arguments}"
            )
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            retryBtn = msgBox.addButton(
                'Try again', qtw.QMessageBox.AcceptRole)

            ret = msgBox.exec()

            if msgBox.clickedButton() == retryBtn:
                self.handleXMLConvert()
            return 

        # * Create success message box
        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle("Success")
        msgBox.setText("Successfully converted ATP XML file")
        msgBox.setIcon(qtw.QMessageBox.Information)
        checkbox = qtw.QCheckBox('Show file in explorer', msgBox)
        checkbox.setChecked(True)
        msgBox.setCheckBox(checkbox)
        ret = msgBox.exec_()

        # * Open file in explorer/finder if option is checked
        if checkbox.isChecked():
            if sys.platform == 'win32':
                xmlOutFile = xmlOutFile.replace('/', '\\')
                subprocess.Popen(f'explorer /select,{xmlOutFile}')

            elif sys.platform == 'darwin':
                subprocess.call(['open', '-R', xmlOutFile])

    # * handle filtering of teststeps for display based on filter type selection
    def handleFilterButtonClicked(self, button):
        filterTypeChecked = self.filterButtonGroupMap[button.text()]

        for testcase, teststeps in self.testCaseBoxList.items():

            # * If testcase type matches filter or filter is both, show testcase and show all its teststeps. Else hide the testcase
            if filterTypeChecked == testcase.type or filterTypeChecked == 'both':
                testcase.show()

                # Show all teststep under the testcase
                for teststep in teststeps:
                    teststep.show()

            else:
                testcase.hide()

        # * Create new autocomplete list for search bar based on filtered data
        teststepDescriptionSet = set()
        # Append title of visible teststeps to autocomplete list
        for teststepBoxList in self.testCaseBoxList.values():
            for teststep in teststepBoxList:
                if teststep.isVisible():
                    teststepDescriptionSet.add(teststep.searchKey)

        # Setup autocompleter
        autoCompleter = qtw.QCompleter(teststepDescriptionSet, self)
        autoCompleter.setFilterMode(qtc.Qt.MatchFlag.MatchContains)
        autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.ui.mainSearchBar_lineEdit.setCompleter(autoCompleter)

        # * Check select all checkbox and call handleSelect All checkbox to reset selection for new filtered data
        self.ui.selectAll_checkBox.setChecked(True)
        self.ui.mainSearchBar_lineEdit.clear()
        self.handleSelectAllCheckBox(2)

        # * Hide all teststeps by default
        for testcaseBox in self.testCaseBoxList:
            if testcaseBox.isChecked:
                testcaseBox.toggle_button.click()
    
    # * handle propagation of mapping data change in data grid
    def handleAbstractItemTextChange(self, item, teststepBox):

        # Check if item edited belongs to table widget
        isTableWidget = type(item) == type(qtw.QTableWidgetItem())

        # * Get item text, parent widget of item, item postion and cleaned description of the teststep box
        changedText = item.text()
        widget = item.tableWidget() if isTableWidget else item.listWidget()
        position = widget.column(item) if isTableWidget else widget.row(item)
        sourceConfigRowCount = teststepBox.data['configRowCount']

        # * Iterate through all teststeps with the same classic description and propagate the changed text
        for teststeps in self.testCaseBoxList.values():

            for teststep in teststeps:

                # Get the target cleaned description for matching purpose
                targetConfigRowCount = teststep.data['configRowCount']

                # If matched, propagate changes to target
                if sourceConfigRowCount == targetConfigRowCount:
                    # Get target table widget
                    widget = teststep.newDataTableWidget if isTableWidget else teststep.newDataListWidget

                    # Get target table item
                    item = widget.item(
                        0, position) if isTableWidget else widget.item(position)

                    # Block signals from table widget to prevent repeated calls to table item changed event
                    widget.blockSignals(True)

                    # Propagate change to table item text
                    item.setText(changedText)

                    # Unblock singals from table widget once text has been changed
                    widget.blockSignals(False)

    # * handle propagation of function parameter insertion in data grid
    def handleRowsInserted(self, modelIndex, first, last, teststepBox, listWidget):
        item = listWidget.item(first)
        sourceConfigRowCount = teststepBox.data['configRowCount']
        sourceId = teststepBox.id

        for teststeps in self.testCaseBoxList.values():

            for teststep in teststeps:

                # Get the target cleaned description for matching purpose
                targetConfigRowCount = teststep.data['configRowCount']
                targetId = teststep.id

                # If matched, propagate changes to target
                if sourceConfigRowCount == targetConfigRowCount and sourceId != targetId:
                    # Get target list widget
                    listWidget = teststep.newDataListWidget

                    # Create new list item
                    newItem = qtw.QListWidgetItem('')
                    newItem.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable |
                                     qtc.Qt.ItemIsDragEnabled | qtc.Qt.ItemIsEnabled)

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

    # * handle propagation of function parameter deletion in data grid
    def handleRowsRemoved(self, modelIndex, first, last, teststepBox, listWidget):
        sourceConfigRowCount = teststepBox.data['configRowCount']
        sourceId = teststepBox.id

        for teststeps in self.testCaseBoxList.values():

            for teststep in teststeps:

                # Get the target cleaned description for matching purpose
                targetConfigRowCount = teststep.data['configRowCount']
                targetId = teststep.id

                # If matched, propagate changes to target
                if sourceConfigRowCount == targetConfigRowCount and sourceId != targetId:
                    # Get target list widget
                    listWidget = teststep.newDataListWidget

                    # Create temp item to trigger repaint event
                    tempItem = qtw.QListWidgetItem('')
                    tempItem.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable |
                                      qtc.Qt.ItemIsDragEnabled | qtc.Qt.ItemIsEnabled)

                    # Block signals from table model widget to prevent repeated calls to table item inserted event
                    # Propagate insertion of new item
                    listWidget.model().blockSignals(True)
                    item = listWidget.takeItem(first)
                    del item
                    listWidget.model().blockSignals(False)

    # * handle saving updated config mapping to config excel file
    def handleConfigUpdate(self):
        configData = {}

        # * Get updated mapping data from UI data grid
        for teststeps in self.testCaseBoxList.values():

            for teststep in teststeps:

                # Get cleaned teststep description
                configRowCount = teststep.data['configRowCount']

                if configRowCount in configData:
                    continue

                # New table data
                description = teststep.newDataTableWidget.item(0, 0).text()
                function_library = teststep.newDataTableWidget.item(0, 1).text()
                function_name = teststep.newDataTableWidget.item(0, 2).text()

                # New List data
                function_parameters = []
                for i in range(teststep.newDataListWidget.count()):
                    param = teststep.newDataListWidget.item(i).text()
                    function_parameters.append(param)

                configData[configRowCount] = {
                    'description': description,
                    'function_name': function_name,
                    'function_library': function_library,
                    'function_parameters': function_parameters
                }

        # * Open file dialog box for user to save new config file
        file = qtw.QFileDialog.getSaveFileName(
            self, 'Save updated config file', './', 'Xlsx files (*.xlsx)'
        )

        # * If user defines save as file, save filepath to variable, else cancel operation
        if file[0]:
            xlsxOutFile = file[0]
        else:
            return

        try:
            data_processor.handleConfigFileUpdate(
                self.functionDefinitionMap, self.xlsxInFile, xlsxOutFile, configData
            )

            # * Create success message box
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle("Success")
            msgBox.setText("Successfully saved updated config file")
            msgBox.setIcon(qtw.QMessageBox.Information)
            checkbox = qtw.QCheckBox('Show file in explorer', msgBox)
            checkbox.setChecked(True)
            msgBox.setCheckBox(checkbox)
            ret = msgBox.exec_()

            # * Open file in explorer/finder if option is checked
            if checkbox.isChecked():
                if sys.platform == 'win32':
                    xlsxOutFile = xlsxOutFile.replace('/', '\\')
                    subprocess.Popen(f'explorer /select,{xlsxOutFile}')

                elif sys.platform == 'darwin':
                    subprocess.call(['open', '-R', xlsxOutFile])
        except Exception as ex:
            # If exception caught is Permission Error set specific exception text
            if type(ex) == PermissionError:
                exception = f"The action can't be completed because the file is open in Excel.\
                \n\nClose the file and try again."

            # Else create generic exception text
            else:
                exception = f"An exception of type {type(ex)} occurred."

            arguments = '\n'.join(
                [f"{index+1}: {arg}" for index,
                    arg in enumerate(list(ex.args))]
            )

            # Create message box to display the error
            msgBox = qtw.QMessageBox()
            msgBox.setWindowTitle('Error')
            msgBox.setText(exception)
            msgBox.setIcon(qtw.QMessageBox.Critical)
            msgBox.setDetailedText(
                f"Here are the error arguments:\
                \n--------------------------------------------------------\
                \n\n{arguments}"
            )
            msgBox.setStandardButtons(qtw.QMessageBox.Ok)
            retryBtn = msgBox.addButton(
                'Try again', qtw.QMessageBox.AcceptRole)

            ret = msgBox.exec()

            if msgBox.clickedButton() == retryBtn:
                self.handleConfigUpdate()

    # * handle refreshing of UI data grid based on latest config file and xml file
    def handleRefreshData(self):
        if self.xlsxInFile and self.xmlInFile:
            # Reprocess config and xml data
            self.handleDataProcessing()

            self.ui.refreshData_btn.setEnabled(True)

    # * handle opening of function definition data view
    def handleFunctionDefinitionView(self):
        functionDefinitionDialog = FunctionDefinitionDialog(self, copy.deepcopy(self.functionDefinitionMap))
        functionDefinitionDialog.accepted.connect(lambda: self.ui.statusbar.showMessage('Function definitions saved'))
        functionDefinitionDialog.open()

    #*************************** Utility functions ******************************* #

    # * Handles reset of application to default state
    def resetAllXmlData(self):
        # clear set of filtered Ids
        self.filteredTeststepIds.clear()

        # Empty list of testcaseBoxes
        self.testCaseBoxList.clear()

        # Remove all widgets inside scroll area
        while self.ui.verticalLayout_3.count():
            item = self.ui.verticalLayout_3.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        # * Clear search bar
        self.ui.mainSearchBar_lineEdit.clear()

        # * Disable scroll area tool widgets
        self.ui.xmlConvert_btn.setEnabled(False)
        self.ui.mainSearchBar_lineEdit.setEnabled(False)

        # * Disable toggle dropdown button and set it to unchecked
        self.ui.showAll_btn.setEnabled(False)
        self.ui.hideAll_btn.setEnabled(False)

        # * Disable select all checkbox and set it to checked
        self.ui.selectAll_checkBox.setEnabled(False)
        self.ui.selectAll_checkBox.setChecked(True)

        # * Disable summary button
        self.ui.xmlSummary_btn.setEnabled(False)

        # * Disable update config button
        self.ui.configFileUpdate_btn.setEnabled(False)

        # * Disable filter group box
        self.ui.scrollAreaFilterBox_widget.setEnabled(False)

    # * Handles centering of application window on open 
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

    # * Handles getting of latest conversion map generated from UI data grid
    def getFinalConversionMap(self):
        # * Create a updated copy of the conversion map based on the latest state of the teststep boxes
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

    #*************************** Virtual functions ******************************* #

    # * Overriding close event function to handle closing of application
    def closeEvent(self, event) -> None:
        # * Create message box to confirm quitting of application
        msgBoxButtonClicked = qtw.QMessageBox.question(
            self, 
            'Closing application window', 
            'Any unsaved progress will be lost. Confirm closing of application?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No
        )
    
        # * Proceed with quitting proceedure if yes is clicked
        if msgBoxButtonClicked == qtw.QMessageBox.Yes:

            if not self.xlsxInFile:
                return event.accept()

            # * Generate function defintion map from config file
            # * Compare function definition maps of config file and application
            # * If there is a difference prompt user to update config file
            try:
                functionDefinitionMap, _ = data_processor.handleFunctionDefinitionData(self.xlsxInFile)
            except KeyError:

                msgBoxButtonClicked = qtw.QMessageBox.warning(
                    self, 
                    'Closing application window', 
                    'Your config file is out of date. Update your config file before quitting?',
                    qtw.QMessageBox.Yes | qtw.QMessageBox.No
                )

                # * Prompt user to save updated config file if yes is clicked
                if msgBoxButtonClicked == qtw.QMessageBox.Yes:
                    self.handleConfigUpdate()

                return event.accept()

            # * If functio definition map is loaded without issues
            # * Use it to check against the application function definitions to see if an update is needed
            # * Create message box to prompt user to save updated config file if needed.
            if DeepDiff(functionDefinitionMap, self.functionDefinitionMap):
                msgBoxButtonClicked = qtw.QMessageBox.warning(
                    self, 
                    'Closing application window', 
                    'Your config file is out of date. Update your config file before quitting?',
                    qtw.QMessageBox.Yes | qtw.QMessageBox.No
                )

                # * Prompt user to save updated config file if yes is clicked
                if msgBoxButtonClicked == qtw.QMessageBox.Yes:
                    self.handleConfigUpdate()

                return event.accept()

            return event.accept()

        # * Prevent application from closing if no is clicked
        event.ignore()


# * Instantiate application and run it
if __name__ == '__main__':
    # Create application and set application icon
    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(qtg.QIcon(os.path.join(baseDir, 'icon.ico')))

    # Create main window
    mainWindow = MainWindow()

    # Open and read style sheet into string format
    with open(os.path.join(baseDir, 'static/style.qss'), 'r') as file:
        stylesheet = file.read()
        
    # Set style sheet
    mainWindow.setStyleSheet(stylesheet)

    # Customize window settings
    mainWindow.setWindowTitle('ATP XML-Converter')
    mainWindow.resize(1600, 900)
    mainWindow.centerWindowOnScreen()
    mainWindow.show()
    
    # Log application start
    logger.info('App started')

    # Execute application
    sys.exit(app.exec_())