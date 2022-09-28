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
        OptionsDialog.resize(574, 520)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(OptionsDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(OptionsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.generalTab)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.OptionsScrollArea = QtWidgets.QScrollArea(self.generalTab)
        self.OptionsScrollArea.setWidgetResizable(True)
        self.OptionsScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.OptionsScrollArea.setObjectName("OptionsScrollArea")
        self.OptionsScrollWidget = QtWidgets.QWidget()
        self.OptionsScrollWidget.setGeometry(QtCore.QRect(0, 0, 530, 175))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OptionsScrollWidget.sizePolicy().hasHeightForWidth())
        self.OptionsScrollWidget.setSizePolicy(sizePolicy)
        self.OptionsScrollWidget.setObjectName("OptionsScrollWidget")
        self.optionsScrollLayout = QtWidgets.QVBoxLayout(self.OptionsScrollWidget)
        self.optionsScrollLayout.setSpacing(6)
        self.optionsScrollLayout.setObjectName("optionsScrollLayout")
        self.markerGroup = QtWidgets.QGroupBox(self.OptionsScrollWidget)
        self.markerGroup.setCheckable(True)
        self.markerGroup.setObjectName("markerGroup")
        self.markerLayout = QtWidgets.QVBoxLayout(self.markerGroup)
        self.markerLayout.setObjectName("markerLayout")
        self.almostBackCheckbox = QtWidgets.QCheckBox(self.markerGroup)
        self.almostBackCheckbox.setChecked(True)
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
        self.browseButtonGroup.setCheckable(True)
        self.browseButtonGroup.setObjectName("browseButtonGroup")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.browseButtonGroup)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.browseButtonBrowserCheckbox = QtWidgets.QCheckBox(self.browseButtonGroup)
        self.browseButtonBrowserCheckbox.setObjectName("browseButtonBrowserCheckbox")
        self.horizontalLayout.addWidget(self.browseButtonBrowserCheckbox)
        self.browseButtonOverviewCheckbox = QtWidgets.QCheckBox(self.browseButtonGroup)
        self.browseButtonOverviewCheckbox.setObjectName("browseButtonOverviewCheckbox")
        self.horizontalLayout.addWidget(self.browseButtonOverviewCheckbox)
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
        self.ActionsScrollWidget.setGeometry(QtCore.QRect(0, 0, 530, 16))
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
        self.advancedTab = QtWidgets.QWidget()
        self.advancedTab.setObjectName("advancedTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.advancedTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.advancedScrollArea = QtWidgets.QScrollArea(self.advancedTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.advancedScrollArea.sizePolicy().hasHeightForWidth())
        self.advancedScrollArea.setSizePolicy(sizePolicy)
        self.advancedScrollArea.setWidgetResizable(True)
        self.advancedScrollArea.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.advancedScrollArea.setObjectName("advancedScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 530, 210))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolsOptionsCheckBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.toolsOptionsCheckBox.setObjectName("toolsOptionsCheckBox")
        self.verticalLayout_2.addWidget(self.toolsOptionsCheckBox)
        self.syncUpdateCheckbox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.syncUpdateCheckbox.setChecked(False)
        self.syncUpdateCheckbox.setObjectName("syncUpdateCheckbox")
        self.verticalLayout_2.addWidget(self.syncUpdateCheckbox)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setWordWrap(True)
        self.label_2.setIndent(12)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.syncTagCheckbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.syncTagCheckbox.setCheckable(True)
        self.syncTagCheckbox.setObjectName("syncTagCheckbox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.syncTagCheckbox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.syncTagLineEdit = QtWidgets.QLineEdit(self.syncTagCheckbox)
        self.syncTagLineEdit.setObjectName("syncTagLineEdit")
        self.verticalLayout_7.addWidget(self.syncTagLineEdit)
        self.label = QtWidgets.QLabel(self.syncTagCheckbox)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.syncTagCheckbox)
        self.syncUpdateButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syncUpdateButton.sizePolicy().hasHeightForWidth())
        self.syncUpdateButton.setSizePolicy(sizePolicy)
        self.syncUpdateButton.setObjectName("syncUpdateButton")
        self.verticalLayout_2.addWidget(self.syncUpdateButton)
        self.advancedScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.advancedScrollArea)
        self.tabWidget.addTab(self.advancedTab, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(OptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.RestoreDefaults
            )
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
        self.markerGroup.setToolTip(_translate("OptionsDialog", "Show a marker on leech cards during review."))
        self.markerGroup.setTitle(_translate("OptionsDialog", "Leech Mark"))
        self.almostBackCheckbox.setText(_translate("OptionsDialog", "Only show on back of cards"))
        self.almostCheckbox.setToolTip(
            _translate(
                "OptionsDialog",
                "When reviewing, displays a mark below the current card if it\'s about to be marked as a leech."
            )
        )
        self.almostCheckbox.setText(_translate("OptionsDialog", "Show unique marker for about-to-be-leeched cards"))
        self.almostLabel.setText(_translate("OptionsDialog", "Marker Position"))
        self.almostPosDropdown.setItemText(0, _translate("OptionsDialog", "Default"))
        self.almostPosDropdown.setItemText(1, _translate("OptionsDialog", "Left"))
        self.almostPosDropdown.setItemText(2, _translate("OptionsDialog", "Right"))
        self.browseButtonGroup.setToolTip(
            _translate(
                "OptionsDialog",
                "Shows a button on bottom bar whenever cards with the leech tag are found in a deck."
            )
        )
        self.browseButtonGroup.setTitle(_translate("OptionsDialog", "Bottom Bar Button"))
        self.browseButtonBrowserCheckbox.setText(_translate("OptionsDialog", "Deck Browser"))
        self.browseButtonOverviewCheckbox.setText(_translate("OptionsDialog", "Deck Overview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("OptionsDialog", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.actionsTab), _translate("OptionsDialog", "Actions"))
        self.toolsOptionsCheckBox.setText(_translate("OptionsDialog", "Show options in Tools menu"))
        self.syncUpdateCheckbox.setToolTip(
            _translate(
                "OptionsDialog",
                "After syncing, updates the entire collection with the current options/actions based on the synced review logs."
            )
        )
        self.syncUpdateCheckbox.setText(_translate("OptionsDialog", "Update collection on-sync"))
        self.label_2.setText(
            _translate(
                "OptionsDialog",
                "* Overwrites non-review/non-reschedule changes to card lapse counts (e.g. Leech Toolkit browser actions, database edits, etc.)."
            )
        )
        self.syncTagCheckbox.setToolTip(
            _translate(
                "OptionsDialog",
                "Keeps track of leech/unleech actions across devices using a custom tag that gets added to any filtered leeches."
            )
        )
        self.syncTagCheckbox.setTitle(
            _translate(
                "OptionsDialog", "Use a custom tag to keep track of toolkit updates across devices\n"
                                 "                                            "
            )
        )
        self.syncTagLineEdit.setText(_translate("OptionsDialog", "leech::toolkit-filtered"))
        self.label.setText(
            _translate(
                "OptionsDialog",
                "* Before syncing/updating, should be updated to the same tag as any other Anki client(s) where it might\'ve also been changed and synced/uploaded."
            )
        )
        self.syncUpdateButton.setToolTip(
            _translate(
                "OptionsDialog",
                "Sync the entire collection based on the current, applied options and review logs."
            )
        )
        self.syncUpdateButton.setText(_translate("OptionsDialog", "Update Collection"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.advancedTab), _translate("OptionsDialog", "Advanced"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
