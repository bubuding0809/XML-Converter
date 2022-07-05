# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiFunctionDefinitionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FunctionDefinitionDialog(object):
    def setupUi(self, FunctionDefinitionDialog):
        FunctionDefinitionDialog.setObjectName("FunctionDefinitionDialog")
        FunctionDefinitionDialog.resize(689, 670)
        self.verticalLayout = QtWidgets.QVBoxLayout(FunctionDefinitionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header_widget = QtWidgets.QWidget(FunctionDefinitionDialog)
        self.header_widget.setObjectName("header_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_2 = QtWidgets.QWidget(self.header_widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.infoIcon_label = QtWidgets.QLabel(self.widget_2)
        self.infoIcon_label.setMaximumSize(QtCore.QSize(30, 30))
        self.infoIcon_label.setText("")
        self.infoIcon_label.setPixmap(QtGui.QPixmap(":/icons/bootstrap-icons-1.8.3/info.png"))
        self.infoIcon_label.setScaledContents(True)
        self.infoIcon_label.setObjectName("infoIcon_label")
        self.horizontalLayout_2.addWidget(self.infoIcon_label)
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayout.addWidget(self.widget_2, 0, QtCore.Qt.AlignTop)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.header_widget)
        self.data_widget = QtWidgets.QWidget(FunctionDefinitionDialog)
        self.data_widget.setObjectName("data_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.data_widget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.dataTreeTools_widget = QtWidgets.QWidget(self.data_widget)
        self.dataTreeTools_widget.setObjectName("dataTreeTools_widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dataTreeTools_widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.dataTreeSearchBox_widget = QtWidgets.QWidget(self.dataTreeTools_widget)
        self.dataTreeSearchBox_widget.setObjectName("dataTreeSearchBox_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.dataTreeSearchBox_widget)
        self.horizontalLayout_4.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_3.addWidget(self.dataTreeSearchBox_widget)
        self.dataTreeButtonBox_widget = QtWidgets.QWidget(self.dataTreeTools_widget)
        self.dataTreeButtonBox_widget.setObjectName("dataTreeButtonBox_widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.dataTreeButtonBox_widget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.showAll_btn = QtWidgets.QPushButton(self.dataTreeButtonBox_widget)
        self.showAll_btn.setObjectName("showAll_btn")
        self.horizontalLayout_5.addWidget(self.showAll_btn)
        self.hideAll_btn = QtWidgets.QPushButton(self.dataTreeButtonBox_widget)
        self.hideAll_btn.setObjectName("hideAll_btn")
        self.horizontalLayout_5.addWidget(self.hideAll_btn)
        self.newFunction_btn = QtWidgets.QPushButton(self.dataTreeButtonBox_widget)
        self.newFunction_btn.setObjectName("newFunction_btn")
        self.horizontalLayout_5.addWidget(self.newFunction_btn)
        self.deleteFunction_btn = QtWidgets.QPushButton(self.dataTreeButtonBox_widget)
        self.deleteFunction_btn.setObjectName("deleteFunction_btn")
        self.horizontalLayout_5.addWidget(self.deleteFunction_btn)
        self.horizontalLayout_3.addWidget(self.dataTreeButtonBox_widget)
        self.gridLayout.addWidget(self.dataTreeTools_widget, 0, 0, 1, 1)
        self.dataTreeMain_widget = QtWidgets.QWidget(self.data_widget)
        self.dataTreeMain_widget.setObjectName("dataTreeMain_widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.dataTreeMain_widget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.functionLibraryTree_widget = QtWidgets.QTreeWidget(self.dataTreeMain_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.functionLibraryTree_widget.sizePolicy().hasHeightForWidth())
        self.functionLibraryTree_widget.setSizePolicy(sizePolicy)
        self.functionLibraryTree_widget.setMinimumSize(QtCore.QSize(500, 0))
        self.functionLibraryTree_widget.setAlternatingRowColors(True)
        self.functionLibraryTree_widget.setUniformRowHeights(False)
        self.functionLibraryTree_widget.setAllColumnsShowFocus(False)
        self.functionLibraryTree_widget.setHeaderHidden(False)
        self.functionLibraryTree_widget.setObjectName("functionLibraryTree_widget")
        self.functionLibraryTree_widget.header().setVisible(True)
        self.functionLibraryTree_widget.header().setHighlightSections(False)
        self.functionLibraryTree_widget.header().setSortIndicatorShown(False)
        self.functionLibraryTree_widget.header().setStretchLastSection(True)
        self.horizontalLayout_6.addWidget(self.functionLibraryTree_widget)
        self.functionParametersList_wigdet = QtWidgets.QListWidget(self.dataTreeMain_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.functionParametersList_wigdet.sizePolicy().hasHeightForWidth())
        self.functionParametersList_wigdet.setSizePolicy(sizePolicy)
        self.functionParametersList_wigdet.setMaximumSize(QtCore.QSize(150, 16777215))
        self.functionParametersList_wigdet.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.functionParametersList_wigdet.setObjectName("functionParametersList_wigdet")
        self.horizontalLayout_6.addWidget(self.functionParametersList_wigdet)
        self.gridLayout.addWidget(self.dataTreeMain_widget, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.data_widget)
        self.dialogButton_box = QtWidgets.QDialogButtonBox(FunctionDefinitionDialog)
        self.dialogButton_box.setOrientation(QtCore.Qt.Horizontal)
        self.dialogButton_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Save)
        self.dialogButton_box.setObjectName("dialogButton_box")
        self.verticalLayout.addWidget(self.dialogButton_box)

        self.retranslateUi(FunctionDefinitionDialog)
        self.dialogButton_box.accepted.connect(FunctionDefinitionDialog.accept) # type: ignore
        self.dialogButton_box.rejected.connect(FunctionDefinitionDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(FunctionDefinitionDialog)

    def retranslateUi(self, FunctionDefinitionDialog):
        _translate = QtCore.QCoreApplication.translate
        FunctionDefinitionDialog.setWindowTitle(_translate("FunctionDefinitionDialog", "Dialog"))
        self.label.setText(_translate("FunctionDefinitionDialog", "Function libary"))
        self.showAll_btn.setToolTip(_translate("FunctionDefinitionDialog", "Expand all test cases"))
        self.showAll_btn.setStatusTip(_translate("FunctionDefinitionDialog", "Expand all test cases"))
        self.showAll_btn.setWhatsThis(_translate("FunctionDefinitionDialog", "Expand all test cases"))
        self.showAll_btn.setText(_translate("FunctionDefinitionDialog", "Show all"))
        self.hideAll_btn.setToolTip(_translate("FunctionDefinitionDialog", "Unexpand all test cases"))
        self.hideAll_btn.setStatusTip(_translate("FunctionDefinitionDialog", "Unexpand all test cases"))
        self.hideAll_btn.setWhatsThis(_translate("FunctionDefinitionDialog", "Unexpand all test cases"))
        self.hideAll_btn.setText(_translate("FunctionDefinitionDialog", "Hide all"))
        self.newFunction_btn.setText(_translate("FunctionDefinitionDialog", "New"))
        self.deleteFunction_btn.setText(_translate("FunctionDefinitionDialog", "delete"))
        self.functionLibraryTree_widget.setSortingEnabled(True)
        self.functionLibraryTree_widget.headerItem().setText(0, _translate("FunctionDefinitionDialog", "Function library"))
        self.functionLibraryTree_widget.headerItem().setText(1, _translate("FunctionDefinitionDialog", "Function name"))

from .resources import bootstrap_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FunctionDefinitionDialog = QtWidgets.QDialog()
    ui = Ui_FunctionDefinitionDialog()
    ui.setupUi(FunctionDefinitionDialog)
    FunctionDefinitionDialog.show()
    sys.exit(app.exec_())
