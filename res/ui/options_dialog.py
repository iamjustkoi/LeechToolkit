# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        OptionsDialog.setObjectName("OptionsDialog")
        OptionsDialog.setWindowModality(QtCore.Qt.WindowModal)
        OptionsDialog.resize(574, 509)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(OptionsDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(OptionsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.generalTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.OptionsScrollArea = QtWidgets.QScrollArea(self.generalTab)
        self.OptionsScrollArea.setWidgetResizable(True)
        self.OptionsScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.OptionsScrollArea.setObjectName("OptionsScrollArea")
        self.OptionsScrollWidget = QtWidgets.QWidget()
        self.OptionsScrollWidget.setGeometry(QtCore.QRect(0, 0, 530, 277))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OptionsScrollWidget.sizePolicy().hasHeightForWidth())
        self.OptionsScrollWidget.setSizePolicy(sizePolicy)
        self.OptionsScrollWidget.setObjectName("OptionsScrollWidget")
        self.optionsScrollLayout = QtWidgets.QVBoxLayout(self.OptionsScrollWidget)
        self.optionsScrollLayout.setObjectName("optionsScrollLayout")
        self.toolsOptionsCheckBox = QtWidgets.QCheckBox(self.OptionsScrollWidget)
        self.toolsOptionsCheckBox.setObjectName("toolsOptionsCheckBox")
        self.optionsScrollLayout.addWidget(self.toolsOptionsCheckBox)
        self.markerGroup = QtWidgets.QGroupBox(self.OptionsScrollWidget)
        self.markerGroup.setObjectName("markerGroup")
        self.markerLayout = QtWidgets.QVBoxLayout(self.markerGroup)
        self.markerLayout.setObjectName("markerLayout")
        self.showMarkerChecbkbox = QtWidgets.QCheckBox(self.markerGroup)
        self.showMarkerChecbkbox.setObjectName("showMarkerChecbkbox")
        self.markerLayout.addWidget(self.showMarkerChecbkbox)
        self.almostBackCheckbox = QtWidgets.QCheckBox(self.markerGroup)
        self.almostBackCheckbox.setObjectName("almostBackCheckbox")
        self.markerLayout.addWidget(self.almostBackCheckbox)
        self.almostCheckbox = QtWidgets.QCheckBox(self.markerGroup)
        self.almostCheckbox.setObjectName("almostCheckbox")
        self.markerLayout.addWidget(self.almostCheckbox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.almostLabel = QtWidgets.QLabel(self.markerGroup)
        self.almostLabel.setObjectName("almostLabel")
        self.horizontalLayout_4.addWidget(self.almostLabel)
        self.almostPosDropdown = QtWidgets.QComboBox(self.markerGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.almostPosDropdown.sizePolicy().hasHeightForWidth())
        self.almostPosDropdown.setSizePolicy(sizePolicy)
        self.almostPosDropdown.setObjectName("almostPosDropdown")
        self.almostPosDropdown.addItem("")
        self.almostPosDropdown.addItem("")
        self.almostPosDropdown.addItem("")
        self.horizontalLayout_4.addWidget(self.almostPosDropdown)
        self.markerLayout.addLayout(self.horizontalLayout_4)
        self.optionsScrollLayout.addWidget(self.markerGroup)
        self.browseButtonGroup = QtWidgets.QGroupBox(self.OptionsScrollWidget)
        self.browseButtonGroup.setObjectName("browseButtonGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.browseButtonGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.browseButtonCheckbox = QtWidgets.QCheckBox(self.browseButtonGroup)
        self.browseButtonCheckbox.setObjectName("browseButtonCheckbox")
        self.verticalLayout.addWidget(self.browseButtonCheckbox)
        self.leechButtonPagesGroup = QtWidgets.QGroupBox(self.browseButtonGroup)
        self.leechButtonPagesGroup.setObjectName("leechButtonPagesGroup")
        self.leechButtonPagesLayout = QtWidgets.QHBoxLayout(self.leechButtonPagesGroup)
        self.leechButtonPagesLayout.setObjectName("leechButtonPagesLayout")
        self.browseButtonBrowserCheckbox = QtWidgets.QCheckBox(self.leechButtonPagesGroup)
        self.browseButtonBrowserCheckbox.setObjectName("browseButtonBrowserCheckbox")
        self.leechButtonPagesLayout.addWidget(self.browseButtonBrowserCheckbox)
        self.browseButtonOverviewCheckbox = QtWidgets.QCheckBox(self.leechButtonPagesGroup)
        self.browseButtonOverviewCheckbox.setObjectName("browseButtonOverviewCheckbox")
        self.leechButtonPagesLayout.addWidget(self.browseButtonOverviewCheckbox)
        self.verticalLayout.addWidget(self.leechButtonPagesGroup)
        self.optionsScrollLayout.addWidget(self.browseButtonGroup)
        self.OptionsScrollArea.setWidget(self.OptionsScrollWidget)
        self.verticalLayout_3.addWidget(self.OptionsScrollArea)
        self.tabWidget.addTab(self.generalTab, "")
        self.actionsTab = QtWidgets.QWidget()
        self.actionsTab.setObjectName("actionsTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.actionsTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ActionsScrollArea = QtWidgets.QScrollArea(self.actionsTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ActionsScrollArea.sizePolicy().hasHeightForWidth())
        self.ActionsScrollArea.setSizePolicy(sizePolicy)
        self.ActionsScrollArea.setWidgetResizable(True)
        self.ActionsScrollArea.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ActionsScrollArea.setObjectName("ActionsScrollArea")
        self.ActionsScrollWidget = QtWidgets.QWidget()
        self.ActionsScrollWidget.setGeometry(QtCore.QRect(0, 0, 488, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ActionsScrollWidget.sizePolicy().hasHeightForWidth())
        self.ActionsScrollWidget.setSizePolicy(sizePolicy)
        self.ActionsScrollWidget.setObjectName("ActionsScrollWidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.ActionsScrollWidget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.actionsScrollFrame = QtWidgets.QFrame(self.ActionsScrollWidget)
        self.actionsScrollFrame.setMouseTracking(True)
        self.actionsScrollFrame.setObjectName("actionsScrollFrame")
        self.actionsScrollLayout = QtWidgets.QVBoxLayout(self.actionsScrollFrame)
        self.actionsScrollLayout.setContentsMargins(-1, 0, -1, 0)
        self.actionsScrollLayout.setObjectName("actionsScrollLayout")
        self.verticalLayout_6.addWidget(self.actionsScrollFrame)
        self.ActionsScrollArea.setWidget(self.ActionsScrollWidget)
        self.verticalLayout_5.addWidget(self.ActionsScrollArea)
        self.tabWidget.addTab(self.actionsTab, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(OptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(OptionsDialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(OptionsDialog.accept)
        self.buttonBox.rejected.connect(OptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Leech Toolkit"))
        self.toolsOptionsCheckBox.setText(_translate("OptionsDialog", "Show options in Tools menu"))
        self.markerGroup.setTitle(_translate("OptionsDialog", "Leech Mark"))
        self.showMarkerChecbkbox.setText(_translate("OptionsDialog", "Show a marker on leech cards during review"))
        self.almostBackCheckbox.setText(_translate("OptionsDialog", "Only show on back of cards"))
        self.almostCheckbox.setToolTip(_translate("OptionsDialog", "When reviewing, displays a mark below the current card if it\'s about to be marked as a leech."))
        self.almostCheckbox.setText(_translate("OptionsDialog", "Show unique marker for about-to-be-leeched cards"))
        self.almostLabel.setText(_translate("OptionsDialog", "Marker Position"))
        self.almostPosDropdown.setItemText(0, _translate("OptionsDialog", "Default"))
        self.almostPosDropdown.setItemText(1, _translate("OptionsDialog", "Left"))
        self.almostPosDropdown.setItemText(2, _translate("OptionsDialog", "Right"))
        self.browseButtonGroup.setTitle(_translate("OptionsDialog", "Bottom Bar Button"))
        self.browseButtonCheckbox.setToolTip(_translate("OptionsDialog", "Show a button on the bottom bar whenever a currently displayed deck has any leeches."))
        self.browseButtonCheckbox.setText(_translate("OptionsDialog", "Enable \"Leech Cards\" button on bottom bar"))
        self.leechButtonPagesGroup.setTitle(_translate("OptionsDialog", "Enabled Pages"))
        self.browseButtonBrowserCheckbox.setText(_translate("OptionsDialog", "Deck Browser"))
        self.browseButtonOverviewCheckbox.setText(_translate("OptionsDialog", "Deck Overview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("OptionsDialog", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.actionsTab), _translate("OptionsDialog", "Actions"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
