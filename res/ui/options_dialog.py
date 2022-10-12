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
        OptionsDialog.resize(533, 520)
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
        self.OptionsScrollWidget.setGeometry(QtCore.QRect(0, 0, 489, 175))
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
        self.ActionsScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ActionsScrollArea.setObjectName("ActionsScrollArea")
        self.ActionsScrollWidget = QtWidgets.QWidget()
        self.ActionsScrollWidget.setGeometry(QtCore.QRect(0, 0, 489, 16))
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
        self.advancedScrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.advancedScrollArea.setObjectName("advancedScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 489, 314))
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
        self.shortcutsGroupbox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.shortcutsGroupbox.setObjectName("shortcutsGroupbox")
        self.gridLayout = QtWidgets.QGridLayout(self.shortcutsGroupbox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.shortcutsGroupbox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.leechShortcutButton = QtWidgets.QPushButton(self.shortcutsGroupbox)
        self.leechShortcutButton.setObjectName("leechShortcutButton")
        self.gridLayout.addWidget(self.leechShortcutButton, 0, 1, 1, 1)
        self.unleechShortcutButton = QtWidgets.QPushButton(self.shortcutsGroupbox)
        self.unleechShortcutButton.setObjectName("unleechShortcutButton")
        self.gridLayout.addWidget(self.unleechShortcutButton, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.shortcutsGroupbox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.shortcutsGroupbox)
        self.advancedScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.advancedScrollArea)
        self.tabWidget.addTab(self.advancedTab, "")
        self.aboutTab = QtWidgets.QWidget()
        self.aboutTab.setObjectName("aboutTab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.aboutTab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.scroll_area = QtWidgets.QScrollArea(self.aboutTab)
        self.scroll_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.about_scroll = QtWidgets.QWidget()
        self.about_scroll.setGeometry(QtCore.QRect(0, 0, 472, 516))
        self.about_scroll.setObjectName("about_scroll")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.about_scroll)
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.setObjectName("scroll_layout")
        self.about_label_header = QtWidgets.QLabel(self.about_scroll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_label_header.sizePolicy().hasHeightForWidth())
        self.about_label_header.setSizePolicy(sizePolicy)
        self.about_label_header.setTextFormat(QtCore.Qt.MarkdownText)
        self.about_label_header.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.about_label_header.setWordWrap(True)
        self.about_label_header.setOpenExternalLinks(True)
        self.about_label_header.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.about_label_header.setObjectName("about_label_header")
        self.scroll_layout.addWidget(self.about_label_header)
        self.support_buttons = QtWidgets.QHBoxLayout()
        self.support_buttons.setContentsMargins(6, 6, 6, 6)
        self.support_buttons.setObjectName("support_buttons")
        self.like_button = QtWidgets.QPushButton(self.about_scroll)
        self.like_button.setMinimumSize(QtCore.QSize(0, 42))
        self.like_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.like_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.like_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.like_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../StudyTimeStats/res/ui/res/img/anki_like.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.like_button.setIcon(icon)
        self.like_button.setIconSize(QtCore.QSize(32, 32))
        self.like_button.setObjectName("like_button")
        self.support_buttons.addWidget(self.like_button)
        self.kofi_button = QtWidgets.QPushButton(self.about_scroll)
        self.kofi_button.setMinimumSize(QtCore.QSize(0, 42))
        self.kofi_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.kofi_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.kofi_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.kofi_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../../StudyTimeStats/res/ui/res/img/kofilogo_blue.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.kofi_button.setIcon(icon1)
        self.kofi_button.setIconSize(QtCore.QSize(32, 32))
        self.kofi_button.setObjectName("kofi_button")
        self.support_buttons.addWidget(self.kofi_button)
        self.patreon_button = QtWidgets.QPushButton(self.about_scroll)
        self.patreon_button.setMinimumSize(QtCore.QSize(0, 42))
        self.patreon_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.patreon_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.patreon_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.patreon_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../../StudyTimeStats/res/ui/res/img/patreon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.patreon_button.setIcon(icon2)
        self.patreon_button.setIconSize(QtCore.QSize(32, 32))
        self.patreon_button.setObjectName("patreon_button")
        self.support_buttons.addWidget(self.patreon_button)
        self.scroll_layout.addLayout(self.support_buttons)
        self.about_label_body = QtWidgets.QLabel(self.about_scroll)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_label_body.sizePolicy().hasHeightForWidth())
        self.about_label_body.setSizePolicy(sizePolicy)
        self.about_label_body.setTextFormat(QtCore.Qt.MarkdownText)
        self.about_label_body.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.about_label_body.setWordWrap(True)
        self.about_label_body.setOpenExternalLinks(True)
        self.about_label_body.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.about_label_body.setObjectName("about_label_body")
        self.scroll_layout.addWidget(self.about_label_body)
        self.scroll_layout.setStretch(2, 1)
        self.scroll_area.setWidget(self.about_scroll)
        self.verticalLayout_8.addWidget(self.scroll_area)
        self.tabWidget.addTab(self.aboutTab, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(OptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(OptionsDialog)
        self.tabWidget.setCurrentIndex(3)
        self.buttonBox.accepted.connect(OptionsDialog.accept)
        self.buttonBox.rejected.connect(OptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Leech Toolkit"))
        self.markerGroup.setToolTip(_translate("OptionsDialog", "Show a marker on leech cards during review."))
        self.markerGroup.setTitle(_translate("OptionsDialog", "Leech Mark"))
        self.almostBackCheckbox.setToolTip(_translate("OptionsDialog", "Disables the mark when only showing the front/answer in reviews."))
        self.almostBackCheckbox.setText(_translate("OptionsDialog", "Only show on back of cards"))
        self.almostCheckbox.setToolTip(_translate("OptionsDialog", "When reviewing, displays a mark below the current card if it\'s about to be marked as a leech."))
        self.almostCheckbox.setText(_translate("OptionsDialog", "Show unique marker for about-to-be-leeched cards"))
        self.almostLabel.setText(_translate("OptionsDialog", "Marker Position"))
        self.almostPosDropdown.setToolTip(_translate("OptionsDialog", "Position of the attached marker. Attaches to the bottom of the reveiwer with a centered default value."))
        self.almostPosDropdown.setItemText(0, _translate("OptionsDialog", "Default"))
        self.almostPosDropdown.setItemText(1, _translate("OptionsDialog", "Left"))
        self.almostPosDropdown.setItemText(2, _translate("OptionsDialog", "Right"))
        self.browseButtonGroup.setToolTip(_translate("OptionsDialog", "Shows a button on bottom bar whenever cards with the leech tag are found in a deck."))
        self.browseButtonGroup.setTitle(_translate("OptionsDialog", "Bottom Bar Button"))
        self.browseButtonBrowserCheckbox.setToolTip(_translate("OptionsDialog", "Enables the button on the main, deck list page."))
        self.browseButtonBrowserCheckbox.setText(_translate("OptionsDialog", "Deck Browser"))
        self.browseButtonOverviewCheckbox.setToolTip(_translate("OptionsDialog", "Enables the button for the page show when viewing a specific deck."))
        self.browseButtonOverviewCheckbox.setText(_translate("OptionsDialog", "Deck Overview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("OptionsDialog", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.actionsTab), _translate("OptionsDialog", "Actions"))
        self.toolsOptionsCheckBox.setToolTip(_translate("OptionsDialog", "Enables a Tools menu shortcut in the toolbar for accessing these options. \n"
"These can also be accessed in the Add-ons window from the \"Config\" button."))
        self.toolsOptionsCheckBox.setText(_translate("OptionsDialog", "Show options in Tools menu"))
        self.syncUpdateCheckbox.setToolTip(_translate("OptionsDialog", "After syncing, updates the entire collection with the current options/actions based on the synced review logs."))
        self.syncUpdateCheckbox.setText(_translate("OptionsDialog", "Update collection on-sync"))
        self.label_2.setText(_translate("OptionsDialog", "* Overwrites non-review/non-reschedule changes to card lapse counts ( Leech Toolkit browser actions, database edits, etc.). "))
        self.syncTagCheckbox.setToolTip(_translate("OptionsDialog", "Keeps track of leech/unleech actions across devices using a custom tag that gets added to any filtered leeches."))
        self.syncTagCheckbox.setTitle(_translate("OptionsDialog", "Use a custom tag to keep track of toolkit updates across devices."))
        self.syncTagLineEdit.setToolTip(_translate("OptionsDialog", "Custom tag text."))
        self.syncTagLineEdit.setText(_translate("OptionsDialog", "leech::toolkit-filtered"))
        self.label.setText(_translate("OptionsDialog", "* Before syncing/updating, should be updated to the same tag as any other Anki client(s) where it might\'ve also been changed and synced/uploaded."))
        self.syncUpdateButton.setToolTip(_translate("OptionsDialog", "Sync the entire collection based on the current, applied options and review logs."))
        self.syncUpdateButton.setText(_translate("OptionsDialog", "Update Collection"))
        self.shortcutsGroupbox.setTitle(_translate("OptionsDialog", "Shortcuts"))
        self.label_3.setText(_translate("OptionsDialog", "Leech"))
        self.leechShortcutButton.setToolTip(_translate("OptionsDialog", "May need to reset for shortcuts to update in reviewer."))
        self.leechShortcutButton.setText(_translate("OptionsDialog", "Ctrl+Shift+L"))
        self.unleechShortcutButton.setToolTip(_translate("OptionsDialog", "May need to reset for shortcuts to update in reviewer."))
        self.unleechShortcutButton.setText(_translate("OptionsDialog", "Ctrl+Shift+U"))
        self.label_4.setText(_translate("OptionsDialog", "Un-Leech"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.advancedTab), _translate("OptionsDialog", "Advanced"))
        self.about_label_header.setText(_translate("OptionsDialog", "## Leech Toolkit 🩸\n"
"Add additional tools and functionality for handling leeches in Anki!\n"
"\n"
"Version: {version}  \n"
"Have any issues or feedback? Feel free to post on the project\'s issue section on [GitHub](https://github.com/iamjustkoi/StudyTimeStats/issues)!  \n"
"\n"
"[Releases/Changelog](https://github.com/iamjustkoi/LeechToolkit/releases)  \n"
"[Source Code](https://github.com/iamjustkoi/LeechToolkit)  \n"
"\n"
"If you want to help support what I do:"))
        self.like_button.setText(_translate("OptionsDialog", "Review on AnkiWeb "))
        self.kofi_button.setText(_translate("OptionsDialog", "  Buy me a coffee "))
        self.patreon_button.setText(_translate("OptionsDialog", "  Become a patron "))
        self.about_label_body.setText(_translate("OptionsDialog", "Every bit helps and is greatly appreciated!\n"
"\n"
"### Text Macros:\n"
"\n"
"- `%date` - the current date based on the system\'s locale (e.g. `2022-10-01`)\n"
"- `%reviews` - the review count for the current card (e.g. `3`)\n"
"- `%re:` - [Regular Expressions](https://learnxinyminutes.com/docs/pcre/)\n"
"    - Example Syntax:\n"
"        - `%re:captured_expression`\n"
"        - `%re:\".*captured with spaces\\W\"`\n"
"        - `%re:\\d\\d\\d\\d-\\d\\d-\\d\\d` (capturing the above date format)\n"
"- `%%` - single % (e.g. `%%reviews` outputs `%reviews` instead of applying the macro)\n"
"\n"
"<br></br>\n"
"Thanks for downloading and happy leeching!  \n"
"-koi  \n"
"<br></br>  \n"
"MIT License    \n"
"©2022 JustKoi (iamjustkoi)  "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aboutTab), _translate("OptionsDialog", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
