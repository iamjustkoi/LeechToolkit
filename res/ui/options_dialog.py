# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        OptionsDialog.setObjectName("OptionsDialog")
        OptionsDialog.setWindowModality(QtCore.Qt.WindowModal)
        OptionsDialog.resize(460, 462)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(OptionsDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(OptionsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.generalTab)
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.OptionsScrollArea = QtWidgets.QScrollArea(self.generalTab)
        self.OptionsScrollArea.setWidgetResizable(True)
        self.OptionsScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.OptionsScrollArea.setObjectName("OptionsScrollArea")
        self.OptionsScrollWidget = QtWidgets.QWidget()
        self.OptionsScrollWidget.setGeometry(QtCore.QRect(0, 0, 413, 415))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OptionsScrollWidget.sizePolicy().hasHeightForWidth())
        self.OptionsScrollWidget.setSizePolicy(sizePolicy)
        self.OptionsScrollWidget.setObjectName("OptionsScrollWidget")
        self.optionsScrollLayout = QtWidgets.QVBoxLayout(self.OptionsScrollWidget)
        self.optionsScrollLayout.setObjectName("optionsScrollLayout")
        self.toolsOptionsCheckBox = QtWidgets.QCheckBox(self.OptionsScrollWidget)
        self.toolsOptionsCheckBox.setChecked(True)
        self.toolsOptionsCheckBox.setObjectName("toolsOptionsCheckBox")
        self.optionsScrollLayout.addWidget(self.toolsOptionsCheckBox)
        self.markerGroup = QtWidgets.QGroupBox(self.OptionsScrollWidget)
        self.markerGroup.setObjectName("markerGroup")
        self.markerLayout = QtWidgets.QVBoxLayout(self.markerGroup)
        self.markerLayout.setObjectName("markerLayout")
        self.showMarkerChecbkbox = QtWidgets.QCheckBox(self.markerGroup)
        self.showMarkerChecbkbox.setChecked(True)
        self.showMarkerChecbkbox.setObjectName("showMarkerChecbkbox")
        self.markerLayout.addWidget(self.showMarkerChecbkbox)
        self.almostBackCheckbox = QtWidgets.QCheckBox(self.markerGroup)
        self.almostBackCheckbox.setChecked(True)
        self.almostBackCheckbox.setObjectName("almostBackCheckbox")
        self.markerLayout.addWidget(self.almostBackCheckbox)
        self.almostCheckbox = QtWidgets.QCheckBox(self.markerGroup)
        self.almostCheckbox.setChecked(True)
        self.almostCheckbox.setObjectName("almostCheckbox")
        self.markerLayout.addWidget(self.almostCheckbox)
        self.markerPosLayout = QtWidgets.QFormLayout()
        self.markerPosLayout.setHorizontalSpacing(64)
        self.markerPosLayout.setObjectName("markerPosLayout")
        self.almostLabel = QtWidgets.QLabel(self.markerGroup)
        self.almostLabel.setObjectName("almostLabel")
        self.markerPosLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.almostLabel)
        self.almostPosDropdown = QtWidgets.QComboBox(self.markerGroup)
        self.almostPosDropdown.setObjectName("almostPosDropdown")
        self.almostPosDropdown.addItem("")
        self.almostPosDropdown.addItem("")
        self.almostPosDropdown.addItem("")
        self.markerPosLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.almostPosDropdown)
        self.markerLayout.addLayout(self.markerPosLayout)
        self.optionsScrollLayout.addWidget(self.markerGroup)
        self.browseButtonGroup = QtWidgets.QGroupBox(self.OptionsScrollWidget)
        self.browseButtonGroup.setObjectName("browseButtonGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.browseButtonGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.browseButtonCheckbox = QtWidgets.QCheckBox(self.browseButtonGroup)
        self.browseButtonCheckbox.setChecked(True)
        self.browseButtonCheckbox.setObjectName("browseButtonCheckbox")
        self.verticalLayout.addWidget(self.browseButtonCheckbox)
        self.leechButtonPagesGroup = QtWidgets.QGroupBox(self.browseButtonGroup)
        self.leechButtonPagesGroup.setObjectName("leechButtonPagesGroup")
        self.leechButtonPagesLayout = QtWidgets.QHBoxLayout(self.leechButtonPagesGroup)
        self.leechButtonPagesLayout.setObjectName("leechButtonPagesLayout")
        self.browseButtonBrowserCheckbox = QtWidgets.QCheckBox(self.leechButtonPagesGroup)
        self.browseButtonBrowserCheckbox.setChecked(True)
        self.browseButtonBrowserCheckbox.setObjectName("browseButtonBrowserCheckbox")
        self.leechButtonPagesLayout.addWidget(self.browseButtonBrowserCheckbox)
        self.browseButtonOverviewCheckbox = QtWidgets.QCheckBox(self.leechButtonPagesGroup)
        self.browseButtonOverviewCheckbox.setChecked(True)
        self.browseButtonOverviewCheckbox.setObjectName("browseButtonOverviewCheckbox")
        self.leechButtonPagesLayout.addWidget(self.browseButtonOverviewCheckbox)
        self.verticalLayout.addWidget(self.leechButtonPagesGroup)
        self.optionsScrollLayout.addWidget(self.browseButtonGroup)
        self.groupBox = QtWidgets.QGroupBox(self.OptionsScrollWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.reverseCheckbox = QtWidgets.QCheckBox(self.groupBox)
        self.reverseCheckbox.setChecked(True)
        self.reverseCheckbox.setObjectName("reverseCheckbox")
        self.verticalLayout_2.addWidget(self.reverseCheckbox)
        self.reverseThresholdLayout = QtWidgets.QHBoxLayout()
        self.reverseThresholdLayout.setObjectName("reverseThresholdLayout")
        self.reverseThresholdLabel = QtWidgets.QLabel(self.groupBox)
        self.reverseThresholdLabel.setObjectName("reverseThresholdLabel")
        self.reverseThresholdLayout.addWidget(self.reverseThresholdLabel)
        self.reverseThreshold = QtWidgets.QSpinBox(self.groupBox)
        self.reverseThreshold.setMaximum(999)
        self.reverseThreshold.setProperty("value", 4)
        self.reverseThreshold.setObjectName("reverseThreshold")
        self.reverseThresholdLayout.addWidget(self.reverseThreshold)
        self.verticalLayout_2.addLayout(self.reverseThresholdLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.consPrefixLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consPrefixLabel.sizePolicy().hasHeightForWidth())
        self.consPrefixLabel.setSizePolicy(sizePolicy)
        self.consPrefixLabel.setObjectName("consPrefixLabel")
        self.horizontalLayout.addWidget(self.consPrefixLabel)
        self.consAnswerSpinbox = QtWidgets.QSpinBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consAnswerSpinbox.sizePolicy().hasHeightForWidth())
        self.consAnswerSpinbox.setSizePolicy(sizePolicy)
        self.consAnswerSpinbox.setSuffix("")
        self.consAnswerSpinbox.setPrefix("")
        self.consAnswerSpinbox.setMinimum(1)
        self.consAnswerSpinbox.setMaximum(9999)
        self.consAnswerSpinbox.setProperty("value", 2)
        self.consAnswerSpinbox.setObjectName("consAnswerSpinbox")
        self.horizontalLayout.addWidget(self.consAnswerSpinbox)
        self.consSuffixLabel = QtWidgets.QLabel(self.groupBox)
        self.consSuffixLabel.setObjectName("consSuffixLabel")
        self.horizontalLayout.addWidget(self.consSuffixLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.reverseMethodDropdown = QtWidgets.QComboBox(self.groupBox)
        self.reverseMethodDropdown.setObjectName("reverseMethodDropdown")
        self.reverseMethodDropdown.addItem("")
        self.reverseMethodDropdown.addItem("")
        self.verticalLayout_2.addWidget(self.reverseMethodDropdown)
        self.optionsScrollLayout.addWidget(self.groupBox)
        self.OptionsScrollArea.setWidget(self.OptionsScrollWidget)
        self.verticalLayout_3.addWidget(self.OptionsScrollArea)
        self.tabWidget.addTab(self.generalTab, "")
        self.actionsTab = QtWidgets.QWidget()
        self.actionsTab.setObjectName("actionsTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.actionsTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ActionsScrollArea = QtWidgets.QScrollArea(self.actionsTab)
        self.ActionsScrollArea.setWidgetResizable(True)
        self.ActionsScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ActionsScrollArea.setObjectName("ActionsScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 416, 369))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.collapsibleLeechActionsGroup = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collapsibleLeechActionsGroup.sizePolicy().hasHeightForWidth())
        self.collapsibleLeechActionsGroup.setSizePolicy(sizePolicy)
        self.collapsibleLeechActionsGroup.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.collapsibleLeechActionsGroup.setFlat(True)
        self.collapsibleLeechActionsGroup.setObjectName("collapsibleLeechActionsGroup")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.collapsibleLeechActionsGroup)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.leechActionsLayout = QtWidgets.QFormLayout()
        self.leechActionsLayout.setObjectName("leechActionsLayout")
        self.flagCheckbox = QtWidgets.QCheckBox(self.collapsibleLeechActionsGroup)
        self.flagCheckbox.setObjectName("flagCheckbox")
        self.leechActionsLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.flagCheckbox)
        self.flagDropdown = QtWidgets.QComboBox(self.collapsibleLeechActionsGroup)
        self.flagDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.flagDropdown.setObjectName("flagDropdown")
        self.flagDropdown.addItem("")
        self.flagDropdown.addItem("")
        self.flagDropdown.addItem("")
        self.flagDropdown.addItem("")
        self.flagDropdown.addItem("")
        self.flagDropdown.addItem("")
        self.flagDropdown.addItem("")
        self.flagDropdown.addItem("")
        self.leechActionsLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.flagDropdown)
        self.suspendCheckbox = QtWidgets.QCheckBox(self.collapsibleLeechActionsGroup)
        self.suspendCheckbox.setObjectName("suspendCheckbox")
        self.leechActionsLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.suspendCheckbox)
        self.addTagsCheckbox = QtWidgets.QCheckBox(self.collapsibleLeechActionsGroup)
        self.addTagsCheckbox.setObjectName("addTagsCheckbox")
        self.leechActionsLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.addTagsCheckbox)
        self.addTagsLine = QtWidgets.QLineEdit(self.collapsibleLeechActionsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addTagsLine.sizePolicy().hasHeightForWidth())
        self.addTagsLine.setSizePolicy(sizePolicy)
        self.addTagsLine.setObjectName("addTagsLine")
        self.leechActionsLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.addTagsLine)
        self.removeTagsCheckbox = QtWidgets.QCheckBox(self.collapsibleLeechActionsGroup)
        self.removeTagsCheckbox.setObjectName("removeTagsCheckbox")
        self.leechActionsLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.removeTagsCheckbox)
        self.removeTagsLine = QtWidgets.QLineEdit(self.collapsibleLeechActionsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeTagsLine.sizePolicy().hasHeightForWidth())
        self.removeTagsLine.setSizePolicy(sizePolicy)
        self.removeTagsLine.setObjectName("removeTagsLine")
        self.leechActionsLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.removeTagsLine)
        self.suspendFrame = QtWidgets.QFrame(self.collapsibleLeechActionsGroup)
        self.suspendFrame.setObjectName("suspendFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.suspendFrame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.suspendOnButton = QtWidgets.QRadioButton(self.suspendFrame)
        self.suspendOnButton.setObjectName("suspendOnButton")
        self.horizontalLayout_2.addWidget(self.suspendOnButton)
        self.suspendOffButton = QtWidgets.QRadioButton(self.suspendFrame)
        self.suspendOffButton.setObjectName("suspendOffButton")
        self.horizontalLayout_2.addWidget(self.suspendOffButton)
        self.leechActionsLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.suspendFrame)
        self.checkBox = QtWidgets.QCheckBox(self.collapsibleLeechActionsGroup)
        self.checkBox.setObjectName("checkBox")
        self.leechActionsLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.checkBox)
        self.forgetFrame = QtWidgets.QFrame(self.collapsibleLeechActionsGroup)
        self.forgetFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.forgetFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.forgetFrame.setObjectName("forgetFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.forgetFrame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.forgetOffRadio = QtWidgets.QRadioButton(self.forgetFrame)
        self.forgetOffRadio.setObjectName("forgetOffRadio")
        self.horizontalLayout_3.addWidget(self.forgetOffRadio)
        self.forgetOnRadio = QtWidgets.QRadioButton(self.forgetFrame)
        self.forgetOnRadio.setObjectName("forgetOnRadio")
        self.horizontalLayout_3.addWidget(self.forgetOnRadio)
        self.leechActionsLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.forgetFrame)
        self.forgetRestorePosCheckbox = QtWidgets.QCheckBox(self.collapsibleLeechActionsGroup)
        self.forgetRestorePosCheckbox.setObjectName("forgetRestorePosCheckbox")
        self.leechActionsLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.forgetRestorePosCheckbox)
        self.forgetResetCheckbox = QtWidgets.QCheckBox(self.collapsibleLeechActionsGroup)
        self.forgetResetCheckbox.setObjectName("forgetResetCheckbox")
        self.leechActionsLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.forgetResetCheckbox)
        self.verticalLayout_7.addLayout(self.leechActionsLayout)
        self.verticalLayout_6.addWidget(self.collapsibleLeechActionsGroup)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.ActionsScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.ActionsScrollArea)
        self.tabWidget.addTab(self.actionsTab, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(OptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(OptionsDialog)
        self.tabWidget.setCurrentIndex(1)
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
        self.groupBox.setTitle(_translate("OptionsDialog", "Leech Reverse"))
        self.reverseCheckbox.setText(_translate("OptionsDialog", "Enable leech reversing"))
        self.reverseThresholdLabel.setText(_translate("OptionsDialog", "Reverse Leech Threshold"))
        self.reverseThreshold.setToolTip(_translate("OptionsDialog", "Un-leeches any cards with a lapse count below this value."))
        self.consPrefixLabel.setText(_translate("OptionsDialog", "Every"))
        self.consSuffixLabel.setText(_translate("OptionsDialog", "correct answer(s) in a row:"))
        self.reverseMethodDropdown.setCurrentText(_translate("OptionsDialog", "Decrease card\'s total lapse count"))
        self.reverseMethodDropdown.setItemText(0, _translate("OptionsDialog", "Decrease card\'s total lapse count"))
        self.reverseMethodDropdown.setItemText(1, _translate("OptionsDialog", "Reset card\'s total lapse count"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("OptionsDialog", "General"))
        self.collapsibleLeechActionsGroup.setTitle(_translate("OptionsDialog", "Leech Actions"))
        self.flagCheckbox.setText(_translate("OptionsDialog", "Set Flag"))
        self.flagDropdown.setItemText(0, _translate("OptionsDialog", "No Flag"))
        self.flagDropdown.setItemText(1, _translate("OptionsDialog", "Red"))
        self.flagDropdown.setItemText(2, _translate("OptionsDialog", "Orange"))
        self.flagDropdown.setItemText(3, _translate("OptionsDialog", "Green"))
        self.flagDropdown.setItemText(4, _translate("OptionsDialog", "Blue"))
        self.flagDropdown.setItemText(5, _translate("OptionsDialog", "Pink"))
        self.flagDropdown.setItemText(6, _translate("OptionsDialog", "Turquise"))
        self.flagDropdown.setItemText(7, _translate("OptionsDialog", "Purple"))
        self.suspendCheckbox.setText(_translate("OptionsDialog", "Suspend"))
        self.addTagsCheckbox.setText(_translate("OptionsDialog", "Add Tag(s)"))
        self.removeTagsCheckbox.setText(_translate("OptionsDialog", "Remove Tag(s)"))
        self.suspendOnButton.setText(_translate("OptionsDialog", "On"))
        self.suspendOffButton.setText(_translate("OptionsDialog", "Off"))
        self.checkBox.setText(_translate("OptionsDialog", "Forget"))
        self.forgetOffRadio.setText(_translate("OptionsDialog", "On"))
        self.forgetOnRadio.setText(_translate("OptionsDialog", "Off"))
        self.forgetRestorePosCheckbox.setText(_translate("OptionsDialog", "Restore import position where possible"))
        self.forgetResetCheckbox.setText(_translate("OptionsDialog", "Reset total reviews and lapses"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.actionsTab), _translate("OptionsDialog", "Actions"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
