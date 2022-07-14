"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt.toolbar import BottomBar
from aqt.deckbrowser import DeckBrowserBottomBar
from aqt.overview import OverviewBottomBar
from aqt import gui_hooks, webview

from .consts import String


# def build_hooks():
#     gui_hooks.webview_will_set_content.append(
#         lambda content, context:
#         build_bottom_bar(content, context)
#     )


def build_bottom_bar():

    # bottom = aqt.toolbar.BottomBar
    # buf = ""
    # drawLinks = deepcopy(self.drawLinks)
    # for b in drawLinks:
    #     if b[0]:
    #         b[0] = tr.actions_shortcut_key(val=shortcut(b[0]))
    #     buf += """
    # <button title='%s' onclick='pycmd(\"%s\");'>%s</button>""" % tuple(
    #         b
    #     )
    # bottom.draw(
    #     buf=buf,
    #     link_handler=_linkHandler,
    #     web_context=DeckBrowserBottomBar(),
    # )

    def draw_bottom_bar(self, buf: str, web_context, link_handler):

        if not (isinstance(web_context, DeckBrowserBottomBar) or isinstance(web_context, OverviewBottomBar)):
            print(f'\n  NOT INSTANCE')
            return

        default_link_handler = link_handler

        edit_leech_url = 'editleeches'

        # if isinstance(bottom_bar, DeckBrowserBottomBar):
        #     print(f'\n  content: {type(bottom_bar)}')
        #     edit_button = BarButton(String.EDIT_LEECHES, edit_leech_url)
        # elif isinstance(bottom_bar, OverviewBottomBar):
        #     edit_button = BarButton(String.EDIT_LEECHES, edit_leech_url)
        #     # default_draw(url=url)

        def link_handler(url):
            if url == edit_leech_url:
                print(f'\n Editing Leeches...')
            default_link_handler(url=url)

        def updated_buf(default_buf):
            button = BarButton(String.EDIT_LEECHES, 'editleeches')
            return '\n'.join([default_buf, button.html])

        return default_draw(self, buf=updated_buf(buf), link_handler=link_handler, web_context=web_context)

    default_draw = BottomBar.draw
    BottomBar.draw = draw_bottom_bar


class BarButton:
    def __init__(self, text: str, cmd: str, shortcut_key=None):
        attributes = f'onclick="pycmd(\'{cmd}\')"'
        attributes += f' title="{String.SHORTCUT_KEY}: {shortcut_key}"' if shortcut_key else ''
        self.html = f'<button {attributes}>{text}</button>'
