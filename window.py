# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(871, 911)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableFIOmain = QtWidgets.QTableWidget(Form)
        self.tableFIOmain.setObjectName("tableFIOmain")
        self.tableFIOmain.setColumnCount(0)
        self.tableFIOmain.setRowCount(0)
        self.horizontalLayout_3.addWidget(self.tableFIOmain)
        self.textHistory = QtWidgets.QTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textHistory.sizePolicy().hasHeightForWidth())
        self.textHistory.setSizePolicy(sizePolicy)
        self.textHistory.setMinimumSize(QtCore.QSize(400, 0))
        self.textHistory.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textHistory.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textHistory.setObjectName("textHistory")
        self.horizontalLayout_3.addWidget(self.textHistory)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tableFirms = QtWidgets.QTableWidget(Form)
        self.tableFirms.setObjectName("tableFirms")
        self.tableFirms.setColumnCount(0)
        self.tableFirms.setRowCount(0)
        self.tableFirms.horizontalHeader().setDefaultSectionSize(1)
        self.tableFirms.horizontalHeader().setMinimumSectionSize(1)
        self.horizontalLayout_5.addWidget(self.tableFirms)
        self.textDescription = QtWidgets.QTextEdit(Form)
        self.textDescription.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textDescription.sizePolicy().hasHeightForWidth())
        self.textDescription.setSizePolicy(sizePolicy)
        self.textDescription.setMinimumSize(QtCore.QSize(0, 0))
        self.textDescription.setMaximumSize(QtCore.QSize(100, 16777215))
        self.textDescription.setBaseSize(QtCore.QSize(0, 0))
        self.textDescription.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textDescription.setObjectName("textDescription")
        self.horizontalLayout_5.addWidget(self.textDescription)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableFIO = QtWidgets.QTableWidget(Form)
        self.tableFIO.setObjectName("tableFIO")
        self.tableFIO.setColumnCount(0)
        self.tableFIO.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableFIO)
        self.tableOKWED = QtWidgets.QTableWidget(Form)
        self.tableOKWED.setObjectName("tableOKWED")
        self.tableOKWED.setColumnCount(0)
        self.tableOKWED.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableOKWED)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableFirm2gis = QtWidgets.QTableWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableFirm2gis.sizePolicy().hasHeightForWidth())
        self.tableFirm2gis.setSizePolicy(sizePolicy)
        self.tableFirm2gis.setObjectName("tableFirm2gis")
        self.tableFirm2gis.setColumnCount(0)
        self.tableFirm2gis.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.tableFirm2gis)
        self.tableContacts2gis = QtWidgets.QTableWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableContacts2gis.sizePolicy().hasHeightForWidth())
        self.tableContacts2gis.setSizePolicy(sizePolicy)
        self.tableContacts2gis.setMaximumSize(QtCore.QSize(300, 16777215))
        self.tableContacts2gis.setObjectName("tableContacts2gis")
        self.tableContacts2gis.setColumnCount(0)
        self.tableContacts2gis.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.tableContacts2gis)
        self.label_desc = QtWidgets.QLabel(Form)
        self.label_desc.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_desc.sizePolicy().hasHeightForWidth())
        self.label_desc.setSizePolicy(sizePolicy)
        self.label_desc.setMinimumSize(QtCore.QSize(0, 0))
        self.label_desc.setMaximumSize(QtCore.QSize(400, 16777215))
        self.label_desc.setLineWidth(1)
        self.label_desc.setObjectName("label_desc")
        self.horizontalLayout_2.addWidget(self.label_desc)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textHistory.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_desc.setText(_translate("Form", "Description"))
