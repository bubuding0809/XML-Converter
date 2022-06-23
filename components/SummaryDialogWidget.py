from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
from .UiSummaryDialog import Ui_SummaryDialog
from .CustomLineEdit import CustomLineEdit


class SummaryDialog(qtw.QDialog):
    def __init__(self, parent=None, data=None, filteredIds=None, *args, **kwargs) -> None:
        super(SummaryDialog, self).__init__(parent, *args, **kwargs)
        
        self.ui = Ui_SummaryDialog()
        self.ui.setupUi(self)
        self.testcaseData = data
        self.filteredTeststepIds = filteredIds
        self.populateSummaryData()
        

        #* Additional UI setup
        self.setWindowModality(qtc.Qt.WindowModal)

        # Create Custom line edit search bar 
        self.ui.summaryData_searchBar = CustomLineEdit(':/icons/bootstrap-icons-1.8.3/search.svg', 'Search')
        self.ui.summaryData_searchBar.setMinimumWidth(200)
        self.ui.summaryData_searchBar.setMaximumWidth(400)
        self.ui.dataTreeSearchBox_widget.layout().insertWidget(0, self.ui.summaryData_searchBar)
        

        #* Set tree widget header to resize to contents
        header = self.ui.dataTree_Widget.header()
        header.setSectionsMovable(True)
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, qtw.QHeaderView.Interactive)


        #* Signal connectors
        self.ui.closeSummary_btn.clicked.connect(self.handleCloseButton)
        self.ui.summaryData_searchBar.textChanged.connect(self.handleSearchBar)
        self.ui.showAll_btn.clicked.connect(self.handleShowAll)
        self.ui.hideAll_btn.clicked.connect(self.handleHideAll)
    
    
        #* Create new autocomplete list for search bar based on filtered data
        teststepDescriptionSet = set()
        #Append title of visible teststeps to autocomplete list
        for teststepBoxList in self.testcaseData.values():
            for teststep in teststepBoxList:
                if teststep.isVisible(): 
                    teststepDescriptionSet.add(teststep.searchKey)

        autoCompleter = qtw.QCompleter(teststepDescriptionSet)
        autoCompleter.setFilterMode(qtc.Qt.MatchFlag.MatchContains)
        autoCompleter.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.ui.summaryData_searchBar.setCompleter(autoCompleter)
        


    #*********************************** Signal handler Methods ********************************#
    
    def populateSummaryData(self):
        for testcase, teststeps in self.testcaseData.items():
            
            #* Create testcase parent item for each testcase
            testcaseItem = qtw.QTreeWidgetItem()
            testcaseItem.setFont(0, qtg.QFont('Arial', pointSize=10))
            testcaseItem.setText(0, testcase.id)
            testcaseItem.setText(1, testcase.type)
            
            #* Add parent item to tree view and set it to expanded
            self.ui.dataTree_Widget.addTopLevelItem(testcaseItem)
            testcaseItem.setExpanded(True)
            
            #* Iterate through each teststep in the teststep list
            for teststep in teststeps:
                
                # If teststep is in the filteredTeststepIds list, add it to the tree view
                if teststep.id in self.filteredTeststepIds:
                    teststepItem = qtw.QTreeWidgetItem(testcaseItem)
                    teststepItem.setText(1, testcase.type)
                    teststepItem.setText(2, str(teststep.id))
                    teststepItem.setText(3, teststep.data['old']['description'])
                    teststepItem.setText(4, teststep.newDataTableWidget.item(0, 0).text())
                    testcaseItem.addChild(teststepItem)

            #* Create counter for number of teststeps selected per testcase
            font = qtg.QFont('Arial', pointSize=10)
            font.setUnderline(True)
            testcaseItem.setFont(5, font)
            testcaseItem.setText(5, f"{testcaseItem.childCount()} / {testcase.teststepsCount}")

            #* If there are no teststeps in the testcase, hide the parent item
            if not testcaseItem.childCount():
                testcaseItem.setHidden(True)
        
        self.ui.totalSelectedCounter_lcd.display(len(self.filteredTeststepIds))



    def handleSearchBar(self, text):
        summaryTree = self.ui.dataTree_Widget
        testcaseList = [summaryTree.topLevelItem(i) for i in range(summaryTree.topLevelItemCount())]


        #* Iterate through every teststep under each testcase to check if its contains search text
        for testcase in testcaseList:

            # Initialize bool flag to check if each testcase contains any visible teststeps 
            isAnyFound = False

            # Iterate through every teststep
            for i in range(testcase.childCount()):
                
                # Get old description text for each teststep
                oldDescription = testcase.child(i).text(2)

                # if the description contains search text, show the item else hide it
                if text.lower() in oldDescription.lower():
                    testcase.child(i).setHidden(False)

                    # Set bool flag to true if there is any visible teststep
                    isAnyFound = True
                else:
                    testcase.child(i).setHidden(True)
            
            #Toggle visibility of testcase based on the boolflag
            testcase.setHidden(False) if isAnyFound else testcase.setHidden(True)

    

    def handleShowAll(self):
        summaryTree = self.ui.dataTree_Widget
        testcaseList = [summaryTree.topLevelItem(i) for i in range(summaryTree.topLevelItemCount())]

        for testcase in testcaseList:
            testcase.setExpanded(True)
    

    
    def handleHideAll(self):
        summaryTree = self.ui.dataTree_Widget
        testcaseList = [summaryTree.topLevelItem(i) for i in range(summaryTree.topLevelItemCount())]
        
        for testcase in testcaseList:
            testcase.setExpanded(False)
    

    def handleCloseButton(self):
        self.close()