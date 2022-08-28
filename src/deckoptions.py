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
from .consts import Config
from .options import ActionsWidget
from .options import ReverseWidget
from ..res.ui.deck_options_form import Ui_DeckOptionsPlaceholder


class DeckOptions(QWidget):
    def __init__(self, did: int):
        super().__init__(flags=mw.windowFlags())
        self.did = did
        self.ui = Ui_DeckOptionsPlaceholder()
        self.ui.setupUi(DeckOptionsPlaceholder=self)

        self.reverse_widget = ReverseWidget(mw.windowFlags())
        self.leech_actions_widget = ActionsWidget(Config.LEECH_ACTIONS, expanded=False)
        self.reverse_actions_widget = ActionsWidget(Config.REVERSE_ACTIONS, expanded=False)

        self.ui.scrollAreaLayout.addWidget(self.reverse_widget)
        self.ui.scrollAreaLayout.addWidget(self.leech_actions_widget)
        self.ui.scrollAreaLayout.addWidget(self.reverse_actions_widget)

    def load(self):
        manager = LeechToolkitConfigManager(mw)
        deck_config = manager.default_config_for_did(self.did)

        self.leech_actions_widget.load(deck_config)
        self.reverse_actions_widget.load(deck_config)
        self.reverse_widget.load(deck_config)

    def save(self):
        deck_config = {}

        self.leech_actions_widget.save(deck_config, True)
        self.reverse_actions_widget.save(deck_config, True)
        self.reverse_widget.save(deck_config, True)

        manager = LeechToolkitConfigManager(mw)
        config_id = str(mw.col.decks.config_dict_for_deck_id(self.did)['id'])

        # Garbage Collection
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
    print(f'deck save hook')
    form = deckconf.form
    form.tab_options.save()

# On Save: Only write to global config if [key]-enabled is true else remove
