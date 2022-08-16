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
)

from ...src.consts import QueueAction


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
        super().paintEvent(event)
        did_elide = False
        painter = QPainter(self)
        metrics = painter.fontMetrics()

        text_width = painter.fontMetrics().horizontalAdvance(self.text())
        text_layout = QTextLayout(self._contents, painter.font())
        text_layout.beginLayout()

        line: QTextLine = text_layout.createLine()
        while line.isValid():
            line.setLineWidth(self.width())
            if text_width <= self.width():
                painter.drawText(QPoint(0, metrics.ascent()), self._contents)
                line.draw(painter, QPoint(0, 0))
            else:
                self._elided_text = metrics.elidedText(self._contents, self._mode, self.width())
                painter.drawText(QPoint(0, metrics.ascent()), self._elided_text)
                did_elide = line.isValid()
            line: QTextLine = text_layout.createLine()

        text_layout.endLayout()

        if did_elide != self.is_elided:
            self.is_elided = did_elide
            self.elision_changed.emit(did_elide)


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
