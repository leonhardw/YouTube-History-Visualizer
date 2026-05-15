# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'visualizer.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

from ui.widgets.custom_widgets import StepTimeEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(478, 418)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionCreate_database = QAction(MainWindow)
        self.actionCreate_database.setObjectName(u"actionCreate_database")
        self.actionLoad_database = QAction(MainWindow)
        self.actionLoad_database.setObjectName(u"actionLoad_database")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.filters_tab = QWidget()
        self.filters_tab.setObjectName(u"filters_tab")
        self.verticalLayout_7 = QVBoxLayout(self.filters_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.loaded_file_label = QLabel(self.filters_tab)
        self.loaded_file_label.setObjectName(u"loaded_file_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loaded_file_label.sizePolicy().hasHeightForWidth())
        self.loaded_file_label.setSizePolicy(sizePolicy)

        self.verticalLayout_7.addWidget(self.loaded_file_label)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.create_db_btn = QPushButton(self.filters_tab)
        self.create_db_btn.setObjectName(u"create_db_btn")

        self.horizontalLayout_8.addWidget(self.create_db_btn)

        self.load_db_btn = QPushButton(self.filters_tab)
        self.load_db_btn.setObjectName(u"load_db_btn")

        self.horizontalLayout_8.addWidget(self.load_db_btn)

        self.manage_db_btn = QPushButton(self.filters_tab)
        self.manage_db_btn.setObjectName(u"manage_db_btn")

        self.horizontalLayout_8.addWidget(self.manage_db_btn)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.statistics_label = QLabel(self.filters_tab)
        self.statistics_label.setObjectName(u"statistics_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.statistics_label.sizePolicy().hasHeightForWidth())
        self.statistics_label.setSizePolicy(sizePolicy1)
        self.statistics_label.setMargin(5)

        self.verticalLayout_7.addWidget(self.statistics_label)

        self.groupBox = QGroupBox(self.filters_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.filters_list = QListWidget(self.groupBox)
        self.filters_list.setObjectName(u"filters_list")

        self.horizontalLayout_2.addWidget(self.filters_list)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.add_filter_btn = QPushButton(self.groupBox)
        self.add_filter_btn.setObjectName(u"add_filter_btn")

        self.verticalLayout.addWidget(self.add_filter_btn)

        self.edit_filter_btn = QPushButton(self.groupBox)
        self.edit_filter_btn.setObjectName(u"edit_filter_btn")

        self.verticalLayout.addWidget(self.edit_filter_btn)

        self.delete_filter_btn = QPushButton(self.groupBox)
        self.delete_filter_btn.setObjectName(u"delete_filter_btn")

        self.verticalLayout.addWidget(self.delete_filter_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_7.addWidget(self.groupBox)

        self.view_as_table_btn = QPushButton(self.filters_tab)
        self.view_as_table_btn.setObjectName(u"view_as_table_btn")

        self.verticalLayout_7.addWidget(self.view_as_table_btn)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.save_db_btn = QPushButton(self.filters_tab)
        self.save_db_btn.setObjectName(u"save_db_btn")

        self.horizontalLayout_9.addWidget(self.save_db_btn)

        self.export_as_csv_btn = QPushButton(self.filters_tab)
        self.export_as_csv_btn.setObjectName(u"export_as_csv_btn")

        self.horizontalLayout_9.addWidget(self.export_as_csv_btn)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.tabWidget.addTab(self.filters_tab, "")
        self.analysis_tab = QWidget()
        self.analysis_tab.setObjectName(u"analysis_tab")
        self.verticalLayout_3 = QVBoxLayout(self.analysis_tab)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(9, -1, -1, -1)
        self.plot_settings_box = QGroupBox(self.analysis_tab)
        self.plot_settings_box.setObjectName(u"plot_settings_box")
        sizePolicy.setHeightForWidth(self.plot_settings_box.sizePolicy().hasHeightForWidth())
        self.plot_settings_box.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.plot_settings_box)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 9, 9, 9)
        self.plot_mode_hbox = QHBoxLayout()
        self.plot_mode_hbox.setObjectName(u"plot_mode_hbox")
        self.label_13 = QLabel(self.plot_settings_box)
        self.label_13.setObjectName(u"label_13")

        self.plot_mode_hbox.addWidget(self.label_13)

        self.plot_watched_rb = QRadioButton(self.plot_settings_box)
        self.plot_mode_group = QButtonGroup(MainWindow)
        self.plot_mode_group.setObjectName(u"plot_mode_group")
        self.plot_mode_group.addButton(self.plot_watched_rb)
        self.plot_watched_rb.setObjectName(u"plot_watched_rb")

        self.plot_mode_hbox.addWidget(self.plot_watched_rb)

        self.plot_uploaded_rb = QRadioButton(self.plot_settings_box)
        self.plot_mode_group.addButton(self.plot_uploaded_rb)
        self.plot_uploaded_rb.setObjectName(u"plot_uploaded_rb")

        self.plot_mode_hbox.addWidget(self.plot_uploaded_rb)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.plot_mode_hbox.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addLayout(self.plot_mode_hbox)

        self.plot_settings_stack = QStackedWidget(self.plot_settings_box)
        self.plot_settings_stack.setObjectName(u"plot_settings_stack")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.plot_settings_stack.sizePolicy().hasHeightForWidth())
        self.plot_settings_stack.setSizePolicy(sizePolicy2)
        self.plot_settings_stack.setFrameShape(QFrame.Shape.NoFrame)
        self.threshold_page = QWidget()
        self.threshold_page.setObjectName(u"threshold_page")
        self.horizontalLayout_4 = QHBoxLayout(self.threshold_page)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.label = QLabel(self.threshold_page)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.threshold_spin = QSpinBox(self.threshold_page)
        self.threshold_spin.setObjectName(u"threshold_spin")
        self.threshold_spin.setMaximum(999999)

        self.horizontalLayout_4.addWidget(self.threshold_spin)

        self.exclude_other_cb = QCheckBox(self.threshold_page)
        self.exclude_other_cb.setObjectName(u"exclude_other_cb")

        self.horizontalLayout_4.addWidget(self.exclude_other_cb)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.plot_settings_stack.addWidget(self.threshold_page)
        self.year_page = QWidget()
        self.year_page.setObjectName(u"year_page")
        self.horizontalLayout_3 = QHBoxLayout(self.year_page)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.label_4 = QLabel(self.year_page)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.year_spin = QSpinBox(self.year_page)
        self.year_spin.setObjectName(u"year_spin")
        self.year_spin.setMinimum(2000)
        self.year_spin.setMaximum(2099)

        self.horizontalLayout_3.addWidget(self.year_spin)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.plot_settings_stack.addWidget(self.year_page)
        self.empty_page = QWidget()
        self.empty_page.setObjectName(u"empty_page")
        self.verticalLayout_4 = QVBoxLayout(self.empty_page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.label_2 = QLabel(self.empty_page)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_4.addWidget(self.label_2)

        self.plot_settings_stack.addWidget(self.empty_page)
        self.time_page = QWidget()
        self.time_page.setObjectName(u"time_page")
        self.horizontalLayout_6 = QHBoxLayout(self.time_page)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.label_10 = QLabel(self.time_page)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_6.addWidget(self.label_10)

        self.interval_combo = QComboBox(self.time_page)
        self.interval_combo.addItem("")
        self.interval_combo.addItem("")
        self.interval_combo.addItem("")
        self.interval_combo.addItem("")
        self.interval_combo.addItem("")
        self.interval_combo.addItem("")
        self.interval_combo.setObjectName(u"interval_combo")

        self.horizontalLayout_6.addWidget(self.interval_combo)

        self.label_11 = QLabel(self.time_page)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_6.addWidget(self.label_11)

        self.start_time_edit = StepTimeEdit(self.time_page)
        self.start_time_edit.setObjectName(u"start_time_edit")

        self.horizontalLayout_6.addWidget(self.start_time_edit)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.plot_settings_stack.addWidget(self.time_page)

        self.verticalLayout_6.addWidget(self.plot_settings_stack)


        self.verticalLayout_3.addWidget(self.plot_settings_box)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.generate_plot_btn = QPushButton(self.analysis_tab)
        self.generate_plot_btn.setObjectName(u"generate_plot_btn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.generate_plot_btn.sizePolicy().hasHeightForWidth())
        self.generate_plot_btn.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.generate_plot_btn)

        self.export_plot_btn = QPushButton(self.analysis_tab)
        self.export_plot_btn.setObjectName(u"export_plot_btn")
        sizePolicy3.setHeightForWidth(self.export_plot_btn.sizePolicy().hasHeightForWidth())
        self.export_plot_btn.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.export_plot_btn)

        self.view_plot_data_as_table_btn = QPushButton(self.analysis_tab)
        self.view_plot_data_as_table_btn.setObjectName(u"view_plot_data_as_table_btn")

        self.horizontalLayout_5.addWidget(self.view_plot_data_as_table_btn)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.tabWidget.addTab(self.analysis_tab, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 478, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.add_filter_btn, self.edit_filter_btn)
        QWidget.setTabOrder(self.edit_filter_btn, self.delete_filter_btn)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionCreate_database)
        self.menuFile.addAction(self.actionLoad_database)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)
        self.plot_settings_stack.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionCreate_database.setText(QCoreApplication.translate("MainWindow", u"Create database", None))
        self.actionLoad_database.setText(QCoreApplication.translate("MainWindow", u"Load database", None))
        self.loaded_file_label.setText(QCoreApplication.translate("MainWindow", u"Loaded file:", None))
        self.create_db_btn.setText(QCoreApplication.translate("MainWindow", u"Create database from Takeout", None))
        self.load_db_btn.setText(QCoreApplication.translate("MainWindow", u"Load database", None))
        self.manage_db_btn.setText(QCoreApplication.translate("MainWindow", u"Manage database", None))
        self.statistics_label.setText(QCoreApplication.translate("MainWindow", u"Statistics", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Filters", None))
        self.add_filter_btn.setText(QCoreApplication.translate("MainWindow", u"Add filter", None))
        self.edit_filter_btn.setText(QCoreApplication.translate("MainWindow", u"Edit filter", None))
        self.delete_filter_btn.setText(QCoreApplication.translate("MainWindow", u"Delete filter", None))
        self.view_as_table_btn.setText(QCoreApplication.translate("MainWindow", u"View as table", None))
        self.save_db_btn.setText(QCoreApplication.translate("MainWindow", u"Save with current filters", None))
        self.export_as_csv_btn.setText(QCoreApplication.translate("MainWindow", u"Export as CSV", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.filters_tab), QCoreApplication.translate("MainWindow", u"Data and Filters", None))
        self.plot_settings_box.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Mode:", None))
        self.plot_watched_rb.setText(QCoreApplication.translate("MainWindow", u"Watched", None))
        self.plot_uploaded_rb.setText(QCoreApplication.translate("MainWindow", u"Uploaded", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Threshold for \"Other\":", None))
        self.exclude_other_cb.setText(QCoreApplication.translate("MainWindow", u"Exclude \"Other\"", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Year:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"No settings for selected plot available.", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Interval:", None))
        self.interval_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"5 Minutes", None))
        self.interval_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"10 Minutes", None))
        self.interval_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"15 Minutes", None))
        self.interval_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"20 Minutes", None))
        self.interval_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"30 Minutes", None))
        self.interval_combo.setItemText(5, QCoreApplication.translate("MainWindow", u"60 Minutes", None))

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Start time:", None))
        self.generate_plot_btn.setText(QCoreApplication.translate("MainWindow", u"Generate plot", None))
        self.export_plot_btn.setText(QCoreApplication.translate("MainWindow", u"Export plot as PNG", None))
        self.view_plot_data_as_table_btn.setText(QCoreApplication.translate("MainWindow", u"View data as table", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analysis_tab), QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

