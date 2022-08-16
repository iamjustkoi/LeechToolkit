# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_field_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditFieldItem(object):
    def setupUi(self, EditFieldItem):
        EditFieldItem.setObjectName("EditFieldItem")
        EditFieldItem.resize(271, 67)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditFieldItem.sizePolicy().hasHeightForWidth())
        EditFieldItem.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(EditFieldItem)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.noteLabel = ElidingLabel(EditFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteLabel.sizePolicy().hasHeightForWidth())
        self.noteLabel.setSizePolicy(sizePolicy)
        self.noteLabel.setMinimumSize(QtCore.QSize(42, 0))
        self.noteLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.noteLabel.setObjectName("noteLabel")
        self.horizontalLayout.addWidget(self.noteLabel)
        self.fieldDropdown = QtWidgets.QComboBox(EditFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fieldDropdown.sizePolicy().hasHeightForWidth())
        self.fieldDropdown.setSizePolicy(sizePolicy)
        self.fieldDropdown.setMaximumSize(QtCore.QSize(128, 16777215))
        self.fieldDropdown.setObjectName("fieldDropdown")
        self.horizontalLayout.addWidget(self.fieldDropdown)
        self.methodDropdown = QtWidgets.QComboBox(EditFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.methodDropdown.sizePolicy().hasHeightForWidth())
        self.methodDropdown.setSizePolicy(sizePolicy)
        self.methodDropdown.setMinimumSize(QtCore.QSize(0, 0))
        self.methodDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.methodDropdown.setObjectName("methodDropdown")
        self.methodDropdown.addItem("")
        self.methodDropdown.addItem("")
        self.methodDropdown.addItem("")
        self.methodDropdown.addItem("")
        self.horizontalLayout.addWidget(self.methodDropdown)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.removeButton = QtWidgets.QPushButton(EditFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy)
        self.removeButton.setStyleSheet(":active { border-style: outset;}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/remove_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setIcon(icon)
        self.removeButton.setFlat(True)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout.addWidget(self.removeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.replaceEdit = QtWidgets.QLineEdit(EditFieldItem)
        self.replaceEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replaceEdit.sizePolicy().hasHeightForWidth())
        self.replaceEdit.setSizePolicy(sizePolicy)
        self.replaceEdit.setMinimumSize(QtCore.QSize(24, 24))
        self.replaceEdit.setObjectName("replaceEdit")
        self.horizontalLayout_2.addWidget(self.replaceEdit)
        self.inputEdit = QtWidgets.QLineEdit(EditFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
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
        self.noteLabel.setText(_translate("EditFieldItem", "sample sample sample sample sample "))
        self.methodDropdown.setItemText(0, _translate("EditFieldItem", "Append"))
        self.methodDropdown.setItemText(1, _translate("EditFieldItem", "Prepend"))
        self.methodDropdown.setItemText(2, _translate("EditFieldItem", "Replace"))
        self.methodDropdown.setItemText(3, _translate("EditFieldItem", "Replace (Regex)"))
        self.replaceEdit.setToolTip(_translate("EditFieldItem", "Text to search for and replace."))
        self.replaceEdit.setPlaceholderText(_translate("EditFieldItem", "Find"))
        self.inputEdit.setPlaceholderText(_translate("EditFieldItem", "Text"))
from .forms import ElidingLabel


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditFieldItem = QtWidgets.QWidget()
    ui = Ui_EditFieldItem()
    ui.setupUi(EditFieldItem)
    EditFieldItem.show()
    sys.exit(app.exec_())
