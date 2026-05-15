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

import locale
import sys
from datetime import datetime, date, time

from PySide6.QtCore import Qt, QAbstractTableModel, QUrl
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtWidgets import (QApplication, QDialog, QTableView, QFileDialog,
                               QAbstractItemView, QMenu, QVBoxLayout, QCheckBox, QHeaderView, QGridLayout, QPushButton, QHBoxLayout, QMessageBox)

from utils.export_data import save_as_csv

locale.setlocale(locale.LC_ALL, '')

from PySide6.QtCore import QSortFilterProxyModel  # Neu importieren


# 1. Erstelle eine neue Klasse für die Filter-Logik
class CustomFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._filter_text = ""
    
    def setFilterText(self, text):
        self._filter_text = text.lower()
        self.invalidateFilter()  # Erzwingt Neu-Filterung
    
    def filterAcceptsRow(self, source_row, source_parent):
        if not self._filter_text:
            return True
        
        # Wir prüfen Spalte 3 und Spalte 5 (Index 2 und 4)
        # Beachte: Index ist 0-basiert. Spalte 3 -> Index 2, Spalte 5 -> Index 4
        model = self.sourceModel()
        
        # Hole Daten aus dem Quell-Modell
        val_col3 = str(model.index(source_row, 2, source_parent).data()).lower()
        val_col5 = str(model.index(source_row, 4, source_parent).data()).lower()
        
        return self._filter_text in val_col3 or self._filter_text in val_col5


class ExtendedTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier or event.angleDelta().x() != 0:
            
            delta = event.angleDelta().y() if event.modifiers() == Qt.KeyboardModifier.ShiftModifier else event.angleDelta().x()
            
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta)
            event.accept()
        else:
            super().wheelEvent(event)


class TableViewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Table view')
        self.resize(800, 600)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowMaximizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        
        self.base_model = None
        self.raw_data = None
        
        self.vbox_layout = QVBoxLayout()
        self.table_view = ExtendedTableView()
        
        self.table_view.setSortingEnabled(True)
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.table_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_view.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.verticalHeader().setDefaultSectionSize(25)
        
        header = self.table_view.horizontalHeader()
        header.setSectionsMovable(True)
        header.setSectionsClickable(True)
        
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.show_header_menu)
        self.table_view.doubleClicked.connect(self.open_link)
        
        self.grid_layout = QGridLayout()
        
        self.hbox = QHBoxLayout()
        
        self.ok_btn = QPushButton('OK')
        self.export_as_csv_btn = QPushButton('Export as CSV')
        
        self.ok_btn.clicked.connect(self.accept)
        self.export_as_csv_btn.clicked.connect(self.export_as_csv)
        
        self.hbox.addWidget(self.export_as_csv_btn)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.ok_btn)
        
        self.vbox_layout.addLayout(self.grid_layout)
        self.vbox_layout.addWidget(self.table_view)
        self.vbox_layout.addLayout(self.hbox)
        self.setLayout(self.vbox_layout)
    
    def export_as_csv(self):
        file_filters = 'CSV files (*.csv);;All files (*.*)'
        filename, _ = QFileDialog.getSaveFileName(self, 'Export CSV as...', filter=file_filters)
        if filename:
            save_as_csv(filename, self.raw_data)
            QMessageBox.information(self, 'Success', 'Successfully exported as CSV.')
    
    def open_link(self, index):
        row = index.row()
        col = index.column()
        if col in [0, 1, 2, 3, 4]:
            data = self.base_model.data(index)
            match col:
                case 0 | 4:
                    link = data
                case 1 | 2:
                    link = self.base_model.data(index.sibling(row, 0))
                case 3:
                    link = self.base_model.data(index.sibling(row, 4))
            if link and str(link).startswith('http'):
                QDesktopServices.openUrl(QUrl(link))
    
    def set_column_widths(self, widths):
        for i, new_width in enumerate(widths):
            self.table_view.setColumnWidth(i, new_width)
    
    def import_data(self, data, hide_columns=None, sort_by_index=None, sort_by_str=None, sort_ascending=False):
        self.raw_data = data
        header_labels = data[0]
        data_sorting_index = None
        if sort_by_index is not None:
            data_sorting_index = sort_by_index
        else:
            if sort_by_str:
                data_sorting_index = header_labels.index(sort_by_str)
        self.base_model = FastTableModel(data)
        self.table_view.setModel(self.base_model)
        
        self.table_view.setSortingEnabled(True)
        if data_sorting_index is not None:
            self.base_model.sort(data_sorting_index, Qt.AscendingOrder if sort_ascending else Qt.DescendingOrder)
            self.table_view.horizontalHeader().setSortIndicator(data_sorting_index, Qt.AscendingOrder if sort_ascending else Qt.DescendingOrder)
        
        if hide_columns is not None:
            column_count = self.base_model.columnCount()
            for i in range(column_count):
                self.table_view.showColumn(i)
            
            for i in hide_columns:
                self.table_view.hideColumn(header_labels.index(i))
        self.create_checkboxes(header_labels)
        
        # self.table_view.resizeColumnsToContents()
    
    def show_header_menu(self, pos):
        menu = QMenu(self)
        column_count = self.base_model.columnCount()
        
        for i in range(column_count):
            header_text = self.base_model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            action = QAction(str(header_text), menu)
            action.setCheckable(True)
            action.setChecked(not self.table_view.isColumnHidden(i))
            action.toggled.connect(lambda checked, idx=i: self.toggle_column(idx, checked))
            menu.addAction(action)
        
        menu.exec(self.table_view.horizontalHeader().mapToGlobal(pos))
    
    def toggle_column(self, index, checked, is_cb=False):
        if checked:
            self.table_view.showColumn(index)
        else:
            self.table_view.hideColumn(index)
        if not is_cb:
            self.grid_layout.itemAt(index).widget().setChecked(checked)
    
    def create_checkboxes(self, headers):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        for i, header in enumerate(headers):
            new_cb = QCheckBox(header)
            new_cb.toggled.connect(lambda checked, idx=i: self.toggle_column(idx, checked, True))
            new_cb.setChecked(not self.table_view.isColumnHidden(i))
            row, col = divmod(i, 8)
            self.grid_layout.addWidget(new_cb, row, col)


