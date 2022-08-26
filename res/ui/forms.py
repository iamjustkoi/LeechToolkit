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
    QStyleOptionSlider,
    QWidget,
)

from .reverse_form import Ui_ReverseForm
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

    def __init__(self, *args):
        super(QSlider, self).__init__(*args)
        self.style = aqt.mw.style()
        self.opt = QStyleOptionSlider()

        self.valueChanged.connect(self.show_tip)
        self.sliderPressed.connect(self.show_tip)

    def show_tip(self):
        rect_handle = self.style.subControlRect(self.style.CC_Slider, self.opt, self.style.SC_SliderHandle)
        x_offset, y_offset = ((rect_handle.width() * 1.5) * -1), -30
        x = rect_handle.right() + (self.sliderPosition() * self.rect().width() / 101) + x_offset
        y = rect_handle.top() + y_offset
        global_pos = self.mapToGlobal(QPoint(x, y))
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


class ReverseWidget(QWidget):
    def __init__(self, flags):
        super().__init__(flags=flags)
        self.ui = Ui_ReverseForm()
        self.ui.setupUi(self)
