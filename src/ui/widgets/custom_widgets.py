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

from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QRegularExpressionValidator, QValidator
from PySide6.QtWidgets import QDoubleSpinBox, QPushButton, QSizePolicy, QTimeEdit


class IntegerOnlyDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDecimals(0)
        self.setGroupSeparatorShown(True)
        regex = QRegularExpressionValidator(r'[0-9]+')
        self.lineEdit().setValidator(regex)
    
    def validate(self, text, pos):
        if ',' in text or '.' in text:
            return QValidator.State.Invalid, text, pos
        return super().validate(text, pos)


class StepTimeEdit(QTimeEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTime(QTime(0, 0))
        self.setWrapping(True)
        self.step_size = 1
    
    def change_step_size(self, step_size):
        self.step_size = step_size
        self.round_minutes()
    
    def stepBy(self, steps):
        section = self.currentSection()
        if section == QTimeEdit.MinuteSection or self.step_size >= 60:
            self.setTime(self.time().addSecs(steps * self.step_size * 60))
        else:
            super().stepBy(steps)
    
    def focusOutEvent(self, event):
        self.round_minutes()
        super().focusOutEvent(event)
    
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.round_minutes()
            self.clearFocus()
        else:
            super().keyPressEvent(event)
    
    def round_minutes(self):
        if self.step_size != 1:
            t = self.time()
            m = t.minute()
            new_minute = (t.minute() // self.step_size) * self.step_size
            self.setTime(QTime(t.hour(), new_minute))


class AnalysisCard(QPushButton):
    def __init__(self, text='', parent=None, *args, **kwargs):
        super().__init__(text, parent=parent)
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
