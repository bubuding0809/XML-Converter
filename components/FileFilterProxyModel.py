import re
from PyQt5 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg
)


#* Custom filter implemented for QFileDialog, using regex to filter filenames to display
class FileFilterProxyModel(qtc.QSortFilterProxyModel):
    def __init__(self, regex=r'.*', parent=None):
        super(FileFilterProxyModel, self).__init__(parent)
        
        # * Regex pattern to ensure that only files matching pattern are displayed in QFileDialog
        self.xlsxFilePattern = re.compile(regex)

    
    def filterAcceptsRow(self, source_row, source_parent) -> bool:
        itemModel = qtc.QAbstractProxyModel.sourceModel(self)
        index0 = itemModel.index(source_row , 0, source_parent)

        return True if re.search(self.xlsxFilePattern, itemModel.data(index0)) else False



