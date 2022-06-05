from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)

import sys
import XML_parser
import subprocess
import random

class TestStepGroupBox(qtw.QGroupBox):
    def __init__(self, title="", parent=None, data=None):
        super(TestStepGroupBox, self).__init__(parent)
        
        # Create teststep_box widget
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(qtc.QSize(0, 100))
        self.setMaximumSize(qtc.QSize(16777215, 150))
        self.setTitle(str(data['old']['id']))
        self.setAlignment(qtc.Qt.AlignLeading|qtc.Qt.AlignLeft|qtc.Qt.AlignVCenter)
        self.setFlat(False)
        self.setCheckable(False)
        self.setChecked(False)
        self.setObjectName("self")
        
        # Create horizontal layout to contain data tables inside teststep_box
        horizontalLayout_9 = qtw.QHBoxLayout(self)
        horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_9.setObjectName("horizontalLayout_9")
        
        ############################################################################################# Old data box ##############################################
        old_1_box = qtw.QGroupBox(self)
        old_1_box.setMinimumSize(qtc.QSize(600, 0))
        old_1_box.setTitle("")
        old_1_box.setObjectName("old_1_box")
        horizontalLayout_2 = qtw.QHBoxLayout(old_1_box)
        horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        ########################################## Table 1 ########################################
        tableWidget = qtw.QTableWidget(old_1_box)
        tableWidget.setMinimumSize(qtc.QSize(377, 0))
        font = qtg.QFont()
        font.setPointSize(10)
        tableWidget.setFont(font)
        tableWidget.setGridStyle(qtc.Qt.SolidLine)
        tableWidget.setWordWrap(True)
        tableWidget.setCornerButtonEnabled(True)
        tableWidget.setObjectName("tableWidget")
        tableWidget.setColumnCount(3)
        tableWidget.setRowCount(1)
        item = qtw.QTableWidgetItem()
        tableWidget.setVerticalHeaderItem(0, item)
        
        # Set table header 0
        item = qtw.QTableWidgetItem()
        item.setText("Description")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget.setHorizontalHeaderItem(0, item)
        
        # Set table header 1
        item = qtw.QTableWidgetItem()
        item.setText('Function name')
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget.setHorizontalHeaderItem(1, item)
        
        # Set table header 2
        item = qtw.QTableWidgetItem()
        item.setText('Function library')
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget.setHorizontalHeaderItem(2, item)
        
        # Set table data
        item = qtw.QTableWidgetItem()
        item.setText(data['old']['description'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget.setItem(0, 0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['old']['function_library'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget.setItem(0, 1, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['old']['function_name'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget.setItem(0, 2, item)
        
        tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.verticalHeader().setStretchLastSection(True)
        horizontalLayout_2.addWidget(tableWidget)
        
        ############################################## Table 3 ########################################
        tableWidget_3 = qtw.QTableWidget(old_1_box)
        font = qtg.QFont()
        font.setPointSize(10)
        tableWidget_3.setFont(font)
        tableWidget_3.setFrameShadow(qtw.QFrame.Sunken)
        tableWidget_3.setDragDropMode(qtw.QAbstractItemView.DragOnly)
        tableWidget_3.setCornerButtonEnabled(True)
        tableWidget_3.setObjectName("tableWidget_3")
        tableWidget_3.setColumnCount(1)
        tableWidget_3.setRowCount(len(data['old']['function_parameters']))
        item = qtw.QTableWidgetItem()
        tableWidget_3.setVerticalHeaderItem(0, item)
        item = qtw.QTableWidgetItem()
        tableWidget_3.setVerticalHeaderItem(1, item)
        item = qtw.QTableWidgetItem()
        tableWidget_3.setVerticalHeaderItem(2, item)
        item = qtw.QTableWidgetItem()
        tableWidget_3.setVerticalHeaderItem(3, item)
        
        # Set table header 0
        item = qtw.QTableWidgetItem()
        item.setText('Function parameters')
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget_3.setHorizontalHeaderItem(0, item)
        
        # Set table data
        for i, param in enumerate(data['old']['function_parameters']):
            item = qtw.QTableWidgetItem()
            item.setText(f"{param['name']}={param['text']}")
            item.setTextAlignment(qtc.Qt.AlignCenter)
            tableWidget_3.setItem(0, i, item)
        
        tableWidget_3.horizontalHeader().setVisible(True)
        tableWidget_3.horizontalHeader().setCascadingSectionResizes(False)
        tableWidget_3.horizontalHeader().setStretchLastSection(True)
        tableWidget_3.verticalHeader().setVisible(False)
        horizontalLayout_2.addWidget(tableWidget_3)
        horizontalLayout_9.addWidget(old_1_box)
        
        # Line divider
        line = qtw.QFrame(self)
        line.setFrameShape(qtw.QFrame.VLine)
        line.setFrameShadow(qtw.QFrame.Sunken)
        line.setObjectName("line")
        horizontalLayout_9.addWidget(line)
        
        ###################################################### New data box ###############################################
        new_1_box = qtw.QGroupBox(self)
        new_1_box.setMinimumSize(qtc.QSize(600, 0))
        new_1_box.setTitle("")
        new_1_box.setObjectName("new_1_box")
        horizontalLayout_4 = qtw.QHBoxLayout(new_1_box)
        horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        ############################################## Table 2 #####################################
        tableWidget_2 = qtw.QTableWidget(new_1_box)
        tableWidget_2.setMinimumSize(qtc.QSize(377, 0))
        font = qtg.QFont()
        font.setPointSize(10)
        tableWidget_2.setFont(font)
        tableWidget_2.setGridStyle(qtc.Qt.SolidLine)
        tableWidget_2.setWordWrap(True)
        tableWidget_2.setCornerButtonEnabled(True)
        tableWidget_2.setObjectName("tableWidget_2")
        tableWidget_2.setColumnCount(3)
        tableWidget_2.setRowCount(1)
        
        item = qtw.QTableWidgetItem()
        tableWidget_2.setVerticalHeaderItem(0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText("Description")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget_2.setHorizontalHeaderItem(0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText("Function Name")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget_2.setHorizontalHeaderItem(1, item)
        
        item = qtw.QTableWidgetItem()
        item.setText("Function library")
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget_2.setHorizontalHeaderItem(2, item)
        
        # Set Table data
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['description'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget_2.setItem(0, 0, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['function_library'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget_2.setItem(0, 1, item)
        
        item = qtw.QTableWidgetItem()
        item.setText(data['new']['function_name'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget_2.setItem(0, 2, item)
        
        tableWidget_2.horizontalHeader().setCascadingSectionResizes(False)
        tableWidget_2.horizontalHeader().setStretchLastSection(True)
        tableWidget_2.verticalHeader().setVisible(False)
        tableWidget_2.verticalHeader().setStretchLastSection(True)
        horizontalLayout_4.addWidget(tableWidget_2)
        
        # Create list widget to contain new function parameter data 
        listWidget_2 = qtw.QListWidget(new_1_box)
        listWidget_2.setMinimumSize(qtc.QSize(0, 0))
        font = qtg.QFont()
        font.setPointSize(10)
        listWidget_2.setFont(font)
        listWidget_2.setObjectName("listWidget_2")
        
        for param in data['new']['function_parameters']:
            item = qtw.QListWidgetItem()
            item.setText(f"{param['name']}={param['text']}")
            listWidget_2.addItem(item)
        
        # Add Function parameter list to new data box
        horizontalLayout_4.addWidget(listWidget_2)
        
        # Add new data box to test_step box
        horizontalLayout_9.addWidget(new_1_box)
        
        #Create radio button for testcase selection
        radioButton = qtw.QRadioButton(self)
        radioButton.setText("")
        radioButton.setObjectName("radioButton")
        radioButton.setChecked(True)
        horizontalLayout_9.addWidget(radioButton)
        