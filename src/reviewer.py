"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import aqt.reviewer
from aqt import reviewer, webview, gui_hooks, utils, mw
from anki import cards

from .config import LeechToolkitConfigManager
from .consts import Config, MARKER_POS_STYLES, LEECH_TAG, REV_DECREASE, REV_RESET, String

conf: dict
max_fails: int
user_conf: dict
mark_html_shell = '''
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

MARKER_TEXT = '🩸'
LEECH_COLOR = 'rgb(248, 105, 86)'
ALMOST_COLOR = 'rgb(248, 197, 86)'
ALMOST_DISTANCE = 1

TOOLTIP_ENABLED = True
TOOLTIP_TIME = 5000


def build_hooks():
    from aqt.gui_hooks import webview_will_set_content
    from aqt.gui_hooks import reviewer_will_end

    reviewer_will_end.append(remove_hooks)

    webview_will_set_content.append(
        lambda content, context:
        on_will_start(content, context) if isinstance(context, reviewer.Reviewer) else None
    )


def on_will_start(content: aqt.webview.WebContent, context: aqt.reviewer.Reviewer):
    remove_hooks()
    if not mw.col.decks.is_filtered(mw.col.decks.get_current_id()):
        global conf, max_fails, user_conf
        conf = mw.col.decks.config_dict_for_deck_id(mw.col.decks.get_current_id())
        max_fails = conf['lapse']['leechFails']
        user_conf = LeechToolkitConfigManager(mw).config

        append_marker_html(content)

        gui_hooks.reviewer_did_show_question.append(on_show_front)
        gui_hooks.reviewer_did_show_answer.append(on_show_back)
        gui_hooks.reviewer_did_answer_card.append(on_answer)


def remove_hooks():
    gui_hooks.reviewer_did_show_question.remove(on_show_front)
    gui_hooks.reviewer_did_show_answer.remove(on_show_back)
    gui_hooks.reviewer_did_answer_card.remove(on_answer)


def append_marker_html(content: aqt.webview.WebContent):
    marker_float = MARKER_POS_STYLES[user_conf[Config.MARKER_POSITION]]
    content.body += mark_html_shell.format(
        marker_id=marker_id, marker_text=MARKER_TEXT, marker_color=LEECH_COLOR, marker_float=marker_float
    )


def on_show_back(card: cards.Card):
    if user_conf[Config.REVERSE_ENABLED]:
        setattr(card, prev_type_attr, card.type)
    update_marker(card, False)


def on_show_front(card: cards.Card):
    update_marker(card, True)


def card_has_consecutive_correct(card: cards.Card, num_correct: int):
    total_correct = len(get_correct_answers(card))
    return total_correct > 0 and total_correct % num_correct == 0


def get_correct_answers(card: cards.Card):
    """
Retrieves all reviews that were correct without any "again" answers.
    :param card: card to use as reference
    :return: a list of correct answers (2-4)
    """
    again_ease = 1

    cmd = f'''
            SELECT ease FROM revlog 
            WHERE cid is {card.id} and ease is not 0
            ORDER BY id DESC
        '''
    answers = card.col.db.list(cmd)
    if again_ease not in answers:
        return answers
    else:
        return answers[:answers.index(again_ease) - 1] if answers.index(again_ease) != 0 else []


def on_answer(context: aqt.reviewer.Reviewer, card: cards.Card, ease: int):
    if hasattr(card, prev_type_attr):
        tooltip = ''

        if user_conf[Config.REVERSE_ENABLED]:
            prev_type = card.__getattribute__(prev_type_attr)

            # Card reverse functions
            if card_has_consecutive_correct(card, user_conf[Config.REVERSE_CONS_ANS]):

                if ease > 1 and card.lapses > 0 and prev_type == cards.CARD_TYPE_REV:
                    if user_conf[Config.REVERSE_METHOD] == REV_DECREASE:
                        card.lapses -= 1
                        tooltip += String.LAPSES_DECREASED
                    elif user_conf[Config.REVERSE_METHOD] == REV_RESET:
                        card.lapses = 0
                        tooltip += String.LAPSES_RESET

                    card.flush()

            if user_conf[Config.REVERSE_THRESHOLD] > card.lapses:
                if ease > 1 and card.note().has_tag(LEECH_TAG) and prev_type == cards.CARD_TYPE_REV:
                    card.note().remove_tag(LEECH_TAG)
                    card.note().flush()
                    tooltip += f'<br>Card Un-Leeched' if tooltip else f'Card Un-leeched'

        if TOOLTIP_ENABLED and tooltip:
            utils.tooltip(tooltip, period=TOOLTIP_TIME, y_offset=200, x_offset=600)

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
        set_marker_color(LEECH_COLOR)
        show_marker(True)
    elif user_conf[Config.USE_ALMOST_MARKER] \
            and card.type == cards.CARD_TYPE_REV \
            and (card.lapses + ALMOST_DISTANCE) >= max_fails:
        set_marker_color(ALMOST_COLOR)
        show_marker(True)
