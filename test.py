import pytest
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
    window.show()

    # * Set test file paths and handle closing of message boxes
    def handle_message_box():
        message_box = qtw.QApplication.activeWindow()
        if message_box != window:
            qtbot.keyPress(message_box, qtc.Qt.Key_Return)

    qtc.QTimer.singleShot(200, handle_message_box)
            
    # * Try to process xlsx file and generate conversion map
    window.handleConversionMapGenerate()
    
    qtc.QTimer.singleShot(200, handle_message_box)

    # * If conversionMap has been generated, conduct checks on config file
    window.handleXLSXProcess()
    
    qtc.QTimer.singleShot(200, handle_message_box)
    
    # * Parse xml data with config mapping, raise messagebox if there are unmatched teststeps
    window.handleDataLoad()

    return window
    
def test_data_load(window, qtbot):
    datagrid_layout = window.ui.verticalLayout_3
    test_case_boxes = [datagrid_layout.itemAt(i).widget() for i in range(datagrid_layout.count()) if datagrid_layout.itemAt(i).widget()]

    # * Check if visible testcase count is correct for both filter
    visible_teststep_count = 0
    for test_case in test_case_boxes:
        
        content_area_layout = test_case.content_area.layout()
        
        for i in range(content_area_layout.count()):
            
            widget = content_area_layout.itemAt(i).widget()
            if not widget: continue
            if widget: visible_teststep_count += 1
    
    assert visible_teststep_count == 9
    
    # * Check if visible testcase count is correct for both filter
    visible_testcase_count = 0
    for i in range(datagrid_layout.count()):
        widget = datagrid_layout.itemAt(i).widget()
        
        if not widget:
            continue
        
        if not widget.isHidden(): visible_testcase_count += 1
        
    assert visible_testcase_count == 3
    
def test_filter_function_only(window, qtbot):
    # * Get scroll area layout widgets
    datagrid_layout = window.ui.verticalLayout_3
    test_case_boxes = [datagrid_layout.itemAt(i).widget() for i in range(datagrid_layout.count()) if datagrid_layout.itemAt(i).widget()]

    # * Apply function only filter
    qtbot.mouseClick(window.ui.filterFunctionOnly_btn, qtc.Qt.LeftButton)

    # * Check if visible teststep count is correct for function only filter
    visible_teststep_count = 0
    for test_case in test_case_boxes:
        
        content_area_layout = test_case.content_area.layout()
        
        for i in range(content_area_layout.count()):
            
            widget = content_area_layout.itemAt(i).widget()
            if not widget: continue
            if widget.isVisible(): visible_teststep_count += 1
    
    assert visible_teststep_count == 2

    # * Check if visible teststep count is correct for function only filter
    visible_testcase_count = 0
    for i in range(datagrid_layout.count()):
        widget = datagrid_layout.itemAt(i).widget()
        
        if not widget:
            continue
        
        if not widget.isHidden(): visible_testcase_count += 1
        
    assert visible_testcase_count == 1

def test_filter_testcase_only(window, qtbot):
    # * Get scroll area layout widgets
    datagrid_layout = window.ui.verticalLayout_3
    test_case_boxes = [datagrid_layout.itemAt(i).widget() for i in range(datagrid_layout.count()) if datagrid_layout.itemAt(i).widget()]

    # * Apply function only filter
    qtbot.mouseClick(window.ui.filterTestcaseOnly_btn, qtc.Qt.LeftButton)

    # * Check if visible teststep count is correct for testcase only filter
    visible_teststep_count = 0
    for test_case in test_case_boxes:
        
        content_area_layout = test_case.content_area.layout()
        
        for i in range(content_area_layout.count()):
            
            widget = content_area_layout.itemAt(i).widget()
            if not widget: continue
            if widget.isVisible(): visible_teststep_count += 1
    
    assert visible_teststep_count == 7
    
    # * Check if visible testcase count is correct for testcase only filter
    visible_testcase_count = 0
    for i in range(datagrid_layout.count()):
        widget = datagrid_layout.itemAt(i).widget()

        if not widget:
            continue
        
        if not widget.isHidden(): visible_testcase_count += 1
        
    assert visible_testcase_count == 2