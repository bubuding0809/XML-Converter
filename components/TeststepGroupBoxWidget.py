from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)


class ListWidget(qtw.QListWidget):

    def __init__(self, atpType, targetListWidget=None, parent=None):
        super(ListWidget,self).__init__(parent)
        self.TYPE = atpType
        self.targetListWidget = targetListWidget
        self.installEventFilter(self)
        


    def keyPressEvent(self, event):
        if event == qtg.QKeySequence.Copy:

            # Get the selected values as a list
            copiedValues = [index.data() for index in self.selectedIndexes()]

            # Join the values and set it to the global clipboard
            clipboard = qtw.QApplication.clipboard()
            clipboard.setText('\n'.join(copiedValues), mode=clipboard.Clipboard)
            

    
    def eventFilter(self, source, event) -> bool:
        #* If the source is not from a ListWidget Object, return
        if source is not self:
            return False
        
        #* Handle event for new parameter list widget
        if source.TYPE == 'DD2.0': 

            # Handle right click context menu
            if event.type() == qtc.QEvent.ContextMenu:
                # Create a context menu and add the actions
                menu = qtw.QMenu()
                
                addParamAction = menu.addAction('Insert below')
                deleteSelectedParamAction = menu.addAction('Delete selected')
                
                action = menu.exec_(event.globalPos())

                # Call the respective functions based on the action
                if action == addParamAction:
                    self.handleDD2ParamActions('ADD')
                elif action == deleteSelectedParamAction:
                    self.handleDD2ParamActions('DELETE')

                return True


            if event == qtg.QKeySequence.Delete:
                #* Get the selected item modelIndexes and use it to delete the selected items
                self.handleDD2ParamActions('DELETE')

                return True

        #* Handle event for old parameter list widget
        elif source.TYPE == 'CLASSIC':

            # Handle right click context menu
            if event.type() == qtc.QEvent.ContextMenu:
                # Create a context menu and add the actions
                menu = qtw.QMenu()
                
                appendSelectedParamAction = menu.addAction('Appended Selected')
                mirrorSelectedParamAction = menu.addAction('Mirror Selected')
                
                action = menu.exec_(event.globalPos())

                if action == appendSelectedParamAction:
                    self.handleClassicParamActions('APPEND')
                elif action == mirrorSelectedParamAction:
                    self.handleClassicParamActions('MIRROR')

                return True

        
        return super(ListWidget, self).eventFilter(source, event)
            
    

    def handleClassicParamActions(self, action):
        #* Clear new list widget if action is mirror
        if action == 'MIRROR':
            for i in range(self.targetListWidget.count()):
                item = self.targetListWidget.takeItem(0)
                
                del item
                
        #* Else append selected items to new param list widget
        for modelIndex in self.selectedIndexes():

            # Get Selected item
            selectedItem = self.item(modelIndex.row())

            # Create new list widget item
            newItem = qtw.QListWidgetItem()
            newItem.setText(selectedItem.text())
            newItem.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable| qtc.Qt.ItemIsDragEnabled | qtc.Qt.ItemIsEnabled)
            self.targetListWidget.addItem(newItem)



    def handleDD2ParamActions(self, action):
            if action == 'DELETE':
                #* Get the selected item modelIndexes and use it to delete the selected items
                for index, modelIndex in enumerate(self.selectedIndexes()):
                    item = self.takeItem(modelIndex.row() - index)  

                    del item
                
            else:
                #* Insert new item below the selected item and set it to be selected and in edit mode
                item = qtw.QListWidgetItem()
                item.setText('name=text')
                item.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable| qtc.Qt.ItemIsDragEnabled | qtc.Qt.ItemIsEnabled)
                self.insertItem(self.currentRow() + 1, item)
                self.setCurrentItem(item)
                self.editItem(item)
    


class TableWidget(qtw.QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget,self).__init__(parent)



    def keyPressEvent(self, event):
        if event == qtg.QKeySequence.Copy:

            # Get the selected values as a list
            copiedValues = [index.data() for index in self.selectedIndexes()]

            # Join the values and set it to the global clipboard
            clipboard = qtw.QApplication.clipboard()
            clipboard.setText(', '.join(copiedValues), mode=clipboard.Clipboard)



