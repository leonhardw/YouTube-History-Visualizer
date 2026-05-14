# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'visualizer_create_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(430, 180)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.browse_takeout_path_btn = QPushButton(Dialog)
        self.browse_takeout_path_btn.setObjectName(u"browse_takeout_path_btn")

        self.gridLayout.addWidget(self.browse_takeout_path_btn, 0, 2, 1, 1)

        self.browse_save_path_btn = QPushButton(Dialog)
        self.browse_save_path_btn.setObjectName(u"browse_save_path_btn")

        self.gridLayout.addWidget(self.browse_save_path_btn, 1, 2, 1, 1)

        self.takeout_file_label = QLabel(Dialog)
        self.takeout_file_label.setObjectName(u"takeout_file_label")

        self.gridLayout.addWidget(self.takeout_file_label, 0, 0, 1, 1)

        self.save_path_edit = QLineEdit(Dialog)
        self.save_path_edit.setObjectName(u"save_path_edit")

        self.gridLayout.addWidget(self.save_path_edit, 1, 1, 1, 1)

        self.takeout_file_edit = QLineEdit(Dialog)
        self.takeout_file_edit.setObjectName(u"takeout_file_edit")

        self.gridLayout.addWidget(self.takeout_file_edit, 0, 1, 1, 1)

        self.database_file_label = QLabel(Dialog)
        self.database_file_label.setObjectName(u"database_file_label")

        self.gridLayout.addWidget(self.database_file_label, 1, 0, 1, 1)

        self.metadata_box = QGroupBox(Dialog)
        self.metadata_box.setObjectName(u"metadata_box")
        sizePolicy.setHeightForWidth(self.metadata_box.sizePolicy().hasHeightForWidth())
        self.metadata_box.setSizePolicy(sizePolicy)
        self.metadata_box.setCheckable(True)
        self.metadata_box.setChecked(False)
        self.horizontalLayout = QHBoxLayout(self.metadata_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(self.metadata_box)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.apikey_edit = QLineEdit(self.metadata_box)
        self.apikey_edit.setObjectName(u"apikey_edit")

        self.horizontalLayout.addWidget(self.apikey_edit)


        self.gridLayout.addWidget(self.metadata_box, 2, 0, 1, 3)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.browse_takeout_path_btn.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.browse_save_path_btn.setText(QCoreApplication.translate("Dialog", u"Browse", None))
        self.takeout_file_label.setText(QCoreApplication.translate("Dialog", u"Path to Takeout file:", None))
        self.database_file_label.setText(QCoreApplication.translate("Dialog", u"Database path:", None))
        self.metadata_box.setTitle(QCoreApplication.translate("Dialog", u"Add metadata", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"API key:", None))
    # retranslateUi

