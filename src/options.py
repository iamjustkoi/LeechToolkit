"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from pathlib import Path

import aqt.flags
from aqt import mw
from aqt.qt import QAction, QDialog, QIcon, QPixmap, QColor, QBitmap, QSize

from .config import LeechToolkitConfigManager
from .consts import String, Config, Action
from .bottombar import build_bottom_bar
from ..res.ui.options_dialog import Ui_OptionsDialog


def bind_actions():
    _bind_config_options()
    _bind_tools_options()


def on_options_called(result=False):
    options = OptionsDialog(LeechToolkitConfigManager(mw))
    options.exec()


def _bind_config_options():
    mw.addonManager.setConfigAction(__name__, on_options_called)


def get_colored_icon(path, color):
    icon = QIcon(path)
    pixmap = icon.pixmap()
    pixmap.fill(color)
    return QIcon(pixmap)


def _bind_tools_options(*args):
    config = LeechToolkitConfigManager(mw).config
    if config[Config.TOOLBAR_ENABLED]:
        options_action = QAction(String.TOOLBAR_OPTIONS, mw)
        options_action.triggered.connect(on_options_called)
        # Handles edge cases where toolbar action already exists in the tools menu
        if options_action.text() not in [action.text() for action in mw.form.menuTools.actions()]:
            mw.form.menuTools.addAction(options_action)
    else:
        for action in mw.form.menuTools.actions():
            if action.text() == String.TOOLBAR_OPTIONS:
                mw.form.menuTools.removeAction(action)


class OptionsDialog(QDialog):

    def __init__(self, manager: LeechToolkitConfigManager):
        super().__init__(flags=manager.mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self._load()

        # Just in case
        self.ui.tabWidget.setCurrentIndex(0)

    def _load(self):
        self.ui.toolsOptionsCheckBox.setChecked(self.config[Config.TOOLBAR_ENABLED])

        self.ui.showMarkerChecbkbox.setChecked(self.config[Config.SHOW_LEECH_MARKER])
        self.ui.almostCheckbox.setChecked(self.config[Config.USE_ALMOST_MARKER])
        self.ui.almostPosDropdown.setCurrentIndex(self.config[Config.MARKER_POSITION])
        self.ui.almostBackCheckbox.setChecked(self.config[Config.ONLY_SHOW_BACK_MARKER])

        self.ui.browseButtonCheckbox.setChecked(self.config[Config.SHOW_BROWSE_BUTTON])
        self.ui.browseButtonBrowserCheckbox.setChecked(self.config[Config.BROWSE_BUTTON_ON_BROWSER])
        self.ui.browseButtonOverviewCheckbox.setChecked(self.config[Config.BROWSE_BUTTON_ON_OVERVIEW])

        self.ui.reverseCheckbox.setChecked(self.config[Config.REVERSE_ENABLED])
        self.ui.reverseMethodDropdown.setCurrentIndex(self.config[Config.REVERSE_METHOD])
        self.ui.reverseThreshold.setValue(self.config[Config.REVERSE_THRESHOLD])
        self.ui.consAnswerSpinbox.setValue(self.config[Config.REVERSE_CONS_ANS])

        # Leech Actions
        action_config = self.config[Config.LEECH_ACTIONS]

        flag_options = action_config[Action.FLAG]
        self.ui.flagCheckbox.setChecked(flag_options[Action.ENABLED])
        self.ui.flagDropdown.setCurrentIndex(flag_options[Action.FLAG_INDEX])

        flag_manager = aqt.flags.FlagManager(mw)
        for index in range(1, self.ui.flagDropdown.count()):
            flag = flag_manager.get_flag(index)
            pixmap = QPixmap(flag.icon.path)
            mask = pixmap.createMaskFromColor(QColor('black'), aqt.qt.Qt.MaskOutColor)
            pixmap.fill(QColor(flag.icon.current_color(mw.pm.night_mode())))
            pixmap.setMask(mask)
            self.ui.flagDropdown.setItemIcon(index, QIcon(pixmap))
            self.ui.flagDropdown.setItemText(index, f'{flag.label}')

    def _save(self):
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()

        self.config[Config.SHOW_LEECH_MARKER] = self.ui.showMarkerChecbkbox.isChecked()
        self.config[Config.USE_ALMOST_MARKER] = self.ui.almostCheckbox.isChecked()
        self.config[Config.MARKER_POSITION] = self.ui.almostPosDropdown.currentIndex()
        self.config[Config.ONLY_SHOW_BACK_MARKER] = self.ui.almostBackCheckbox.isChecked()

        self.config[Config.SHOW_BROWSE_BUTTON] = self.ui.browseButtonCheckbox.isChecked()
        self.config[Config.BROWSE_BUTTON_ON_BROWSER] = self.ui.browseButtonBrowserCheckbox.isChecked()
        self.config[Config.BROWSE_BUTTON_ON_OVERVIEW] = self.ui.browseButtonOverviewCheckbox.isChecked()

        self.config[Config.REVERSE_ENABLED] = self.ui.reverseCheckbox.isChecked()
        self.config[Config.REVERSE_METHOD] = self.ui.reverseMethodDropdown.currentIndex()
        self.config[Config.REVERSE_THRESHOLD] = self.ui.reverseThreshold.value()
        self.config[Config.REVERSE_CONS_ANS] = self.ui.consAnswerSpinbox.value()

        # Leech Actions
        action_config = self.config[Config.LEECH_ACTIONS]

        flag_options = action_config[Action.FLAG]
        flag_options[Action.ENABLED] = self.ui.flagCheckbox.isChecked()
        flag_options[Action.FLAG_INDEX] = self.ui.flagDropdown.currentIndex()

        self.ui.flagCheckbox.setChecked(self.config[Config.LEECH_ACTIONS][Action.FLAG][Action.ENABLED])
        self.manager.write_config()

    def accept(self) -> None:
        self._save()
        super().accept()
        bind_actions()
        mw.reset()