class TeststepGroupBoxWidget(qtw.QGroupBox):
    def __init__(self, title="", parent=None, data=None):
        super(TeststepGroupBoxWidget, self).__init__(parent)
        self.setObjectName('TeststepGroupBox')
        self.setAccessibleName('TeststepGroupBox')
        
        # Global attributes
        self.data = data
        self.id = data['id']
        self.searchKey = data['old']['description']
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
        self.hLayout_teststepBox.setContentsMargins(0, 0, 5, 0)
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
        oldDataTableWidget_1.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
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
        
        
        ############################################## oldDataListWidget ########################################
        newDataBox = qtw.QGroupBox(self)
        self.newDataListWidget = ListWidget('DD2.0', newDataBox)
        self.oldDataListWidget = ListWidget('CLASSIC', self.newDataListWidget, oldDataBox)
        self.oldDataListWidget.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
        self.oldDataListWidget.setMinimumSize(qtc.QSize(0, 0))
        self.oldDataListWidget.setMaximumSize(qtc.QSize(300,10000))
        font = qtg.QFont()
        font.setPointSize(10)
        self.oldDataListWidget.setFont(font)
        self.oldDataListWidget.setObjectName("oldDataListWidget")
        
        for name, text in data['old']['function_parameters'].items():
            item = qtw.QListWidgetItem()
            item.setText(f"{name}={text}")
            self.oldDataListWidget.addItem(item)
        
        # Add Function parameter list to old data box
        hLayout_oldDataBox.addWidget(self.oldDataListWidget)
        
        # Add completed oldDataBox to teststep horizontal layout
        self.hLayout_teststepBox.addWidget(oldDataBox)
        

        ###################################################### Line divider ##############################################
        line = qtw.QFrame(self)
        line.setFrameShape(qtw.QFrame.VLine)
        line.setFrameShadow(qtw.QFrame.Sunken)
        line.setObjectName("line")
        self.hLayout_teststepBox.addWidget(line)
        

        ###################################################### New data box ###############################################
        newDataBox.setMinimumSize(qtc.QSize(0, 0))
        newDataBox.setTitle("")
        newDataBox.setObjectName("newDataBox")
        hLayout_newDataBox = qtw.QHBoxLayout(newDataBox)
        hLayout_newDataBox.setContentsMargins(0, 0, 0, 0)
        hLayout_newDataBox.setObjectName("hLayout_newDataBox")
        

        ############################################## newDataTableWidget #####################################
        self.newDataTableWidget = TableWidget(newDataBox)
        self.newDataTableWidget.setMinimumSize(qtc.QSize(0, 0))
        font = qtg.QFont()
        font.setPointSize(10)
        self.newDataTableWidget.setFont(font)
        self.newDataTableWidget.setGridStyle(qtc.Qt.SolidLine)
        self.newDataTableWidget.setWordWrap(True)
        self.newDataTableWidget.setCornerButtonEnabled(True)
        self.newDataTableWidget.setObjectName("newDataTableWidget")
        self.newDataTableWidget.setColumnCount(3)
        self.newDataTableWidget.setRowCount(1)
        
        
        item = qtw.QTableWidgetItem()
        self.newDataTableWidget.setVerticalHeaderItem(0, item)
        
        # Set table header 1
        item = qtw.QTableWidgetItem()
        item.setText("Description")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.newDataTableWidget.setHorizontalHeaderItem(0, item)
        
        # Set table header 2
        item = qtw.QTableWidgetItem()
        item.setText("Function library")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.newDataTableWidget.setHorizontalHeaderItem(1, item)
        
        # Set table header 3
        item = qtw.QTableWidgetItem()
        item.setText("Function name")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.newDataTableWidget.setHorizontalHeaderItem(2, item)
        
        # Set Table data
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['description'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        self.newDataTableWidget.setItem(0, 0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['function_library'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        self.newDataTableWidget.setItem(0, 1, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['function_name'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        self.newDataTableWidget.setItem(0, 2, item)
        
        self.newDataTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.newDataTableWidget.horizontalHeader().setStretchLastSection(True)
        self.newDataTableWidget.verticalHeader().setVisible(False)
        self.newDataTableWidget.verticalHeader().setStretchLastSection(True)
        hLayout_newDataBox.addWidget(self.newDataTableWidget)
        
        ############################################## newDataListWidget #####################################
        self.newDataListWidget.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
        self.newDataListWidget.setEditTriggers(qtw.QAbstractItemView.DoubleClicked)
        self.newDataListWidget.setMinimumSize(qtc.QSize(0, 0))
        self.newDataListWidget.setMaximumSize(qtc.QSize(300, 10000))
        font = qtg.QFont()
        font.setPointSize(10)
        self.newDataListWidget.setFont(font)
        self.newDataListWidget.setObjectName("newDataListWidget")
        
        for name, text in data['new']['function_parameters'].items():
            item = qtw.QListWidgetItem()
            item.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEditable| qtc.Qt.ItemIsDragEnabled | qtc.Qt.ItemIsEnabled)
            item.setText(f"{name}={text}")
            self.newDataListWidget.addItem(item)
        
        # Add Function parameter list to new data box
        hLayout_newDataBox.addWidget(self.newDataListWidget)
        
        # Add new data box to test_step box
        self.hLayout_teststepBox.addWidget(newDataBox)
        
        #Create radio button for testcase selection
        radioButton = qtw.QRadioButton(self)
        radioButton.setText("")
        radioButton.setObjectName("radioButton")
        radioButton.setChecked(True)
        self.hLayout_teststepBox.addWidget(radioButton)
        
    

    def getNewTeststepMap(self):
        #* Get list of function parameters from teststep data box
        paramStringList = []
        for i in range(self.newDataListWidget.count()):
            paramStringList.append(self.newDataListWidget.item(i).text())
        
        #* Parse the parameter strings into a obj readable by xmlParser
        function_parameters = {}
        
        # Loop through the parameter strings and if the string contains a = then split it into a key and value
        for param in paramStringList:
            param_data = param.split('=')
            if len(param_data) == 2 and param_data[0]:
                function_parameters[param_data[0]] = param_data[1]

        #* Create updated teststep conversion mapping
        newTeststepMap = {
            #Get new teststep description
            'description': self.newDataTableWidget.item(0, 0).text(),
            
            #Get new teststep function library
            'function_library': self.newDataTableWidget.item(0, 1).text(),
            
            #Get new teststep function name
            'function_name': self.newDataTableWidget.item(0, 2).text(),
            
            #Get new teststep function parameters
            'function_parameters': function_parameters
        }

        return newTeststepMap
    


    def __str__(self):
        return f"TestStepGroupBox object <{self.title}>"