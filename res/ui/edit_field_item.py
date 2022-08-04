# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_field_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FieldWidgetItem(object):
    def setupUi(self, FieldWidgetItem):
        FieldWidgetItem.setObjectName("FieldWidgetItem")
        FieldWidgetItem.resize(271, 67)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FieldWidgetItem)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(FieldWidgetItem)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.noteLabel = ElidingLabel(self.frame)
        self.noteLabel.setMinimumSize(QtCore.QSize(42, 0))
        self.noteLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.noteLabel.setObjectName("noteLabel")
        self.horizontalLayout_4.addWidget(self.noteLabel)
        self.fieldDropdown = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fieldDropdown.sizePolicy().hasHeightForWidth())
        self.fieldDropdown.setSizePolicy(sizePolicy)
        self.fieldDropdown.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.fieldDropdown.setObjectName("fieldDropdown")
        self.horizontalLayout_4.addWidget(self.fieldDropdown)
        self.horizontalLayout.addWidget(self.frame)
        self.methodDropdown = QtWidgets.QComboBox(FieldWidgetItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
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
        self.removeButton = QtWidgets.QPushButton(FieldWidgetItem)
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
        self.replaceEdit = QtWidgets.QLineEdit(FieldWidgetItem)
        self.replaceEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replaceEdit.sizePolicy().hasHeightForWidth())
        self.replaceEdit.setSizePolicy(sizePolicy)
        self.replaceEdit.setMinimumSize(QtCore.QSize(24, 24))
        self.replaceEdit.setObjectName("replaceEdit")
        self.horizontalLayout_2.addWidget(self.replaceEdit)
        self.inputEdit = QtWidgets.QLineEdit(FieldWidgetItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputEdit.sizePolicy().hasHeightForWidth())
        self.inputEdit.setSizePolicy(sizePolicy)
        self.inputEdit.setObjectName("inputEdit")
        self.horizontalLayout_2.addWidget(self.inputEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(FieldWidgetItem)
        QtCore.QMetaObject.connectSlotsByName(FieldWidgetItem)

    def retranslateUi(self, FieldWidgetItem):
        _translate = QtCore.QCoreApplication.translate
        self.methodDropdown.setItemText(0, _translate("FieldWidgetItem", "Append"))
        self.methodDropdown.setItemText(1, _translate("FieldWidgetItem", "Prepend"))
        self.methodDropdown.setItemText(2, _translate("FieldWidgetItem", "Replace"))
        self.methodDropdown.setItemText(3, _translate("FieldWidgetItem", "Replace (Regex)"))
        self.replaceEdit.setToolTip(_translate("FieldWidgetItem", "Text to search for and replace."))
        self.replaceEdit.setPlaceholderText(_translate("FieldWidgetItem", "Find"))
        self.inputEdit.setPlaceholderText(_translate("FieldWidgetItem", "Output"))
from .forms import ElidingLabel


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FieldWidgetItem = QtWidgets.QWidget()
    ui = Ui_FieldWidgetItem()
    ui.setupUi(FieldWidgetItem)
    FieldWidgetItem.show()
    sys.exit(app.exec_())
