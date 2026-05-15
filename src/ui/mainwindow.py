#  Copyright (C) 2026  leonhardw
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import math
from datetime import time, datetime
from typing import Literal

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRunnable, Signal, Slot, QThreadPool, QObject, QTime, QTimer
from PySide6.QtWidgets import (QMainWindow, QDialog, QFileDialog, QProgressBar,
                               QVBoxLayout, QLabel, QMessageBox, QButtonGroup, QGridLayout, QGroupBox, QSizePolicy, QPushButton, QLineEdit, QHBoxLayout)

from core import analyzer as wa
from core import parser as wp
from core.analyzer import VIEW, UPLOAD
from core.visualizer import WatchHistoryVisualizer
from ui.generated.ui_visualizer import Ui_MainWindow
from ui.generated.ui_visualizer_create_dialog import Ui_Dialog as Ui_CreateDialog
from ui.generated.ui_visualizer_filter import Ui_Dialog
from ui.widgets.custom_widgets import AnalysisCard
from ui.widgets.extendedtableview import TableViewDialog
from utils import export_data
from utils.advanced_filters import filter_to_str, str_to_list


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal()
    progress = Signal(int)


class APICallWorker(QRunnable):
    def __init__(self, parser, only_missing=False):
        super().__init__()
        self.signals = WorkerSignals()
        self.parser = parser
        self.only_missing = only_missing
    
    @Slot()
    def run(self):
        self.parser.progress_callback = self.update_progress
        try:
            if self.only_missing:
                self.parser.add_missing_metadata()
            else:
                self.parser.add_metadata()
        except:
            self.signals.error.emit()
        else:
            self.signals.finished.emit()
    
    def update_progress(self, current, total):
        value = int((current / total) * 100)
        self.signals.progress.emit(value)


