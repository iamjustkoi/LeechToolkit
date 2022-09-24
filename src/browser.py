"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""

import re

import aqt.browser
from anki.collection import Collection
from aqt import gui_hooks, mw
from aqt.qt import (
    QDialog,
    QDialogButtonBox,
)
from aqt.utils import (
    skip_if_selection_is_empty,
    ensure_editor_saved,
)

from .config import LeechToolkitConfigManager
from .consts import MENU_CARDS_TEXT
from ..res.ui.set_lapse_dialog import Ui_SetLapseDialog

TOOLKIT_ACTIONS = 'Too&lkit Actions'
ACTION_LEECH = '&Leech'
ACTION_UNLEECH = '&Un-leech'
ACTION_SET_LAPSES = '&Set Lapses...'
STORED_LAPSE_INPUT = 'storedLapseInput'


def build_hooks():
    gui_hooks.browser_menus_did_init.append(init_browser)


def _get_menu(menu_bar: aqt.qt.QMenuBar, menu_text):
    for action in menu_bar.actions():
        if action.text() == menu_text:
            return action.parent()
    return menu_bar.addMenu(menu_text)


def init_browser(browser: aqt.browser.Browser):
    menu_bar = browser.menuBar()
    menu = _get_menu(menu_bar, MENU_CARDS_TEXT)
    menu.addSeparator()
    sub_menu = menu.addMenu(TOOLKIT_ACTIONS)
    sub_menu.addAction(ACTION_LEECH)
    sub_menu.addAction(ACTION_UNLEECH)
    menu.addAction(ACTION_SET_LAPSES, lambda *args: set_lapses(browser))


def set_lapses(browser: aqt.browser.Browser):
    dialog = SetLapseDialog(LeechToolkitConfigManager(mw), browser)
    dialog.exec()


def leech():
    pass


def unleech():
    pass


class SetLapseDialog(QDialog):
    def __init__(self, manager: LeechToolkitConfigManager, browser: aqt.browser.Browser):
        super().__init__(flags=mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.browser = browser
        self.table = browser.table
        self.editor = browser.editor
        self.ui = Ui_SetLapseDialog()
        self.ui.setupUi(SetLapseDialog=self)

        def on_text_changed(text: str):
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(re.search(r'\d', text.strip()) is not None)

        self.ui.lineEdit.textChanged.connect(on_text_changed)

        self.ui.lineEdit.setValidator(aqt.qt.QRegExpValidator(aqt.qt.QRegExp(r'(\d*|\s*|((\+|-|\/|\*)(\d|\s)))*')))
        self.ui.lineEdit.setText(self.config.get(STORED_LAPSE_INPUT, ''))

    @skip_if_selection_is_empty
    @ensure_editor_saved
    def accept(self):
        line_text = self.ui.lineEdit.text().strip()

        cards = []
        for cid in self.browser.selectedCards():
            card = mw.col.get_card(cid)
            card.lapses = int(eval(f'{card.lapses if line_text[0] in "*/+-" else ""}{line_text}'))
            cards.append(card)
        Collection.update_cards(self.browser.col, cards)

        self.table.reset()
        self.config[STORED_LAPSE_INPUT] = line_text
        self.manager.save_config()
        self.close()
