# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'actions_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_ActionsWidget(object):
    def setupUi(self, ActionsWidget):
        ActionsWidget.setObjectName("ActionsWidget")
        ActionsWidget.resize(443, 739)
        self.verticalLayout = QtWidgets.QVBoxLayout(ActionsWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.expandoWidget = ExpandoWidget(ActionsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expandoWidget.sizePolicy().hasHeightForWidth())
        self.expandoWidget.setSizePolicy(sizePolicy)
        self.expandoWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.expandoWidget.setObjectName("expandoWidget")
        self.leechActionsExpandoLayout = QtWidgets.QHBoxLayout(self.expandoWidget)
        self.leechActionsExpandoLayout.setContentsMargins(0, 0, 0, 0)
        self.leechActionsExpandoLayout.setSpacing(0)
        self.leechActionsExpandoLayout.setObjectName("leechActionsExpandoLayout")
        self.expandoButton = QtWidgets.QToolButton(self.expandoWidget)
        self.expandoButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.expandoButton.setStyleSheet("border: none;")
        self.expandoButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.expandoButton.setArrowType(QtCore.Qt.RightArrow)
        self.expandoButton.setObjectName("expandoButton")
        self.leechActionsExpandoLayout.addWidget(self.expandoButton)
        self.expandoLine = QtWidgets.QFrame(self.expandoWidget)
        self.expandoLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.expandoLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.expandoLine.setObjectName("expandoLine")
        self.leechActionsExpandoLayout.addWidget(self.expandoLine)
        self.verticalLayout.addWidget(self.expandoWidget)
        self.actionsFrame = QtWidgets.QFrame(ActionsWidget)
        self.actionsFrame.setObjectName("actionsFrame")
        self.leechActionsLayout = QtWidgets.QFormLayout(self.actionsFrame)
        self.leechActionsLayout.setContentsMargins(12, 0, 0, 0)
        self.leechActionsLayout.setObjectName("leechActionsLayout")
        self.flagCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.flagCheckbox.setObjectName("flagCheckbox")
        self.leechActionsLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.flagCheckbox)
        self.flagDropdown = QtWidgets.QComboBox(self.actionsFrame)
        self.flagDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
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
        self.suspendCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.suspendCheckbox.setObjectName("suspendCheckbox")
        self.leechActionsLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.suspendCheckbox)
        self.suspendFrame = QtWidgets.QFrame(self.actionsFrame)
        self.suspendFrame.setObjectName("suspendFrame")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.suspendFrame)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.suspendOnButton = QtWidgets.QRadioButton(self.suspendFrame)
        self.suspendOnButton.setObjectName("suspendOnButton")
        self.horizontalLayout_9.addWidget(self.suspendOnButton)
        self.suspendOffButton = QtWidgets.QRadioButton(self.suspendFrame)
        self.suspendOffButton.setObjectName("suspendOffButton")
        self.horizontalLayout_9.addWidget(self.suspendOffButton)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.leechActionsLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.suspendFrame)
        self.addTagsCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.addTagsCheckbox.setObjectName("addTagsCheckbox")
        self.leechActionsLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.addTagsCheckbox)
        self.addTagsLine = QtWidgets.QLineEdit(self.actionsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addTagsLine.sizePolicy().hasHeightForWidth())
        self.addTagsLine.setSizePolicy(sizePolicy)
        self.addTagsLine.setClearButtonEnabled(True)
        self.addTagsLine.setObjectName("addTagsLine")
        self.leechActionsLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.addTagsLine)
        self.removeTagsCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.removeTagsCheckbox.setObjectName("removeTagsCheckbox")
        self.leechActionsLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.removeTagsCheckbox)
        self.removeTagsLine = QtWidgets.QLineEdit(self.actionsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeTagsLine.sizePolicy().hasHeightForWidth())
        self.removeTagsLine.setSizePolicy(sizePolicy)
        self.removeTagsLine.setClearButtonEnabled(True)
        self.removeTagsLine.setObjectName("removeTagsLine")
        self.leechActionsLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.removeTagsLine)
        self.forgetCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.forgetCheckbox.setObjectName("forgetCheckbox")
        self.leechActionsLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.forgetCheckbox)
        self.forgetFrame = QtWidgets.QFrame(self.actionsFrame)
        self.forgetFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.forgetFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.forgetFrame.setObjectName("forgetFrame")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.forgetFrame)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.forgetOnRadio = QtWidgets.QRadioButton(self.forgetFrame)
        self.forgetOnRadio.setObjectName("forgetOnRadio")
        self.horizontalLayout_13.addWidget(self.forgetOnRadio)
        self.forgetOffRadio = QtWidgets.QRadioButton(self.forgetFrame)
        self.forgetOffRadio.setObjectName("forgetOffRadio")
        self.horizontalLayout_13.addWidget(self.forgetOffRadio)
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem1)
        self.leechActionsLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.forgetFrame)
        self.forgetRestorePosCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.forgetRestorePosCheckbox.setObjectName("forgetRestorePosCheckbox")
        self.leechActionsLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.forgetRestorePosCheckbox)
        self.forgetResetCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.forgetResetCheckbox.setObjectName("forgetResetCheckbox")
        self.leechActionsLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.forgetResetCheckbox)
        self.editFieldsCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.editFieldsCheckbox.setObjectName("editFieldsCheckbox")
        self.leechActionsLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.editFieldsCheckbox)
        self.deckMoveCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.deckMoveCheckbox.setObjectName("deckMoveCheckbox")
        self.leechActionsLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.deckMoveCheckbox)
        self.deckMoveLine = QtWidgets.QLineEdit(self.actionsFrame)
        self.deckMoveLine.setClearButtonEnabled(True)
        self.deckMoveLine.setObjectName("deckMoveLine")
        self.leechActionsLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.deckMoveLine)
        self.rescheduleCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.rescheduleCheckbox.setObjectName("rescheduleCheckbox")
        self.leechActionsLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.rescheduleCheckbox)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.rescheduleText1 = QtWidgets.QLabel(self.actionsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rescheduleText1.sizePolicy().hasHeightForWidth())
        self.rescheduleText1.setSizePolicy(sizePolicy)
        self.rescheduleText1.setObjectName("rescheduleText1")
        self.horizontalLayout_14.addWidget(self.rescheduleText1)
        self.rescheduleFromDays = QtWidgets.QSpinBox(self.actionsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rescheduleFromDays.sizePolicy().hasHeightForWidth())
        self.rescheduleFromDays.setSizePolicy(sizePolicy)
        self.rescheduleFromDays.setMaximum(9999)
        self.rescheduleFromDays.setObjectName("rescheduleFromDays")
        self.horizontalLayout_14.addWidget(self.rescheduleFromDays)
        self.rescheduleText2 = QtWidgets.QLabel(self.actionsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rescheduleText2.sizePolicy().hasHeightForWidth())
        self.rescheduleText2.setSizePolicy(sizePolicy)
        self.rescheduleText2.setObjectName("rescheduleText2")
        self.horizontalLayout_14.addWidget(self.rescheduleText2)
        self.rescheduleToDays = QtWidgets.QSpinBox(self.actionsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rescheduleToDays.sizePolicy().hasHeightForWidth())
        self.rescheduleToDays.setSizePolicy(sizePolicy)
        self.rescheduleToDays.setMaximum(9999)
        self.rescheduleToDays.setObjectName("rescheduleToDays")
        self.horizontalLayout_14.addWidget(self.rescheduleToDays)
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem2)
        self.leechActionsLayout.setLayout(9, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_14)
        self.rescheduleResetCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.rescheduleResetCheckbox.setObjectName("rescheduleResetCheckbox")
        self.leechActionsLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.rescheduleResetCheckbox)
        self.queueCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.queueCheckbox.setObjectName("queueCheckbox")
        self.leechActionsLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.queueCheckbox)
        self.frame_6 = QtWidgets.QFrame(self.actionsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.queueFromDropdown = QtWidgets.QComboBox(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueFromDropdown.sizePolicy().hasHeightForWidth())
        self.queueFromDropdown.setSizePolicy(sizePolicy)
        self.queueFromDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.queueFromDropdown.setObjectName("queueFromDropdown")
        self.queueFromDropdown.addItem("")
        self.queueFromDropdown.addItem("")
        self.queueFromDropdown.addItem("")
        self.horizontalLayout_16.addWidget(self.queueFromDropdown)
        self.queueFromSpinbox = QueueSpinBox(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueFromSpinbox.sizePolicy().hasHeightForWidth())
        self.queueFromSpinbox.setSizePolicy(sizePolicy)
        self.queueFromSpinbox.setMinimum(-9999999)
        self.queueFromSpinbox.setMaximum(9999999)
        self.queueFromSpinbox.setObjectName("queueFromSpinbox")
        self.horizontalLayout_16.addWidget(self.queueFromSpinbox)
        self.queueTilda = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueTilda.sizePolicy().hasHeightForWidth())
        self.queueTilda.setSizePolicy(sizePolicy)
        self.queueTilda.setObjectName("queueTilda")
        self.horizontalLayout_16.addWidget(self.queueTilda)
        self.queueToDropdown = QtWidgets.QComboBox(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueToDropdown.sizePolicy().hasHeightForWidth())
        self.queueToDropdown.setSizePolicy(sizePolicy)
        self.queueToDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.queueToDropdown.setObjectName("queueToDropdown")
        self.queueToDropdown.addItem("")
        self.queueToDropdown.addItem("")
        self.queueToDropdown.addItem("")
        self.horizontalLayout_16.addWidget(self.queueToDropdown)
        self.queueToSpinbox = QueueSpinBox(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueToSpinbox.sizePolicy().hasHeightForWidth())
        self.queueToSpinbox.setSizePolicy(sizePolicy)
        self.queueToSpinbox.setMinimum(-9999999)
        self.queueToSpinbox.setMaximum(9999999)
        self.queueToSpinbox.setObjectName("queueToSpinbox")
        self.horizontalLayout_16.addWidget(self.queueToSpinbox)
        self.verticalLayout_15.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_17.addWidget(self.label_3)
        self.queueLabelTop = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueLabelTop.sizePolicy().hasHeightForWidth())
        self.queueLabelTop.setSizePolicy(sizePolicy)
        self.queueLabelTop.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.queueLabelTop.setObjectName("queueLabelTop")
        self.horizontalLayout_17.addWidget(self.queueLabelTop)
        self.queueLabelTopPos = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueLabelTopPos.sizePolicy().hasHeightForWidth())
        self.queueLabelTopPos.setSizePolicy(sizePolicy)
        self.queueLabelTopPos.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.queueLabelTopPos.setObjectName("queueLabelTopPos")
        self.horizontalLayout_17.addWidget(self.queueLabelTopPos)
        spacerItem3 = QtWidgets.QSpacerItem(6, 0, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem3)
        self.queueLabelBottom = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueLabelBottom.sizePolicy().hasHeightForWidth())
        self.queueLabelBottom.setSizePolicy(sizePolicy)
        self.queueLabelBottom.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.queueLabelBottom.setObjectName("queueLabelBottom")
        self.horizontalLayout_17.addWidget(self.queueLabelBottom)
        self.queueLabelBottomPos = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueLabelBottomPos.sizePolicy().hasHeightForWidth())
        self.queueLabelBottomPos.setSizePolicy(sizePolicy)
        self.queueLabelBottomPos.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.queueLabelBottomPos.setObjectName("queueLabelBottomPos")
        self.horizontalLayout_17.addWidget(self.queueLabelBottomPos)
        spacerItem4 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem4)
        self.verticalLayout_15.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_15.addLayout(self.verticalLayout_15)
        self.leechActionsLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.frame_6)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.queueSimilarCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.queueSimilarCheckbox.setObjectName("queueSimilarCheckbox")
        self.verticalLayout_16.addWidget(self.queueSimilarCheckbox)
        self.frame_7 = QtWidgets.QFrame(self.actionsFrame)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_17.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.groupBox_4 = QtWidgets.QGroupBox(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.queueExcludeTextEdit = QtWidgets.QTextEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueExcludeTextEdit.sizePolicy().hasHeightForWidth())
        self.queueExcludeTextEdit.setSizePolicy(sizePolicy)
        self.queueExcludeTextEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.queueExcludeTextEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.queueExcludeTextEdit.setTabChangesFocus(True)
        self.queueExcludeTextEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.queueExcludeTextEdit.setObjectName("queueExcludeTextEdit")
        self.verticalLayout_19.addWidget(self.queueExcludeTextEdit)
        self.verticalLayout_18.addWidget(self.groupBox_4)
        spacerItem5 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_18.addItem(spacerItem5)
        self.horizontalLayout_19.addLayout(self.verticalLayout_18)
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.groupBox_5 = QtWidgets.QGroupBox(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.groupBox_5.setObjectName("groupBox_5")
        self._4 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self._4.setObjectName("_4")
        self.queueIncludeFieldsCheckbox = QtWidgets.QCheckBox(self.groupBox_5)
        self.queueIncludeFieldsCheckbox.setObjectName("queueIncludeFieldsCheckbox")
        self._4.addWidget(self.queueIncludeFieldsCheckbox)
        self.queueExcludedFieldList = QtWidgets.QListWidget(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueExcludedFieldList.sizePolicy().hasHeightForWidth())
        self.queueExcludedFieldList.setSizePolicy(sizePolicy)
        self.queueExcludedFieldList.setMaximumSize(QtCore.QSize(16777215, 256))
        self.queueExcludedFieldList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.queueExcludedFieldList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.queueExcludedFieldList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.queueExcludedFieldList.setProperty("showDropIndicator", False)
        self.queueExcludedFieldList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.queueExcludedFieldList.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.queueExcludedFieldList.setItemAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.queueExcludedFieldList.setObjectName("queueExcludedFieldList")
        self._4.addWidget(self.queueExcludedFieldList)
        self.frame_8 = QtWidgets.QFrame(self.groupBox_5)
        self.frame_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_8.setObjectName("frame_8")
        self._5 = QtWidgets.QHBoxLayout(self.frame_8)
        self._5.setContentsMargins(0, 0, 0, 0)
        self._5.setObjectName("_5")
        self.queueAddFieldButton = QtWidgets.QToolButton(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queueAddFieldButton.sizePolicy().hasHeightForWidth())
        self.queueAddFieldButton.setSizePolicy(sizePolicy)
        self.queueAddFieldButton.setMinimumSize(QtCore.QSize(64, 24))
        self.queueAddFieldButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.queueAddFieldButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.queueAddFieldButton.setArrowType(QtCore.Qt.NoArrow)
        self.queueAddFieldButton.setObjectName("queueAddFieldButton")
        self._5.addWidget(self.queueAddFieldButton)
        self._4.addWidget(self.frame_8)
        self.verticalLayout_20.addWidget(self.groupBox_5)
        spacerItem6 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_20.addItem(spacerItem6)
        self.horizontalLayout_19.addLayout(self.verticalLayout_20)
        self.verticalLayout_17.addLayout(self.horizontalLayout_19)
        self.verticalLayout_16.addWidget(self.frame_7)
        self.horizontalLayout_18.addLayout(self.verticalLayout_16)
        self.leechActionsLayout.setLayout(14, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_18)
        self.queueSiblingCheckbox = QtWidgets.QCheckBox(self.actionsFrame)
        self.queueSiblingCheckbox.setObjectName("queueSiblingCheckbox")
        self.leechActionsLayout.setWidget(16, QtWidgets.QFormLayout.FieldRole, self.queueSiblingCheckbox)
        self.editFieldsGroup = QtWidgets.QGroupBox(self.actionsFrame)
        self.editFieldsGroup.setObjectName("editFieldsGroup")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.editFieldsGroup)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.editFieldsList = QtWidgets.QListWidget(self.editFieldsGroup)
        self.editFieldsList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.editFieldsList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.editFieldsList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.editFieldsList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.editFieldsList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.editFieldsList.setProperty("showDropIndicator", False)
        self.editFieldsList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.editFieldsList.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.editFieldsList.setItemAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.editFieldsList.setObjectName("editFieldsList")
        self.verticalLayout_21.addWidget(self.editFieldsList)
        self.editAddFieldButton = QtWidgets.QPushButton(self.editFieldsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editAddFieldButton.sizePolicy().hasHeightForWidth())
        self.editAddFieldButton.setSizePolicy(sizePolicy)
        self.editAddFieldButton.setObjectName("editAddFieldButton")
        self.verticalLayout_21.addWidget(self.editAddFieldButton)
        self.leechActionsLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.editFieldsGroup)
        self.frame_9 = QtWidgets.QFrame(self.actionsFrame)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 20))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_4 = QtWidgets.QLabel(self.frame_9)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_20.addWidget(self.label_4)
        self.queueRatioSlider = TipSlider(self.frame_9)
        self.queueRatioSlider.setMinimum(0)
        self.queueRatioSlider.setMaximum(100)
        self.queueRatioSlider.setOrientation(QtCore.Qt.Horizontal)
        self.queueRatioSlider.setObjectName("queueRatioSlider")
        self.horizontalLayout_20.addWidget(self.queueRatioSlider)
        self.leechActionsLayout.setWidget(15, QtWidgets.QFormLayout.FieldRole, self.frame_9)
        self.verticalLayout.addWidget(self.actionsFrame)

        self.retranslateUi(ActionsWidget)
        QtCore.QMetaObject.connectSlotsByName(ActionsWidget)

    def retranslateUi(self, ActionsWidget):
        _translate = QtCore.QCoreApplication.translate
        ActionsWidget.setWindowTitle(_translate("ActionsWidget", "Form"))
        self.flagCheckbox.setText(_translate("ActionsWidget", "Set Flag"))
        self.flagDropdown.setItemText(0, _translate("ActionsWidget", "No Flag"))
        self.flagDropdown.setItemText(1, _translate("ActionsWidget", "Red"))
        self.flagDropdown.setItemText(2, _translate("ActionsWidget", "Orange"))
        self.flagDropdown.setItemText(3, _translate("ActionsWidget", "Green"))
        self.flagDropdown.setItemText(4, _translate("ActionsWidget", "Blue"))
        self.flagDropdown.setItemText(5, _translate("ActionsWidget", "Pink"))
        self.flagDropdown.setItemText(6, _translate("ActionsWidget", "Turquise"))
        self.flagDropdown.setItemText(7, _translate("ActionsWidget", "Purple"))
        self.suspendCheckbox.setText(_translate("ActionsWidget", "Suspend"))
        self.suspendOnButton.setText(_translate("ActionsWidget", "On"))
        self.suspendOffButton.setText(_translate("ActionsWidget", "Off"))
        self.addTagsCheckbox.setText(_translate("ActionsWidget", "Add Tag(s)"))
        self.removeTagsCheckbox.setText(_translate("ActionsWidget", "Remove Tag(s)"))
        self.forgetCheckbox.setText(_translate("ActionsWidget", "Forget"))
        self.forgetOnRadio.setText(_translate("ActionsWidget", "On"))
        self.forgetOffRadio.setText(_translate("ActionsWidget", "Off"))
        self.forgetRestorePosCheckbox.setText(_translate("ActionsWidget", "Restore imported position where possible"))
        self.forgetResetCheckbox.setText(_translate("ActionsWidget", "Reset total reviews and lapses"))
        self.editFieldsCheckbox.setText(_translate("ActionsWidget", "Edit Field(s)"))
        self.deckMoveCheckbox.setText(_translate("ActionsWidget", "Move to Deck"))
        self.rescheduleCheckbox.setText(_translate("ActionsWidget", "Set Due Date"))
        self.rescheduleText1.setText(_translate("ActionsWidget", "Between"))
        self.rescheduleText2.setText(_translate("ActionsWidget", "and"))
        self.rescheduleToDays.setSuffix(_translate("ActionsWidget", " days"))
        self.rescheduleResetCheckbox.setToolTip(_translate("ActionsWidget",
                                                           "Updates the card\'s interval using the time between the current day and the updated date."))
        self.rescheduleResetCheckbox.setText(_translate("ActionsWidget", "Update interval"))
        self.queueCheckbox.setToolTip(
            _translate("ActionsWidget", "Adds the card to the new queue using the specified range."))
        self.queueCheckbox.setText(_translate("ActionsWidget", "Add to New"))
        self.queueFromDropdown.setItemText(0, _translate("ActionsWidget", "Top"))
        self.queueFromDropdown.setItemText(1, _translate("ActionsWidget", "Bottom"))
        self.queueFromDropdown.setItemText(2, _translate("ActionsWidget", "Position"))
        self.queueTilda.setText(_translate("ActionsWidget", "～"))
        self.queueToDropdown.setItemText(0, _translate("ActionsWidget", "Top"))
        self.queueToDropdown.setItemText(1, _translate("ActionsWidget", "Bottom"))
        self.queueToDropdown.setItemText(2, _translate("ActionsWidget", "Position"))
        self.label_3.setText(_translate("ActionsWidget", "(Current)"))
        self.queueLabelTop.setText(_translate("ActionsWidget", "Top:"))
        self.queueLabelTopPos.setText(_translate("ActionsWidget", "0"))
        self.queueLabelBottom.setText(_translate("ActionsWidget", "Bottom:"))
        self.queueLabelBottomPos.setText(_translate("ActionsWidget", "0"))
        self.queueSimilarCheckbox.setToolTip(_translate("ActionsWidget", "Using the given range:\n"
                                                                         "Places the card near another one in the queue based on how similar they are."))
        self.queueSimilarCheckbox.setText(_translate("ActionsWidget", "Place near similar cards"))
        self.groupBox_4.setTitle(_translate("ActionsWidget", "Ignored Text"))
        self.groupBox_5.setTitle(_translate("ActionsWidget", "Filtered Fields"))
        self.queueIncludeFieldsCheckbox.setToolTip(
            _translate("ActionsWidget", "Filters to only match the following fields instead of filtering them out."))
        self.queueIncludeFieldsCheckbox.setText(_translate("ActionsWidget", "Inclusive"))
        self.queueExcludedFieldList.setSortingEnabled(True)
        self.queueAddFieldButton.setText(_translate("ActionsWidget", "Add"))
        self.queueSiblingCheckbox.setToolTip(_translate("ActionsWidget", "Using the given range:\n"
                                                                         "Place the card next to another one if they\'re each siblings of the same note-type."))
        self.queueSiblingCheckbox.setText(_translate("ActionsWidget", "Place near sibling cards"))
        self.editFieldsGroup.setTitle(_translate("ActionsWidget", "Fields"))
        self.editFieldsList.setSortingEnabled(True)
        self.editAddFieldButton.setText(_translate("ActionsWidget", "Add..."))
        self.label_4.setText(_translate("ActionsWidget", "Similarity"))
        self.queueRatioSlider.setToolTip(_translate("ActionsWidget",
                                                    "Controls how similar a card\'s fields must be for it to be considered \"similar\"."))


from .forms import ExpandoWidget, QueueSpinBox, TipSlider

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ActionsWidget = QtWidgets.QWidget()
    ui = Ui_ActionsWidget()
    ui.setupUi(ActionsWidget)
    ActionsWidget.show()
    sys.exit(app.exec_())
