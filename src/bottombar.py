"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt.toolbar import BottomBar
from aqt.deckbrowser import DeckBrowserBottomBar
from aqt.overview import OverviewBottomBar
from aqt import dialogs, mw

from .consts import String, LEECHES_URL

leech_search_flag = 'tag:leech'


def build_bottom_bar():

    def draw_bottom_bar(self, buf: str, web_context, link_handler):
        if isinstance(web_context, (OverviewBottomBar, DeckBrowserBottomBar)):

            deck_search_flag = 'deck:current' if mw.state == 'overview' else 'deck:*'
            total_leeches = len(mw.col.find_cards(f'{leech_search_flag} {deck_search_flag}'))

            if total_leeches > 0:
                default_link_handler = link_handler

                def leech_link_handler(url):
                    if url == LEECHES_URL:
                        dialogs.open("Browser", mw, search=(leech_search_flag, deck_search_flag))

                    default_link_handler(url=url)

                def updated_buf(default_buf):
                    button = BarButton(String.VIEW_LEECHES, LEECHES_URL)
                    return '\n'.join([default_buf, button.html])

                return default_draw(self, buf=updated_buf(buf), link_handler=leech_link_handler, web_context=web_context)

        return default_draw(self, buf=buf, link_handler=link_handler, web_context=web_context)

    default_draw = BottomBar.draw
    BottomBar.draw = draw_bottom_bar


class BarButton:
    def __init__(self, text: str, cmd: str, shortcut_key=None):
        attributes = f'onclick="pycmd(\'{cmd}\')"'
        attributes += f' title="{String.SHORTCUT_KEY}: {shortcut_key}"' if shortcut_key else ''
        self.html = f'<button {attributes}>{text}</button>'
