from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)
from .UiWarningDialog import Ui_WarningDialog
from .UiWarningTab import Ui_WarningTab
import sys
import os

class WarningTab(qtw.QWidget):

    def __init__(self, parent=None, data=None, *args, **kwargs) -> None:
        super(WarningTab, self).__init__(parent, *args, **kwargs)

        self.ui = Ui_WarningTab()
        self.ui.setupUi(self)
        self.data = data

        # * Set tree widget header to resize to contents
        header = self.ui.dataTree_Widget.header()
        header.setSectionsMovable(True)
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)

        # * Populate warning tab with warning information
        self.ui.warningDescription_label.setText(self.data['warning'])
        if data['title'] == 'Empty fields':
            self.handlePopulateEmptyFieldsWarning()
        else:
            self.handlePopulateOtherWarning()
    
    def handlePopulateEmptyFieldsWarning(self):
        
        # * Iterate through data
        for row, mapping in self.data['data'].items():
            warningItem = qtw.QTreeWidgetItem()

            font = qtg.QFont('Arial', pointSize=10)
            font.setBold(True)

            warningItem.setFont(0, font)
            warningItem.setText(0, self.data['worksheet'])

            warningItem.setFont(1, font)
            warningItem.setText(1, f"row - {row}")

            for i in range(3):
                warningItem.setForeground(i, qtg.QColor('white'))
                warningItem.setBackground(i, qtg.QColor('darkGrey'))
            
            self.ui.dataTree_Widget.addTopLevelItem(warningItem)
            warningItem.setExpanded(True)

            for index, (field, location) in enumerate(mapping.items()):
                emptyFieldItem = qtw.QTreeWidgetItem()
                emptyFieldItem.setText(0, str(index+1))
                emptyFieldItem.setText(1, location)
                emptyFieldItem.setText(2, field)
                warningItem.addChild(emptyFieldItem)

    def handlePopulateOtherWarning(self):

        # * Iterate through data
        for field, source in self.data['data'].items():
            warningItem = qtw.QTreeWidgetItem()

            font = qtg.QFont('Arial', pointSize=10)
            font.setBold(True)

            warningItem.setFont(0, font)
            warningItem.setText(0, self.data['worksheet'])

            warningItem.setFont(1, font)
            warningItem.setText(1, source)

            warningItem.setFont(2, font)
            warningItem.setText(2, field)

            for i in range(3):
                warningItem.setForeground(i, qtg.QColor('white'))
                warningItem.setBackground(i, qtg.QColor('darkGrey'))
            
            self.ui.dataTree_Widget.addTopLevelItem(warningItem)


class WarningDialog(qtw.QDialog):

    def __init__(self, parent=None, xlsxInFile='', warning_data=None, *args, **kwargs) -> None:
        super(WarningDialog, self).__init__(parent, *args, **kwargs)

        self.ui = Ui_WarningDialog()
        self.ui.setupUi(self)
        self.xlsxInFile = xlsxInFile
        self.warning_data = warning_data

        self.handlePopulateWarningData()

        # * Additional UI setup
        self.setWindowModality(qtc.Qt.WindowModal)
        self.ui.warningSourceFile_edit.setText(self.xlsxInFile)

        # * Signal connectors
        self.ui.closeWarning_btn.clicked.connect(lambda: self.close())
        self.ui.editConfig_btn.clicked.connect(self.handleOpenConfigFile)

    #*********************************** Signal handler Methods ********************************#

    def handlePopulateWarningData(self):
        # * Iterate through warning data
        # * If data item of warning_data is present, create a warning tab for the data and add it to the tab widget
        for warning_data in self.warning_data:
            if warning_data['data']:
                warningTab = WarningTab(data=warning_data)
                icon = qtg.QIcon(':/icons/bootstrap-icons-1.8.3/bell-fill.svg')
                self.ui.warningsTab_widget.addTab(warningTab, icon, warning_data['title'])

    def handleOpenConfigFile(self):
        # * If user clicks edit config button, open config file in default program
        # macOS
        if sys.platform == 'darwin':
            subprocess.call(('open', self.xlsxInFile))
        # Windows
        elif sys.platform == 'win32':
            os.startfile(self.xlsxInFile)
