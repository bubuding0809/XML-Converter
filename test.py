import pytest
from app import MainWindow
from PyQt5 import QtCore as qtc
from samples import testFilePaths as testfiles
import sys


@pytest.fixture
def window(qtbot):
    window = MainWindow()
    window.xlsxInFile = testfiles.CONFIG_PATH_WIN32 if sys.platform == 'win32' else testfiles.CONFIG_PATH_DARWIN
    window.xmlInFile = testfiles.INPUT_PATH_WIN32 if sys.platform == 'win32' else testfiles.INPUT_PATH_DARWIN
    window.ui.configFilePath_display.setText(window.xlsxInFile)
    window.ui.xmlFilePath_display.setText(window.xmlInFile)
    qtbot.addWidget(window)

    return window
    
def test_data_load(window, qtbot):
    window.show()
    # * Try to process xlsx file and generate conversion map
    if len(window.xlsxInFile):
        window.handleConversionMapGenerate()

    # * If conversionMap has been generated, conduct checks on config file
    if window.conversionMap:
        window.handleXLSXProcess()
        
    if window.conversionMap and window.xmlInFile:
        window.handleDataLoad()
        
    test_case_box = window.ui.verticalLayout_3.itemAt(0).widget()
    teststeps = test_case_box.content_area.layout()
            
    teststepCount = len(
            [teststeps.itemAt(i).widget() for i in range(teststeps.count()) if teststeps.itemAt(i).widget()]
        )
    assert teststepCount == 3
        
