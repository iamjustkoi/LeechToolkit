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

marker_id = 'leech_marker'
prev_type_attr = 'prevtype'

marker_text = '🩸'
almost_color = 'rgb(248, 197, 86)'
leech_color = 'rgb(248, 105, 86)'
almost_leech_distance = 1
TOOLTIP_ENABLED = True


def build_hooks():
    from aqt.gui_hooks import webview_will_set_content
    from aqt.gui_hooks import reviewer_did_show_question
    from aqt.gui_hooks import reviewer_did_show_answer
    from aqt.gui_hooks import reviewer_did_answer_card
    webview_will_set_content.append(
        lambda content, context:
        on_will_start(content, context) if isinstance(context, reviewer.Reviewer) else None
    )
    reviewer_did_show_question.append(on_show_front)
    reviewer_did_show_answer.append(on_show_back)
    reviewer_did_answer_card.append(on_answer)


def on_will_start(content: aqt.webview.WebContent, context: aqt.reviewer.Reviewer):
    global conf, max_fails, user_conf
    conf = mw.col.decks.config_dict_for_deck_id(mw.col.decks.get_current_id())
    max_fails = conf['lapse']['leechFails']
    user_conf = LeechToolkitConfigManager(mw).config

    append_marker_html(content)


def append_marker_html(content: aqt.webview.WebContent):
    marker_float = MARKER_POS_STYLES[user_conf[Config.MARKER_POSITION]]
    content.body += almost_leech_html.format(
        marker_id=marker_id, marker_text=marker_text, marker_color=leech_color, marker_float=marker_float
    )


def on_show_back(card: cards.Card):
    if user_conf[Config.REVERSE_ENABLED]:
        setattr(card, prev_type_attr, card.type)
    update_marker(card, False)


def on_show_front(card: cards.Card):
    # print(f'    CardType({CARD_TYPE_STR[card.type]})')
    update_marker(card, True)


def on_answer(context: aqt.reviewer.Reviewer, card: cards.Card, ease: int):
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
                    tooltip += f'<br>Card Un-Leeched' if tooltip else f'Card Un-leeched'

        if TOOLTIP_ENABLED and tooltip:
            utils.tooltip(tooltip, y_offset=200, x_offset=600)

        delattr(card, prev_type_attr)


def set_marker_color(color: str):
    mw.web.eval(f'document.getElementById("{marker_id}").style.textShadow = "0 0 0 {color}";')


def show_marker(show=False):
    """
Changes the display state of the leech marker.
    :param show: new visibility
    """
    if show:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "unset"')
    else:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "none"')


def update_marker(card: cards.Card, is_front: bool):
    """
Updates marker style/visibility based on user options and current card's attributes.
    :param card: referenced card
    :param is_front: current display state for card in reviewer
    """
    if not user_conf[Config.SHOW_LEECH_MARKER] or (user_conf[Config.ONLY_SHOW_BACK_MARKER] and is_front):
        show_marker(False)
    elif card.note().has_tag(LEECH_TAG):
        set_marker_color(leech_color)
        show_marker(True)
    elif user_conf[Config.USE_ALMOST_MARKER] \
            and card.type == cards.CARD_TYPE_REV \
            and (card.lapses + almost_leech_distance) >= max_fails:
        set_marker_color(almost_color)
        show_marker(True)
