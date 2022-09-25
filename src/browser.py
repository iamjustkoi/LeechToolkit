"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""

import re

import anki.collection
import aqt.browser
from anki.collection import Collection
from aqt import gui_hooks, mw
from aqt.operations import CollectionOp
from aqt.qt import (
    QDialog,
    QDialogButtonBox,
)
from aqt.utils import (
    skip_if_selection_is_empty,
    ensure_editor_saved,
)

from .config import LeechToolkitConfigManager, merge_fields
from .consts import MENU_CARDS_TEXT, Config, LEECH_TAG
from .updates import run_action_updates, update_card
from ..res.ui.set_lapse_dialog import Ui_SetLapseDialog

TOOLKIT_ACTIONS = 'Too&lkit Actions'
ACTION_LEECH = '&Leech'
ACTION_UNLEECH = '&Un-Leech'
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
    manager = LeechToolkitConfigManager(mw)

    menu = _get_menu(browser.menuBar(), MENU_CARDS_TEXT)
    menu.addSeparator()

    sub_menu = menu.addMenu(TOOLKIT_ACTIONS)

    sub_menu.addAction(ACTION_LEECH, lambda *args: apply_leech_updates(manager, browser, Config.LEECH_ACTIONS))
    sub_menu.addAction(ACTION_UNLEECH, lambda *args: apply_leech_updates(manager, browser, Config.UN_LEECH_ACTIONS))

    menu.addAction(ACTION_SET_LAPSES, lambda *args: show_set_lapses(manager, browser))


# def collection_op(browser, callback_with_result):
#     if action_type in (ACTION_LEECH, ACTION_UNLEECH):
#         CollectionOp(browser, callback_with_result).success(None)


def show_set_lapses(manager: LeechToolkitConfigManager, browser: aqt.browser.Browser):
    dialog = SetLapseDialog(manager, browser)
    dialog.exec()


def apply_leech_updates(manager: LeechToolkitConfigManager, browser: aqt.browser.Browser, action_type):
    toolkit_configs = manager.get_all_configs()
    total_updates = 0

    for cid in browser.selectedCards():
        card = browser.col.get_card(cid)
        if action_type == Config.LEECH_ACTIONS:
            run_action_updates(card, toolkit_configs[str(card.did)], Config.LEECH_ACTIONS, reload=False)
            card.note().add_tag(LEECH_TAG)
        elif action_type == Config.UN_LEECH_ACTIONS:
            run_action_updates(card, toolkit_configs[str(card.did)], Config.UN_LEECH_ACTIONS, reload=False)
            card.note().remove_tag(LEECH_TAG)
        update_card(card)
        total_updates += 1

    browser.table.reset()

    if action_type == Config.LEECH_ACTIONS:
        show_update_tip('Leeched', total_updates)
    elif action_type == Config.UN_LEECH_ACTIONS:
        show_update_tip('Un-leeched', total_updates)

    # return anki.collection.OpChanges


def show_update_tip(prefix: str, total_updated: int):
    aqt.utils.tooltip(f'{prefix} {total_updated} card{"s" if total_updated != 1 else ""}')


class SetLapseDialog(QDialog):
    def __init__(self, manager: LeechToolkitConfigManager, browser: aqt.browser.Browser):
        super().__init__(parent=browser, flags=browser.windowFlags())
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

        lone_symbol_validator = aqt.qt.QRegExpValidator(aqt.qt.QRegExp(r'(\d|\s*|[+\-/*](\s*\d|\d))*'))
        self.ui.lineEdit.setValidator(lone_symbol_validator)
        self.ui.lineEdit.setText(self.config.get(STORED_LAPSE_INPUT, ''))

    @skip_if_selection_is_empty
    @ensure_editor_saved
    def accept(self):
        raw_text = self.ui.lineEdit.text()
        formatted_text = re.sub(r'(?<!\d)0*(?!\D|$)', '', self.ui.lineEdit.text().strip().replace(' ', ''))
        updated_cards = []
        for cid in self.browser.selectedCards():
            card = self.browser.col.get_card(cid)
            result = int(eval(f'{card.lapses}{formatted_text}' if formatted_text[0] in r'+-\*' else formatted_text))
            card.lapses = max(result, 0)
            updated_cards.append(card)

        self.table.reset()
        self.config[STORED_LAPSE_INPUT] = raw_text
        self.manager.save_config()
        self.close()

        show_update_tip('Updated lapse count for', len(updated_cards))

        # return anki.collection.OpChanges
