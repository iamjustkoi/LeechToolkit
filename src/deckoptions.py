"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt import tr
from aqt.deckconf import DeckConf


def build_hooks():
    from aqt.gui_hooks import deck_conf_did_setup_ui_form

    deck_conf_did_setup_ui_form.append(setup_deck_options)
    # deck_conf_did_load_config.append()
    # deck_conf_will_save_config.append()


def setup_deck_options(deckconf: DeckConf):
    form = deckconf.form
    tab_widget = form.tabWidget

    for i in range(tab_widget.count()):
        if tab_widget.tabText(i) == tr.scheduling_lapses():
            print(f' wid: {tab_widget.tabText(i)}')
            tab_widget.insertTab(i + 1, )

    # form.tabWidget.insertTab()
