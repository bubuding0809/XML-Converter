from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
from .pyqtui.UiFunctionDefinitionDialog import Ui_FunctionDefinitionDialog
from .pyqtui.UiNewFunctionDialog import Ui_NewFunctionDialog
from .CustomLineEdit import CustomLineEdit
import sys
import os
import subprocess
import data_processor
from deepdiff import DeepDiff

class NewFunctionDialog(qtw.QDialog):

    def __init__(self, parent=None, data=None, *args, **kwargs) -> None:
        super(NewFunctionDialog, self).__init__(parent, *args, **kwargs)

        self.ui = Ui_NewFunctionDialog()
        self.ui.setupUi(self)
        self.data = data

        # * Additional UI setup
        # Set dialog title
        self.setWindowTitle('Function definitions')

        # Set object name for buttons to receive custom styling
        self.ui.addParam_btn.setObjectName('IconOnlyButton')
        self.ui.removeParam_btn.setObjectName('IconOnlyButton')

        # Install event filter for function parameter list to add addtional functionality
        self.ui.functionParameterlist_widget.installEventFilter(self)

        # Get save button from dialog button box and set it to disabled 
        self.saveBtn = self.ui.dialogButton_box.button(qtw.QDialogButtonBox.Save)
        self.saveBtn.setEnabled(False)

        functionLibraryCompleter = qtw.QCompleter([functionLibrary for functionLibrary in self.data.keys()])
        functionLibraryCompleter.setFilterMode(qtc.Qt.MatchFlag.MatchContains)
        functionLibraryCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.ui.functionLibrary_edit.setCompleter(functionLibraryCompleter)
        
        #* Event Signal Handlers
        self.accepted.connect(self.handleSaveNewFunction)
        self.ui.functionLibrary_edit.textChanged.connect(self.handleFormInputChange)
        self.ui.functionName_edit.textChanged.connect(self.handleFormInputChange)
        self.ui.addParam_btn.clicked.connect(lambda: self.handleParamListActions('ADD'))
        self.ui.removeParam_btn.clicked.connect(lambda: self.handleParamListActions('DELETE'))

    def handleSaveNewFunction(self):
        newFunctionLibrary = self.ui.functionLibrary_edit.text().strip()
        newFunctionName = self.ui.functionName_edit.text().strip()
        newFunctionParameters = [
            self.ui.functionParameterlist_widget.item(i).text().strip() 
            for i in range(self.ui.functionParameterlist_widget.count())
            if self.ui.functionParameterlist_widget.item(i).text()
        ]

        if newFunctionLibrary and newFunctionName:
            self.data[newFunctionLibrary][newFunctionName] = {
                'rowCount': None,
                'function_parameters': newFunctionParameters
            }

    def handleFormInputChange(self):
        newFunctionLibrary = self.ui.functionLibrary_edit.text()
        newFunctionName = data_processor.removeWhiteSpace(self.ui.functionName_edit.text().lower())

        #* Check if new function name is unique
        exisitingFunctionNames = (
            data_processor.removeWhiteSpace(functionName.lower()) 
            for functionNames in self.data.values() 
            for functionName in functionNames.keys()
        )

        isUniqueName = not (newFunctionName and newFunctionName in exisitingFunctionNames)

        #* if function name is unique and both libray and name fields are not empty, enable saveBtn
        if isUniqueName and newFunctionLibrary and newFunctionName:
            self.saveBtn.setEnabled(True)
        else:
            self.saveBtn.setEnabled(False)
        
        #* Display tooltip prompt for invalid function name if function name is not unique
        if not isUniqueName:
            qtw.QToolTip.showText(
                self.ui.functionName_edit.mapToGlobal(qtc.QPoint(0, 10)), 
                'Function name is already in use',
                self.ui.functionName_edit,
                self.ui.functionName_edit.rect(),
                1500
            )

    def handleParamListActions(self, action):
        listWidget = self.ui.functionParameterlist_widget
        if action == 'DELETE':
            #* Get the selected item modelIndexes and use it to delete the selected items
            for index, modelIndex in enumerate(listWidget.selectedIndexes()):
                item = listWidget.takeItem(modelIndex.row() - index)  
                del item
        else:
            #* Insert new item below the selected item and set it to be selected and in edit mode
            item = qtw.QListWidgetItem()
            item.setText('functionParameter')
            item.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable| qtc.Qt.ItemIsDragEnabled | qtc.Qt.ItemIsEnabled)
            listWidget.insertItem(listWidget.currentRow() + 1, item)
            listWidget.setCurrentItem(item)
            listWidget.editItem(item)
    
    # ************************ Virtual functions ************************ #
    
    def eventFilter(self, source, event) -> bool:
        #* If the source is not from a ListWidget Object, return
        if source is not self.ui.functionParameterlist_widget:
            return False

        # Handle right click context menu
        if event.type() == qtc.QEvent.ContextMenu:
            # Create a context menu and add the actions
            menu = qtw.QMenu()
            
            addParamAction = menu.addAction('Insert below')
            deleteSelectedParamAction = menu.addAction('Delete selected')
            
            action = menu.exec_(event.globalPos())

            # Call the respective functions based on the action
            if action == addParamAction:
                self.handleParamListActions('ADD')
            elif action == deleteSelectedParamAction:
                self.handleParamListActions('DELETE')

            return True


        if event == qtg.QKeySequence.Delete:
            #* Get the selected item modelIndexes and use it to delete the selected items
            self.handleParamListActions('DELETE')

            return True

        return super(NewFunctionDialog, self).eventFilter(source, event)
    
    def accept(self) -> None:
        paramList = self.ui.functionParameterlist_widget
        newFunctionParameters = [paramList.item(i).text() for i in range(paramList.count()) if paramList.item(i).text()]

        if len(newFunctionParameters) != len(set(newFunctionParameters)):
            qtw.QMessageBox.critical(self, 'Error', 'There are duplicate function parameter, please ensure that all parameters are unique.')
        else:
            super().accept()