class FastTableModel(QAbstractTableModel):
    def __init__(self, data_list):
        super().__init__()
        self._headers = data_list[0]
        self._data = []
        for row in data_list[1:]:
            processed_row = []
            for val in row:
                processed_row.append(val)
            self._data.append(processed_row)
    
    def rowCount(self, parent=None):
        return len(self._data)
    
    def columnCount(self, parent=None):
        return len(self._headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.TextAlignmentRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, (int, float)):
                if type(value) is bool:
                    return Qt.AlignLeft | Qt.AlignVCenter
                return Qt.AlignRight | Qt.AlignVCenter
            else:
                return Qt.AlignLeft | Qt.AlignVCenter
        
        if role == Qt.DisplayRole:
            data_to_display = self._data[index.row()][index.column()]
            if type(data_to_display) is datetime:
                data_to_display = data_to_display.strftime('%Y-%m-%d %H:%M:%S')
            elif type(data_to_display) is date:
                data_to_display = data_to_display.strftime('%Y-%m-%d')
            elif type(data_to_display) is time:
                data_to_display = data_to_display.strftime('%H:%M:%S')
            elif type(data_to_display) is bool:
                data_to_display = 'Yes' if data_to_display else 'No'
            elif isinstance(data_to_display, (int, float)):
                data_to_display = f'{data_to_display:n}'
            return str(data_to_display) if data_to_display is not None else 'None'
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section < len(self._headers):
                return self._headers[section]
        return None
    
    def sort(self, column: int, order: Qt.SortOrder = Qt.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        reverse = (order == Qt.DescendingOrder)
        
        try:
            self._data.sort(key=lambda x: float(x[column]) if x[column] else 0, reverse=reverse)
        except (ValueError, TypeError):
            self._data.sort(key=lambda x: str(x[column]), reverse=reverse)
        
        self.layoutChanged.emit()


def test_dialog():
    app = QApplication(sys.argv)
    window = TableViewDialog()
    
    data = [['One', 'Watched at', 'Three'],
            [1, 20, 3],
            [4, 5, 6],
            [7, 30, 9]]
    window.import_data(data, hide_columns=('Three',))
    window.show()
    window.import_data(data, hide_columns=('One',))
    sys.exit(app.exec())


if __name__ == '__main__':
    test_dialog()
