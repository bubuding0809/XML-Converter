# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiWarningTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WarningTab(object):
    def setupUi(self, WarningTab):
        WarningTab.setObjectName("WarningTab")
        WarningTab.resize(615, 437)
        self.verticalLayout = QtWidgets.QVBoxLayout(WarningTab)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.warningDescription_label = QtWidgets.QLabel(WarningTab)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.warningDescription_label.setFont(font)
        self.warningDescription_label.setText("")
        self.warningDescription_label.setWordWrap(True)
        self.warningDescription_label.setIndent(1)
        self.warningDescription_label.setObjectName("warningDescription_label")
        self.verticalLayout.addWidget(self.warningDescription_label)
        self.dataTree_Widget = QtWidgets.QTreeWidget(WarningTab)
        self.dataTree_Widget.setInputMethodHints(QtCore.Qt.ImhNone)
        self.dataTree_Widget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dataTree_Widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.dataTree_Widget.setAutoScroll(True)
        self.dataTree_Widget.setTabKeyNavigation(True)
        self.dataTree_Widget.setProperty("showDropIndicator", True)
        self.dataTree_Widget.setAlternatingRowColors(True)
        self.dataTree_Widget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.dataTree_Widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.dataTree_Widget.setRootIsDecorated(True)
        self.dataTree_Widget.setUniformRowHeights(False)
        self.dataTree_Widget.setAnimated(True)
        self.dataTree_Widget.setAllColumnsShowFocus(False)
        self.dataTree_Widget.setWordWrap(True)
        self.dataTree_Widget.setHeaderHidden(False)
        self.dataTree_Widget.setExpandsOnDoubleClick(True)
        self.dataTree_Widget.setObjectName("dataTree_Widget")
        self.dataTree_Widget.header().setVisible(True)
        self.dataTree_Widget.header().setCascadingSectionResizes(True)
        self.dataTree_Widget.header().setHighlightSections(False)
        self.dataTree_Widget.header().setSortIndicatorShown(False)
        self.dataTree_Widget.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.dataTree_Widget)

        self.retranslateUi(WarningTab)
        QtCore.QMetaObject.connectSlotsByName(WarningTab)

    def retranslateUi(self, WarningTab):
        _translate = QtCore.QCoreApplication.translate
        WarningTab.setWindowTitle(_translate("WarningTab", "Form"))
        self.dataTree_Widget.setSortingEnabled(False)
        self.dataTree_Widget.headerItem().setText(0, _translate("WarningTab", "Worksheet"))
        self.dataTree_Widget.headerItem().setText(1, _translate("WarningTab", "Source"))
        self.dataTree_Widget.headerItem().setText(2, _translate("WarningTab", "Issues"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WarningTab = QtWidgets.QWidget()
    ui = Ui_WarningTab()
    ui.setupUi(WarningTab)
    WarningTab.show()
    sys.exit(app.exec_())