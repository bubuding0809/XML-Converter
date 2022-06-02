from tabnanny import check
from Ui_MainWindow import Ui_MainWindow

from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
)

import sys
import XML_parser
import subprocess


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        #Initialize UI to main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Event connectors
        self.ui.xlsx_infiledialogue_button.clicked.connect(self.handleXLSXInput)
        self.ui.xml_infiledialogue_button.clicked.connect(self.handleXMLInput)
        self.ui.xml_outfiledialogue_button.clicked.connect(self.handleXMLOutput)
        self.ui.xml_convert_button.clicked.connect(self.HandleXMLConvert)
        
        #Global variables
        self.xlsxInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/config.xlsx'
        self.xmlInFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/input.xml'
        self.xmlOutFile = '/Users/dingruoqian/Desktop/code/XML-Converter/testdata/output.xml'

        
        self.ui.xlsx_input_label.setText(self.xmlInFile)
        self.ui.xml_input_label.setText(self.xmlInFile)
        self.ui.xml_output_label.setText(self.xmlOutFile)
        
    #************************* Event Handler methods ****************************#
    def handleXLSXInput(self):
        file = qtw.QFileDialog.getOpenFileName(self, 'Input config XLSX file', directory='', filter='Xlsx files (*.xlsx)')
        if file:
            self.xlsxInFile = file[0]
            
            self.ui.xlsx_input_label.setText(file[0])
            
        

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
            
            self.ui.xml_output_label.setText(filePath + '.xml')
            
            
            
    def HandleXMLConvert(self):
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
        

            
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())
