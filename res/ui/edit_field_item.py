# Form implementation generated from reading ui file 'edit_field_item.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditFieldItem(object):
    def setupUi(self, EditFieldItem):
        EditFieldItem.setObjectName("EditFieldItem")
        EditFieldItem.resize(289, 67)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditFieldItem.sizePolicy().hasHeightForWidth())
        EditFieldItem.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(EditFieldItem)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fieldButtonLabel = QtWidgets.QToolButton(parent=EditFieldItem)
        self.fieldButtonLabel.setMinimumSize(QtCore.QSize(64, 24))
        self.fieldButtonLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WhatsThisCursor))
        self.fieldButtonLabel.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.fieldButtonLabel.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.fieldButtonLabel.setObjectName("fieldButtonLabel")
        self.horizontalLayout.addWidget(self.fieldButtonLabel)
        self.methodDropdown = QtWidgets.QComboBox(parent=EditFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.methodDropdown.sizePolicy().hasHeightForWidth())
        self.methodDropdown.setSizePolicy(sizePolicy)
        self.methodDropdown.setMinimumSize(QtCore.QSize(0, 0))
        self.methodDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.methodDropdown.setObjectName("methodDropdown")
        self.methodDropdown.addItem("")
        self.methodDropdown.addItem("")
        self.methodDropdown.addItem("")
        self.methodDropdown.addItem("")
        self.horizontalLayout.addWidget(self.methodDropdown)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.removeButton = QtWidgets.QPushButton(parent=EditFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy)
        self.removeButton.setStyleSheet(":active { border-style: outset;}\n"
"\n"
"                     :hover {\n"
"                     background-color:rgba(138, 138, 138, 0.314);\n"
"                     border-radius: 2px;\n"
"                     }\n"
"                 ")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/remove_icon.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.removeButton.setIcon(icon)
        self.removeButton.setFlat(True)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout.addWidget(self.removeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.replaceEdit = QtWidgets.QLineEdit(parent=EditFieldItem)
        self.replaceEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replaceEdit.sizePolicy().hasHeightForWidth())
        self.replaceEdit.setSizePolicy(sizePolicy)
        self.replaceEdit.setMinimumSize(QtCore.QSize(24, 24))
        self.replaceEdit.setObjectName("replaceEdit")
        self.horizontalLayout_2.addWidget(self.replaceEdit)
        self.inputEdit = QtWidgets.QLineEdit(parent=EditFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputEdit.sizePolicy().hasHeightForWidth())
        self.inputEdit.setSizePolicy(sizePolicy)
        self.inputEdit.setObjectName("inputEdit")
        self.horizontalLayout_2.addWidget(self.inputEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(EditFieldItem)
        QtCore.QMetaObject.connectSlotsByName(EditFieldItem)

    def retranslateUi(self, EditFieldItem):
        _translate = QtCore.QCoreApplication.translate
        self.fieldButtonLabel.setText(_translate("EditFieldItem", "sample sample sample"))
        self.methodDropdown.setItemText(0, _translate("EditFieldItem", "Append"))
        self.methodDropdown.setItemText(1, _translate("EditFieldItem", "Prepend"))
        self.methodDropdown.setItemText(2, _translate("EditFieldItem", "Replace"))
        self.methodDropdown.setItemText(3, _translate("EditFieldItem", "Replace (Regex)"))
        self.replaceEdit.setToolTip(_translate("EditFieldItem", "Text to search for and replace."))
        self.replaceEdit.setPlaceholderText(_translate("EditFieldItem", "Find"))
        self.inputEdit.setPlaceholderText(_translate("EditFieldItem", "Text"))
