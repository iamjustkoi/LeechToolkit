"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import anki.cards
from aqt import reviewer
from aqt import webview
from aqt import mw, gui_hooks

from .config import LeechToolkitConfigManager
from .consts import Config

from_lapse = 1
marker_id = 'leech_marker'
marker_text = '🩸'
marker_color = 'rgb(248, 197, 86)'
almost_leech_html = '''
<style>
    #{marker_id} {{
        color: transparent;  
        text-shadow: 0 0 0 {marker_color};
        font-size: .4em !important;
        float: right;
        display: none;
    }}
</style>
<div id="{marker_id}">{marker_text}</div>
'''


def build_hooks():
    gui_hooks.reviewer_did_show_answer.append(on_did_show_answer)
    gui_hooks.reviewer_did_answer_card.append(on_reviewer_did_answer)
    gui_hooks.webview_will_set_content.append(
        lambda content, context:
        on_will_start(content, context) if isinstance(context, reviewer.Reviewer) else None
    )


def on_will_start(content: webview.WebContent, context: reviewer.Reviewer):
    global almost_leech_html
    if LeechToolkitConfigManager(mw).config[Config.SHOW_ALMOST_LEECH_MARKER]:
        content.body += almost_leech_html.format(
            marker_id=marker_id,
            marker_text=marker_text,
            marker_color=marker_color
        )


def on_did_show_answer(card: anki.cards.Card):
    conf = mw.col.decks.config_dict_for_deck_id(card.current_deck_id())
    max_fails = conf['lapse']['leechFails']
    print(f'card.lapses: {card.lapses}')

    if card.type == anki.cards.CARD_TYPE_REV and (card.lapses + from_lapse) >= max_fails:
        # print(f'\n  trace on')
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "unset"')


def on_reviewer_did_answer(anki_reviewer, card, ease):
    mw.web.eval(f'document.getElementById("{marker_id}").style.display = "none";')
    # print(f'answered')
