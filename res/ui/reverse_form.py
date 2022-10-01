# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reverse_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ReverseForm(object):
    def setupUi(self, ReverseForm):
        ReverseForm.setObjectName("ReverseForm")
        ReverseForm.resize(319, 109)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ReverseForm.sizePolicy().hasHeightForWidth())
        ReverseForm.setSizePolicy(sizePolicy)
        ReverseForm.setMinimumSize(QtCore.QSize(128, 32))
        self.reverseLayout = QtWidgets.QVBoxLayout(ReverseForm)
        self.reverseLayout.setContentsMargins(0, 0, 0, 0)
        self.reverseLayout.setObjectName("reverseLayout")
        self.reverseGroup = QtWidgets.QGroupBox(ReverseForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverseGroup.sizePolicy().hasHeightForWidth())
        self.reverseGroup.setSizePolicy(sizePolicy)
        self.reverseGroup.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.reverseGroup.setCheckable(True)
        self.reverseGroup.setObjectName("reverseGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.reverseGroup)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.reverseThresholdLayout = QtWidgets.QHBoxLayout()
        self.reverseThresholdLayout.setContentsMargins(0, 0, 0, 0)
        self.reverseThresholdLayout.setObjectName("reverseThresholdLayout")
        self.reverseThresholdLabel = QtWidgets.QLabel(self.reverseGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reverseThresholdLabel.sizePolicy().hasHeightForWidth())
        self.reverseThresholdLabel.setSizePolicy(sizePolicy)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consSuffixLabel.sizePolicy().hasHeightForWidth())
        self.consSuffixLabel.setSizePolicy(sizePolicy)
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
        self.reverseLayout.addWidget(self.reverseGroup)

        self.retranslateUi(ReverseForm)
        QtCore.QMetaObject.connectSlotsByName(ReverseForm)

    def retranslateUi(self, ReverseForm):
        _translate = QtCore.QCoreApplication.translate
        self.reverseGroup.setToolTip(
            _translate("ReverseForm", "Reverse card lapses based on the number of correct review answers they have.")
        )
        self.reverseGroup.setTitle(_translate("ReverseForm", "Lapse Reverse"))
        self.reverseThresholdLabel.setText(_translate("ReverseForm", "Un-leech Threshold"))
        self.useLeechThresholdCheckbox.setToolTip(
            _translate(
                "ReverseForm", "Use the same threshold as the current leech threshold (Anki Default:\n"
                               "                                             8).\n"
                               "                                         "
            )
        )
        self.useLeechThresholdCheckbox.setText(_translate("ReverseForm", "Same as Leech Threshold"))
        self.reverseThresholdSpinbox.setToolTip(
            _translate("ReverseForm", "Un-leeches any cards with a lapse count below this value.")
        )
        self.consPrefixLabel.setText(_translate("ReverseForm", "Every"))
        self.consAnswerSpinbox.setToolTip(
            _translate("ReverseForm", "Number of correct (not again) answers in a row to consider a card reversed.")
        )
        self.consSuffixLabel.setText(_translate("ReverseForm", "correct answer(s) in a row:"))
        self.reverseMethodDropdown.setToolTip(_translate("ReverseForm", "Method for reversing a card\'s leech count."))
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