class MainWindow(QMainWindow, Ui_MainWindow):
    property_plots = ('Videos per views\n(Bar chart)',
                      'Videos per duration\n(Bar chart)',
                      'Videos per channel\n(Pie chart)',
                      'My most watched videos\n(Pie chart)',
                      'Videos per language\n(Pie chart)')
    
    time_plots = ('Videos per day of month\n(Bar chart)',
                  'Videos per month of year\n(Bar chart)',
                  'Videos per year\n(Bar chart)',
                  'Videos per weekday\n(Bar chart)',
                  'Videos per day of year\n(Line chart)',
                  'Videos per total months\n(Line chart)',
                  'Videos per time of day\n(Bar chart)',
                  'Time of day per year\n(Heatmap, absolute)',
                  'Time of day per year\n(Heatmap, percentages)'
                  )
    
    accuracies = {0: 5, 1: 10, 2: 15, 3: 20, 4: 30, 5: 60, 6: 120}
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowTitle('YouTube History Visualizer')
        
        self.loaded_file = None
        self.analyzer = None
        self.visualizer = None
        self.metadata_included = False
        
        self.filters = []
        
        self.tabWidget.setCurrentIndex(0)
        self.filters_list.setWordWrap(True)
        
        self.plot_watched_rb.setChecked(True)
        self.set_plot_mode_enabled(False)
        self.selected_plot_group = QButtonGroup(self)
        self.setup_plot_lists()
        self.selected_plot_group.button(0).setChecked(True)
        self.selected_plot_group.idClicked.connect(self.update_plot_settings)
        self.update_plot_settings(0)
        
        self.accuracy_combo_bars.currentIndexChanged.connect(lambda: self.set_timeedit_step_size('leftmost_time'))
        self.accuracy_combo_heatmap.currentIndexChanged.connect(lambda: self.set_timeedit_step_size('topmost_time'))
        self.set_timeedit_step_size('leftmost_time')
        self.set_timeedit_step_size('topmost_time')
        
        self.show_plot_btn.clicked.connect(lambda: self.handle_plot('show'))
        self.save_plot_btn.clicked.connect(lambda: self.handle_plot('save'))
        self.view_plot_as_table_btn.clicked.connect(self.view_plot_as_table)
        
        self.create_db_btn.clicked.connect(self.create_database)
        self.load_db_btn.clicked.connect(self.load_database)
        self.save_db_btn.clicked.connect(self.save_database)
        self.manage_db_btn.clicked.connect(self.manage_database)
        self.export_as_csv_btn.clicked.connect(self.export_as_csv)
        self.view_as_table_btn.clicked.connect(self.view_as_table)
        
        self.filter_dialog = FilterDialog(self)  # preloaded for better performance (dialog expected to be opened multiple times)
        self.edit_filter_btn.clicked.connect(self.edit_filter)
        self.add_filter_btn.clicked.connect(self.add_filter)
        self.delete_filter_btn.clicked.connect(self.delete_filter)
        
        self.actionCreate_database.triggered.connect(self.create_database)
        self.actionLoad_database.triggered.connect(self.load_database)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.show_about_dialog)
        
        self.threshold_spin.setValue(50)
        self.show_plot_btn.setDefault(True)
        self.plot_mode_group.idClicked.connect(lambda button_id: self.set_plot_year_range())
        
        self.set_data_buttons_enabled(False, data_loaded=False)
        self.add_filter_btn.setEnabled(False)
        self.edit_filter_btn.setEnabled(False)
        self.delete_filter_btn.setEnabled(False)
    
    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()
    
    def set_data_buttons_enabled(self, state, data_loaded=True):
        self.save_plot_btn.setEnabled(state)
        self.show_plot_btn.setEnabled(state)
        self.view_plot_as_table_btn.setEnabled(state)
        
        self.save_db_btn.setEnabled(state)
        self.export_as_csv_btn.setEnabled(state)
        self.view_as_table_btn.setEnabled(state)
        self.manage_db_btn.setEnabled(state)
    
    def set_data_buttons_state(self):
        if len(self.analyzer.watch_data) > 0:
            self.set_data_buttons_enabled(True)
        else:
            self.set_data_buttons_enabled(False)
    
    def setup_plot_lists(self):
        layout = self.analysis_tab.layout()
        self.analysis_tab.setUpdatesEnabled(False)
        self.plots_vbox = QVBoxLayout()
        self.property_plots_box = QGroupBox('Property plots')
        self.property_plots_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.property_plots_grid = QGridLayout()
        rb_id = 0
        
        for i, plot in enumerate(self.property_plots):
            radiobutton = AnalysisCard(plot)
            self.selected_plot_group.addButton(radiobutton, rb_id)
            self.property_plots_grid.addWidget(radiobutton, 0, i)
            rb_id += 1
        self.property_plots_box.setLayout(self.property_plots_grid)
        
        self.time_plots_grid = QGridLayout()
        self.time_plots_box = QGroupBox('Time plots')
        self.time_plots_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        for i, plot in enumerate(self.time_plots):
            radiobutton = AnalysisCard(plot)
            self.selected_plot_group.addButton(radiobutton, rb_id)
            self.time_plots_grid.addWidget(radiobutton, i // 3, i % 3)
            rb_id += 1
        
        self.time_plots_box.setLayout(self.time_plots_grid)
        
        self.plots_vbox.addWidget(self.property_plots_box)
        self.plots_vbox.addWidget(self.time_plots_box)
        
        layout.insertLayout(0, self.plots_vbox)
        self.analysis_tab.setUpdatesEnabled(True)
    
    def update_plot_settings(self, rb_id):
        current = rb_id
        if current in (2, 3, 4):
            self.plot_settings_stack.setCurrentWidget(self.threshold_page)
        elif current == 9:
            self.plot_settings_stack.setCurrentWidget(self.year_page)
            self.set_plot_year_range()
        elif current == 11:
            self.plot_settings_stack.setCurrentWidget(self.leftmost_time_page)
        elif current in (12, 13):
            self.plot_settings_stack.setCurrentWidget(self.topmost_time_page)
        else:
            self.plot_settings_stack.setCurrentWidget(self.empty_page)
        
        if current <= 4:
            self.set_plot_mode_enabled(False)
        else:
            self.set_plot_mode_enabled(True)
    
    def set_plot_year_range(self):
        if self.plot_settings_stack.currentWidget() == self.year_page:
            if self.plot_watched_rb.isChecked():
                first, last = self.analyzer.first_date.year, self.analyzer.last_date.year
                self.year_spin.setRange(first, last)
            else:
                first, last = self.analyzer.first_upload_date.year, self.analyzer.last_upload_date.year
                self.year_spin.setRange(first, last)
    
    def set_plot_mode_enabled(self, state):
        for i in range(self.plot_mode_hbox.count()):
            item = self.plot_mode_hbox.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setEnabled(state)
        
        if not self.metadata_included:
            self.plot_uploaded_rb.setEnabled(False)
    
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key.Key_Return:
            if self.tabWidget.currentWidget() == self.analysis_tab:
                if self.show_plot_btn.isEnabled():
                    self.handle_plot('show')
    
    def set_timeedit_step_size(self, widget: Literal['leftmost_time', 'topmost_time']):
        if widget == 'leftmost_time':
            self.leftmost_time_edit.change_step_size(self.accuracies[self.accuracy_combo_bars.currentIndex()])
        elif widget == 'topmost_time':
            self.topmost_time_edit.change_step_size(self.accuracies[self.accuracy_combo_heatmap.currentIndex()])
    
    # noinspection PyUnboundLocalVariable
    def handle_plot(self, plot_mode: Literal['show', 'save']):
        selected_plot = self.selected_plot_group.checkedId()
        if plot_mode == 'save':
            self.visualizer.save_plots = True
            filename, _ = QFileDialog.getSaveFileName(self, filter='PNG images (*.png)')
            if filename:
                self.visualizer.save_filename = filename
            else:
                return
        else:
            self.visualizer.save_plots = False
        if selected_plot >= 5:
            mode = VIEW if self.plot_watched_rb.isChecked() else UPLOAD
        match selected_plot:
            case 0:
                self.visualizer.visualize_videos_per_views()
            case 1:
                self.visualizer.visualize_videos_per_duration()
            case 2:
                self.visualizer.visualize_videos_per_channel(min_videos_per_channel=self.threshold_spin.value())
            case 3:
                self.visualizer.visualize_most_watched_videos(min_views=self.threshold_spin.value(), exclude_other=True)
            case 4:
                self.visualizer.visualize_videos_per_language(min_videos_per_language=self.threshold_spin.value())
            case 5:
                self.visualizer.visualize_videos_per_date_unit('day', mode=mode)
            case 6:
                self.visualizer.visualize_videos_per_date_unit('month', mode=mode)
            case 7:
                self.visualizer.visualize_videos_per_date_unit('year', mode=mode)
            case 8:
                self.visualizer.visualize_videos_per_date_unit('weekday', mode=mode)
            case 9:
                year = self.year_spin.value()
                self.visualizer.visualize_days_per_year(year=year, mode=mode)
            case 10:
                self.visualizer.visualize_all_months(mode=mode)
            case 11:
                accuracy = self.accuracies[self.accuracy_combo_bars.currentIndex()]
                leftmost_time = self.leftmost_time_edit.time()
                minutes = leftmost_time.hour() * 60 + leftmost_time.minute()
                self.visualizer.visualize_videos_per_time(accuracy=accuracy, rotate=minutes, mode=mode)
            case 12 | 13:
                accuracy = self.accuracies[self.accuracy_combo_heatmap.currentIndex()]
                topmost_time = self.topmost_time_edit.time()
                minutes = topmost_time.hour() * 60 + topmost_time.minute()
                absolute = None
                if selected_plot == 12:
                    absolute = True
                elif selected_plot == 13:
                    absolute = False
                self.visualizer.visualize_time_per_year_heatmap(accuracy=accuracy, rotate=-minutes, absolute=absolute, mode=mode)
    
    # noinspection PyUnboundLocalVariable
    def view_plot_as_table(self):
        sort_by = 0
        header_x, header_y = 'x', 'Videos'
        sort_ascending = True
        hide_columns = None
        
        selected_plot = self.selected_plot_group.checkedId()
        if selected_plot >= 4:
            mode = VIEW if self.plot_watched_rb.isChecked() else UPLOAD
        match selected_plot:
            case 0:
                data = self.visualizer.get_videos_per_views()
                header_x = 'Views'
            case 1:
                data = self.visualizer.get_videos_per_duration()
                header_x = 'Views'
            case 2:
                data = self.visualizer.get_videos_per_channel(min_videos_per_channel=self.threshold_spin.value())
                sort_by = 2  # (number, channel, views)
                sort_ascending = False
                header_x = 'Channel'
            case 3:
                data = self.visualizer.get_most_watched_videos(min_views=self.threshold_spin.value())
                sort_by = 2  # (number, video, own views)
                sort_ascending = False
                header_x = 'Most Watched Videos'
            case 4:
                data = self.visualizer.get_videos_per_language(min_videos_per_language=self.threshold_spin.value())
                sort_by = 2  # (number, language, views)
                sort_ascending = False
                header_x = 'Language'
            case 5:
                data = self.visualizer.get_videos_per_date_unit('day', mode=mode)
                header_x = 'Day'
            case 6:
                data = self.visualizer.get_videos_per_date_unit('month', mode=mode)
                header_x = 'Month'
            case 7:
                data = self.visualizer.get_videos_per_date_unit('year', mode=mode)
                data = list(data)
                data[0] = [str(year) for year in data[0]]
                header_x = 'Year'
            case 8:
                data = self.visualizer.get_videos_per_date_unit('weekday', mode=mode)
                header_x = 'Weekday'
            case 9:
                year = self.year_spin.value()
                data = self.visualizer.get_days_per_year(year=year, mode=mode)
                data = list(data)
                data[0] = [day.strftime('%Y-%m-%d') for day in data[0]]
                header_x = 'Day of year'
            case 10:
                data = self.visualizer.get_all_months(mode=mode)
                data = list(data)
                data[0] = [month.strftime('%Y-%m') for month in data[0]]
                header_x = 'Month'
            case 11:
                accuracy = self.accuracies[self.accuracy_combo_bars.currentIndex()]
                leftmost_time = self.leftmost_time_edit.time()
                minutes = leftmost_time.hour() * 60 + leftmost_time.minute()
                data = self.visualizer.get_videos_per_time(accuracy=accuracy, rotate=minutes, mode=mode)
                header_x = 'Time'
            case 12 | 13:
                accuracy = self.accuracies[self.accuracy_combo_heatmap.currentIndex()]
                topmost_time = self.topmost_time_edit.time()
                minutes = topmost_time.hour() * 60 + topmost_time.minute()
                absolute = None
                if selected_plot == 12:
                    absolute = True
                elif selected_plot == 13:
                    absolute = False
                data = self.visualizer.get_time_per_year(accuracy=accuracy, rotate=-minutes, absolute=absolute, mode=mode, as_heatmap=False)
        
        data = list(data)
        if selected_plot in (12, 13):
            data[0] = ['Time'] + [str(i) for i in data[0]]
            for i in range(1, len(data)):
                data[i][0] = data[i][0].strftime('%H:%M')
            translated_data = data
        else:
            if selected_plot in (5, 6, 7, 11):
                translated_data = list(zip(*data))
                translated_data.insert(0, (header_x, header_y))
            else:
                data.insert(0, range(1, len(data[0]) + 1))
                translated_data = list(zip(*data))
                translated_data.insert(0, ('#', header_x, header_y))
        self.table_view_dialog = TableViewDialog(self)
        self.table_view_dialog.import_data(translated_data, hide_columns=hide_columns, sort_by_index=sort_by, sort_ascending=sort_ascending)
        self.table_view_dialog.table_view.resizeColumnsToContents()
        self.table_view_dialog.exec()
    
    def create_database(self):
        create_db_dialog = CreateDatabaseDialog(self)
        if create_db_dialog.exec():
            self.load_database(path=create_db_dialog.save_to)
    
    def load_database(self, checked=None, path=None):
        if path is None:
            file_filters = 'Data file (*.lw);;All files (*.*)'
            filename, _ = QFileDialog.getOpenFileName(self, 'Choose file...', filter=file_filters)
        else:
            filename = path
        if filename:
            self.loaded_file = filename
            data = wa.load_watch_data(self.loaded_file)
            self.metadata_included = data[0]
            self.analyzer = wa.WatchHistoryAnalyzer(watch_data=data[1], metadata_included=self.metadata_included)
            self.visualizer = WatchHistoryVisualizer(self.analyzer)
            self.statistics_label.setText(f'Matching videos: {len(self.analyzer.watch_data)}')
            self.loaded_file_label.setText(f'Loaded file: {self.loaded_file}')
            self.set_data_buttons_state()
            
            self.add_filter_btn.setEnabled(True)
            self.edit_filter_btn.setEnabled(True)
            self.delete_filter_btn.setEnabled(False)
            
            self.set_metadata_plots_enabled(self.metadata_included)
            self.set_metadata_filters_enabled(self.metadata_included)
            
            self.add_default_filter()
    
    def save_database(self):
        file_filters = 'Data file (*.lw);;All files (*.*)'
        filename, _ = QFileDialog.getSaveFileName(self, 'Save file as...', filter=file_filters)
        if filename:
            export_data.save_watch_data(filename, self.analyzer.watch_data, metadata_included=self.metadata_included)
            QMessageBox.information(self, 'Success', f'Database saved successfully.')
    
    def manage_database(self):
        ManageDatabaseDialog(self, self.analyzer, self.loaded_file).exec()
    
    def export_as_csv(self):
        file_filters = 'CSV files (*.csv);;All files (*.*)'
        filename, _ = QFileDialog.getSaveFileName(self, 'Export CSV as...', filter=file_filters)
        if filename:
            export_data.save_as_csv(filename, self.analyzer.watch_data)
            QMessageBox.information(self, 'Success', f'Successfully exported as CSV.')
    
    def view_as_table(self):
        hide_columns = ('Link', 'Video ID', 'Channel link')
        
        # Link, Video ID, Video title, Channel, Channel link, Watched at, Deleted, YouTube Music,
        # Uploaded at, Language, Global views, Likes, Comments, Duration (in s), My views, My views per channel
        widths = (290, 100, 300, 200, 380, 125, 60, 100, 125, 75, 75, 75, 75, 85, 60, 125)
        self.table_view_dialog = TableViewDialog(self)
        self.table_view_dialog.import_data(self.analyzer.to_table(), hide_columns=hide_columns, sort_by_str='Watched at')
        self.table_view_dialog.set_column_widths(widths)
        self.table_view_dialog.exec()
    
    def add_filter(self):
        self.filters.append(
            {'platform': {'include': True, 'youtube': True, 'music': True}, 'availability': {'include': True, 'available': True, 'deleted': True}})
        self.filters_list.addItem(filter_to_str(self.filters[-1]))
        self.filters_list.setCurrentRow(self.filters_list.count() - 1)
        result = self.edit_filter()
        if not result:
            del self.filters[-1]
            self.filters_list.takeItem(self.filters_list.currentRow())
    
    def edit_filter(self):
        idx = self.filters_list.currentRow()
        if idx == -1:
            return False
        current_filter = self.filters[idx]
        self.filter_dialog.set_view_date_range(self.analyzer._get_oldest_and_newest(original_data=True, mode=VIEW))
        self.filter_dialog.set_upload_date_range(self.analyzer._get_oldest_and_newest(original_data=True, mode=UPLOAD))
        self.filter_dialog.initialize_widgets(current_filter)
        if self.filter_dialog.exec():
            self.filters[idx] = self.filter_dialog.filter_data
            self.filters_list.currentItem().setText(filter_to_str(self.filters[idx],
                                                                  view_date_range=self.analyzer._get_oldest_and_newest(original_data=True, mode=VIEW),
                                                                  upload_date_range=self.analyzer._get_oldest_and_newest(original_data=True, mode=UPLOAD)))
            self.update_filters()
            return True
        else:
            return False
    
    def delete_filter(self):
        idx = self.filters_list.currentRow()
        del self.filters[idx]
        self.filters_list.takeItem(self.filters_list.currentRow())
        self.update_filters(delete=True)
    
    def update_filters(self, delete=False):
        if delete and len(self.filters) == 0:
            self.add_default_filter()
        self.analyzer.apply_advanced_filters(self.filters)
        total_videos = len(self.analyzer.watch_data)
        self.statistics_label.setText(f'Matching videos: {total_videos}')
        if total_videos > 0:
            self.set_data_buttons_enabled(True)
        else:
            self.set_data_buttons_enabled(False)
        
        if len(self.filters) == 1 and self.filters[0] == {'platform': {'include': True, 'youtube': True, 'music': True},
                                                          'availability': {'include': True, 'available': True, 'deleted': True}}:
            self.delete_filter_btn.setEnabled(False)
        else:
            self.delete_filter_btn.setEnabled(True)
    
    def add_default_filter(self):
        self.filters.clear()
        self.filters_list.clear()
        self.filters.append(
            {'platform': {'include': True, 'youtube': True, 'music': True}, 'availability': {'include': True, 'available': True, 'deleted': True}})
        self.filters_list.addItem(filter_to_str(self.filters[-1]))
        self.filters_list.setCurrentRow(self.filters_list.count() - 1)
        self.delete_filter_btn.setEnabled(False)
    
    def set_metadata_plots_enabled(self, state):
        layout = self.property_plots_grid
        buttons = ((0, 0), (0, 1), (0, 4))
        for row, col in buttons:
            layout.itemAtPosition(row, col).widget().setEnabled(state)
        
        self.plot_uploaded_rb.setEnabled(state)
        if not state:
            self.plot_watched_rb.setChecked(True)
            self.selected_plot_group.button(2).setChecked(True)
        else:
            self.selected_plot_group.button(0).setChecked(True)
        
        self.set_plot_mode_enabled(False)
    
    def set_metadata_filters_enabled(self, state):
        self.filter_dialog.uploaded_filters_tab.setEnabled(state)
        
        for cb in (self.filter_dialog.views_cb, self.filter_dialog.languages_cb, self.filter_dialog.duration_cb):
            cb.setEnabled(state)


class ProgressDialog(QDialog):
    def __init__(self, parent=None, parser=None, save_to=None, only_missing=False):
        super().__init__(parent)
        self.setWindowTitle('Working...')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        self.threadpool = QThreadPool()
        
        self.progress_bar = QProgressBar(self)
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(QLabel('Adding metadata...'))
        self.vbox_layout.addWidget(self.progress_bar)
        self.setLayout(self.vbox_layout)
        
        self.parser = parser
        self.save_to = save_to
        self.only_missing = only_missing
        
        QTimer.singleShot(0, self.start_api_calls)
    
    def reject(self):
        pass  # don't cancel on Esc
    
    def start_api_calls(self):
        worker = APICallWorker(self.parser, only_missing=self.only_missing)
        worker.signals.finished.connect(self.api_calls_completed)
        worker.signals.error.connect(self.handle_error)
        worker.signals.progress.connect(self.progress_bar.setValue)
        self.threadpool.start(worker)
    
    def api_calls_completed(self):
        self.parser.save_watch_data(self.save_to)
        super().accept()
    
    def handle_error(self):
        QMessageBox.critical(None, 'Error', 'Invalid API key.')
        super().reject()


class CreateDatabaseDialog(QDialog, Ui_CreateDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedHeight(self.height())
        self.setMinimumWidth(400)
        self.setWindowTitle('Create database')
        
        self.parser = None
        self.save_to = None
        
        self.browse_takeout_path_btn.clicked.connect(self.browse_takeout_path)
        self.browse_save_path_btn.clicked.connect(self.browse_save_path)
    
    def browse_takeout_path(self):
        file_filters = 'Takeout HTML files (*.html);;All files (*.*)'
        filename, _ = QFileDialog.getOpenFileName(self, 'Choose file...', filter=file_filters)
        if filename:
            self.takeout_file_edit.setText(filename)
    
    def browse_save_path(self):
        file_filters = 'Data file (*.lw);;All files (*.*)'
        filename, _ = QFileDialog.getSaveFileName(self, 'Save file as...', filter=file_filters)
        if filename:
            self.save_path_edit.setText(filename)
    
    def accept(self):
        self.set_all_enabled(False)
        takeout_file = self.takeout_file_edit.text()
        self.save_to = self.save_path_edit.text()
        total_items = wp.WatchHistoryParser(filename=takeout_file, get_metadata=False, add_occurences=False, only_total_count=True).total_items
        if self.metadata_box.isChecked():
            answer = QMessageBox.question(self, 'Add metadata', f'''Adding metadata to {total_items} items will take about {round(total_items / 6000, 1)} minutes.
This will use {math.ceil(total_items / 50)} API tokens. Proceed?''',
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                          QMessageBox.StandardButton.No
                                          )
            if answer == QMessageBox.StandardButton.Yes:
                api_key = self.apikey_edit.text()
                self.parser = wp.WatchHistoryParser(filename=takeout_file, get_metadata=True, add_occurences=True,
                                                    yt_api_key=api_key)
                self.progress_dialog = ProgressDialog(self, self.parser, self.save_to)
                self.progress_dialog.exec()
                QMessageBox.information(self, 'Success', f'Metadata for {total_items} items added. Database created successfully.')
        else:
            self.parser = wp.WatchHistoryParser(filename=takeout_file, get_metadata=False, add_occurences=True)
            self.parser.save_watch_data(self.save_to)
            QMessageBox.information(self, 'Success', f'Database with {total_items} items created successfully.')
        
        self.set_all_enabled(True)
        super().accept()
    
    def set_all_enabled(self, state):
        # ok_button = self.buttonBox.button(QDialogButtonBox.StandardButton.Ok)
        # ok_button.setEnabled(state)
        self.buttonBox.setEnabled(state)
        self.takeout_file_edit.setEnabled(state)
        self.save_path_edit.setEnabled(state)
        self.metadata_box.setEnabled(state)
        self.browse_takeout_path_btn.setEnabled(state)
        self.browse_save_path_btn.setEnabled(state)
        self.takeout_file_label.setEnabled(state)
        self.database_file_label.setEnabled(state)
    
    def update_progress(self, current, total):
        self.progressBar.setValue(100 * current / total)


class ManageDatabaseDialog(QDialog):
    def __init__(self, parent=None, analyzer=None, save_to=None):
        super().__init__(parent)
        self.setWindowTitle('Manage database')
        
        self.analyzer = analyzer
        self.save_to = save_to
        
        self.apikey_edit = QLineEdit()
        self.add_metadata_btn = QPushButton('Add missing metadata')
        self.update_metadata_btn = QPushButton('Update metadata')
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(QLabel('API key:'))
        self.hbox.addWidget(self.apikey_edit)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.add_metadata_btn)
        self.vbox.addWidget(self.update_metadata_btn)
        self.setLayout(self.vbox)
        
        self.add_metadata_btn.setDefault(True)
        self.add_metadata_btn.setAutoDefault(True)
        self.update_metadata_btn.setAutoDefault(False)
        
        self.update_metadata_btn.clicked.connect(self.update_metadata)
        self.add_metadata_btn.clicked.connect(self.add_missing_metadata)
    
    def update_metadata(self):
        parser = wp.WatchHistoryParser(watch_data=self.analyzer.watch_data, yt_api_key=self.apikey_edit.text())
        total_items = len(self.analyzer.watch_data)
        answer = QMessageBox.question(self, 'Update metadata', f'''Updating all metadata of {total_items} items will take about {round(total_items / 6000, 1)} minutes.
This will use {math.ceil(total_items / 50)} API tokens. Proceed?''',
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No
                                      )
        if answer == QMessageBox.StandardButton.Yes:
            api_key = self.apikey_edit.text()
            self.progress_dialog = ProgressDialog(self, parser, self.save_to)
            result = self.progress_dialog.exec()
            if result:
                QMessageBox.information(self, 'Success', f'Metadata for {total_items} items updated. Database saved successfully.')
    
    def add_missing_metadata(self):
        parser = wp.WatchHistoryParser(watch_data=self.analyzer.watch_data, yt_api_key=self.apikey_edit.text())
        total_items = parser.get_missing_metadata_count()
        answer = QMessageBox.question(self, 'Add missing metadata',
                                      f'''Adding missing metadata to {total_items} items will take about {round(total_items / 6000, 1)} minutes.
This will use {math.ceil(total_items / 50)} API tokens. Proceed?''',
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.No
                                      )
        if answer == QMessageBox.StandardButton.Yes:
            api_key = self.apikey_edit.text()
            self.progress_dialog = ProgressDialog(self, parser, self.save_to, only_missing=True)
            result = self.progress_dialog.exec()
            if result:
                QMessageBox.information(self, 'Success', f'Metadata for {total_items} items added. Database saved successfully.')


class FilterDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Filters')
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowMaximizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        
        self.tabWidget.setCurrentIndex(0)
        self.filter_data = {}
        
        self.minimum_datetime = None
        self.maximum_datetime = None
        
        self.watched_time_range_min_btn.clicked.connect(lambda: self.watched_time_range_min_edit.setTime(QTime(0, 0, 0)))
        self.watched_time_range_max_btn.clicked.connect(lambda: self.watched_time_range_max_edit.setTime(QTime(23, 59, 59)))
        
        self.property_checkboxes = (self.title_cb, self.channel_cb, self.views_cb, self.userviews_cb,
                                    self.userviews_channel_cb, self.languages_cb, self.duration_cb)
        self.weekdays_watched_checkboxes = (self.weekdays_watched_mon, self.weekdays_watched_tue, self.weekdays_watched_wed,
                                            self.weekdays_watched_thu, self.weekdays_watched_fri, self.weekdays_watched_sat, self.weekdays_watched_sun)
        self.weekdays_uploaded_checkboxes = (self.weekdays_uploaded_mon, self.weekdays_uploaded_tue, self.weekdays_uploaded_wed,
                                             self.weekdays_uploaded_thu, self.weekdays_uploaded_fri, self.weekdays_uploaded_sat, self.weekdays_uploaded_sun)
        
        for i, checkbox in enumerate(self.property_checkboxes):
            checkbox.toggled.connect(lambda state, row=i: self.set_row_diabled(row, state))
            self.set_row_diabled(i, False)
    
    def set_view_date_range(self, date_range):
        self.minimum_datetime = date_range[0]
        self.maximum_datetime = date_range[1]
        self.date_watched_from.setMinimumDateTime(self.minimum_datetime)
        self.date_watched_to.setMaximumDateTime(self.maximum_datetime)
        self.date_watched_set_oldest_btn.clicked.connect(lambda: self.date_watched_from.setDateTime(self.minimum_datetime))
        self.date_watched_set_newest_btn.clicked.connect(lambda: self.date_watched_to.setDateTime(self.maximum_datetime))
    
    def set_upload_date_range(self, date_range):
        if date_range:
            self.minimum_datetime = date_range[0]
            self.maximum_datetime = date_range[1]
        else:
            self.minimum_datetime = datetime(1970, 1, 1)
            self.maximum_datetime = datetime(1970, 1, 1)
        self.date_uploaded_from.setMinimumDateTime(self.minimum_datetime)
        self.date_uploaded_to.setMaximumDateTime(self.maximum_datetime)
        self.date_uploaded_set_oldest_btn.clicked.connect(lambda: self.date_uploaded_from.setDateTime(self.minimum_datetime))
        self.date_uploaded_set_newest_btn.clicked.connect(lambda: self.date_uploaded_to.setDateTime(self.maximum_datetime))
    
    # noinspection PyInconsistentReturns
    def accept(self):
        # ---------- Property filters ---------- #
        if self.title_cb.isChecked():
            include = True if self.title_combo.currentIndex() == 0 else False
            self.filter_data['title'] = {'include': include, 'regex': self.title_regex_cb.isChecked(), 'value': self.title_edit.text()}
        else:
            self.delete_filter('title')
        
        if self.channel_cb.isChecked():
            include = True if self.channel_combo.currentIndex() == 0 else False
            self.filter_data['channel'] = {'include': include, 'regex': self.channel_regex_cb.isChecked(), 'value': self.channel_edit.text()}
        else:
            self.delete_filter('channel')
        if self.views_cb.isChecked():
            include = True if self.views_combo.currentIndex() == 0 else False
            self.filter_data['total_views'] = {'include': include, 'range': (int(self.views_min.value()), int(self.views_max.value()))}
        else:
            self.delete_filter('total_views')
        
        if self.userviews_cb.isChecked():
            include = True if self.userviews_combo.currentIndex() == 0 else False
            self.filter_data['user_views'] = {'include': include, 'range': (self.userviews_min.value(), self.userviews_max.value())}
        else:
            self.delete_filter('user_views')
        
        if self.userviews_channel_cb.isChecked():
            include = True if self.userviews_channel_combo.currentIndex() == 0 else False
            self.filter_data['user_channel_views'] = {'include': include, 'range': (self.userviews_channel_min.value(), self.userviews_channel_max.value())}
        else:
            self.delete_filter('user_channel_views')
        
        if self.languages_cb.isChecked():
            include = True if self.languages_combo.currentIndex() == 0 else False
            self.filter_data['languages'] = {'include': include, 'values': self.languages_edit.text()}
        else:
            self.delete_filter('languages')
        
        if self.duration_cb.isChecked():
            include = True if self.duration_combo.currentIndex() == 0 else False
            self.filter_data['duration'] = {'include': include, 'range': (self.duration_min.time().msecsSinceStartOfDay() // 1000,
                                                                          self.duration_max.time().msecsSinceStartOfDay() // 1000)}
        else:
            self.delete_filter('duration')
        
        yt_checked = self.youtube_rb.isChecked() or self.platform_both_rb.isChecked()
        yt_music_checked = self.music_rb.isChecked() or self.platform_both_rb.isChecked()
        self.filter_data['platform'] = {'include': True, 'youtube': yt_checked, 'music': yt_music_checked}
        
        include_available = self.available_rb.isChecked() or self.availability_both_rb.isChecked()
        include_deleted = self.deleted_rb.isChecked() or self.availability_both_rb.isChecked()
        self.filter_data['availability'] = {'include': True, 'available': include_available, 'deleted': include_deleted}
        
        # ---------- Watched time filters ---------- #
        if self.date_watched_box.isChecked():
            min_date = self.date_watched_from.date().toPython()
            max_date = self.date_watched_to.date().toPython()
            include = True if self.date_watched_include_rb.isChecked() else False
            self.filter_data['date_watched'] = {'include': include, 'range': (min_date, max_date)}
        else:
            self.delete_filter('date_watched')
        
        if self.time_watched_box.isChecked():
            min_time = self.watched_time_range_min_edit.time().toPython()
            max_time = self.watched_time_range_max_edit.time().toPython()
            include = self.watched_time_range_include_rb.isChecked()
            self.filter_data['time_watched'] = {'include': include, 'range': (min_time, max_time)}
        else:
            self.delete_filter('time_watched')
        
        if self.days_of_month_watched_box.isChecked():
            days_of_month = self.days_of_month_watched_edit.text()
            if not str_to_list(days_of_month, check_day=True):
                QMessageBox.critical(self, 'Error!', 'Please enter valid days for "Watched: Days of Month" in the format 3, 5, 8-10, 12.')
                return None
            self.filter_data['days_of_month_watched'] = {'include': True, 'values': days_of_month}
        else:
            self.delete_filter('days_of_month_watched')
        
        if self.months_watched_box.isChecked():
            months = self.months_watched_edit.text()
            if not str_to_list(months, check_month=True):
                QMessageBox.critical(self, 'Error!', 'Please enter valid months for "Watched: Months" in the format 3, 5, 8-10, 12')
                return None
            self.filter_data['months_watched'] = {'include': True, 'values': months}
        else:
            self.delete_filter('months_watched')
        
        if self.weekdays_watched_box.isChecked():
            weekdays = []
            for i, cb in enumerate(self.weekdays_watched_checkboxes):
                if cb.isChecked():
                    weekdays.append(i)
            self.filter_data['weekdays_watched'] = {'include': True, 'values': weekdays}
        else:
            self.delete_filter('weekdays_watched')
        
        # ---------- Uploaded time filters ---------- #
        if self.date_uploaded_box.isChecked():
            min_date = self.date_uploaded_from.date().toPython()
            max_date = self.date_uploaded_to.date().toPython()
            include = True if self.date_uploaded_include_rb.isChecked() else False
            self.filter_data['date_uploaded'] = {'include': include, 'range': (min_date, max_date)}
        else:
            self.delete_filter('date_uploaded')
        
        if self.time_uploaded_box.isChecked():
            min_time = self.uploaded_time_range_min_edit.time().toPython()
            max_time = self.uploaded_time_range_max_edit.time().toPython()
            include = self.uploaded_time_range_include_rb.isChecked()
            self.filter_data['time_uploaded'] = {'include': include, 'range': (min_time, max_time)}
        else:
            self.delete_filter('time_uploaded')
        
        if self.days_of_month_uploaded_box.isChecked():
            days_of_month = self.days_of_month_uploaded_edit.text()
            if not str_to_list(days_of_month, check_day=True):
                QMessageBox.critical(self, 'Error!', 'Please enter valid days for "Uploaded: Days of Month"  in the format 3, 5, 8-10, 12.')
                return None
            self.filter_data['days_of_month_uploaded'] = {'include': True, 'values': days_of_month}
        else:
            self.delete_filter('days_of_month_uploaded')
        
        if self.months_uploaded_box.isChecked():
            months = self.months_uploaded_edit.text()
            if not str_to_list(months, check_month=True):
                QMessageBox.critical(self, 'Error!', 'Please enter valid months for "Uploaded: Months" in the format 3, 5, 8-10, 12.')
                return None
            self.filter_data['months_uploaded'] = {'include': True, 'values': months}
        else:
            self.delete_filter('months_uploaded')
        
        if self.weekdays_uploaded_box.isChecked():
            weekdays = []
            for i, cb in enumerate(self.weekdays_uploaded_checkboxes):
                if cb.isChecked():
                    weekdays.append(i)
            self.filter_data['weekdays_uploaded'] = {'include': True, 'values': weekdays}
        else:
            self.delete_filter('weekdays_uploaded')
        
        super().accept()
    
    def delete_filter(self, filter_name):
        if filter_name in self.filter_data.keys():
            del self.filter_data[filter_name]
    
    def initialize_widgets(self, filters):
        self.filter_data = filters
        self.reset_widgets()
        for key, value in self.filter_data.items():
            include = value['include']
            match key:
                # ---------- Property filters ---------- #
                case 'title':
                    self.title_cb.setChecked(True)
                    self.title_combo.setCurrentIndex(not include)  # 0 = contains, 1 = does not contain
                    self.title_regex_cb.setChecked(value['regex'])
                    self.title_edit.setText(value['value'])
                case 'channel':
                    self.channel_cb.setChecked(True)
                    self.channel_combo.setCurrentIndex(not include)
                    self.channel_regex_cb.setChecked(value['regex'])
                    self.channel_edit.setText(value['value'])
                case 'total_views':
                    self.views_cb.setChecked(True)
                    self.views_combo.setCurrentIndex(not include)
                    self.views_min.setValue(value['range'][0])
                    self.views_max.setValue(value['range'][1])
                case 'user_views':
                    self.userviews_cb.setChecked(True)
                    self.userviews_combo.setCurrentIndex(not include)
                    self.userviews_min.setValue(value['range'][0])
                    self.userviews_max.setValue(value['range'][1])
                case 'user_channel_views':
                    self.userviews_channel_cb.setChecked(True)
                    self.userviews_channel_combo.setCurrentIndex(not include)
                    self.userviews_channel_min.setValue(value['range'][0])
                    self.userviews_channel_max.setValue(value['range'][1])
                case 'languages':
                    self.languages_cb.setChecked(True)
                    self.languages_combo.setCurrentIndex(not include)
                    self.languages_edit.setText(value['values'])
                case 'duration':
                    self.duration_cb.setChecked(True)
                    self.duration_combo.setCurrentIndex(not include)
                    self.duration_min.setTime(QTime.fromMSecsSinceStartOfDay(value['range'][0] * 1000))
                    self.duration_max.setTime(QTime.fromMSecsSinceStartOfDay(value['range'][1] * 1000))
                case 'platform':
                    yt = value['youtube']
                    yt_music = value['music']
                    if yt and yt_music:
                        self.platform_both_rb.setChecked(True)
                    elif yt_music and not yt:
                        self.music_rb.setChecked(True)
                    elif yt and not yt_music:
                        self.youtube_rb.setChecked(True)
                case 'availability':
                    available = value['available']
                    deleted = value['deleted']
                    if available and deleted:
                        self.availability_both_rb.setChecked(True)
                    elif not available and deleted:
                        self.deleted_rb.setChecked(True)
                    elif available and not deleted:
                        self.available_rb.setChecked(True)
                
                # ---------- Watched time filters ---------- #
                case 'date_watched':
                    self.date_watched_box.setChecked(True)
                    self.date_watched_from.setDate(value['range'][0])
                    self.date_watched_to.setDate(value['range'][1])
                    if include:
                        self.date_watched_include_rb.setChecked(True)
                    else:
                        self.date_watched_exclude_rb.setChecked(True)
                case 'time_watched':
                    self.time_watched_box.setChecked(True)
                    self.watched_time_range_min_edit.setTime(value['range'][0])
                    self.watched_time_range_max_edit.setTime(value['range'][1])
                    if include:
                        self.watched_time_range_include_rb.setChecked(True)
                    else:
                        self.watched_time_range_exclude_rb.setChecked(True)
                case 'days_of_month_watched':
                    self.days_of_month_watched_box.setChecked(True)
                    self.days_of_month_watched_edit.setText(value['values'])
                case 'months_watched':
                    self.months_watched_box.setChecked(True)
                    self.months_watched_edit.setText(value['values'])
                case 'weekdays_watched':
                    self.weekdays_watched_box.setChecked(True)
                    for i, cb in enumerate(self.weekdays_watched_checkboxes):
                        if i in value['values']:
                            cb.setChecked(True)
                        else:
                            cb.setChecked(False)
                
                # ---------- Uploaded time filters ---------- #
                case 'date_uploaded':
                    self.date_uploaded_box.setChecked(True)
                    self.date_uploaded_from.setDate(value['range'][0])
                    self.date_uploaded_to.setDate(value['range'][1])
                    if include:
                        self.date_uploaded_include_rb.setChecked(True)
                    else:
                        self.date_uploaded_exclude_rb.setChecked(True)
                case 'time_uploaded':
                    self.time_uploaded_box.setChecked(True)
                    self.uploaded_time_range_min_edit.setTime(value['range'][0])
                    self.uploaded_time_range_max_edit.setTime(value['range'][1])
                    if include:
                        self.uploaded_time_range_include_rb.setChecked(True)
                    else:
                        self.uploaded_time_range_exclude_rb.setChecked(True)
                case 'days_of_month_uploaded':
                    self.days_of_month_uploaded_box.setChecked(True)
                    self.days_of_month_uploaded_edit.setText(value['values'])
                case 'months_uploaded':
                    self.months_uploaded_box.setChecked(True)
                    self.months_uploaded_edit.setText(value['values'])
                case 'weekdays_uploaded':
                    self.weekdays_uploaded_box.setChecked(True)
                    for i, cb in enumerate(self.weekdays_uploaded_checkboxes):
                        if i in value['values']:
                            cb.setChecked(True)
                        else:
                            cb.setChecked(False)
    
    def reset_widgets(self):
        # ---------- Property filters ---------- #
        self.title_cb.setChecked(False)
        self.title_combo.setCurrentIndex(0)
        self.title_regex_cb.setChecked(False)
        self.title_edit.setText('')
        
        self.channel_cb.setChecked(False)
        self.channel_combo.setCurrentIndex(0)
        self.channel_regex_cb.setChecked(False)
        self.channel_edit.setText('')
        
        self.views_cb.setChecked(False)
        self.views_combo.setCurrentIndex(0)
        self.views_min.setValue(0)
        self.views_max.setValue(0)
        
        self.userviews_cb.setChecked(False)
        self.userviews_combo.setCurrentIndex(0)
        self.userviews_min.setValue(0)
        self.userviews_max.setValue(0)
        
        self.userviews_channel_cb.setChecked(False)
        self.userviews_channel_combo.setCurrentIndex(0)
        self.userviews_channel_min.setValue(0)
        self.userviews_channel_max.setValue(0)
        
        self.languages_cb.setChecked(False)
        self.languages_combo.setCurrentIndex(0)
        self.languages_edit.setText('')
        
        self.duration_cb.setChecked(False)
        self.duration_combo.setCurrentIndex(0)
        self.duration_min.setTime(time(0, 0, 0))
        self.duration_max.setTime(time(0, 0, 0))
        
        self.platform_both_rb.setChecked(True)
        self.availability_both_rb.setChecked(True)
        
        # ---------- Watched time filters ---------- #
        self.date_watched_box.setChecked(False)
        self.date_watched_from.setDateTime(self.minimum_datetime)
        self.date_watched_to.setDateTime(self.maximum_datetime)
        self.date_watched_include_rb.setChecked(True)
        
        self.time_watched_box.setChecked(False)
        self.watched_time_range_min_edit.setTime(QTime(0, 0, 0))
        self.watched_time_range_max_edit.setTime(QTime(23, 59, 59))
        self.watched_time_range_include_rb.setChecked(True)
        
        self.days_of_month_watched_box.setChecked(False)
        self.days_of_month_watched_edit.setText('')
        
        self.months_watched_box.setChecked(False)
        self.months_watched_edit.setText('')
        
        self.weekdays_watched_box.setChecked(False)
        for cb in self.weekdays_watched_checkboxes:
            cb.setChecked(True)
        
        # ---------- Uploaded time filters ---------- #
        self.date_uploaded_box.setChecked(False)
        self.date_uploaded_from.setDateTime(self.minimum_datetime)
        self.date_uploaded_to.setDateTime(self.maximum_datetime)
        self.date_uploaded_include_rb.setChecked(True)
        
        self.time_uploaded_box.setChecked(False)
        self.uploaded_time_range_min_edit.setTime(QTime(0, 0, 0))
        self.uploaded_time_range_max_edit.setTime(QTime(23, 59, 59))
        self.uploaded_time_range_include_rb.setChecked(True)
        
        self.days_of_month_uploaded_box.setChecked(False)
        self.days_of_month_uploaded_edit.setText('')
        
        self.months_uploaded_box.setChecked(False)
        self.months_uploaded_edit.setText('')
        
        self.weekdays_uploaded_box.setChecked(False)
        for cb in self.weekdays_uploaded_checkboxes:
            cb.setChecked(True)
    
    def set_row_diabled(self, row_index, enabled):
        for i in range(self.properties_grid.count()):
            item = self.properties_grid.itemAt(i)
            pos = self.properties_grid.getItemPosition(i)
            if pos[0] == row_index and pos[1] > 0:
                widget = item.widget()
                if widget:
                    widget.setEnabled(enabled)
                else:
                    layout = item.layout()
                    if layout:
                        for j in range(layout.count()):
                            sub_item = layout.itemAt(j)
                            widget = sub_item.widget()
                            if widget:
                                widget.setEnabled(enabled)


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('About YouTube History Visualizer')
        
        self.vbox = QtWidgets.QVBoxLayout()
        self.license_text = '''Copyright (C) 2026  leonhardw
<br>
Source code available on <a href="https://github.com/leonhardw/YouTube-History-Visualizer">GitHub</a>
<br><br>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <a href="https://www.gnu.org/licenses/">&lt;https://www.gnu.org/licenses/&gt;</a>.'''
        self.license_label = QLabel()
        self.license_label.setTextFormat(Qt.RichText)
        self.license_label.setWordWrap(True)
        self.license_label.setText(self.license_text)
        self.license_label.setOpenExternalLinks(True)
        
        self.hbox = QHBoxLayout()
        self.about_qt_btn = QPushButton('About Qt')
        self.about_qt_btn.clicked.connect(self.show_about_qt_dialog)
        
        self.close_btn = QPushButton('Close')
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setDefault(True)
        
        self.hbox.addWidget(self.about_qt_btn)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.close_btn)
        
        self.vbox.addWidget(self.license_label)
        self.vbox.addLayout(self.hbox)
        
        self.setLayout(self.vbox)
    
    def show_about_qt_dialog(self):
        QMessageBox.aboutQt(self, 'About Qt')
