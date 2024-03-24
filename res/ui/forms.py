import re
from typing import List

import aqt
import aqt.qt
from aqt import Qt
from aqt.qt import (
    QLabel,
    QPoint,
    pyqtSignal,
    QPainter,
    QTextLayout,
    QTextLine,
    QPaintEvent,
    QSizePolicy,
    QSpinBox,
    QComboBox,
    QSlider,
    QToolTip,
    QStyleOptionSlider,
    QWidget,
    QCompleter,
)

from ...src.consts import CURRENT_QT_VER, QueueAction

if CURRENT_QT_VER == 6:
    from aqt.qt import (
        QPointF
    )

    Qt.ElideRight = Qt.TextElideMode.ElideRight
    Qt.MatchContains = Qt.MatchFlag.MatchContains
    QSizePolicy.Expanding = QSizePolicy.Policy.Expanding
    QSizePolicy.Preferred = QSizePolicy.Policy.Preferred


class ElidingLabel(QLabel):
    _contents: str
    _elided_text: str
    elision_changed = pyqtSignal(bool)
    is_elided = False

    def __init__(self, text='', mode: Qt.TextElideMode = Qt.ElideRight, **kwargs):
        """
        QLabel with automatic elision based on the label's minimum size.

        :param text: label text
        :param mode: QTextElideMode used for positioning label ellipses
        """
        super().__init__()
        self._mode = mode
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def setText(self, text: str):
        self._contents = text
        self._elided_text = text
        self.update()

    def text(self):
        return self._contents

    def elided_text(self):
        return self._elided_text

    def paintEvent(self, event: QPaintEvent):
        """
        Redraw label object to place ellipses and shorten label size to scalar.

        :param event: default event flag, used for super call
        """
        super().paintEvent(event)
        did_elide = False
        painter = QPainter(self)
        metrics = painter.fontMetrics()

        text_width = painter.fontMetrics().horizontalAdvance(self.text())
        text_layout = QTextLayout(self._contents, painter.font())
        text_layout.beginLayout()

        # Casting just to see calls a little easier and not get any psuedo-warnings
        line: QTextLine = text_layout.createLine()
        while line.isValid():
            line.setLineWidth(self.width())
            if text_width <= self.width():
                painter.drawText(QPoint(0, metrics.ascent()), self._contents)

                if CURRENT_QT_VER == 6:
                    line.draw(painter, QPointF(0, 0))
                else:
                    # noinspection PyTypeChecker
                    line.draw(painter, QPoint(0, 0))

            else:
                self._elided_text = metrics.elidedText(self._contents, self._mode, self.width())
                painter.drawText(QPoint(0, metrics.ascent()), self._elided_text)
                did_elide = line.isValid()
            line: QTextLine = text_layout.createLine()

        text_layout.endLayout()

        if did_elide != self.is_elided:
            self.is_elided = did_elide


class QueueSpinBox(QSpinBox):
    _ref_methods = (QueueAction.TOP, QueueAction.BOTTOM)
    dropdown = QComboBox()

    def __int__(self, *args):
        super.__init__(*args)

    def textFromValue(self, val):
        if self.dropdown.currentIndex() in self._ref_methods:
            return f'{"+" if val > 0 else ""}{val}'
        else:
            return str(abs(val))

    def stepBy(self, step):
        new_step = step
        if self.dropdown.currentIndex() == QueueAction.POS:
            if self.value() < 0:
                new_step = -step
            if self.value() == 0 and step < 0:
                new_step = 0
        return super(QueueSpinBox, self).stepBy(new_step)

    def formatted_value(self):
        return self.value() if self.dropdown.currentIndex() in self._ref_methods else abs(self.value())

    def refresh(self):
        self.setValue(self.value())


