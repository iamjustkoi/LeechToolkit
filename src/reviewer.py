"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import anki.cards
import aqt.reviewer
from aqt import reviewer
from aqt import webview
from aqt import mw, gui_hooks, utils
from anki import cards

from .config import LeechToolkitConfigManager
from .consts import Config, MARKER_POS_STYLES, REV_DECREASE, LEECH_TAG, CARD_TYPE_STR

conf: dict
max_fails: int
user_conf: dict
almost_leech_html = '''
<style>
    #{marker_id} {{
        color: transparent;  
        text-shadow: 0 0 0 {marker_color};
        font-size: .4em !important;
        float: {marker_float};
        display: none;
    }}
</style>
<div id="{marker_id}">{marker_text}</div>
'''

from_lapse = 1
marker_id = 'leech_marker'
marker_text = '🩸'
marker_color = 'rgb(248, 197, 86)'
prev_type_attr = 'prevtype'

decrease_enabled = True
tooltip_enabled = True


def build_hooks():
    from aqt.gui_hooks import webview_will_set_content
    from aqt.gui_hooks import reviewer_did_show_question
    from aqt.gui_hooks import reviewer_did_show_answer
    from aqt.gui_hooks import reviewer_did_answer_card
    webview_will_set_content.append(
        lambda content, context:
        on_will_start(content, context) if isinstance(context, reviewer.Reviewer) else None
    )
    reviewer_did_show_question.append(on_did_show_question)
    reviewer_did_show_answer.append(on_did_show_answer)
    reviewer_did_answer_card.append(on_did_answer)


def on_will_start(content: aqt.webview.WebContent, context: aqt.reviewer.Reviewer):
    global conf, max_fails, user_conf
    conf = mw.col.decks.config_dict_for_deck_id(mw.col.decks.get_current_id())
    max_fails = conf['lapse']['leechFails']
    user_conf = LeechToolkitConfigManager(mw).config

    append_html(content)


def append_html(content: aqt.webview.WebContent):
    if user_conf[Config.SHOW_ALMOST_LEECH_MARKER]:
        marker_float = MARKER_POS_STYLES[user_conf[Config.ALMOST_MARK_POSITION]]
        content.body += almost_leech_html.format(
            marker_id=marker_id, marker_text=marker_text, marker_color=marker_color, marker_float=marker_float
        )


def on_did_show_answer(card: cards.Card):
    # user_conf[Config.]
    if user_conf[Config.REVERSE_ENABLED]:
        setattr(card, prev_type_attr, card.type)

    if card.type == cards.CARD_TYPE_REV and (card.lapses + from_lapse) >= max_fails:
        show_marker(True)


def on_did_show_question(card: cards.Card):
    print(f'CardType({CARD_TYPE_STR[card.type]})')
    if user_conf[Config.ALMOST_ON_BACK]:
        show_marker(False)
    else:
        if card.type == cards.CARD_TYPE_REV and (card.lapses + from_lapse) >= max_fails:
            show_marker(True)


def on_did_answer(context: aqt.reviewer.Reviewer, card: cards.Card, ease: int):
    if hasattr(card, prev_type_attr):
        tooltip = ''
        if user_conf[Config.REVERSE_ENABLED]:
            prev_type = card.__getattribute__(prev_type_attr)
            if user_conf[Config.REVERSE_METHOD] == REV_DECREASE:
                if ease > 1 and card.lapses > 0 and prev_type == cards.CARD_TYPE_REV:
                    card.lapses -= 1
                    card.flush()
                    tooltip += f'Card\'s lapses set to: {card.lapses}'

            if user_conf[Config.REVERSE_THRESHOLD] > card.lapses:
                if ease > 1 and card.note().has_tag(LEECH_TAG) and prev_type == cards.CARD_TYPE_REV:
                    card.note().remove_tag(LEECH_TAG)
                    card.note().flush()
                    tooltip += f'\nCard Un-Leeched' if len(tooltip) > 0 else f'Card Un-leeched'

        if tooltip_enabled and len(tooltip) > 0:
            utils.tooltip(tooltip, y_offset=200, x_offset=600)
        delattr(card, prev_type_attr)


def show_marker(show=False):
    if show:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "unset"')
    else:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "none"')
