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
from ..res.ui.deck_options import Ui_DeckOptions


class DeckOptions(QWidget):
    def __init__(self, deck_config):
        super().__init__(flags=mw.windowFlags())
        self.ui = Ui_DeckOptions()
        self.ui.setupUi(DeckOptions=self)

        self.reverse_widget = ReverseWidget(mw.windowFlags())
        self.ui.leech_actions_widget = ActionsWidget(deck_config, Config.LEECH_ACTIONS, expanded=False)
        self.ui.reverse_actions_widget = ActionsWidget(deck_config, Config.REVERSE_ACTIONS, expanded=False)

        self.ui.scrollAreaLayout.addWidget(self.reverse_widget)
        self.ui.scrollAreaLayout.addWidget(self.ui.leech_actions_widget)
        self.ui.scrollAreaLayout.addWidget(self.ui.reverse_actions_widget)

        self.ui.leech_actions_widget.load()
        self.ui.reverse_actions_widget.load()


def build_hooks():
    from aqt.gui_hooks import deck_conf_did_setup_ui_form

    deck_conf_did_setup_ui_form.append(setup_deck_options)
    # deck_conf_did_load_config.append()
    # deck_conf_will_save_config.append()


def setup_deck_options(deckconf: DeckConf):
    form = deckconf.form
    config_manager = LeechToolkitConfigManager(mw)
    deck_config = config_manager.config_for_did(deckconf.deck['id'])

    tab_options = DeckOptions(deck_config)

    tab_widget = form.tabWidget
    for i in range(tab_widget.count()):
        if tab_widget.tabText(i) == tr.scheduling_lapses():
            print(f' wid: {tab_widget.tabText(i)}')
            tab_widget.insertTab(i + 1, tab_options, 'Leech Toolkit')

    # form.tabWidget.insertTab()

# On Save: Only write to global config if [key]-enabled is true else remove
