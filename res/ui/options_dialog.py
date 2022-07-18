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
        OptionsDialog.resize(381, 353)
        self.optionsLayout = QtWidgets.QVBoxLayout(OptionsDialog)
        self.optionsLayout.setObjectName("optionsLayout")
        self.OptionsScrollArea = QtWidgets.QScrollArea(OptionsDialog)
        self.OptionsScrollArea.setWidgetResizable(True)
        self.OptionsScrollArea.setObjectName("OptionsScrollArea")
        self.OptionsScrollWidget = QtWidgets.QWidget()
        self.OptionsScrollWidget.setGeometry(QtCore.QRect(0, -37, 344, 348))
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
        self.almostCheckbox = QtWidgets.QCheckBox(self.markerGroup)
        self.almostCheckbox.setChecked(True)
        self.almostCheckbox.setObjectName("almostCheckbox")
        self.markerLayout.addWidget(self.almostCheckbox)
        self.almostBackCheckbox = QtWidgets.QCheckBox(self.markerGroup)
        self.almostBackCheckbox.setChecked(True)
        self.almostBackCheckbox.setObjectName("almostBackCheckbox")
        self.markerLayout.addWidget(self.almostBackCheckbox)
        self.almostPosLayout = QtWidgets.QFormLayout()
        self.almostPosLayout.setHorizontalSpacing(64)
        self.almostPosLayout.setObjectName("almostPosLayout")
        self.almostLabel = QtWidgets.QLabel(self.markerGroup)
        self.almostLabel.setObjectName("almostLabel")
        self.almostPosLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.almostLabel)
        self.almostPosDropdown = QtWidgets.QComboBox(self.markerGroup)
        self.almostPosDropdown.setObjectName("almostPosDropdown")
        self.almostPosDropdown.addItem("")
        self.almostPosDropdown.addItem("")
        self.almostPosDropdown.addItem("")
        self.almostPosLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.almostPosDropdown)
        self.markerLayout.addLayout(self.almostPosLayout)
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
        self.reverseMethodDropdown = QtWidgets.QComboBox(self.groupBox)
        self.reverseMethodDropdown.setObjectName("reverseMethodDropdown")
        self.reverseMethodDropdown.addItem("")
        self.reverseMethodDropdown.addItem("")
        self.verticalLayout_2.addWidget(self.reverseMethodDropdown)
        self.reverseThresholdLayout = QtWidgets.QHBoxLayout()
        self.reverseThresholdLayout.setObjectName("reverseThresholdLayout")
        self.reverseThresholdLabel = QtWidgets.QLabel(self.groupBox)
        self.reverseThresholdLabel.setObjectName("reverseThresholdLabel")
        self.reverseThresholdLayout.addWidget(self.reverseThresholdLabel)
        self.reverseThreshold = QtWidgets.QSpinBox(self.groupBox)
        self.reverseThreshold.setMaximum(999)
        self.reverseThreshold.setProperty("value", 8)
        self.reverseThreshold.setObjectName("reverseThreshold")
        self.reverseThresholdLayout.addWidget(self.reverseThreshold)
        self.verticalLayout_2.addLayout(self.reverseThresholdLayout)
        self.optionsScrollLayout.addWidget(self.groupBox)
        self.OptionsScrollArea.setWidget(self.OptionsScrollWidget)
        self.optionsLayout.addWidget(self.OptionsScrollArea)
        self.buttonBox = QtWidgets.QDialogButtonBox(OptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.optionsLayout.addWidget(self.buttonBox)

        self.retranslateUi(OptionsDialog)
        self.buttonBox.accepted.connect(OptionsDialog.accept)
        self.buttonBox.rejected.connect(OptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Leech Toolkit"))
        self.toolsOptionsCheckBox.setText(_translate("OptionsDialog", "Show options in Tools menu"))
        self.markerGroup.setTitle(_translate("OptionsDialog", "Almost Leech Mark"))
        self.almostCheckbox.setToolTip(_translate("OptionsDialog", "When reviewing, displays a mark below the current card if it\'s about to be marked as a leech."))
        self.almostCheckbox.setText(_translate("OptionsDialog", "Enable almost-leech mark in reviews"))
        self.almostBackCheckbox.setText(_translate("OptionsDialog", "Only show on back of card"))
        self.almostLabel.setText(_translate("OptionsDialog", "Marker Position"))
        self.almostPosDropdown.setItemText(0, _translate("OptionsDialog", "Default"))
        self.almostPosDropdown.setItemText(1, _translate("OptionsDialog", "Left"))
        self.almostPosDropdown.setItemText(2, _translate("OptionsDialog", "Right"))
        self.browseButtonGroup.setTitle(_translate("OptionsDialog", "Leech Cards Button"))
        self.browseButtonCheckbox.setToolTip(_translate("OptionsDialog", "Enables a button on the bottom bar to quickly view all leech cards for all on-screen decks."))
        self.browseButtonCheckbox.setText(_translate("OptionsDialog", "Show \"Leech Cards\" button on Anki\'s bottom bar"))
        self.leechButtonPagesGroup.setTitle(_translate("OptionsDialog", "Enabled Pages"))
        self.browseButtonBrowserCheckbox.setText(_translate("OptionsDialog", "Deck Browser"))
        self.browseButtonOverviewCheckbox.setText(_translate("OptionsDialog", "Deck Overview"))
        self.groupBox.setTitle(_translate("OptionsDialog", "Leech Reverse"))
        self.reverseCheckbox.setText(_translate("OptionsDialog", "Use leech reversing"))
        self.reverseMethodDropdown.setItemText(0, _translate("OptionsDialog", "Decrease lapse count on correct answer"))
        self.reverseMethodDropdown.setItemText(1, _translate("OptionsDialog", "Reset lapse count on consecutive correct answers"))
        self.reverseThresholdLabel.setText(_translate("OptionsDialog", "Reverse Leech Threshold"))
        self.reverseThreshold.setToolTip(_translate("OptionsDialog", "Un-leeches a card that\'s lapse count has gone below this value."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
