# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reverse_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_ReverseForm(object):
    def setupUi(self, ReverseForm):
        ReverseForm.setObjectName("ReverseForm")
        ReverseForm.resize(389, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ReverseForm.sizePolicy().hasHeightForWidth())
        ReverseForm.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(ReverseForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.reverseGroup = QtWidgets.QGroupBox(ReverseForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverseGroup.sizePolicy().hasHeightForWidth())
        self.reverseGroup.setSizePolicy(sizePolicy)
        self.reverseGroup.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.reverseGroup.setObjectName("reverseGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.reverseGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.reverseCheckbox = QtWidgets.QCheckBox(self.reverseGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverseCheckbox.sizePolicy().hasHeightForWidth())
        self.reverseCheckbox.setSizePolicy(sizePolicy)
        self.reverseCheckbox.setChecked(True)
        self.reverseCheckbox.setObjectName("reverseCheckbox")
        self.verticalLayout_2.addWidget(self.reverseCheckbox)
        self.reverseThresholdLayout = QtWidgets.QHBoxLayout()
        self.reverseThresholdLayout.setObjectName("reverseThresholdLayout")
        self.reverseThresholdLabel = QtWidgets.QLabel(self.reverseGroup)
        self.reverseThresholdLabel.setObjectName("reverseThresholdLabel")
        self.reverseThresholdLayout.addWidget(self.reverseThresholdLabel)
        self.useLeechThresholdCheckbox = QtWidgets.QCheckBox(self.reverseGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.useLeechThresholdCheckbox.sizePolicy().hasHeightForWidth())
        self.useLeechThresholdCheckbox.setSizePolicy(sizePolicy)
        self.useLeechThresholdCheckbox.setObjectName("useLeechThresholdCheckbox")
        self.reverseThresholdLayout.addWidget(self.useLeechThresholdCheckbox)
        self.reverseThresholdSpinbox = QtWidgets.QSpinBox(self.reverseGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverseThresholdSpinbox.sizePolicy().hasHeightForWidth())
        self.reverseThresholdSpinbox.setSizePolicy(sizePolicy)
        self.reverseThresholdSpinbox.setMaximum(999)
        self.reverseThresholdSpinbox.setProperty("value", 4)
        self.reverseThresholdSpinbox.setObjectName("reverseThresholdSpinbox")
        self.reverseThresholdLayout.addWidget(self.reverseThresholdSpinbox)
        self.verticalLayout_2.addLayout(self.reverseThresholdLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.consPrefixLabel = QtWidgets.QLabel(self.reverseGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consPrefixLabel.sizePolicy().hasHeightForWidth())
        self.consPrefixLabel.setSizePolicy(sizePolicy)
        self.consPrefixLabel.setObjectName("consPrefixLabel")
        self.horizontalLayout.addWidget(self.consPrefixLabel)
        self.consAnswerSpinbox = QtWidgets.QSpinBox(self.reverseGroup)
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
        self.consSuffixLabel = QtWidgets.QLabel(self.reverseGroup)
        self.consSuffixLabel.setObjectName("consSuffixLabel")
        self.horizontalLayout.addWidget(self.consSuffixLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.reverseMethodDropdown = QtWidgets.QComboBox(self.reverseGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverseMethodDropdown.sizePolicy().hasHeightForWidth())
        self.reverseMethodDropdown.setSizePolicy(sizePolicy)
        self.reverseMethodDropdown.setObjectName("reverseMethodDropdown")
        self.reverseMethodDropdown.addItem("")
        self.reverseMethodDropdown.addItem("")
        self.verticalLayout_2.addWidget(self.reverseMethodDropdown)
        self.verticalLayout.addWidget(self.reverseGroup)

        self.retranslateUi(ReverseForm)
        QtCore.QMetaObject.connectSlotsByName(ReverseForm)

    def retranslateUi(self, ReverseForm):
        _translate = QtCore.QCoreApplication.translate
        ReverseForm.setWindowTitle(_translate("ReverseForm", "ReverseForm"))
        self.reverseGroup.setTitle(_translate("ReverseForm", "Leech Reverse"))
        self.reverseCheckbox.setText(_translate("ReverseForm", "Enable leech reversing"))
        self.reverseThresholdLabel.setText(_translate("ReverseForm", "Reverse Threshold"))
        self.useLeechThresholdCheckbox.setText(_translate("ReverseForm", "Same as Leech Threshold"))
        self.reverseThresholdSpinbox.setToolTip(
            _translate("ReverseForm", "Un-leeches any cards with a lapse count below this value."))
        self.consPrefixLabel.setText(_translate("ReverseForm", "Every"))
        self.consSuffixLabel.setText(_translate("ReverseForm", "correct answer(s) in a row:"))
        self.reverseMethodDropdown.setCurrentText(_translate("ReverseForm", "Decrease card\'s total lapse count"))
        self.reverseMethodDropdown.setItemText(0, _translate("ReverseForm", "Decrease card\'s total lapse count"))
        self.reverseMethodDropdown.setItemText(1, _translate("ReverseForm", "Reset card\'s total lapse count"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ReverseForm = QtWidgets.QWidget()
    ui = Ui_ReverseForm()
    ui.setupUi(ReverseForm)
    ReverseForm.show()
    sys.exit(app.exec_())