class FunctionDefinitionDialog(qtw.QDialog):

    def __init__(self, parent=None, functionDefinitionMap=None, *args, **kwargs) -> None:
        super(FunctionDefinitionDialog, self).__init__(parent, *args, **kwargs)

        self.parent = parent
        self.functionDefinitionMap = functionDefinitionMap
        self.ui = Ui_FunctionDefinitionDialog()
        self.ui.setupUi(self)
        self.handlepopulateFunctionDefinitionData()

        # * Additional UI setup
        header = self.ui.functionLibraryTree_widget.header()
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)

        #  Create custom line edit for search bar
        self.ui.functionDefinition_searchBar = CustomLineEdit(':/icons/bootstrap-icons-1.8.3/search.svg', 'Search')
        self.ui.functionDefinition_searchBar.setMinimumWidth(300)
        self.ui.functionDefinition_searchBar.setMaximumWidth(400)
        self.ui.dataTreeSearchBox_widget.layout().insertWidget(0,  self.ui.functionDefinition_searchBar)

        # Setup autocompleter for function names in search bar
        self.setSearchBarAutoCompleter()

        # Set dialog title
        self.setWindowTitle('Function definitions')

        # * Event Signal Connectors
        self.ui.newFunction_btn.clicked.connect(self.handleNewFunction)
        self.ui.functionLibraryTree_widget.itemClicked.connect(self.handlepopulateFunctionParameterList)
        self.ui.functionDefinition_searchBar.textChanged.connect(self.handleSearchBar)
        self.ui.showAll_btn.clicked.connect(lambda: self.handleDropDown(True))
        self.ui.hideAll_btn.clicked.connect(lambda: self.handleDropDown(False))
        self.ui.deleteFunction_btn.clicked.connect(self.handleDeleteFuncton)

    def handlepopulateFunctionDefinitionData(self):
        for functionLibrary, functionNames in self.functionDefinitionMap.items():
            functionLibraryItem = qtw.QTreeWidgetItem()
            font = qtg.QFont('Arial', pointSize=10)
            font.setBold(True)

            functionLibraryItem.setFont(0, font)
            functionLibraryItem.setText(0, functionLibrary)

            for i in range(2):
                functionLibraryItem.setForeground(i, qtg.QColor('white'))
                functionLibraryItem.setBackground(i, qtg.QColor('darkGrey'))

            self.ui.functionLibraryTree_widget.addTopLevelItem(functionLibraryItem)

            for functionName, data in functionNames.items():
                functionNameItem = qtw.QTreeWidgetItem()
                functionNameItem.setText(1, functionName)
                functionLibraryItem.addChild(functionNameItem)
    
    def handlepopulateFunctionParameterList(self, item):
        # * Get Top level function library item and function name item
        functionlibraryItem = item.parent()
        functionName = item.text(1)

        # Clear parameter list widget
        self.ui.functionParametersList_wigdet.clear()

        # * If item clicked is a function name item
        # * Display function parameters in the parameter list widget
        if functionlibraryItem and functionName:
            functionLibrary = functionlibraryItem.text(0)
            functionParameters = self.functionDefinitionMap[functionLibrary][functionName]['function_parameters']
            self.ui.functionParametersList_wigdet.addItems(functionParameters)
    
    def handleNewFunction(self):
        newFunctionDialog = NewFunctionDialog(self, self.functionDefinitionMap)
        newFunctionDialog.accepted.connect(self.refreshFunctionDefinitionData)
        newFunctionDialog.open()

    def handleDeleteFuncton(self):
        selectedItem = self.ui.functionLibraryTree_widget.selectedItems()
        if selectedItem: 
            selectedItem = selectedItem[0]
        else:
            return
        
        informativeText = ''
        if not selectedItem.text(0) and selectedItem.text(1):
            informativeText = f"{selectedItem.text(1)} will be removed"
        else:
            informativeText = f"{selectedItem.text(0)} and all its functions will be removed."

        msgBox = qtw.QMessageBox()
        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle("Confirm deletion")
        msgBox.setText("Please confirm that you are trying to delete the following item:")
        msgBox.setInformativeText(informativeText)
        msgBox.setIcon(qtw.QMessageBox.Question)
        msgBox.setStandardButtons(qtw.QMessageBox.Cancel)
        confrimBtn = msgBox.addButton('confirm', qtw.QMessageBox.AcceptRole)

        ret = msgBox.exec_()

        if msgBox.clickedButton() == confrimBtn:
            # * Delete selected item from the function definition data
            # If selected item is a function library, delete entire function library and set all its children user role data to DELETED
            if selectedItem.text(0): 
                del self.functionDefinitionMap[selectedItem.text(0)]
                selectedItem.setHidden(True)

                for i in range(selectedItem.childCount()):
                    selectedItem.child(i).setHidden(True)
                    selectedItem.child(i).setData(1, qtc.Qt.UserRole, 'DELETED')

            # Else delete selected function name and set its children user role data to DELETED
            else: 
                del self.functionDefinitionMap[selectedItem.parent().text(0)][selectedItem.text(1)]

                selectedItem.setHidden(True)
                selectedItem.setData(1, qtc.Qt.UserRole, 'DELETED')
            
            # * refresh function definition data
            self.ui.functionParametersList_wigdet.clear()

            # * Refresh search bar autocompleter with updated data
            self.setSearchBarAutoCompleter()

    def handleDropDown(self, isExpand):
        functionLibraryTree = self.ui.functionLibraryTree_widget
        functionLibraryGenerator = (
            functionLibraryTree.topLevelItem(i) 
            for i in range(functionLibraryTree.topLevelItemCount())
        )

        for functionLibrary in functionLibraryGenerator:
            functionLibrary.setExpanded(isExpand)
    
    def handleSearchBar(self, text):
        functionLibraryTree = self.ui.functionLibraryTree_widget
        functionLibraryItems = [functionLibraryTree.topLevelItem(i) for i in range(functionLibraryTree.topLevelItemCount())]

        # * Iterate through every teststep under each testcase to check if its contains search text
        for functionLibrary in functionLibraryItems:

            # Initialize bool flag to check if each testcase contains any visible teststeps
            isAnyFound = False

            # Iterate through every teststep
            for i in range(functionLibrary.childCount()):
                
                functioNameItem = functionLibrary.child(i)
                # Get old description text for each teststep
                functionName = functioNameItem.text(1)

                # if the description contains search text, show the item else hide it
                if text.lower() in functionName.lower() and functioNameItem.data(1, qtc.Qt.UserRole) != 'DELETED':
                    functioNameItem.setHidden(False)

                    # Set bool flag to true if there is any visible teststep
                    isAnyFound = True
                else:
                    functioNameItem.setHidden(True)

            # Toggle visibility of testcase based on the boolflag
            functionLibrary.setHidden(False) if isAnyFound else functionLibrary.setHidden(True)

    #*************************** Utility functions ******************************* #

    def refreshFunctionDefinitionData(self):
        # * Reset all data fields
        self.ui.functionLibraryTree_widget.clear()
        self.ui.functionParametersList_wigdet.clear()
        self.ui.functionDefinition_searchBar.clear()
        
        # * Repopulate data tree with updated data
        self.handlepopulateFunctionDefinitionData()

        # * Refresh search bar autocompleter with updated data
        self.setSearchBarAutoCompleter()

    def setSearchBarAutoCompleter(self):
        autoCompleter = qtw.QCompleter([function_name for function_names in self.functionDefinitionMap.values() for function_name in function_names])
        autoCompleter.setFilterMode(qtc.Qt.MatchFlag.MatchContains)
        autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.ui.functionDefinition_searchBar.setCompleter(autoCompleter)

    #*************************** Virtual functions ******************************* #

    def accept(self):
        msgBoxButtonClicked = qtw.QMessageBox.question(
            self, 'Confirmation',
            'Once saved, changes cannot be reverted.\n\nProceed with saving?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No
        )

        if msgBoxButtonClicked == qtw.QMessageBox.No:
            return

        # * Try to update the function definition data base with the new data
        try:
            self.parent.functionDefinitionMap = self.functionDefinitionMap
            data_processor.handleFunctionDefinitionDataUpdate(self.parent.functionDefinitionMap, self.parent.functionDefintionInFile)
        except PermissionError:
            msgBoxButtonClicked = qtw.QMessageBox.critical(
                self,
                'Error',
                f'{self.parent.functionDefintionInFile}\nfailed to update, ensure that file is closed before trying to update.',
                qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel
            )

            # * if Ok is clicked, automatically switch to opened function definiiton database for user to close
            if msgBoxButtonClicked == qtw.QMessageBox.Ok:
                # macOS
                if sys.platform == 'darwin':
                    subprocess.call(('open', self.parent.functionDefintionInFile))
                # Windows
                elif sys.platform == 'win32':
                    os.startfile(self.parent.functionDefintionInFile)
        else:
            super().accept()

    def reject(self):
        if not DeepDiff( self.functionDefinitionMap, self.parent.functionDefinitionMap):
            return super().reject()

        msgBoxButtonClicked = qtw.QMessageBox.question(
            self, 
            'Close Function definition window', 
            'Are you sure you want to close without saving your changes? All changes will be lost.',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Save
        )
    
        if msgBoxButtonClicked == qtw.QMessageBox.Yes:
            super().reject()
        elif msgBoxButtonClicked == qtw.QMessageBox.Save:
            self.accept()
 
