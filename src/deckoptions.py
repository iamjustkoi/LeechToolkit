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

        self.reverse_form = ReverseWidget(mw.windowFlags())
        self.leech_actions_form = ActionsWidget(Config.LEECH_ACTIONS, expanded=False)
        self.reverse_actions_form = ActionsWidget(Config.UN_LEECH_ACTIONS, expanded=False)

        self.ui.scrollAreaLayout.addWidget(self.reverse_form)
        self.ui.scrollAreaLayout.addWidget(self.leech_actions_form)
        self.ui.scrollAreaLayout.addWidget(self.reverse_actions_form)

    def load(self):
        deck_conf = LeechToolkitConfigManager(mw).get_conf_for_did(self.did)
        global_conf = self.get_global_conf()

        self.leech_actions_form.load_all(deck_conf[Config.LEECH_ACTIONS], global_conf[Config.LEECH_ACTIONS])
        self.reverse_actions_form.load_all(deck_conf[Config.UN_LEECH_ACTIONS], global_conf[Config.UN_LEECH_ACTIONS])
        self.reverse_form.load(deck_conf[Config.REVERSE_OPTIONS])
        self.reverse_form.load_default(deck_conf[Config.REVERSE_OPTIONS], global_conf[Config.REVERSE_OPTIONS])

    @staticmethod
    def get_global_conf():
        # Using separate manager instances to reduce overwrite issues #bandaid-fix
        return LeechToolkitConfigManager(mw).get_global_deck_conf()

    def save(self):
        deck_conf = LeechToolkitConfigManager(mw).get_conf_for_did(self.did)

        # is not same as global: save
        self.leech_actions_form.write_all(deck_conf[Config.LEECH_ACTIONS])
        self.reverse_actions_form.write_all(deck_conf[Config.UN_LEECH_ACTIONS])
        self.reverse_form.write(deck_conf[Config.REVERSE_OPTIONS])

        def get_diffs(conf: dict, comp_conf: dict):
            result = {}
            for key in conf:
                if conf[key] != comp_conf[key]:
                    result[key] = get_diffs(conf[key], comp_conf[key]) if isinstance(conf[key], dict) else conf[key]
            return result

        manager = LeechToolkitConfigManager(mw)
        config_id = str(mw.col.decks.config_dict_for_deck_id(self.did)['id'])
        min_deck_conf = get_diffs(deck_conf, self.get_global_conf())
        if len(min_deck_conf) <= 0:
            manager.config.pop(config_id, None)
        else:
            manager.config[config_id] = min_deck_conf
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


def load_deck_options(deck_conf: DeckConf, *args):
    form = deck_conf.form
    form.tab_options.load()


def save_deck_options(deck_conf: DeckConf, *args):
    form = deck_conf.form
    form.tab_options.save()

# On Save: Only save to global config if [key]-enabled is true else remove
