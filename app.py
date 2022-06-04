from UiMainWindow import Ui_MainWindow
from test_ui.test_ui_collapseableWidget import CollapsibleBox

from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)

import sys
import XML_parser
import subprocess
import random


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
        
        #Global variables
        self.xlsxInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/config.xlsx'
        self.xmlInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/input.xml'
        self.xmlOutFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/output.xml'

        
        self.ui.xlsxConfig_input_label.setText(self.xmlInFile)
        self.ui.xml_input_label.setText(self.xmlInFile)
        self.ui.fileLocation_input_label.setText(self.xmlOutFile)
        
    #************************* Event Handler methods ****************************#
    def handleXLSXInput(self):
        file = qtw.QFileDialog.getOpenFileName(self, 'Input config XLSX file', directory='', filter='Xlsx files (*.xlsx)')
        if file:
            self.xlsxInFile = file[0]
            
            self.ui.xlsxConfig_input_label.setText(file[0])
            
        

    def handleXMLInput(self):
        file = qtw.QFileDialog.getOpenFileName(self, 'Input ATP XML file', directory='', filter='XML files (*.xml)' )
        
        if file:
            self.xmlInFile = file[0]
            
            self.ui.xml_input_label.setText(file[0])

            
  
    def handleXMLOutput(self):
        file = qtw.QFileDialog.getSaveFileName(self, 'Save converted ATP XML file', directory='')
        filePath = file[0]
        
        if len(filePath):
            self.xmlOutFile = filePath + '.xml'
            
            self.ui.fileLocation_input_label.setText(filePath + '.xml')
            
            
    def handleXMLConvert(self):
        if not self.xlsxInFile or not self.xmlInFile or not self.xmlOutFile:
            
            #Create error message box
            qtw.QMessageBox.critical(self, 'Error', 'Ensure all required fields are filled')
            return print('Ensure all required fields are filled')

        #Execute XML conversion
        atpMap = XML_parser.handleXlsx(self.xlsxInFile)
        XML_parser.convertXML(self.xmlInFile, self.xmlOutFile, atpMap)
        
        #Create success message box
        msgBox = qtw.QMessageBox()
        msgBox.setWindowTitle("Success")
        msgBox.setText("Successfully converted ATP XML file")
        msgBox.setIcon(qtw.QMessageBox.Information)
        checkbox = qtw.QCheckBox('Show file in explorer', msgBox)
        checkbox.setChecked(True)
        msgBox.setCheckBox(checkbox)
        
        ret = msgBox.exec_()
        
        if checkbox.isChecked():
            subprocess.call(["open", "-R", self.xmlOutFile])
        
    def handleXMLLoad(self):
        # atpMap = XML_parser.handleXlsx(self.xlsxInFile)
        # xmlOldData = XML_parser.getTestStepData(self.xmlInFile, atpMap)
        
        # for i, data in enumerate(xmlOldData):
        #     self.createTeststepBox(data, i)
        for i in range(10):
            self.createCollapseableBox()
    
    def createTeststepBox(self, parent):
        
        # Create teststep_box widget
        teststep_box = qtw.QGroupBox(parent)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(teststep_box.sizePolicy().hasHeightForWidth())
        teststep_box.setSizePolicy(sizePolicy)
        teststep_box.setMinimumSize(qtc.QSize(0, 150))
        teststep_box.setMaximumSize(qtc.QSize(16777215, 16777215))
        #teststep_box.setTitle(str(data['id']))
        teststep_box.setAlignment(qtc.Qt.AlignLeading|qtc.Qt.AlignLeft|qtc.Qt.AlignVCenter)
        teststep_box.setFlat(False)
        teststep_box.setCheckable(False)
        teststep_box.setChecked(False)
        teststep_box.setObjectName("teststep_box")
        
        # Create horizontal layout to contain data tables inside teststep_box
        horizontalLayout_9 = qtw.QHBoxLayout(teststep_box)
        horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_9.setObjectName("horizontalLayout_9")
        
        ############################################################################################# Old data box ##############################################
        old_1_box = qtw.QGroupBox(teststep_box)
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
        #item.setText(data['description'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget.setItem(0, 0, item)
        
        item = qtw.QTableWidgetItem()
        #item.setText(data['function_library'])
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget.setItem(0, 1, item)
        
        item = qtw.QTableWidgetItem()
        #item.setText(data['function_name'])
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
        tableWidget_3.setRowCount(4)
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
        # for i, param in enumerate(data['function_parameters']):
        #     item = qtw.QTableWidgetItem()
        #     item.setText(f"{param['name']}={param['text']}")
        #     item.setTextAlignment(qtc.Qt.AlignCenter)
        #     tableWidget_3.setItem(0, i, item)
        
        tableWidget_3.horizontalHeader().setVisible(True)
        tableWidget_3.horizontalHeader().setCascadingSectionResizes(False)
        tableWidget_3.horizontalHeader().setStretchLastSection(True)
        tableWidget_3.verticalHeader().setVisible(False)
        horizontalLayout_2.addWidget(tableWidget_3)
        horizontalLayout_9.addWidget(old_1_box)
        
        # Line divider
        line = qtw.QFrame(teststep_box)
        line.setFrameShape(qtw.QFrame.VLine)
        line.setFrameShadow(qtw.QFrame.Sunken)
        line.setObjectName("line")
        horizontalLayout_9.addWidget(line)
        
        ###################################################### New data box ###############################################
        new_1_box = qtw.QGroupBox(teststep_box)
        new_1_box.setMinimumSize(qtc.QSize(600, 0))
        new_1_box.setTitle("")
        new_1_box.setObjectName("new_1_box")
        horizontalLayout_4 = qtw.QHBoxLayout(new_1_box)
        horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_4.setObjectName("horizontalLayout_4")
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
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget_2.setHorizontalHeaderItem(0, item)
        item = qtw.QTableWidgetItem()
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget_2.setHorizontalHeaderItem(1, item)
        item = qtw.QTableWidgetItem()
        font = qtg.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        tableWidget_2.setHorizontalHeaderItem(2, item)
        item = qtw.QTableWidgetItem()
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget_2.setItem(0, 0, item)
        item = qtw.QTableWidgetItem()
        item.setTextAlignment(qtc.Qt.AlignCenter)
        tableWidget_2.setItem(0, 1, item)
        item = qtw.QTableWidgetItem()
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
        item = qtw.QListWidgetItem()
        listWidget_2.addItem(item)
        item = qtw.QListWidgetItem()
        listWidget_2.addItem(item)
        item = qtw.QListWidgetItem()
        listWidget_2.addItem(item)
        item = qtw.QListWidgetItem()
        listWidget_2.addItem(item)
        horizontalLayout_4.addWidget(listWidget_2)
        
        # Add new data box to test_step box
        horizontalLayout_9.addWidget(new_1_box)
        
        #Create radio button for testcase selection
        radioButton = qtw.QRadioButton(teststep_box)
        radioButton.setText("")
        radioButton.setObjectName("radioButton")
        horizontalLayout_9.addWidget(radioButton)
        
        return teststep_box
        #self.ui.verticalLayout_3.insertWidget(index, teststep_box)
            
    def createCollapseableBox(self):
        box = CollapsibleBox(title='testcase')
        self.ui.verticalLayout_3.insertWidget(0, box)
        
        vlayout = qtw.QVBoxLayout()
        for i in range(10):
            label = qtw.QLabel("{}".format(i))
            color = qtg.QColor(*[random.randint(0, 255) for _ in range(3)])
            label.setStyleSheet("background-color: {}; color : white;".format(color.name()))
            label.setAlignment(qtc.Qt.AlignCenter)
            
            vlayout.addWidget(label)
            # teststep_box = self.createTeststepBox(box)
            # vlayout.addWidget(teststep_box)
        
        box.setLayout(vlayout)
        
        #Insert collapseable testcase box into scroll area vlayout
        self.ui.verticalLayout_3.insertWidget(0,box)
        
            
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())
