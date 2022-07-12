"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt.qt import QDialog

from . import actions
from .config import LeechToolkitConfigManager
from .consts import Config
from res.ui.options_dialog import Ui_OptionsDialog


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

    def _save(self):
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()
        self.manager.write_config()

    def accept(self) -> None:
        self._save()
        super().accept()
        actions.bind_options_actions()
