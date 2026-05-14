# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'visualizer_filter.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QCheckBox,
    QComboBox, QDateEdit, QDateTimeEdit, QDialog,
    QDialogButtonBox, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTimeEdit, QVBoxLayout, QWidget)

from ui.widgets.custom_widgets import IntegerOnlyDoubleSpinBox

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(660, 521)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.property_filters_tab = QWidget()
        self.property_filters_tab.setObjectName(u"property_filters_tab")
        self.verticalLayout_5 = QVBoxLayout(self.property_filters_tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.properties_grid = QGridLayout()
        self.properties_grid.setObjectName(u"properties_grid")
        self.properties_grid.setHorizontalSpacing(6)
        self.properties_grid.setContentsMargins(0, -1, -1, -1)
        self.channel_combo = QComboBox(self.property_filters_tab)
        self.channel_combo.addItem("")
        self.channel_combo.addItem("")
        self.channel_combo.setObjectName(u"channel_combo")

        self.properties_grid.addWidget(self.channel_combo, 1, 1, 1, 1)

        self.views_cb = QCheckBox(self.property_filters_tab)
        self.views_cb.setObjectName(u"views_cb")

        self.properties_grid.addWidget(self.views_cb, 2, 0, 1, 1)

        self.channel_cb = QCheckBox(self.property_filters_tab)
        self.channel_cb.setObjectName(u"channel_cb")

        self.properties_grid.addWidget(self.channel_cb, 1, 0, 1, 1)

        self.userviews_combo = QComboBox(self.property_filters_tab)
        self.userviews_combo.addItem("")
        self.userviews_combo.addItem("")
        self.userviews_combo.setObjectName(u"userviews_combo")

        self.properties_grid.addWidget(self.userviews_combo, 3, 1, 1, 1)

        self.duration_max = QTimeEdit(self.property_filters_tab)
        self.duration_max.setObjectName(u"duration_max")
        self.duration_max.setProperty(u"showGroupSeparator", True)
        self.duration_max.setCurrentSection(QDateTimeEdit.Section.HourSection)

        self.properties_grid.addWidget(self.duration_max, 6, 4, 1, 1)

        self.label_3 = QLabel(self.property_filters_tab)
        self.label_3.setObjectName(u"label_3")

        self.properties_grid.addWidget(self.label_3, 8, 0, 1, 1)

        self.duration_cb = QCheckBox(self.property_filters_tab)
        self.duration_cb.setObjectName(u"duration_cb")

        self.properties_grid.addWidget(self.duration_cb, 6, 0, 1, 1)

        self.userviews_max = QSpinBox(self.property_filters_tab)
        self.userviews_max.setObjectName(u"userviews_max")
        self.userviews_max.setProperty(u"showGroupSeparator", True)
        self.userviews_max.setMaximum(100000)

        self.properties_grid.addWidget(self.userviews_max, 3, 4, 1, 1)

        self.availability_hbox = QHBoxLayout()
        self.availability_hbox.setObjectName(u"availability_hbox")
        self.available_rb = QRadioButton(self.property_filters_tab)
        self.availability_group = QButtonGroup(Dialog)
        self.availability_group.setObjectName(u"availability_group")
        self.availability_group.addButton(self.available_rb)
        self.available_rb.setObjectName(u"available_rb")
        self.available_rb.setChecked(True)

        self.availability_hbox.addWidget(self.available_rb)

        self.deleted_rb = QRadioButton(self.property_filters_tab)
        self.availability_group.addButton(self.deleted_rb)
        self.deleted_rb.setObjectName(u"deleted_rb")

        self.availability_hbox.addWidget(self.deleted_rb)

        self.availability_both_rb = QRadioButton(self.property_filters_tab)
        self.availability_group.addButton(self.availability_both_rb)
        self.availability_both_rb.setObjectName(u"availability_both_rb")

        self.availability_hbox.addWidget(self.availability_both_rb)


        self.properties_grid.addLayout(self.availability_hbox, 8, 1, 1, 4)

        self.views_max = IntegerOnlyDoubleSpinBox(self.property_filters_tab)
        self.views_max.setObjectName(u"views_max")
        self.views_max.setProperty(u"showGroupSeparator", True)
        self.views_max.setDecimals(0)
        self.views_max.setMaximum(30000000000.000000000000000)
        self.views_max.setSingleStep(1000.000000000000000)

        self.properties_grid.addWidget(self.views_max, 2, 4, 1, 1)

        self.userviews_cb = QCheckBox(self.property_filters_tab)
        self.userviews_cb.setObjectName(u"userviews_cb")

        self.properties_grid.addWidget(self.userviews_cb, 3, 0, 1, 1)

        self.platform_hbox = QHBoxLayout()
        self.platform_hbox.setObjectName(u"platform_hbox")
        self.youtube_rb = QRadioButton(self.property_filters_tab)
        self.platform_group = QButtonGroup(Dialog)
        self.platform_group.setObjectName(u"platform_group")
        self.platform_group.addButton(self.youtube_rb)
        self.youtube_rb.setObjectName(u"youtube_rb")
        self.youtube_rb.setChecked(True)

        self.platform_hbox.addWidget(self.youtube_rb)

        self.music_rb = QRadioButton(self.property_filters_tab)
        self.platform_group.addButton(self.music_rb)
        self.music_rb.setObjectName(u"music_rb")

        self.platform_hbox.addWidget(self.music_rb)

        self.platform_both_rb = QRadioButton(self.property_filters_tab)
        self.platform_group.addButton(self.platform_both_rb)
        self.platform_both_rb.setObjectName(u"platform_both_rb")

        self.platform_hbox.addWidget(self.platform_both_rb)


        self.properties_grid.addLayout(self.platform_hbox, 7, 1, 1, 4)

        self.languages_cb = QCheckBox(self.property_filters_tab)
        self.languages_cb.setObjectName(u"languages_cb")

        self.properties_grid.addWidget(self.languages_cb, 5, 0, 1, 1)

        self.userviews_channel_cb = QCheckBox(self.property_filters_tab)
        self.userviews_channel_cb.setObjectName(u"userviews_channel_cb")

        self.properties_grid.addWidget(self.userviews_channel_cb, 4, 0, 1, 1)

        self.languages_combo = QComboBox(self.property_filters_tab)
        self.languages_combo.addItem("")
        self.languages_combo.addItem("")
        self.languages_combo.setObjectName(u"languages_combo")

        self.properties_grid.addWidget(self.languages_combo, 5, 1, 1, 1)

        self.title_cb = QCheckBox(self.property_filters_tab)
        self.title_cb.setObjectName(u"title_cb")

        self.properties_grid.addWidget(self.title_cb, 0, 0, 1, 1)

        self.label = QLabel(self.property_filters_tab)
        self.label.setObjectName(u"label")

        self.properties_grid.addWidget(self.label, 7, 0, 1, 1)

        self.duration_combo = QComboBox(self.property_filters_tab)
        self.duration_combo.addItem("")
        self.duration_combo.addItem("")
        self.duration_combo.setObjectName(u"duration_combo")

        self.properties_grid.addWidget(self.duration_combo, 6, 1, 1, 1)

        self.views_combo = QComboBox(self.property_filters_tab)
        self.views_combo.addItem("")
        self.views_combo.addItem("")
        self.views_combo.setObjectName(u"views_combo")

        self.properties_grid.addWidget(self.views_combo, 2, 1, 1, 1)

        self.userviews_channel_combo = QComboBox(self.property_filters_tab)
        self.userviews_channel_combo.addItem("")
        self.userviews_channel_combo.addItem("")
        self.userviews_channel_combo.setObjectName(u"userviews_channel_combo")

        self.properties_grid.addWidget(self.userviews_channel_combo, 4, 1, 1, 1)

        self.title_combo = QComboBox(self.property_filters_tab)
        self.title_combo.addItem("")
        self.title_combo.addItem("")
        self.title_combo.setObjectName(u"title_combo")

        self.properties_grid.addWidget(self.title_combo, 0, 1, 1, 1)

        self.userviews_channel_max = QSpinBox(self.property_filters_tab)
        self.userviews_channel_max.setObjectName(u"userviews_channel_max")
        self.userviews_channel_max.setProperty(u"showGroupSeparator", True)
        self.userviews_channel_max.setMaximum(100000)

        self.properties_grid.addWidget(self.userviews_channel_max, 4, 4, 1, 1)

        self.views_min = IntegerOnlyDoubleSpinBox(self.property_filters_tab)
        self.views_min.setObjectName(u"views_min")
        self.views_min.setProperty(u"showGroupSeparator", True)
        self.views_min.setDecimals(0)
        self.views_min.setMaximum(30000000000.000000000000000)
        self.views_min.setSingleStep(1000.000000000000000)

        self.properties_grid.addWidget(self.views_min, 2, 2, 1, 1)

        self.userviews_min = QSpinBox(self.property_filters_tab)
        self.userviews_min.setObjectName(u"userviews_min")
        self.userviews_min.setProperty(u"showGroupSeparator", True)
        self.userviews_min.setMaximum(100000)

        self.properties_grid.addWidget(self.userviews_min, 3, 2, 1, 1)

        self.userviews_channel_min = QSpinBox(self.property_filters_tab)
        self.userviews_channel_min.setObjectName(u"userviews_channel_min")
        self.userviews_channel_min.setProperty(u"showGroupSeparator", True)
        self.userviews_channel_min.setMaximum(100000)

        self.properties_grid.addWidget(self.userviews_channel_min, 4, 2, 1, 1)

        self.duration_min = QTimeEdit(self.property_filters_tab)
        self.duration_min.setObjectName(u"duration_min")
        self.duration_min.setInputMethodHints(Qt.InputMethodHint.ImhPreferNumbers)
        self.duration_min.setProperty(u"showGroupSeparator", True)
        self.duration_min.setCurrentSection(QDateTimeEdit.Section.HourSection)

        self.properties_grid.addWidget(self.duration_min, 6, 2, 1, 1)

        self.label_4 = QLabel(self.property_filters_tab)
        self.label_4.setObjectName(u"label_4")

        self.properties_grid.addWidget(self.label_4, 2, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.label_5 = QLabel(self.property_filters_tab)
        self.label_5.setObjectName(u"label_5")

        self.properties_grid.addWidget(self.label_5, 3, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.label_6 = QLabel(self.property_filters_tab)
        self.label_6.setObjectName(u"label_6")

        self.properties_grid.addWidget(self.label_6, 4, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.label_7 = QLabel(self.property_filters_tab)
        self.label_7.setObjectName(u"label_7")

        self.properties_grid.addWidget(self.label_7, 6, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.languages_edit = QLineEdit(self.property_filters_tab)
        self.languages_edit.setObjectName(u"languages_edit")

        self.properties_grid.addWidget(self.languages_edit, 5, 2, 1, 3)

        self.channel_hbox = QHBoxLayout()
        self.channel_hbox.setObjectName(u"channel_hbox")
        self.channel_regex_cb = QCheckBox(self.property_filters_tab)
        self.channel_regex_cb.setObjectName(u"channel_regex_cb")

        self.channel_hbox.addWidget(self.channel_regex_cb)

        self.channel_edit = QLineEdit(self.property_filters_tab)
        self.channel_edit.setObjectName(u"channel_edit")

        self.channel_hbox.addWidget(self.channel_edit)


        self.properties_grid.addLayout(self.channel_hbox, 1, 2, 1, 3)

        self.title_hbox = QHBoxLayout()
        self.title_hbox.setObjectName(u"title_hbox")
        self.title_regex_cb = QCheckBox(self.property_filters_tab)
        self.title_regex_cb.setObjectName(u"title_regex_cb")

        self.title_hbox.addWidget(self.title_regex_cb)

        self.title_edit = QLineEdit(self.property_filters_tab)
        self.title_edit.setObjectName(u"title_edit")

        self.title_hbox.addWidget(self.title_edit)


        self.properties_grid.addLayout(self.title_hbox, 0, 2, 1, 3)


        self.verticalLayout_5.addLayout(self.properties_grid)

        self.tabWidget.addTab(self.property_filters_tab, "")
        self.watched_filters_tab = QWidget()
        self.watched_filters_tab.setObjectName(u"watched_filters_tab")
        self.verticalLayout_4 = QVBoxLayout(self.watched_filters_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.date_watched_box = QGroupBox(self.watched_filters_tab)
        self.date_watched_box.setObjectName(u"date_watched_box")
        self.date_watched_box.setCheckable(True)
        self.date_watched_box.setChecked(False)
        self.verticalLayout = QVBoxLayout(self.date_watched_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.date_watched_date_hbox = QHBoxLayout()
        self.date_watched_date_hbox.setObjectName(u"date_watched_date_hbox")
        self.label_2 = QLabel(self.date_watched_box)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.date_watched_date_hbox.addWidget(self.label_2)

        self.date_watched_set_oldest_btn = QPushButton(self.date_watched_box)
        self.date_watched_set_oldest_btn.setObjectName(u"date_watched_set_oldest_btn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.date_watched_set_oldest_btn.sizePolicy().hasHeightForWidth())
        self.date_watched_set_oldest_btn.setSizePolicy(sizePolicy1)

        self.date_watched_date_hbox.addWidget(self.date_watched_set_oldest_btn)

        self.date_watched_from = QDateEdit(self.date_watched_box)
        self.date_watched_from.setObjectName(u"date_watched_from")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.date_watched_from.sizePolicy().hasHeightForWidth())
        self.date_watched_from.setSizePolicy(sizePolicy2)
        self.date_watched_from.setCalendarPopup(True)

        self.date_watched_date_hbox.addWidget(self.date_watched_from)

        self.label_8 = QLabel(self.date_watched_box)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)

        self.date_watched_date_hbox.addWidget(self.label_8)

        self.date_watched_to = QDateEdit(self.date_watched_box)
        self.date_watched_to.setObjectName(u"date_watched_to")
        sizePolicy2.setHeightForWidth(self.date_watched_to.sizePolicy().hasHeightForWidth())
        self.date_watched_to.setSizePolicy(sizePolicy2)
        self.date_watched_to.setCalendarPopup(True)

        self.date_watched_date_hbox.addWidget(self.date_watched_to)

        self.date_watched_set_newest_btn = QPushButton(self.date_watched_box)
        self.date_watched_set_newest_btn.setObjectName(u"date_watched_set_newest_btn")
        sizePolicy1.setHeightForWidth(self.date_watched_set_newest_btn.sizePolicy().hasHeightForWidth())
        self.date_watched_set_newest_btn.setSizePolicy(sizePolicy1)

        self.date_watched_date_hbox.addWidget(self.date_watched_set_newest_btn)


        self.verticalLayout.addLayout(self.date_watched_date_hbox)

        self.date_watched_mode_hbox = QHBoxLayout()
        self.date_watched_mode_hbox.setObjectName(u"date_watched_mode_hbox")
        self.date_watched_include_rb = QRadioButton(self.date_watched_box)
        self.include_date_watched_group = QButtonGroup(Dialog)
        self.include_date_watched_group.setObjectName(u"include_date_watched_group")
        self.include_date_watched_group.addButton(self.date_watched_include_rb)
        self.date_watched_include_rb.setObjectName(u"date_watched_include_rb")
        self.date_watched_include_rb.setChecked(True)

        self.date_watched_mode_hbox.addWidget(self.date_watched_include_rb)

        self.date_watched_exclude_rb = QRadioButton(self.date_watched_box)
        self.include_date_watched_group.addButton(self.date_watched_exclude_rb)
        self.date_watched_exclude_rb.setObjectName(u"date_watched_exclude_rb")

        self.date_watched_mode_hbox.addWidget(self.date_watched_exclude_rb)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.date_watched_mode_hbox.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.date_watched_mode_hbox)


        self.verticalLayout_4.addWidget(self.date_watched_box)

        self.time_watched_box = QGroupBox(self.watched_filters_tab)
        self.time_watched_box.setObjectName(u"time_watched_box")
        self.time_watched_box.setCheckable(True)
        self.time_watched_box.setChecked(False)
        self.verticalLayout_8 = QVBoxLayout(self.time_watched_box)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_10 = QLabel(self.time_watched_box)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_10)

        self.watched_time_range_min_btn = QPushButton(self.time_watched_box)
        self.watched_time_range_min_btn.setObjectName(u"watched_time_range_min_btn")
        sizePolicy1.setHeightForWidth(self.watched_time_range_min_btn.sizePolicy().hasHeightForWidth())
        self.watched_time_range_min_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.watched_time_range_min_btn)

        self.watched_time_range_min_edit = QTimeEdit(self.time_watched_box)
        self.watched_time_range_min_edit.setObjectName(u"watched_time_range_min_edit")

        self.horizontalLayout_2.addWidget(self.watched_time_range_min_edit)

        self.label_12 = QLabel(self.time_watched_box)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_12)

        self.watched_time_range_max_edit = QTimeEdit(self.time_watched_box)
        self.watched_time_range_max_edit.setObjectName(u"watched_time_range_max_edit")

        self.horizontalLayout_2.addWidget(self.watched_time_range_max_edit)

        self.watched_time_range_max_btn = QPushButton(self.time_watched_box)
        self.watched_time_range_max_btn.setObjectName(u"watched_time_range_max_btn")
        sizePolicy1.setHeightForWidth(self.watched_time_range_max_btn.sizePolicy().hasHeightForWidth())
        self.watched_time_range_max_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.watched_time_range_max_btn)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.watched_time_range_include_rb = QRadioButton(self.time_watched_box)
        self.include_time_watched_group = QButtonGroup(Dialog)
        self.include_time_watched_group.setObjectName(u"include_time_watched_group")
        self.include_time_watched_group.addButton(self.watched_time_range_include_rb)
        self.watched_time_range_include_rb.setObjectName(u"watched_time_range_include_rb")

        self.horizontalLayout_9.addWidget(self.watched_time_range_include_rb)

        self.watched_time_range_exclude_rb = QRadioButton(self.time_watched_box)
        self.include_time_watched_group.addButton(self.watched_time_range_exclude_rb)
        self.watched_time_range_exclude_rb.setObjectName(u"watched_time_range_exclude_rb")

        self.horizontalLayout_9.addWidget(self.watched_time_range_exclude_rb)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_9)


        self.verticalLayout_4.addWidget(self.time_watched_box)

        self.days_of_month_watched_box = QGroupBox(self.watched_filters_tab)
        self.days_of_month_watched_box.setObjectName(u"days_of_month_watched_box")
        self.days_of_month_watched_box.setCheckable(True)
        self.days_of_month_watched_box.setChecked(False)
        self.horizontalLayout_4 = QHBoxLayout(self.days_of_month_watched_box)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.days_of_month_watched_edit = QLineEdit(self.days_of_month_watched_box)
        self.days_of_month_watched_edit.setObjectName(u"days_of_month_watched_edit")

        self.horizontalLayout_4.addWidget(self.days_of_month_watched_edit)


        self.verticalLayout_4.addWidget(self.days_of_month_watched_box)

        self.months_watched_box = QGroupBox(self.watched_filters_tab)
        self.months_watched_box.setObjectName(u"months_watched_box")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.months_watched_box.sizePolicy().hasHeightForWidth())
        self.months_watched_box.setSizePolicy(sizePolicy3)
        self.months_watched_box.setCheckable(True)
        self.months_watched_box.setChecked(False)
        self.horizontalLayout_5 = QHBoxLayout(self.months_watched_box)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.months_watched_edit = QLineEdit(self.months_watched_box)
        self.months_watched_edit.setObjectName(u"months_watched_edit")

        self.horizontalLayout_5.addWidget(self.months_watched_edit)


        self.verticalLayout_4.addWidget(self.months_watched_box)

        self.weekdays_watched_box = QGroupBox(self.watched_filters_tab)
        self.weekdays_watched_box.setObjectName(u"weekdays_watched_box")
        self.weekdays_watched_box.setCheckable(True)
        self.weekdays_watched_box.setChecked(False)
        self.horizontalLayout_3 = QHBoxLayout(self.weekdays_watched_box)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.weekdays_watched_mon = QCheckBox(self.weekdays_watched_box)
        self.weekdays_watched_mon.setObjectName(u"weekdays_watched_mon")
        self.weekdays_watched_mon.setChecked(True)

        self.horizontalLayout_3.addWidget(self.weekdays_watched_mon)

        self.weekdays_watched_tue = QCheckBox(self.weekdays_watched_box)
        self.weekdays_watched_tue.setObjectName(u"weekdays_watched_tue")
        self.weekdays_watched_tue.setChecked(True)

        self.horizontalLayout_3.addWidget(self.weekdays_watched_tue)

        self.weekdays_watched_wed = QCheckBox(self.weekdays_watched_box)
        self.weekdays_watched_wed.setObjectName(u"weekdays_watched_wed")
        self.weekdays_watched_wed.setChecked(True)

        self.horizontalLayout_3.addWidget(self.weekdays_watched_wed)

        self.weekdays_watched_thu = QCheckBox(self.weekdays_watched_box)
        self.weekdays_watched_thu.setObjectName(u"weekdays_watched_thu")
        self.weekdays_watched_thu.setChecked(True)

        self.horizontalLayout_3.addWidget(self.weekdays_watched_thu)

        self.weekdays_watched_fri = QCheckBox(self.weekdays_watched_box)
        self.weekdays_watched_fri.setObjectName(u"weekdays_watched_fri")
        self.weekdays_watched_fri.setChecked(True)

        self.horizontalLayout_3.addWidget(self.weekdays_watched_fri)

        self.weekdays_watched_sat = QCheckBox(self.weekdays_watched_box)
        self.weekdays_watched_sat.setObjectName(u"weekdays_watched_sat")
        self.weekdays_watched_sat.setChecked(True)

        self.horizontalLayout_3.addWidget(self.weekdays_watched_sat)

        self.weekdays_watched_sun = QCheckBox(self.weekdays_watched_box)
        self.weekdays_watched_sun.setObjectName(u"weekdays_watched_sun")
        self.weekdays_watched_sun.setChecked(True)

        self.horizontalLayout_3.addWidget(self.weekdays_watched_sun)


        self.verticalLayout_4.addWidget(self.weekdays_watched_box)

        self.tabWidget.addTab(self.watched_filters_tab, "")
        self.uploaded_filters_tab = QWidget()
        self.uploaded_filters_tab.setObjectName(u"uploaded_filters_tab")
        self.verticalLayout_7 = QVBoxLayout(self.uploaded_filters_tab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.date_uploaded_box = QGroupBox(self.uploaded_filters_tab)
        self.date_uploaded_box.setObjectName(u"date_uploaded_box")
        self.date_uploaded_box.setCheckable(True)
        self.date_uploaded_box.setChecked(False)
        self.verticalLayout_6 = QVBoxLayout(self.date_uploaded_box)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.date_uploaded_date_hbox = QHBoxLayout()
        self.date_uploaded_date_hbox.setObjectName(u"date_uploaded_date_hbox")
        self.label_11 = QLabel(self.date_uploaded_box)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)

        self.date_uploaded_date_hbox.addWidget(self.label_11)

        self.date_uploaded_set_oldest_btn = QPushButton(self.date_uploaded_box)
        self.date_uploaded_set_oldest_btn.setObjectName(u"date_uploaded_set_oldest_btn")
        sizePolicy1.setHeightForWidth(self.date_uploaded_set_oldest_btn.sizePolicy().hasHeightForWidth())
        self.date_uploaded_set_oldest_btn.setSizePolicy(sizePolicy1)

        self.date_uploaded_date_hbox.addWidget(self.date_uploaded_set_oldest_btn)

        self.date_uploaded_from = QDateEdit(self.date_uploaded_box)
        self.date_uploaded_from.setObjectName(u"date_uploaded_from")
        self.date_uploaded_from.setCalendarPopup(True)

        self.date_uploaded_date_hbox.addWidget(self.date_uploaded_from)

        self.label_9 = QLabel(self.date_uploaded_box)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)

        self.date_uploaded_date_hbox.addWidget(self.label_9)

        self.date_uploaded_to = QDateEdit(self.date_uploaded_box)
        self.date_uploaded_to.setObjectName(u"date_uploaded_to")
        self.date_uploaded_to.setCalendarPopup(True)

        self.date_uploaded_date_hbox.addWidget(self.date_uploaded_to)

        self.date_uploaded_set_newest_btn = QPushButton(self.date_uploaded_box)
        self.date_uploaded_set_newest_btn.setObjectName(u"date_uploaded_set_newest_btn")
        sizePolicy1.setHeightForWidth(self.date_uploaded_set_newest_btn.sizePolicy().hasHeightForWidth())
        self.date_uploaded_set_newest_btn.setSizePolicy(sizePolicy1)

        self.date_uploaded_date_hbox.addWidget(self.date_uploaded_set_newest_btn)


        self.verticalLayout_6.addLayout(self.date_uploaded_date_hbox)

        self.date_uploaded_mode_hbox = QHBoxLayout()
        self.date_uploaded_mode_hbox.setObjectName(u"date_uploaded_mode_hbox")
        self.date_uploaded_include_rb = QRadioButton(self.date_uploaded_box)
        self.include_date_uploaded_group = QButtonGroup(Dialog)
        self.include_date_uploaded_group.setObjectName(u"include_date_uploaded_group")
        self.include_date_uploaded_group.addButton(self.date_uploaded_include_rb)
        self.date_uploaded_include_rb.setObjectName(u"date_uploaded_include_rb")
        self.date_uploaded_include_rb.setChecked(True)

        self.date_uploaded_mode_hbox.addWidget(self.date_uploaded_include_rb)

        self.date_uploaded_exclude_rb = QRadioButton(self.date_uploaded_box)
        self.include_date_uploaded_group.addButton(self.date_uploaded_exclude_rb)
        self.date_uploaded_exclude_rb.setObjectName(u"date_uploaded_exclude_rb")

        self.date_uploaded_mode_hbox.addWidget(self.date_uploaded_exclude_rb)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.date_uploaded_mode_hbox.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.date_uploaded_mode_hbox)


        self.verticalLayout_7.addWidget(self.date_uploaded_box)

        self.time_uploaded_box = QGroupBox(self.uploaded_filters_tab)
        self.time_uploaded_box.setObjectName(u"time_uploaded_box")
        self.time_uploaded_box.setCheckable(True)
        self.time_uploaded_box.setChecked(False)
        self.verticalLayout_9 = QVBoxLayout(self.time_uploaded_box)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_13 = QLabel(self.time_uploaded_box)
        self.label_13.setObjectName(u"label_13")
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)

        self.horizontalLayout_10.addWidget(self.label_13)

        self.uploaded_time_range_min_btn = QPushButton(self.time_uploaded_box)
        self.uploaded_time_range_min_btn.setObjectName(u"uploaded_time_range_min_btn")
        sizePolicy1.setHeightForWidth(self.uploaded_time_range_min_btn.sizePolicy().hasHeightForWidth())
        self.uploaded_time_range_min_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_10.addWidget(self.uploaded_time_range_min_btn)

        self.uploaded_time_range_min_edit = QTimeEdit(self.time_uploaded_box)
        self.uploaded_time_range_min_edit.setObjectName(u"uploaded_time_range_min_edit")

        self.horizontalLayout_10.addWidget(self.uploaded_time_range_min_edit)

        self.label_14 = QLabel(self.time_uploaded_box)
        self.label_14.setObjectName(u"label_14")
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)

        self.horizontalLayout_10.addWidget(self.label_14)

        self.uploaded_time_range_max_edit = QTimeEdit(self.time_uploaded_box)
        self.uploaded_time_range_max_edit.setObjectName(u"uploaded_time_range_max_edit")

        self.horizontalLayout_10.addWidget(self.uploaded_time_range_max_edit)

        self.uploaded_time_range_max_btn = QPushButton(self.time_uploaded_box)
        self.uploaded_time_range_max_btn.setObjectName(u"uploaded_time_range_max_btn")
        sizePolicy1.setHeightForWidth(self.uploaded_time_range_max_btn.sizePolicy().hasHeightForWidth())
        self.uploaded_time_range_max_btn.setSizePolicy(sizePolicy1)

        self.horizontalLayout_10.addWidget(self.uploaded_time_range_max_btn)


        self.verticalLayout_9.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.uploaded_time_range_include_rb = QRadioButton(self.time_uploaded_box)
        self.include_time_uploaded_group = QButtonGroup(Dialog)
        self.include_time_uploaded_group.setObjectName(u"include_time_uploaded_group")
        self.include_time_uploaded_group.addButton(self.uploaded_time_range_include_rb)
        self.uploaded_time_range_include_rb.setObjectName(u"uploaded_time_range_include_rb")

        self.horizontalLayout_11.addWidget(self.uploaded_time_range_include_rb)

        self.uploaded_time_range_exclude_rb = QRadioButton(self.time_uploaded_box)
        self.include_time_uploaded_group.addButton(self.uploaded_time_range_exclude_rb)
        self.uploaded_time_range_exclude_rb.setObjectName(u"uploaded_time_range_exclude_rb")

        self.horizontalLayout_11.addWidget(self.uploaded_time_range_exclude_rb)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)


        self.verticalLayout_9.addLayout(self.horizontalLayout_11)


        self.verticalLayout_7.addWidget(self.time_uploaded_box)

        self.days_of_month_uploaded_box = QGroupBox(self.uploaded_filters_tab)
        self.days_of_month_uploaded_box.setObjectName(u"days_of_month_uploaded_box")
        self.days_of_month_uploaded_box.setCheckable(True)
        self.days_of_month_uploaded_box.setChecked(False)
        self.horizontalLayout_7 = QHBoxLayout(self.days_of_month_uploaded_box)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.days_of_month_uploaded_edit = QLineEdit(self.days_of_month_uploaded_box)
        self.days_of_month_uploaded_edit.setObjectName(u"days_of_month_uploaded_edit")

        self.horizontalLayout_7.addWidget(self.days_of_month_uploaded_edit)


        self.verticalLayout_7.addWidget(self.days_of_month_uploaded_box)

        self.months_uploaded_box = QGroupBox(self.uploaded_filters_tab)
        self.months_uploaded_box.setObjectName(u"months_uploaded_box")
        sizePolicy3.setHeightForWidth(self.months_uploaded_box.sizePolicy().hasHeightForWidth())
        self.months_uploaded_box.setSizePolicy(sizePolicy3)
        self.months_uploaded_box.setCheckable(True)
        self.months_uploaded_box.setChecked(False)
        self.horizontalLayout_6 = QHBoxLayout(self.months_uploaded_box)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.months_uploaded_edit = QLineEdit(self.months_uploaded_box)
        self.months_uploaded_edit.setObjectName(u"months_uploaded_edit")

        self.horizontalLayout_6.addWidget(self.months_uploaded_edit)


        self.verticalLayout_7.addWidget(self.months_uploaded_box)

        self.weekdays_uploaded_box = QGroupBox(self.uploaded_filters_tab)
        self.weekdays_uploaded_box.setObjectName(u"weekdays_uploaded_box")
        self.weekdays_uploaded_box.setCheckable(True)
        self.weekdays_uploaded_box.setChecked(False)
        self.horizontalLayout_8 = QHBoxLayout(self.weekdays_uploaded_box)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.weekdays_uploaded_mon = QCheckBox(self.weekdays_uploaded_box)
        self.weekdays_uploaded_mon.setObjectName(u"weekdays_uploaded_mon")
        self.weekdays_uploaded_mon.setChecked(True)

        self.horizontalLayout_8.addWidget(self.weekdays_uploaded_mon)

        self.weekdays_uploaded_tue = QCheckBox(self.weekdays_uploaded_box)
        self.weekdays_uploaded_tue.setObjectName(u"weekdays_uploaded_tue")
        self.weekdays_uploaded_tue.setChecked(True)

        self.horizontalLayout_8.addWidget(self.weekdays_uploaded_tue)

        self.weekdays_uploaded_wed = QCheckBox(self.weekdays_uploaded_box)
        self.weekdays_uploaded_wed.setObjectName(u"weekdays_uploaded_wed")
        self.weekdays_uploaded_wed.setChecked(True)

        self.horizontalLayout_8.addWidget(self.weekdays_uploaded_wed)

        self.weekdays_uploaded_thu = QCheckBox(self.weekdays_uploaded_box)
        self.weekdays_uploaded_thu.setObjectName(u"weekdays_uploaded_thu")
        self.weekdays_uploaded_thu.setChecked(True)

        self.horizontalLayout_8.addWidget(self.weekdays_uploaded_thu)

        self.weekdays_uploaded_fri = QCheckBox(self.weekdays_uploaded_box)
        self.weekdays_uploaded_fri.setObjectName(u"weekdays_uploaded_fri")
        self.weekdays_uploaded_fri.setChecked(True)

        self.horizontalLayout_8.addWidget(self.weekdays_uploaded_fri)

        self.weekdays_uploaded_sat = QCheckBox(self.weekdays_uploaded_box)
        self.weekdays_uploaded_sat.setObjectName(u"weekdays_uploaded_sat")
        self.weekdays_uploaded_sat.setChecked(True)

        self.horizontalLayout_8.addWidget(self.weekdays_uploaded_sat)

        self.weekdays_uploaded_sun = QCheckBox(self.weekdays_uploaded_box)
        self.weekdays_uploaded_sun.setObjectName(u"weekdays_uploaded_sun")
        self.weekdays_uploaded_sun.setChecked(True)

        self.horizontalLayout_8.addWidget(self.weekdays_uploaded_sun)


        self.verticalLayout_7.addWidget(self.weekdays_uploaded_box)

        self.tabWidget.addTab(self.uploaded_filters_tab, "")

        self.horizontalLayout.addWidget(self.tabWidget)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.tabWidget, self.date_watched_box)
        QWidget.setTabOrder(self.date_watched_box, self.date_watched_set_oldest_btn)
        QWidget.setTabOrder(self.date_watched_set_oldest_btn, self.date_watched_from)
        QWidget.setTabOrder(self.date_watched_from, self.date_watched_to)
        QWidget.setTabOrder(self.date_watched_to, self.date_watched_set_newest_btn)
        QWidget.setTabOrder(self.date_watched_set_newest_btn, self.date_watched_include_rb)
        QWidget.setTabOrder(self.date_watched_include_rb, self.date_watched_exclude_rb)
        QWidget.setTabOrder(self.date_watched_exclude_rb, self.time_watched_box)
        QWidget.setTabOrder(self.time_watched_box, self.watched_time_range_min_btn)
        QWidget.setTabOrder(self.watched_time_range_min_btn, self.watched_time_range_min_edit)
        QWidget.setTabOrder(self.watched_time_range_min_edit, self.watched_time_range_max_edit)
        QWidget.setTabOrder(self.watched_time_range_max_edit, self.watched_time_range_max_btn)
        QWidget.setTabOrder(self.watched_time_range_max_btn, self.watched_time_range_include_rb)
        QWidget.setTabOrder(self.watched_time_range_include_rb, self.watched_time_range_exclude_rb)
        QWidget.setTabOrder(self.watched_time_range_exclude_rb, self.days_of_month_watched_box)
        QWidget.setTabOrder(self.days_of_month_watched_box, self.days_of_month_watched_edit)
        QWidget.setTabOrder(self.days_of_month_watched_edit, self.months_watched_box)
        QWidget.setTabOrder(self.months_watched_box, self.months_watched_edit)
        QWidget.setTabOrder(self.months_watched_edit, self.weekdays_watched_box)
        QWidget.setTabOrder(self.weekdays_watched_box, self.weekdays_watched_mon)
        QWidget.setTabOrder(self.weekdays_watched_mon, self.weekdays_watched_tue)
        QWidget.setTabOrder(self.weekdays_watched_tue, self.weekdays_watched_wed)
        QWidget.setTabOrder(self.weekdays_watched_wed, self.weekdays_watched_thu)
        QWidget.setTabOrder(self.weekdays_watched_thu, self.weekdays_watched_fri)
        QWidget.setTabOrder(self.weekdays_watched_fri, self.weekdays_watched_sat)
        QWidget.setTabOrder(self.weekdays_watched_sat, self.weekdays_watched_sun)
        QWidget.setTabOrder(self.weekdays_watched_sun, self.date_uploaded_box)
        QWidget.setTabOrder(self.date_uploaded_box, self.date_uploaded_set_oldest_btn)
        QWidget.setTabOrder(self.date_uploaded_set_oldest_btn, self.date_uploaded_from)
        QWidget.setTabOrder(self.date_uploaded_from, self.date_uploaded_to)
        QWidget.setTabOrder(self.date_uploaded_to, self.date_uploaded_set_newest_btn)
        QWidget.setTabOrder(self.date_uploaded_set_newest_btn, self.date_uploaded_include_rb)
        QWidget.setTabOrder(self.date_uploaded_include_rb, self.date_uploaded_exclude_rb)
        QWidget.setTabOrder(self.date_uploaded_exclude_rb, self.time_uploaded_box)
        QWidget.setTabOrder(self.time_uploaded_box, self.uploaded_time_range_min_btn)
        QWidget.setTabOrder(self.uploaded_time_range_min_btn, self.uploaded_time_range_min_edit)
        QWidget.setTabOrder(self.uploaded_time_range_min_edit, self.uploaded_time_range_max_edit)
        QWidget.setTabOrder(self.uploaded_time_range_max_edit, self.uploaded_time_range_max_btn)
        QWidget.setTabOrder(self.uploaded_time_range_max_btn, self.uploaded_time_range_include_rb)
        QWidget.setTabOrder(self.uploaded_time_range_include_rb, self.uploaded_time_range_exclude_rb)
        QWidget.setTabOrder(self.uploaded_time_range_exclude_rb, self.days_of_month_uploaded_box)
        QWidget.setTabOrder(self.days_of_month_uploaded_box, self.days_of_month_uploaded_edit)
        QWidget.setTabOrder(self.days_of_month_uploaded_edit, self.months_uploaded_box)
        QWidget.setTabOrder(self.months_uploaded_box, self.months_uploaded_edit)
        QWidget.setTabOrder(self.months_uploaded_edit, self.weekdays_uploaded_box)
        QWidget.setTabOrder(self.weekdays_uploaded_box, self.weekdays_uploaded_mon)
        QWidget.setTabOrder(self.weekdays_uploaded_mon, self.weekdays_uploaded_tue)
        QWidget.setTabOrder(self.weekdays_uploaded_tue, self.weekdays_uploaded_wed)
        QWidget.setTabOrder(self.weekdays_uploaded_wed, self.weekdays_uploaded_thu)
        QWidget.setTabOrder(self.weekdays_uploaded_thu, self.weekdays_uploaded_fri)
        QWidget.setTabOrder(self.weekdays_uploaded_fri, self.weekdays_uploaded_sat)
        QWidget.setTabOrder(self.weekdays_uploaded_sat, self.weekdays_uploaded_sun)
        QWidget.setTabOrder(self.weekdays_uploaded_sun, self.title_cb)
        QWidget.setTabOrder(self.title_cb, self.title_combo)
        QWidget.setTabOrder(self.title_combo, self.title_regex_cb)
        QWidget.setTabOrder(self.title_regex_cb, self.title_edit)
        QWidget.setTabOrder(self.title_edit, self.channel_cb)
        QWidget.setTabOrder(self.channel_cb, self.channel_combo)
        QWidget.setTabOrder(self.channel_combo, self.channel_regex_cb)
        QWidget.setTabOrder(self.channel_regex_cb, self.channel_edit)
        QWidget.setTabOrder(self.channel_edit, self.views_cb)
        QWidget.setTabOrder(self.views_cb, self.views_combo)
        QWidget.setTabOrder(self.views_combo, self.views_min)
        QWidget.setTabOrder(self.views_min, self.views_max)
        QWidget.setTabOrder(self.views_max, self.userviews_cb)
        QWidget.setTabOrder(self.userviews_cb, self.userviews_combo)
        QWidget.setTabOrder(self.userviews_combo, self.userviews_min)
        QWidget.setTabOrder(self.userviews_min, self.userviews_max)
        QWidget.setTabOrder(self.userviews_max, self.userviews_channel_cb)
        QWidget.setTabOrder(self.userviews_channel_cb, self.userviews_channel_combo)
        QWidget.setTabOrder(self.userviews_channel_combo, self.userviews_channel_min)
        QWidget.setTabOrder(self.userviews_channel_min, self.userviews_channel_max)
        QWidget.setTabOrder(self.userviews_channel_max, self.languages_cb)
        QWidget.setTabOrder(self.languages_cb, self.languages_combo)
        QWidget.setTabOrder(self.languages_combo, self.languages_edit)
        QWidget.setTabOrder(self.languages_edit, self.duration_cb)
        QWidget.setTabOrder(self.duration_cb, self.duration_combo)
        QWidget.setTabOrder(self.duration_combo, self.duration_min)
        QWidget.setTabOrder(self.duration_min, self.duration_max)
        QWidget.setTabOrder(self.duration_max, self.youtube_rb)
        QWidget.setTabOrder(self.youtube_rb, self.music_rb)
        QWidget.setTabOrder(self.music_rb, self.platform_both_rb)
        QWidget.setTabOrder(self.platform_both_rb, self.available_rb)
        QWidget.setTabOrder(self.available_rb, self.deleted_rb)
        QWidget.setTabOrder(self.deleted_rb, self.availability_both_rb)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.channel_combo.setItemText(0, QCoreApplication.translate("Dialog", u"contains", None))
        self.channel_combo.setItemText(1, QCoreApplication.translate("Dialog", u"does not contain", None))

        self.views_cb.setText(QCoreApplication.translate("Dialog", u"Total views", None))
        self.channel_cb.setText(QCoreApplication.translate("Dialog", u"Channel name", None))
        self.userviews_combo.setItemText(0, QCoreApplication.translate("Dialog", u"in range", None))
        self.userviews_combo.setItemText(1, QCoreApplication.translate("Dialog", u"not in range", None))

        self.duration_max.setDisplayFormat(QCoreApplication.translate("Dialog", u"HH:mm:ss", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Availability:", None))
        self.duration_cb.setText(QCoreApplication.translate("Dialog", u"Video duration", None))
        self.available_rb.setText(QCoreApplication.translate("Dialog", u"Available", None))
        self.deleted_rb.setText(QCoreApplication.translate("Dialog", u"Deleted", None))
        self.availability_both_rb.setText(QCoreApplication.translate("Dialog", u"Both", None))
        self.userviews_cb.setText(QCoreApplication.translate("Dialog", u"My views", None))
        self.youtube_rb.setText(QCoreApplication.translate("Dialog", u"YouTube", None))
        self.music_rb.setText(QCoreApplication.translate("Dialog", u"YouTube Music", None))
        self.platform_both_rb.setText(QCoreApplication.translate("Dialog", u"Both", None))
        self.languages_cb.setText(QCoreApplication.translate("Dialog", u"Languages", None))
        self.userviews_channel_cb.setText(QCoreApplication.translate("Dialog", u"My views per channel", None))
        self.languages_combo.setItemText(0, QCoreApplication.translate("Dialog", u"include", None))
        self.languages_combo.setItemText(1, QCoreApplication.translate("Dialog", u"exclude", None))

        self.title_cb.setText(QCoreApplication.translate("Dialog", u"Title", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Platform:", None))
        self.duration_combo.setItemText(0, QCoreApplication.translate("Dialog", u"in range", None))
        self.duration_combo.setItemText(1, QCoreApplication.translate("Dialog", u"not in range", None))

        self.views_combo.setItemText(0, QCoreApplication.translate("Dialog", u"in range", None))
        self.views_combo.setItemText(1, QCoreApplication.translate("Dialog", u"not in range", None))

        self.userviews_channel_combo.setItemText(0, QCoreApplication.translate("Dialog", u"in range", None))
        self.userviews_channel_combo.setItemText(1, QCoreApplication.translate("Dialog", u"not in range", None))

        self.title_combo.setItemText(0, QCoreApplication.translate("Dialog", u"contains", None))
        self.title_combo.setItemText(1, QCoreApplication.translate("Dialog", u"does not contain", None))

        self.duration_min.setDisplayFormat(QCoreApplication.translate("Dialog", u"HH:mm:ss", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"to", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"to", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"to", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"to", None))
        self.languages_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"ISO codes, e.g. en, de, fr", None))
        self.channel_regex_cb.setText(QCoreApplication.translate("Dialog", u"RegEx", None))
        self.title_regex_cb.setText(QCoreApplication.translate("Dialog", u"RegEx", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.property_filters_tab), QCoreApplication.translate("Dialog", u"Property filters", None))
        self.date_watched_box.setTitle(QCoreApplication.translate("Dialog", u"Watched: Date Range", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"From:", None))
        self.date_watched_set_oldest_btn.setText(QCoreApplication.translate("Dialog", u"Set to oldest", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"To:", None))
        self.date_watched_set_newest_btn.setText(QCoreApplication.translate("Dialog", u"Set to newest", None))
        self.date_watched_include_rb.setText(QCoreApplication.translate("Dialog", u"Include range", None))
        self.date_watched_exclude_rb.setText(QCoreApplication.translate("Dialog", u"Exclude range", None))
        self.time_watched_box.setTitle(QCoreApplication.translate("Dialog", u"Watched: Time Range", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"From:", None))
        self.watched_time_range_min_btn.setText(QCoreApplication.translate("Dialog", u"00:00", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"To:", None))
        self.watched_time_range_max_btn.setText(QCoreApplication.translate("Dialog", u"23:59", None))
        self.watched_time_range_include_rb.setText(QCoreApplication.translate("Dialog", u"Include range", None))
        self.watched_time_range_exclude_rb.setText(QCoreApplication.translate("Dialog", u"Exclude range", None))
        self.days_of_month_watched_box.setTitle(QCoreApplication.translate("Dialog", u"Watched: Days of Month", None))
        self.days_of_month_watched_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"comma-separated or range (e.g. 3, 5, 8-10, 12)", None))
        self.months_watched_box.setTitle(QCoreApplication.translate("Dialog", u"Watched: Months", None))
        self.months_watched_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"comma-separated or range (e.g. 3, 5, 8-10, 12)", None))
        self.weekdays_watched_box.setTitle(QCoreApplication.translate("Dialog", u"Watched: Weekdays", None))
        self.weekdays_watched_mon.setText(QCoreApplication.translate("Dialog", u"Mon", None))
        self.weekdays_watched_tue.setText(QCoreApplication.translate("Dialog", u"Tue", None))
        self.weekdays_watched_wed.setText(QCoreApplication.translate("Dialog", u"Wed", None))
        self.weekdays_watched_thu.setText(QCoreApplication.translate("Dialog", u"Thu", None))
        self.weekdays_watched_fri.setText(QCoreApplication.translate("Dialog", u"Fri", None))
        self.weekdays_watched_sat.setText(QCoreApplication.translate("Dialog", u"Sat", None))
        self.weekdays_watched_sun.setText(QCoreApplication.translate("Dialog", u"Sun", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.watched_filters_tab), QCoreApplication.translate("Dialog", u"Watched filters", None))
        self.date_uploaded_box.setTitle(QCoreApplication.translate("Dialog", u"Uploaded: Date Range", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"From:", None))
        self.date_uploaded_set_oldest_btn.setText(QCoreApplication.translate("Dialog", u"Set to oldest", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"To:", None))
        self.date_uploaded_set_newest_btn.setText(QCoreApplication.translate("Dialog", u"Set to newest", None))
        self.date_uploaded_include_rb.setText(QCoreApplication.translate("Dialog", u"Include range", None))
        self.date_uploaded_exclude_rb.setText(QCoreApplication.translate("Dialog", u"Exclude range", None))
        self.time_uploaded_box.setTitle(QCoreApplication.translate("Dialog", u"Uploaded: Time Range", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"From:", None))
        self.uploaded_time_range_min_btn.setText(QCoreApplication.translate("Dialog", u"00:00", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"To:", None))
        self.uploaded_time_range_max_btn.setText(QCoreApplication.translate("Dialog", u"23:59", None))
        self.uploaded_time_range_include_rb.setText(QCoreApplication.translate("Dialog", u"Include range", None))
        self.uploaded_time_range_exclude_rb.setText(QCoreApplication.translate("Dialog", u"Exclude range", None))
        self.days_of_month_uploaded_box.setTitle(QCoreApplication.translate("Dialog", u"Uploaded: Days of Month", None))
        self.days_of_month_uploaded_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"comma-separated or range (e.g. 3, 5, 8-10, 12)", None))
        self.months_uploaded_box.setTitle(QCoreApplication.translate("Dialog", u"Uploaded: Months", None))
        self.months_uploaded_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"comma-separated or range (e.g. 3, 5, 8-10, 12)", None))
        self.weekdays_uploaded_box.setTitle(QCoreApplication.translate("Dialog", u"Uploaded: Weekdays", None))
        self.weekdays_uploaded_mon.setText(QCoreApplication.translate("Dialog", u"Mon", None))
        self.weekdays_uploaded_tue.setText(QCoreApplication.translate("Dialog", u"Tue", None))
        self.weekdays_uploaded_wed.setText(QCoreApplication.translate("Dialog", u"Wed", None))
        self.weekdays_uploaded_thu.setText(QCoreApplication.translate("Dialog", u"Thu", None))
        self.weekdays_uploaded_fri.setText(QCoreApplication.translate("Dialog", u"Fri", None))
        self.weekdays_uploaded_sat.setText(QCoreApplication.translate("Dialog", u"Sat", None))
        self.weekdays_uploaded_sun.setText(QCoreApplication.translate("Dialog", u"Sun", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.uploaded_filters_tab), QCoreApplication.translate("Dialog", u"Uploaded filters", None))
    # retranslateUi

