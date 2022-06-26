import pytest
import time
from app import MainWindow
from PyQt5 import (
    QtCore as qtc,
    QtWidgets as qtw
)
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
    
    def handle_message_box():
        message_box = qtw.QApplication.activeWindow()
        if message_box != window:
            qtbot.keyPress(message_box, qtc.Qt.Key_Return)
            
    # * Try to process xlsx file and generate conversion map
    window.handleConversionMapGenerate()
    
    qtc.QTimer.singleShot(0, handle_message_box)

    # * If conversionMap has been generated, conduct checks on config file
    window.handleXLSXProcess()
    
    qtc.QTimer.singleShot(0, handle_message_box)
    
    # * Parse xml data with config mapping, raise messagebox if there are unmatched teststeps
    window.handleDataLoad()
    
    datagrid_layout = window.ui.verticalLayout_3
    test_case_boxes = [datagrid_layout.itemAt(i).widget() for i in range(datagrid_layout.count()) if datagrid_layout.itemAt(i).widget()]

    teststepCount = 0
    for test_case in test_case_boxes:
        
        content_area_layout = test_case.content_area.layout()
        
        for i in range(content_area_layout.count()):
            
            widget = content_area_layout.itemAt(i).widget()
            if not widget: continue
            if widget: teststepCount += 1
    
    assert teststepCount == 9
    
    # * Apply function only filter
    qtbot.mouseClick(window.ui.filterBoth_btn, qtc.Qt.LeftButton)
    
    # * Get scroll area layout widgets
    datagrid_layout = window.ui.verticalLayout_3
    
    visible_count = 0
    for i in range(datagrid_layout.count()):
        widget = datagrid_layout.itemAt(i).widget()
        
        if not widget:
            continue
        
        if not widget.isHidden(): visible_count += 1
        
    assert visible_count == 3
    
         
def test_filter_function_only(window, qtbot):
    
    def handle_message_box():
            message_box = qtw.QApplication.activeWindow()
            if message_box != window:
                qtbot.keyPress(message_box, qtc.Qt.Key_Return)
                
    # * Try to process xlsx file and generate conversion map
    window.handleConversionMapGenerate()
    
    qtc.QTimer.singleShot(50, handle_message_box)

    # * If conversionMap has been generated, conduct checks on config file
    window.handleXLSXProcess()
    
    qtc.QTimer.singleShot(50, handle_message_box)
    
    # * Parse xml data with config mapping, raise messagebox if there are unmatched teststeps
    window.handleDataLoad()
    
    # * Apply function only filter
    qtbot.mouseClick(window.ui.filterFunctionOnly_btn, qtc.Qt.LeftButton)
    
    # * Get scroll area layout widgets
    datagrid_layout = window.ui.verticalLayout_3
    
    visible_count = 0
    for i in range(datagrid_layout.count()):
        widget = datagrid_layout.itemAt(i).widget()
        
        if not widget:
            continue
        
        print(widget)
        print(widget.isHidden())
        
        if not widget.isHidden(): visible_count += 1
        
    assert visible_count == 1

def test_filter_testcase_only(window, qtbot):
    def handle_message_box():
            message_box = qtw.QApplication.activeWindow()
            if message_box != window:
                qtbot.keyPress(message_box, qtc.Qt.Key_Return)
                
    # * Try to process xlsx file and generate conversion map
    window.handleConversionMapGenerate()
    
    qtc.QTimer.singleShot(0, handle_message_box)

    # * If conversionMap has been generated, conduct checks on config file
    window.handleXLSXProcess()
    
    qtc.QTimer.singleShot(0, handle_message_box)
    
    # * Parse xml data with config mapping, raise messagebox if there are unmatched teststeps
    window.handleDataLoad()
    
    # * Apply function only filter
    qtbot.mouseClick(window.ui.filterTestcaseOnly_btn, qtc.Qt.LeftButton)
    
    # * Get scroll area layout widgets
    datagrid_layout = window.ui.verticalLayout_3
    
    visible_count = 0
    for i in range(datagrid_layout.count()):
        widget = datagrid_layout.itemAt(i).widget()

        if not widget:
            continue
        
        if not widget.isHidden(): visible_count += 1
        
    assert visible_count == 2