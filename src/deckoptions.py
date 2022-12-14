"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import traceback

from aqt import mw
from aqt.deckconf import DeckConf
from aqt.qt import (
    QWidget,
)

from .config import LeechToolkitConfigManager
from .consts import Config, ErrorMsg
from .legacy import _try_get_deck_and_child_ids
from .options import ActionsWidget
from .options import ReverseWidget
from ..res.ui.deck_options_form import Ui_DeckOptionsPlaceholder

try:
    from aqt import tr
except ImportError:
    class tr:
        @staticmethod
        def scheduling_lapses():
            return 'Lapses'


    print(f'{traceback.format_exc()}\n{ErrorMsg.MODULE_NOT_FOUND_LEGACY}')


class DeckOptions(QWidget):
    config_id: str = ''

    def __init__(self, did):
        super().__init__(flags=mw.windowFlags())
        self.ui = Ui_DeckOptionsPlaceholder()
        self.ui.setupUi(DeckOptionsPlaceholder=self)

        self.reverse_form = ReverseWidget(flags=mw.windowFlags(), global_conf=False)
        self.ui.reverseWidget.layout().addWidget(self.reverse_form)

        dids = [int(i) for i in _try_get_deck_and_child_ids(did)]

        self.leech_actions_form = ActionsWidget(Config.LEECH_ACTIONS, expanded=False, dids=dids)
        self.ui.scrollAreaLayout.addWidget(self.leech_actions_form)

        self.unleech_actions_from = ActionsWidget(Config.UN_LEECH_ACTIONS, expanded=False, dids=dids)
        self.ui.scrollAreaLayout.addWidget(self.unleech_actions_from)

    def set_config_id(self, config_id: str):
        self.config_id = config_id

    def load_ui(self):
        deck_conf = LeechToolkitConfigManager(mw).get_group_conf(self.config_id)
        self.leech_actions_form.load_ui(deck_conf[Config.LEECH_ACTIONS])
        self.unleech_actions_from.load_ui(deck_conf[Config.UN_LEECH_ACTIONS])
        self.reverse_form.load_ui(deck_conf[Config.REVERSE_OPTIONS])

    def setup_default_buttons(self):
        deck_conf = LeechToolkitConfigManager(mw).get_group_conf(self.config_id)
        global_conf = LeechToolkitConfigManager(mw).get_global_deck_conf()

        self.leech_actions_form.setup_restorables(deck_conf[Config.LEECH_ACTIONS], global_conf[Config.LEECH_ACTIONS], )
        self.unleech_actions_from.setup_restorables(
            deck_conf[Config.UN_LEECH_ACTIONS],
            global_conf[Config.UN_LEECH_ACTIONS], )
        self.reverse_form.setup_restorables(deck_conf[Config.REVERSE_OPTIONS], global_conf[Config.REVERSE_OPTIONS], )

    def save(self):
        deck_conf = LeechToolkitConfigManager(mw).get_group_conf(self.config_id)

        # is not same as global: save
        self.leech_actions_form.write_all(deck_conf[Config.LEECH_ACTIONS])
        self.unleech_actions_from.write_all(deck_conf[Config.UN_LEECH_ACTIONS])
        self.reverse_form.write(deck_conf[Config.REVERSE_OPTIONS])

        def get_diffs(conf: dict, comp_conf: dict):
            result = {}
            for key in conf:
                if conf[key] != comp_conf[key]:
                    result[key] = get_diffs(conf[key], comp_conf[key]) if isinstance(conf[key], dict) else conf[key]
            return result

        min_deck_conf = get_diffs(deck_conf, LeechToolkitConfigManager(mw).get_global_deck_conf())
        manager = LeechToolkitConfigManager(mw)

        if len(min_deck_conf) <= 0:
            manager.config.pop(self.config_id, None)
        else:
            manager.config[self.config_id] = min_deck_conf

        manager.save_config()


def build_hooks():
    from aqt.gui_hooks import deck_conf_did_setup_ui_form
    from aqt.gui_hooks import deck_conf_did_load_config
    from aqt.gui_hooks import deck_conf_will_save_config

    deck_conf_did_setup_ui_form.append(setup_deck_options)
    deck_conf_did_load_config.append(load_deck_options)
    deck_conf_will_save_config.append(save_deck_options)


def setup_deck_options(deck_conf: DeckConf):
    form = deck_conf.form
    form.tab_options = DeckOptions(deck_conf.deck['id'])

    tab_widget = form.tabWidget
    for i in range(tab_widget.count()):
        if tab_widget.tabText(i) == tr.scheduling_lapses():
            tab_widget.insertTab(i + 1, form.tab_options, 'Leech Toolkit')


def load_deck_options(deck_conf: DeckConf, deck_dict: dict, deck_conf_dict: dict):
    form = deck_conf.form
    tab_options: DeckOptions = form.tab_options
    config_id = str(deck_conf_dict["id"])
    if tab_options.config_id != config_id:
        tab_options.set_config_id(config_id)
        tab_options.load_ui()
        tab_options.setup_default_buttons()


def save_deck_options(deck_conf: DeckConf, *args):
    tab_options: DeckOptions = deck_conf.form.tab_options
    tab_options.save()

# On Save: Only save to global config if [key]-enabled is true else remove
