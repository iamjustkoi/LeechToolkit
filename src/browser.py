"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""

import re

import anki.collection
from anki.collection import OpChanges
from aqt.operations import (
    CollectionOp,
)
from aqt.browser import Browser
from aqt import gui_hooks, mw
from aqt.qt import (
    QDialog,
    QDialogButtonBox,
    QMenuBar,
    QRegExpValidator,
    QRegExp,
)
from aqt.utils import (
    skip_if_selection_is_empty,
    ensure_editor_saved,
    tooltip,
)

from .config import LeechToolkitConfigManager, merge_fields
from .consts import MENU_CARDS_TEXT, Config, LEECH_TAG, String
from .updates import run_action_updates
from ..res.ui.set_lapse_dialog import Ui_SetLapseDialog


def build_hooks():
    gui_hooks.browser_menus_did_init.append(init_browser)


def _get_menu(menu_bar: QMenuBar, menu_text):
    for action in menu_bar.actions():
        if action.text() == menu_text:
            return action.parent()
    return menu_bar.addMenu(menu_text)


def init_browser(browser: Browser):
    manager = LeechToolkitConfigManager(mw)

    menu = _get_menu(browser.menuBar(), MENU_CARDS_TEXT)
    menu.addSeparator()

    sub_menu = menu.addMenu(String.TOOLKIT_ACTIONS)
    sub_menu.addAction(
        String.ACTION_LEECH,
        lambda *args: apply_leech_updates(manager, browser, Config.LEECH_ACTIONS)
    )
    sub_menu.addAction(
        String.ACTION_UNLEECH,
        lambda *args: apply_leech_updates(manager, browser, Config.UN_LEECH_ACTIONS)
    )

    menu.addAction(String.ACTION_SET_LAPSES, lambda *args: show_set_lapses(manager, browser))


def show_set_lapses(manager: LeechToolkitConfigManager, browser: Browser):
    dialog = SetLapseDialog(manager, browser)
    dialog.exec()


def start_collection_op(browser, op_callback, tip_message: str, count):
    op = CollectionOp(browser, op_callback)

    def reset_and_show_tip():
        browser.table.reset()
        message = tip_message.format(count) if tip_message.find('{}') >= 0 else tip_message
        tooltip(message, parent=browser)

    op.success(lambda *args: reset_and_show_tip())
    op.run_in_background()


def apply_leech_updates(manager: LeechToolkitConfigManager, browser: Browser, action_type: str, skip_undo_entry=False):
    def action_operation(col: anki.collection.Collection) -> OpChanges or None:
        toolkit_configs = manager.get_all_configs()

        changes = None
        msg = String.ENTRY_LEECH_ACTIONS if action_type == Config.UN_LEECH_ACTIONS else String.ENTRY_UNLEECH_ACTIONS
        entry = col.add_custom_undo_entry(msg)

        for cid in browser.selectedCards():
            card = col.get_card(cid)
            if action_type == Config.LEECH_ACTIONS:
                run_action_updates(card, toolkit_configs[str(card.did)], Config.LEECH_ACTIONS, reload=False)
                card.note().add_tag(LEECH_TAG)
            elif action_type == Config.UN_LEECH_ACTIONS:
                run_action_updates(card, toolkit_configs[str(card.did)], Config.UN_LEECH_ACTIONS, reload=False)
                card.note().remove_tag(LEECH_TAG)

            if not skip_undo_entry:
                # MAX 30 UNDO ENTRIES STORED #
                col.update_card(card)
                col.update_note(card.note())

                # Single update + merge also steps around the differences between Anki ~.45 and >=~.46 update functions
                changes = col.merge_undo_entries(entry)

        return changes

    if skip_undo_entry:
        return action_operation(browser.col)

    if action_type == Config.LEECH_ACTIONS:
        tip_message = String.TIP_LEECHED_TEMPLATE
    else:
        tip_message = String.TIP_UNLEECHED_TEMPLATE
    return start_collection_op(browser, lambda col: action_operation(col), tip_message, len(browser.selected_cards()))