class TipSlider(QSlider):
    # todo the init function should accept the parent argument if we want to use pyuic6
    def __init__(self, *args):
        super(QSlider, self).__init__(*args)
        self.style = aqt.mw.style()
        self.opt = QStyleOptionSlider()

        self.valueChanged.connect(self.show_tip)
        self.sliderPressed.connect(self.show_tip)

    def show_tip(self):
        cc_slider = self.style.CC_Slider if CURRENT_QT_VER == 5 else \
            self.style.ComplexControl.CC_Slider
        sc_slider = self.style.SC_SliderHandle if CURRENT_QT_VER == 5 else \
            self.style.SubControl.SC_SliderHandle
        rect_handle = self.style.subControlRect(cc_slider, self.opt, sc_slider)
        x_offset, y_offset = ((rect_handle.width() * 1.5) * -1), -30
        x = rect_handle.right() + (self.sliderPosition() * self.rect().width() / 101) + x_offset
        y = rect_handle.top() + y_offset
        global_pos = self.mapToGlobal(QPoint(x, y))
        # noinspection PyArgumentList
        QToolTip.showText(global_pos, f'{self.value()}%')


class ExpandoWidget(QWidget):
    click_function = None

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_click_function(self, function: callable):
        self.click_function = function

    def mousePressEvent(self, event: aqt.qt.QMouseEvent) -> None:
        super(ExpandoWidget, self).mousePressEvent(event)
        if self.click_function:
            self.click_function()


class CustomCompleter(QCompleter):

    def __init__(self, parent_line_edit: aqt.qt.QLineEdit) -> None:
        QCompleter.__init__(self, aqt.qt.QStringListModel(), parent_line_edit)

        self.current_data: List[str] = []
        self.cursor_index: int or None = None
        self.cursor_item_pos: int or None = None

        self.line_edit = parent_line_edit

        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setCompletionPrefix(' ')

        def focus_event(event):
            default_focus_evt(event)
            if len(self.line_edit.text()) <= 0:
                self.complete()

        def release_event(event):
            default_release_evt(event)
            if len(self.line_edit.text()) <= 0:
                self.complete()

        default_focus_evt = self.line_edit.focusInEvent
        default_release_evt = self.line_edit.mouseReleaseEvent
        self.line_edit.focusInEvent = focus_event
        self.line_edit.mouseReleaseEvent = release_event

    def set_list(self, data: List[str]):
        self.setModel(aqt.qt.QStringListModel(data))

    def get_path_pos(self):
        return sum([len(item) for item in self.current_data[:self.cursor_index]])

    def splitPath(self, path: str) -> List[str]:
        """
        Splits the line edit's path based on a variety of filters, updates the current cursor position variables,
        and outputs a list with a single item to use as
        auto-completion suggestions.
        
        :param path: the current path to split/filter
        :return: a list containing a single string to use as a reference for completer suggestions
        """
        formatted_path = re.sub('  +', ' ', path)
        stripped_path = formatted_path.strip()
        cursor_pos = self.line_edit.cursorPosition()
        self.cursor_index = stripped_path.count(' ', 0, cursor_pos)
        self.current_data = formatted_path.strip().split(' ')
        self.cursor_item_pos = cursor_pos - self.get_path_pos()

        if formatted_path.endswith(' ') and cursor_pos >= len(formatted_path):
            self.current_data.append('')
            self.cursor_index += 1
            return ['']

        if cursor_pos == 0:
            self.current_data.insert(0, '')
            self.cursor_index = 0
            return ['']

        item_macro_pos = self.current_data[self.cursor_index].rfind('%', 1)
        if self.cursor_item_pos > item_macro_pos > 0:
            return [self.current_data[self.cursor_index][item_macro_pos:]]

        return [self.current_data[self.cursor_index]]

    def pathFromIndex(self, index: aqt.qt.QModelIndex) -> str:
        """
    Retrieves the line edit's path from the given index data.

        :param index: QModelIndex used as a reference for what to insert
        :return: the string output of the given path result
        """
        if self.cursor_index is None:
            return self.line_edit.text()

        current_item = self.current_data[self.cursor_index]
        item_macro_pos = self.current_data[self.cursor_index].rfind('%', 1)

        if self.cursor_item_pos > item_macro_pos > 0:
            self.current_data[self.cursor_index] = current_item[:item_macro_pos] + index.data()
        else:
            self.current_data[self.cursor_index] = index.data()

        def update_cursor_pos():
            raw_pos = self.get_path_pos() + len(self.current_data[:self.cursor_index])
            self.line_edit.setCursorPosition(len(self.current_data[self.cursor_index]) + raw_pos)

        # Timer to update cursor after completion (delayed)
        aqt.qt.QTimer(aqt.mw).singleShot(0, update_cursor_pos)

        return ' '.join(self.current_data)
