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
        OptionsDialog.resize(416, 346)
        self.optionsLayout = QtWidgets.QVBoxLayout(OptionsDialog)
        self.optionsLayout.setObjectName("optionsLayout")
        self.OptionsScrollArea = QtWidgets.QScrollArea(OptionsDialog)
        self.OptionsScrollArea.setWidgetResizable(True)
        self.OptionsScrollArea.setObjectName("OptionsScrollArea")
        self.OptionsScrollWidget = QtWidgets.QWidget()
        self.OptionsScrollWidget.setObjectName("OptionsScrollWidget")
        self.optionsScrollLayout = QtWidgets.QVBoxLayout(self.OptionsScrollWidget)
        self.optionsScrollLayout.setObjectName("optionsScrollLayout")
        self.checkBox = QtWidgets.QCheckBox(self.OptionsScrollWidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.optionsScrollLayout.addWidget(self.checkBox)
        spacerItem = QtWidgets.QSpacerItem(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.optionsScrollLayout.addItem(spacerItem)
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
        self.checkBox.setText(_translate("OptionsDialog", "Show options in Tools menu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OptionsDialog = QtWidgets.QDialog()
    ui = Ui_OptionsDialog()
    ui.setupUi(OptionsDialog)
    OptionsDialog.show()
    sys.exit(app.exec_())
