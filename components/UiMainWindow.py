# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1122, 842)
        MainWindow.setStyleSheet("")
        MainWindow.setIconSize(QtCore.QSize(40, 40))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 233, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 233, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 233, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 233, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(233, 233, 233))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(141, 141, 141))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.centralwidget.setPalette(palette)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setup_widget = QtWidgets.QWidget(self.centralwidget)
        self.setup_widget.setObjectName("setup_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.setup_widget)
        self.gridLayout.setContentsMargins(5, 10, 0, 10)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.xmlGroup_box = QtWidgets.QGroupBox(self.setup_widget)
        self.xmlGroup_box.setObjectName("xmlGroup_box")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.xmlGroup_box)
        self.horizontalLayout_9.setContentsMargins(5, 0, 5, 5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.xmlFileUpload_btn = QtWidgets.QPushButton(self.xmlGroup_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xmlFileUpload_btn.sizePolicy().hasHeightForWidth())
        self.xmlFileUpload_btn.setSizePolicy(sizePolicy)
        self.xmlFileUpload_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.xmlFileUpload_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/bootstrap-icons-1.8.3/filetype-xml.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.xmlFileUpload_btn.setIcon(icon)
        self.xmlFileUpload_btn.setIconSize(QtCore.QSize(25, 25))
        self.xmlFileUpload_btn.setDefault(False)
        self.xmlFileUpload_btn.setObjectName("xmlFileUpload_btn")
        self.horizontalLayout_9.addWidget(self.xmlFileUpload_btn)
        self.xmlFilePath_display = QtWidgets.QLineEdit(self.xmlGroup_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xmlFilePath_display.sizePolicy().hasHeightForWidth())
        self.xmlFilePath_display.setSizePolicy(sizePolicy)
        self.xmlFilePath_display.setMinimumSize(QtCore.QSize(400, 0))
        self.xmlFilePath_display.setReadOnly(True)
        self.xmlFilePath_display.setObjectName("xmlFilePath_display")
        self.horizontalLayout_9.addWidget(self.xmlFilePath_display)
        self.gridLayout.addWidget(self.xmlGroup_box, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.configGroup_box = QtWidgets.QGroupBox(self.setup_widget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.configGroup_box.setFont(font)
        self.configGroup_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.configGroup_box.setFlat(False)
        self.configGroup_box.setCheckable(False)
        self.configGroup_box.setChecked(False)
        self.configGroup_box.setObjectName("configGroup_box")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.configGroup_box)
        self.horizontalLayout_7.setContentsMargins(5, 0, 5, 5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.configFileUpload_btn = QtWidgets.QPushButton(self.configGroup_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configFileUpload_btn.sizePolicy().hasHeightForWidth())
        self.configFileUpload_btn.setSizePolicy(sizePolicy)
        self.configFileUpload_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.configFileUpload_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/bootstrap-icons-1.8.3/filetype-xlsx.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.configFileUpload_btn.setIcon(icon1)
        self.configFileUpload_btn.setIconSize(QtCore.QSize(25, 25))
        self.configFileUpload_btn.setDefault(False)
        self.configFileUpload_btn.setObjectName("configFileUpload_btn")
        self.horizontalLayout_7.addWidget(self.configFileUpload_btn)
        self.configFilePath_display = QtWidgets.QLineEdit(self.configGroup_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configFilePath_display.sizePolicy().hasHeightForWidth())
        self.configFilePath_display.setSizePolicy(sizePolicy)
        self.configFilePath_display.setMinimumSize(QtCore.QSize(400, 0))
        self.configFilePath_display.setReadOnly(True)
        self.configFilePath_display.setObjectName("configFilePath_display")
        self.horizontalLayout_7.addWidget(self.configFilePath_display)
        self.configFileUpdate_btn = QtWidgets.QPushButton(self.configGroup_box)
        self.configFileUpdate_btn.setEnabled(False)
        self.configFileUpdate_btn.setObjectName("configFileUpdate_btn")
        self.horizontalLayout_7.addWidget(self.configFileUpdate_btn)
        self.gridLayout.addWidget(self.configGroup_box, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.setup_widget)
        self.data_widget = QtWidgets.QWidget(self.centralwidget)
        self.data_widget.setObjectName("data_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.data_widget)
        self.verticalLayout_2.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea_tools = QtWidgets.QWidget(self.data_widget)
        self.scrollArea_tools.setObjectName("scrollArea_tools")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollArea_tools)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollAreaSearchBox_widget = QtWidgets.QWidget(self.scrollArea_tools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(22)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaSearchBox_widget.sizePolicy().hasHeightForWidth())
        self.scrollAreaSearchBox_widget.setSizePolicy(sizePolicy)
        self.scrollAreaSearchBox_widget.setObjectName("scrollAreaSearchBox_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaSearchBox_widget)
        self.horizontalLayout_2.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollAreaFilterBox_widget = QtWidgets.QGroupBox(self.scrollAreaSearchBox_widget)
        self.scrollAreaFilterBox_widget.setEnabled(False)
        self.scrollAreaFilterBox_widget.setObjectName("scrollAreaFilterBox_widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.scrollAreaFilterBox_widget)
        self.horizontalLayout_6.setContentsMargins(5, 0, 5, 5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.filterTestcaseOnly_btn = QtWidgets.QRadioButton(self.scrollAreaFilterBox_widget)
        self.filterTestcaseOnly_btn.setObjectName("filterTestcaseOnly_btn")
        self.horizontalLayout_6.addWidget(self.filterTestcaseOnly_btn)
        self.filterFunctionOnly_btn = QtWidgets.QRadioButton(self.scrollAreaFilterBox_widget)
        self.filterFunctionOnly_btn.setObjectName("filterFunctionOnly_btn")
        self.horizontalLayout_6.addWidget(self.filterFunctionOnly_btn)
        self.filterBoth_btn = QtWidgets.QRadioButton(self.scrollAreaFilterBox_widget)
        self.filterBoth_btn.setChecked(True)
        self.filterBoth_btn.setObjectName("filterBoth_btn")
        self.horizontalLayout_6.addWidget(self.filterBoth_btn)
        self.horizontalLayout_2.addWidget(self.scrollAreaFilterBox_widget)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.scrollAreaSearchBox_widget, 0, QtCore.Qt.AlignVCenter)
        self.scrollAreaButtonBox_widget = QtWidgets.QWidget(self.scrollArea_tools)
        self.scrollAreaButtonBox_widget.setObjectName("scrollAreaButtonBox_widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaButtonBox_widget)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.xml_refreshData_btn = QtWidgets.QPushButton(self.scrollAreaButtonBox_widget)
        self.xml_refreshData_btn.setEnabled(False)
        self.xml_refreshData_btn.setObjectName("xml_refreshData_btn")
        self.horizontalLayout_3.addWidget(self.xml_refreshData_btn)
        self.xml_clearTeststeps_btn = QtWidgets.QPushButton(self.scrollAreaButtonBox_widget)
        self.xml_clearTeststeps_btn.setEnabled(False)
        self.xml_clearTeststeps_btn.setObjectName("xml_clearTeststeps_btn")
        self.horizontalLayout_3.addWidget(self.xml_clearTeststeps_btn)
        self.showAll_btn = QtWidgets.QPushButton(self.scrollAreaButtonBox_widget)
        self.showAll_btn.setEnabled(False)
        self.showAll_btn.setCheckable(False)
        self.showAll_btn.setObjectName("showAll_btn")
        self.horizontalLayout_3.addWidget(self.showAll_btn)
        self.hideAll_btn = QtWidgets.QPushButton(self.scrollAreaButtonBox_widget)
        self.hideAll_btn.setEnabled(False)
        self.hideAll_btn.setObjectName("hideAll_btn")
        self.horizontalLayout_3.addWidget(self.hideAll_btn)
        self.selectAll_checkBox = QtWidgets.QCheckBox(self.scrollAreaButtonBox_widget)
        self.selectAll_checkBox.setEnabled(False)
        self.selectAll_checkBox.setCheckable(True)
        self.selectAll_checkBox.setChecked(True)
        self.selectAll_checkBox.setObjectName("selectAll_checkBox")
        self.horizontalLayout_3.addWidget(self.selectAll_checkBox)
        self.horizontalLayout.addWidget(self.scrollAreaButtonBox_widget)
        self.verticalLayout_2.addWidget(self.scrollArea_tools)
        self.scrollArea = QtWidgets.QScrollArea(self.data_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1093, 540))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.data_widget)
        self.convert_widget = QtWidgets.QWidget(self.centralwidget)
        self.convert_widget.setObjectName("convert_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.convert_widget)
        self.gridLayout_2.setContentsMargins(5, -1, 0, 12)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 2, 1, 1)
        self.xml_convert_btn = QtWidgets.QPushButton(self.convert_widget)
        self.xml_convert_btn.setEnabled(False)
        self.xml_convert_btn.setObjectName("xml_convert_btn")
        self.gridLayout_2.addWidget(self.xml_convert_btn, 0, 1, 1, 1)
        self.xml_summary_btn = QtWidgets.QPushButton(self.convert_widget)
        self.xml_summary_btn.setEnabled(False)
        self.xml_summary_btn.setObjectName("xml_summary_btn")
        self.gridLayout_2.addWidget(self.xml_summary_btn, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.convert_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1122, 26))
        self.menubar.setObjectName("menubar")
        self.menuConverter = QtWidgets.QMenu(self.menubar)
        self.menuConverter.setObjectName("menuConverter")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsdf = QtWidgets.QAction(MainWindow)
        self.actionsdf.setObjectName("actionsdf")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/bootstrap-icons-1.8.3/save2-fill.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit_2 = QtWidgets.QAction(MainWindow)
        self.actionExit_2.setObjectName("actionExit_2")
        self.actionSomething = QtWidgets.QAction(MainWindow)
        self.actionSomething.setObjectName("actionSomething")
        self.actionExit_3 = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/bootstrap-icons-1.8.3/file-excel-fill.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit_3.setIcon(icon3)
        self.actionExit_3.setObjectName("actionExit_3")
        self.actionFunction_definitions = QtWidgets.QAction(MainWindow)
        self.actionFunction_definitions.setEnabled(False)
        self.actionFunction_definitions.setObjectName("actionFunction_definitions")
        self.menuConverter.addSeparator()
        self.menuConverter.addAction(self.actionFunction_definitions)
        self.menubar.addAction(self.menuConverter.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.xmlGroup_box.setTitle(_translate("MainWindow", "ATP xml"))
        self.xmlFilePath_display.setPlaceholderText(_translate("MainWindow", "ATP xml filepath"))
        self.configGroup_box.setTitle(_translate("MainWindow", "Config mapping"))
        self.configFilePath_display.setPlaceholderText(_translate("MainWindow", "Excel config filepath"))
        self.configFileUpdate_btn.setToolTip(_translate("MainWindow", "Update config with latest changes to mapping"))
        self.configFileUpdate_btn.setStatusTip(_translate("MainWindow", "Update config with latest changes to mapping"))
        self.configFileUpdate_btn.setWhatsThis(_translate("MainWindow", "Update config with latest changes to mapping"))
        self.configFileUpdate_btn.setText(_translate("MainWindow", "Update"))
        self.scrollAreaFilterBox_widget.setTitle(_translate("MainWindow", "Filters"))
        self.filterTestcaseOnly_btn.setText(_translate("MainWindow", "Test case"))
        self.filterFunctionOnly_btn.setText(_translate("MainWindow", "Function"))
        self.filterBoth_btn.setText(_translate("MainWindow", "Both"))
        self.xml_refreshData_btn.setToolTip(_translate("MainWindow", "Filter and load xml teststep data based on config"))
        self.xml_refreshData_btn.setStatusTip(_translate("MainWindow", "Filter and load xml teststep data based on config"))
        self.xml_refreshData_btn.setWhatsThis(_translate("MainWindow", "Filter and load xml teststep data based on config"))
        self.xml_refreshData_btn.setText(_translate("MainWindow", "Refresh"))
        self.xml_clearTeststeps_btn.setToolTip(_translate("MainWindow", "Clear data grid of and loaded xml teststeps"))
        self.xml_clearTeststeps_btn.setStatusTip(_translate("MainWindow", "Clear data grid of and loaded xml teststeps"))
        self.xml_clearTeststeps_btn.setWhatsThis(_translate("MainWindow", "Clear data grid of and loaded xml teststeps"))
        self.xml_clearTeststeps_btn.setText(_translate("MainWindow", "Clear"))
        self.showAll_btn.setToolTip(_translate("MainWindow", "Enable drop down on all testcase items"))
        self.showAll_btn.setStatusTip(_translate("MainWindow", "Disable all drop down on testcase items"))
        self.showAll_btn.setWhatsThis(_translate("MainWindow", "Disable all drop down on testcase items"))
        self.showAll_btn.setText(_translate("MainWindow", "Show all"))
        self.hideAll_btn.setToolTip(_translate("MainWindow", "Disable all drop down on testcase items"))
        self.hideAll_btn.setStatusTip(_translate("MainWindow", "Disable all drop down on testcase items"))
        self.hideAll_btn.setWhatsThis(_translate("MainWindow", "Disable all drop down on testcase items"))
        self.hideAll_btn.setText(_translate("MainWindow", "Hide all"))
        self.selectAll_checkBox.setToolTip(_translate("MainWindow", "Toggle all teststep selection"))
        self.selectAll_checkBox.setStatusTip(_translate("MainWindow", "Toggle all teststep selection"))
        self.selectAll_checkBox.setWhatsThis(_translate("MainWindow", "Toggle all teststep selection"))
        self.selectAll_checkBox.setText(_translate("MainWindow", "Select all"))
        self.xml_convert_btn.setToolTip(_translate("MainWindow", "Convert all selected teststeps"))
        self.xml_convert_btn.setStatusTip(_translate("MainWindow", "Convert all selected teststeps"))
        self.xml_convert_btn.setWhatsThis(_translate("MainWindow", "Convert all selected teststeps"))
        self.xml_convert_btn.setText(_translate("MainWindow", "Convert"))
        self.xml_summary_btn.setToolTip(_translate("MainWindow", "Summary of selected teststeps for conversion"))
        self.xml_summary_btn.setStatusTip(_translate("MainWindow", "Summary of selected teststeps for conversion"))
        self.xml_summary_btn.setWhatsThis(_translate("MainWindow", "Summary of selected teststeps for conversion"))
        self.xml_summary_btn.setText(_translate("MainWindow", "Summary"))
        self.menuConverter.setTitle(_translate("MainWindow", "File"))
        self.actionsdf.setText(_translate("MainWindow", "sdf"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit_2.setText(_translate("MainWindow", "Exit"))
        self.actionSomething.setText(_translate("MainWindow", "Exit"))
        self.actionExit_3.setText(_translate("MainWindow", "Close"))
        self.actionFunction_definitions.setText(_translate("MainWindow", "Function definitions"))

from .resources import bootstrap_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
