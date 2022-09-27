"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt import dialogs, mw
from aqt.deckbrowser import DeckBrowserBottomBar
from aqt.overview import OverviewBottomBar
from aqt.toolbar import BottomBar

from .config import LeechToolkitConfigManager
from .consts import String, Config, LEECH_TAG, LEECHES_URL

leech_search_flag = f'tag:{LEECH_TAG}'


def build_bottom_bar():

    def draw_bottom_bar(self, buf: str, web_context, link_handler):
        """
        Custom handler for drawing Anki's bottom bar.
        :param self: Anki window/QT object
        :param buf: base string buffer for the bottom bar's html
        :param web_context: Anki's current page context
        :param link_handler: base link handler for buttons
        :return: custom bottom bar
        """
        if isinstance(web_context, (OverviewBottomBar, DeckBrowserBottomBar)):
            deck_search_flag = 'deck:current' if mw.state == 'overview' else 'deck:*'
            total_leeches = len(mw.col.find_cards(f'{leech_search_flag} {deck_search_flag}'))

            if total_leeches > 0:
                default_link_handler = link_handler

                def leech_link_handler(url):
                    """
                Custom link handler that adds functionality for the run_action-browse button's link.
                    :param url: passed url string to handle
                    """
                    if url == LEECHES_URL:
                        dialogs.open("Browser", mw, search=(leech_search_flag, deck_search_flag))

                    default_link_handler(url=url)

                def updated_buf(default_buf):
                    """
                Formats and returns a custom html string.
                    :param default_buf: referenced buffer
                    :return: formatted string-buffer with new or removed html elements
                    """
                    button_conf = LeechToolkitConfigManager(mw).config[Config.BUTTON_OPTIONS]
                    button_html = BarButton(String.VIEW_LEECHES, LEECHES_URL).html
                    if button_conf[Config.SHOW_BUTTON]:
                        if isinstance(web_context, OverviewBottomBar) and button_conf[Config.SHOW_OVERVIEW_BUTTON]:
                            return '\n'.join([default_buf, button_html])
                        elif isinstance(web_context, DeckBrowserBottomBar) and button_conf[Config.SHOW_BROWSER_BUTTON]:
                            return '\n'.join([default_buf, button_html])
                    return default_buf.replace(button_html, '')

                return default_draw(
                    self,
                    buf=updated_buf(buf),
                    web_context=web_context,
                    link_handler=leech_link_handler
                )

        return default_draw(
            self,
            buf=buf,
            web_context=web_context,
            link_handler=link_handler
        )

    # Swap default/current and custom draw methods
    default_draw = BottomBar.draw
    BottomBar.draw = draw_bottom_bar


class BarButton:
    def __init__(self, text: str, cmd: str, shortcut_key=None):
        attributes = f'onclick="pycmd(\'{cmd}\')"'
        attributes += f' title="{String.BUTTON_SHORTCUT_HINT}: {shortcut_key}"' if shortcut_key else ''
        self.html = f'<button {attributes}>{text}</button>'
