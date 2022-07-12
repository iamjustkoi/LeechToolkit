"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt.qt import QDialog

from src.config import LeechToolkitConfigManager
from res.ui.options_dialog import Ui_OptionsDialog


class OptionsDialog(QDialog):

    def __init__(self, manager: LeechToolkitConfigManager):
        super().__init__(flags=manager.mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)
