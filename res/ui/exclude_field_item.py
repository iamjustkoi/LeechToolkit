# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exclude_field_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ExcludedFieldItem(object):
    def setupUi(self, ExcludedFieldItem):
        ExcludedFieldItem.setObjectName("ExcludedFieldItem")
        ExcludedFieldItem.resize(115, 31)
        ExcludedFieldItem.setStyleSheet("#ExcudedFieldItem {\n"
"  transition: transform .3s ease-out;\n"
"}\n"
"\n"
"#ExcudedFieldItem:hover {\n"
"  transform: translate(10px, 15px);\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(ExcludedFieldItem)
        self.horizontalLayout.setContentsMargins(-1, 6, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fieldLabel = ElidingLabel(ExcludedFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fieldLabel.sizePolicy().hasHeightForWidth())
        self.fieldLabel.setSizePolicy(sizePolicy)
        self.fieldLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.fieldLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.fieldLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.fieldLabel.setObjectName("fieldLabel")
        self.horizontalLayout.addWidget(self.fieldLabel)
        self.removeButton = QtWidgets.QPushButton(ExcludedFieldItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy)
        self.removeButton.setStyleSheet(":active { border-style: outset;}\n"
"\n"
":hover {\n"
"    background-color:rgba(138, 138, 138, 0.314);\n"
"    border-radius: 2px;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/remove_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removeButton.setIcon(icon)
        self.removeButton.setFlat(True)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout.addWidget(self.removeButton)

        self.retranslateUi(ExcludedFieldItem)
        QtCore.QMetaObject.connectSlotsByName(ExcludedFieldItem)

    def retranslateUi(self, ExcludedFieldItem):
        _translate = QtCore.QCoreApplication.translate
        self.fieldLabel.setText(_translate("ExcludedFieldItem", "SampleText"))
from .forms import ElidingLabel


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExcludedFieldItem = QtWidgets.QWidget()
    ui = Ui_ExcludedFieldItem()
    ui.setupUi(ExcludedFieldItem)
    ExcludedFieldItem.show()
    sys.exit(app.exec_())
