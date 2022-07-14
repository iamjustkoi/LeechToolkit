"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt import mw
from aqt.qt import QAction, QDialog

from .config import LeechToolkitConfigManager
from .consts import String, Config
from ..res.ui.options_dialog import Ui_OptionsDialog


def bind_actions():
    _bind_config_options()
    _bind_tools_options()


def on_options_called(result=False):
    options = OptionsDialog(LeechToolkitConfigManager(mw))
    options.exec()


def _bind_tools_options(changes=None, obj=None):
    """
Updates the toolbar actions menu with the options shortcut. Expects an Operation Change hook call,
but can also be used as a general update push, too.
    :param changes: unused OpChanges object
    :param obj: unused options object
    """
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


def _bind_config_options():
    mw.addonManager.setConfigAction(__name__, on_options_called)


class OptionsDialog(QDialog):

    def __init__(self, manager: LeechToolkitConfigManager):
        super().__init__(flags=manager.mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self._load()

    def _load(self):
        self.ui.toolsOptionsCheckBox.setChecked(self.config[Config.TOOLBAR_ENABLED])
        self.ui.almostMarkCheckbox.setChecked(self.config[Config.SHOW_ALMOST_LEECH_MARKER])
        self.ui.almostPosDropdown.setCurrentIndex(self.config[Config.ALMOST_MARKER_POSITION])

    def _save(self):
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()
        self.config[Config.SHOW_ALMOST_LEECH_MARKER] = self.ui.almostMarkCheckbox.isChecked()
        self.config[Config.ALMOST_MARKER_POSITION] = self.ui.almostPosDropdown.currentIndex()
        self.manager.write_config()

    def accept(self) -> None:
        self._save()
        super().accept()
        bind_actions()