class SetLapseDialog(QDialog):
    def __init__(self, manager: LeechToolkitConfigManager, browser: Browser):
        super().__init__(parent=browser, flags=browser.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.browser = browser

        # Used in accept function's decorators to prevent bad update interruptions
        self.table = browser.table
        self.editor = browser.editor

        self.ui = Ui_SetLapseDialog()
        self.ui.setupUi(SetLapseDialog=self)

        def on_text_changed(text: str):
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(re.search(r'\d', text.strip()) is not None)

        self.ui.lineEdit.textChanged.connect(on_text_changed)

        lone_symbol_validator = QRegExpValidator(QRegExp(r'(\d|\s*|[+\-/*](\s*\d|\d))*'))
        self.ui.lineEdit.setValidator(lone_symbol_validator)
        self.ui.lineEdit.setText(self.config.get(Config.SET_LAPSES_INPUT, ''))

        self.ui.updateLeechesCheckbox.setChecked(self.config.get(Config.SET_LAPSE_UPDATE_LEECHES, False))

    @skip_if_selection_is_empty
    @ensure_editor_saved
    def accept(self):
        raw_stripped_text = self.ui.lineEdit.text().strip()
        # Remove spaces and any duplicate/leading 0's
        formatted_text = re.sub(r'(?<!\d)0*(?!\D|$)', '', raw_stripped_text.replace(' ', ''))

        def set_lapses_operation(col: anki.collection.Collection) -> OpChanges or None:
            entry = col.add_custom_undo_entry(String.ENTRY_SET_LAPSES)
            changes = None

            # Stash all the dictionaries, but should be replaced with fewer calls based on selected cards
            toolkit_configs: dict = {}
            if self.ui.updateLeechesCheckbox.isChecked():
                for deck_name_id in col.decks.all_names_and_ids():
                    config_id = col.decks.get(deck_name_id.id)['conf']
                    toolkit_configs[f'{deck_name_id.id}'] = merge_fields(
                        self.config.get(str(config_id), {}),
                        self.config,
                    )

            for cid in self.browser.selectedCards():
                card = self.browser.col.get_card(cid)
                result = int(eval(f'{card.lapses}{formatted_text}' if formatted_text[0] in r'+-\*' else formatted_text))
                card.lapses = max(result, 0)

                if self.ui.updateLeechesCheckbox.isChecked():
                    toolkit_config = toolkit_configs.get(str(card.did), self.config)
                    reverse_conf = toolkit_config[Config.REVERSE_OPTIONS]

                    if reverse_conf[Config.REVERSE_USE_LEECH_THRESHOLD]:
                        reverse_threshold = col.decks.config_dict_for_deck_id(card.did)['lapse']['leechFails']
                    else:
                        reverse_threshold = reverse_conf[Config.REVERSE_THRESHOLD]

                    if card.lapses < reverse_threshold:
                        run_action_updates(card, toolkit_config, Config.UN_LEECH_ACTIONS, reload=False)
                        card.note().remove_tag(LEECH_TAG)
                    else:
                        run_action_updates(card, toolkit_config, Config.LEECH_ACTIONS, reload=False)
                        card.note().add_tag(LEECH_TAG)

                    # Add note update to undo logs
                    col.update_note(card.note())

                col.update_card(card)

                # Single update + merge also steps around the differences between Anki ~.45 and >=~.46 update functions
                changes = col.merge_undo_entries(entry)

            return changes

        count = len(self.browser.selectedCards())
        start_collection_op(self.browser, lambda col: set_lapses_operation(col), String.TIP_SET_LAPSES_TEMPLATE, count)

        self.config[Config.SET_LAPSES_INPUT] = raw_stripped_text
        self.config[Config.SET_LAPSE_UPDATE_LEECHES] = self.ui.updateLeechesCheckbox.isChecked()
        self.manager.save_config()
        self.close()
