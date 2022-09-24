"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""

# from aqt.browser.browser import
import aqt.browser
from aqt import gui_hooks

from src.consts import MENU_CARDS_TEXT


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
    sub_menu = menu.addMenu('Toolkit Actions')
    sub_menu.addAction('Leech')
    sub_menu.addAction('Un-leech')
    menu.addAction('Set Lapses...')
    pass
