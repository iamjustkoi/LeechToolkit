import aqt
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
    QStyle,
    QStyleOptionSlider,
    QMouseEvent,
    QRect,
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

    def __init__(self, *args, tip_offset=45):
        super(QSlider, self).__init__(*args)
        style: QStyle = aqt.mw.style()
        opt = QStyleOptionSlider()

        self.global_pos = QPoint(0, 0)

        def show_tip():
            rect_handle: QRect = style.subControlRect(style.CC_Slider, opt, style.SC_SliderHandle)
            # pos = self.mapToGlobal(rect_handle.topLeft() + tip_offset)
            # pos = self.mapTo(self, rect_handle.topLeft() + tip_offset)
            x = self.global_pos.x()
            y = self.y() + self.window().y()
            pos = self.mapTo(self, QPoint(x, y))

            print(f'cood({x}, {y})')

            QToolTip.showText(pos, str(self.value()), self)

        self.valueChanged.connect(show_tip)
        # self.enterEvent = self.show_tip
        # self.mouseReleaseEvent = self.show_tip

    def mouseMoveEvent(self, evt: QMouseEvent):
        super().mouseMoveEvent(evt)
        self.global_pos = evt.globalPos()
