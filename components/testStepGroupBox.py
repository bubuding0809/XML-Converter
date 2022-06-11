from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)



class ListWidget(qtw.QListWidget):
    def __init__(self, parent=None):
        super(ListWidget,self).__init__(parent)

    def keyPressEvent(self, event):
        if event == qtg.QKeySequence.Copy:

            # Get the selected values as a list
            copiedValues = [index.data() for index in self.selectedIndexes()]

            # Join the values and set it to the global clipboard
            clipboard = qtw.QApplication.clipboard()
            clipboard.setText('\n'.join(copiedValues), mode=clipboard.Clipboard)

            print(clipboard.text(mode=clipboard.Clipboard))



class TableWidget(qtw.QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget,self).__init__(parent)
        self.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)


    def keyPressEvent(self, event):
        if event == qtg.QKeySequence.Copy:

            # Get the selected values as a list
            copiedValues = [index.data() for index in self.selectedIndexes()]

            # Join the values and set it to the global clipboard
            clipboard = qtw.QApplication.clipboard()
            clipboard.setText(', '.join(copiedValues), mode=clipboard.Clipboard)

            print(clipboard.text(mode=clipboard.Clipboard))




class TestStepGroupBox(qtw.QGroupBox):
    def __init__(self, title="", parent=None, data=None):
        super(TestStepGroupBox, self).__init__(parent)
        
        # Global attributes
        self.id = data['id']
        self.title = title
        

        # Create teststep_box widget
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(qtc.QSize(0, 80))
        self.setMaximumSize(qtc.QSize(16777215, 100))
        self.setTitle(self.title)
        self.setAlignment(qtc.Qt.AlignLeading|qtc.Qt.AlignLeft|qtc.Qt.AlignVCenter)
        self.setFlat(False)
        self.setCheckable(False)
        self.setChecked(False)
        self.setObjectName("self")
        

        # Create horizontal layout to contain data tables inside teststep_box
        self.hLayout_teststepBox = qtw.QHBoxLayout(self)
        self.hLayout_teststepBox.setContentsMargins(0, 0, 0, 0)
        self.hLayout_teststepBox.setObjectName("hLayout_teststepBox")
        

        ############################################################################################# oldDataBox ##############################################
        oldDataBox = qtw.QGroupBox(self)
        oldDataBox.setMinimumSize(qtc.QSize(0, 0))
        oldDataBox.setTitle("")
        oldDataBox.setObjectName("oldDataBox")
        hLayout_oldDataBox = qtw.QHBoxLayout(oldDataBox)
        hLayout_oldDataBox.setContentsMargins(0, 0, 0, 0)
        hLayout_oldDataBox.setObjectName("hLayout_oldDataBox")
        

        ########################################## oldDataTableWidget_1 ########################################
        oldDataTableWidget_1 = TableWidget(oldDataBox)
        oldDataTableWidget_1.setMinimumSize(qtc.QSize(0, 0))
        font = qtg.QFont()
        font.setPointSize(10)
        oldDataTableWidget_1.setFont(font)
        oldDataTableWidget_1.setGridStyle(qtc.Qt.SolidLine)
        oldDataTableWidget_1.setWordWrap(True)
        oldDataTableWidget_1.setCornerButtonEnabled(True)
        oldDataTableWidget_1.setObjectName("oldDataTableWidget_1")
        oldDataTableWidget_1.setColumnCount(3)
        oldDataTableWidget_1.setRowCount(1)
        item = qtw.QTableWidgetItem()
        oldDataTableWidget_1.setVerticalHeaderItem(0, item)
        
        # Set table header 0
        item = qtw.QTableWidgetItem()
        item.setText("Description")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        oldDataTableWidget_1.setHorizontalHeaderItem(0, item)
        
        # Set table header 1
        item = qtw.QTableWidgetItem()
        item.setText('Function name')
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        oldDataTableWidget_1.setHorizontalHeaderItem(1, item)
        
        # Set table header 2
        item = qtw.QTableWidgetItem()
        item.setText('Function library')
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        oldDataTableWidget_1.setHorizontalHeaderItem(2, item)
        
        # Set table data
        item = qtw.QTableWidgetItem()
        item.setText(data['old']['description'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        oldDataTableWidget_1.setItem(0, 0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['old']['function_library'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        oldDataTableWidget_1.setItem(0, 1, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['old']['function_name'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        oldDataTableWidget_1.setItem(0, 2, item)
        
        oldDataTableWidget_1.horizontalHeader().setCascadingSectionResizes(False)
        oldDataTableWidget_1.horizontalHeader().setStretchLastSection(True)
        oldDataTableWidget_1.verticalHeader().setVisible(False)
        oldDataTableWidget_1.verticalHeader().setStretchLastSection(True)
        hLayout_oldDataBox.addWidget(oldDataTableWidget_1)
        
        
        ############################################## oldDataListWidget_1 ########################################
        oldDataListWidget_1 = ListWidget(oldDataBox)
        oldDataListWidget_1.setSelectionMode(2)
        oldDataListWidget_1.setMinimumSize(qtc.QSize(0, 0))
        oldDataListWidget_1.setMaximumSize(qtc.QSize(300,10000))
        font = qtg.QFont()
        font.setPointSize(10)
        oldDataListWidget_1.setFont(font)
        oldDataListWidget_1.setObjectName("oldDataListWidget_1")
        
        for param in data['old']['function_parameters']:
            item = qtw.QListWidgetItem()
            item.setText(f"{param['name']}={param['text']}")
            oldDataListWidget_1.addItem(item)
        
        # Add Function parameter list to old data box
        hLayout_oldDataBox.addWidget(oldDataListWidget_1)
        
        # Add completed oldDataBox to teststep horizontal layout
        self.hLayout_teststepBox.addWidget(oldDataBox)
        

        ###################################################### Line divider ##############################################
        line = qtw.QFrame(self)
        line.setFrameShape(qtw.QFrame.VLine)
        line.setFrameShadow(qtw.QFrame.Sunken)
        line.setObjectName("line")
        self.hLayout_teststepBox.addWidget(line)
        

        ###################################################### New data box ###############################################
        newDataBox = qtw.QGroupBox(self)
        newDataBox.setMinimumSize(qtc.QSize(0, 0))
        newDataBox.setTitle("")
        newDataBox.setObjectName("newDataBox")
        hLayout_newDataBox = qtw.QHBoxLayout(newDataBox)
        hLayout_newDataBox.setContentsMargins(0, 0, 0, 0)
        hLayout_newDataBox.setObjectName("hLayout_newDataBox")
        

        ############################################## newDataTableWidget_1 #####################################
        newDataTableWidget_1 = qtw.QTableWidget(newDataBox)
        newDataTableWidget_1.setMinimumSize(qtc.QSize(0, 0))
        font = qtg.QFont()
        font.setPointSize(10)
        newDataTableWidget_1.setFont(font)
        newDataTableWidget_1.setGridStyle(qtc.Qt.SolidLine)
        newDataTableWidget_1.setWordWrap(True)
        newDataTableWidget_1.setCornerButtonEnabled(True)
        newDataTableWidget_1.setObjectName("newDataTableWidget_1")
        newDataTableWidget_1.setColumnCount(3)
        newDataTableWidget_1.setRowCount(1)
        
        item = qtw.QTableWidgetItem()
        newDataTableWidget_1.setVerticalHeaderItem(0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText("Description")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        newDataTableWidget_1.setHorizontalHeaderItem(0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText("Function Name")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        newDataTableWidget_1.setHorizontalHeaderItem(1, item)
        
        item = qtw.QTableWidgetItem()
        item.setText("Function library")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        newDataTableWidget_1.setHorizontalHeaderItem(2, item)
        
        # Set Table data
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['description'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        newDataTableWidget_1.setItem(0, 0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['function_library'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        newDataTableWidget_1.setItem(0, 1, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['function_name'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        newDataTableWidget_1.setItem(0, 2, item)
        
        newDataTableWidget_1.horizontalHeader().setCascadingSectionResizes(False)
        newDataTableWidget_1.horizontalHeader().setStretchLastSection(True)
        newDataTableWidget_1.verticalHeader().setVisible(False)
        newDataTableWidget_1.verticalHeader().setStretchLastSection(True)
        hLayout_newDataBox.addWidget(newDataTableWidget_1)
        
        # Create list widget to contain new function parameter data 
        newDataListWidget_1 = ListWidget(newDataBox)
        newDataListWidget_1.setMinimumSize(qtc.QSize(0, 0))
        newDataListWidget_1.setMaximumSize(qtc.QSize(300, 10000))
        font = qtg.QFont()
        font.setPointSize(10)
        newDataListWidget_1.setFont(font)
        newDataListWidget_1.setObjectName("newDataListWidget_1")
        
        for param in data['new']['function_parameters']:
            item = qtw.QListWidgetItem()
            item.setText(f"{param['name']}={param['text']}")
            newDataListWidget_1.addItem(item)
        
        # Add Function parameter list to new data box
        hLayout_newDataBox.addWidget(newDataListWidget_1)
        
        # Add new data box to test_step box
        self.hLayout_teststepBox.addWidget(newDataBox)
        
        #Create radio button for testcase selection
        radioButton = qtw.QRadioButton(self)
        radioButton.setText("")
        radioButton.setObjectName("radioButton")
        radioButton.setChecked(True)
        self.hLayout_teststepBox.addWidget(radioButton)
        
    
    
    def __str__(self):
        return f"TestStepGroupBox object <{self.title}>"