"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt import mw
from aqt import tr
from aqt.deckconf import DeckConf
from aqt.qt import (
    QWidget,
)

from .config import LeechToolkitConfigManager
from .consts import Config, Action
from .options import ActionsWidget
from .options import ReverseWidget
from ..res.ui.deck_options_form import Ui_DeckOptionsPlaceholder


def filter_enabled_actions(actions_conf: dict):
    result = {}
    for key in actions_conf.keys():
        if actions_conf[key][Action.ENABLED]:
            result[key] = actions_conf[key]
    return result


class DeckOptions(QWidget):
    def __init__(self, did: int):
        super().__init__(flags=mw.windowFlags())
        self.did = did
        self.ui = Ui_DeckOptionsPlaceholder()
        self.ui.setupUi(DeckOptionsPlaceholder=self)

        self.reverse_form = ReverseWidget(mw.windowFlags())
        self.leech_actions_form = ActionsWidget(Config.LEECH_ACTIONS, expanded=False)
        self.reverse_actions_form = ActionsWidget(Config.UN_LEECH_ACTIONS, expanded=False)

        self.ui.scrollAreaLayout.addWidget(self.reverse_form)
        self.ui.scrollAreaLayout.addWidget(self.leech_actions_form)
        self.ui.scrollAreaLayout.addWidget(self.reverse_actions_form)

    def load(self):
        manager = LeechToolkitConfigManager(mw)
        deck_config = manager.placeholder_config_for_did(self.did)

        self.leech_actions_form.load(deck_config[Config.LEECH_ACTIONS])
        self.reverse_actions_form.load(deck_config[Config.UN_LEECH_ACTIONS])
        self.reverse_form.load(deck_config[Config.REVERSE_OPTIONS])

    def save(self):
        manager = LeechToolkitConfigManager(mw)
        deck_config = manager.placeholder_config_for_did(self.did)

        self.leech_actions_form.save(deck_config[Config.LEECH_ACTIONS])
        deck_config[Config.LEECH_ACTIONS] = filter_enabled_actions(deck_config[Config.LEECH_ACTIONS])
        deck_config.pop(Config.LEECH_ACTIONS, None) if len(deck_config[Config.LEECH_ACTIONS]) <= 0 else None

        self.reverse_actions_form.save(deck_config[Config.UN_LEECH_ACTIONS])
        deck_config[Config.UN_LEECH_ACTIONS] = filter_enabled_actions(deck_config[Config.UN_LEECH_ACTIONS])
        deck_config.pop(Config.UN_LEECH_ACTIONS, None) if len(deck_config[Config.UN_LEECH_ACTIONS]) <= 0 else None

        self.reverse_form.save(deck_config[Config.REVERSE_OPTIONS])
        if not deck_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
            deck_config.pop(Config.REVERSE_OPTIONS, None)

        # Garbage Collection
        config_id = str(mw.col.decks.config_dict_for_deck_id(self.did)['id'])
        if len(deck_config) <= 0:
            manager.config.pop(config_id, None)
        else:
            manager.config[config_id] = deck_config

        manager.write_config()


def build_hooks():
    from aqt.gui_hooks import deck_conf_did_setup_ui_form
    from aqt.gui_hooks import deck_conf_did_load_config
    from aqt.gui_hooks import deck_conf_will_save_config

    deck_conf_did_setup_ui_form.append(setup_deck_options)
    deck_conf_did_load_config.append(load_deck_options)
    deck_conf_will_save_config.append(save_deck_options)


def setup_deck_options(deckconf: DeckConf):
    form = deckconf.form
    form.tab_options = DeckOptions(deckconf.deck['id'])

    tab_widget = form.tabWidget
    for i in range(tab_widget.count()):
        if tab_widget.tabText(i) == tr.scheduling_lapses():
            tab_widget.insertTab(i + 1, form.tab_options, 'Leech Toolkit')


def load_deck_options(deckconf: DeckConf, *args):
    form = deckconf.form
    form.tab_options.load()


def save_deck_options(deckconf: DeckConf, *args):
    form = deckconf.form
    form.tab_options.save()

# On Save: Only write to global config if [key]-enabled is true else remove
