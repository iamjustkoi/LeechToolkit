"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt.toolbar import BottomBar
from aqt.deckbrowser import DeckBrowserBottomBar
from aqt.overview import OverviewBottomBar
from aqt import dialogs, mw

from .consts import String


def build_bottom_bar():

    def draw_bottom_bar(self, buf: str, web_context, link_handler):
        default_link_handler = link_handler
        edit_leech_url = 'editleeches'

        def link_handler(url):
            if isinstance(web_context, (OverviewBottomBar, DeckBrowserBottomBar)) and url == edit_leech_url:
                leech_flag = 'tag:leech'
                deck_flag = 'deck:current' if isinstance(web_context, OverviewBottomBar) else 'deck:*'
                dialogs.open("Browser", mw, search=(leech_flag, deck_flag))
            default_link_handler(url=url)

        def updated_buf(default_buf):
            button = BarButton(String.VIEW_LEECHES, edit_leech_url)
            return '\n'.join([default_buf, button.html])

        return default_draw(self, buf=updated_buf(buf), link_handler=link_handler, web_context=web_context)

    default_draw = BottomBar.draw
    BottomBar.draw = draw_bottom_bar


class BarButton:
    def __init__(self, text: str, cmd: str, shortcut_key=None):
        attributes = f'onclick="pycmd(\'{cmd}\')"'
        attributes += f' title="{String.SHORTCUT_KEY}: {shortcut_key}"' if shortcut_key else ''
        self.html = f'<button {attributes}>{text}</button>'
