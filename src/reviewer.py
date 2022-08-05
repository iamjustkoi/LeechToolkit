"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import Literal

import anki.cards
import aqt.reviewer
from anki.collection import OpChanges
from anki.consts import CardType
from aqt import reviewer, webview, gui_hooks, utils, mw
from anki import cards, hooks

from .actions import LeechActionManager
from .config import LeechToolkitConfigManager
from .consts import Config, String, MARKER_POS_STYLES, LEECH_TAG, REV_DECREASE, REV_RESET

conf: dict
max_fails: int
user_conf: dict
action_manager: LeechActionManager
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
was_leech_attr = 'was_leech'

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
        global conf, max_fails, user_conf, action_manager
        conf = mw.col.decks.config_dict_for_deck_id(mw.col.decks.get_current_id())
        max_fails = conf['lapse']['leechFails']
        user_conf = LeechToolkitConfigManager(mw).config
        action_manager = LeechActionManager(context, mw.col.decks.get_current_id(), user_conf)

        gui_hooks.reviewer_did_show_question.append(on_show_front)
        gui_hooks.reviewer_did_show_answer.append(on_show_back)
        gui_hooks.reviewer_did_answer_card.append(on_answer)
        hooks.card_did_leech.append(mark_leeched)

        append_marker_html(content)


def remove_hooks():
    gui_hooks.reviewer_did_show_question.remove(on_show_front)
    gui_hooks.reviewer_did_show_answer.remove(on_show_back)
    gui_hooks.reviewer_did_answer_card.remove(on_answer)
    try:
        hooks.card_did_leech.remove(mark_leeched)
    except NameError:
        print(f'Action manager not defined yet.')


def mark_leeched(card: anki.cards.Card):
    setattr(card, was_leech_attr, True)
    print(f'update_leech')


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
    # # @DEBUG
    # action_manager.leech_update(card, debug=True)


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
    print(f'on_answer')

    updated_card = card.col.get_card(card.id)

    if hasattr(card, prev_type_attr):
        updated_card = reverse_update(card, ease, card.__getattribute__(prev_type_attr))
        delattr(card, prev_type_attr)

    if hasattr(card, was_leech_attr):
        updated_card = action_manager.leech_update(card)
        delattr(card, was_leech_attr)

    if was_card_updated(card, updated_card):
        update_card(updated_card)


def update_card(card: anki.cards.Card) -> OpChanges:
    card.flush()
    card.note().flush()
    return aqt.reviewer.OpChanges(card=True, note=True)


def reverse_update(card: anki.cards.Card, ease: int, prev_type: CardType):
    updated_card = card.col.get_card(card.id)
    if user_conf[Config.REVERSE_ENABLED]:
        if card_has_consecutive_correct(updated_card, user_conf[Config.REVERSE_CONS_ANS]):
            if ease > 1 and updated_card.lapses > 0 and prev_type == cards.CARD_TYPE_REV:
                if user_conf[Config.REVERSE_METHOD] == REV_DECREASE:
                    updated_card.lapses -= 1
                elif user_conf[Config.REVERSE_METHOD] == REV_RESET:
                    updated_card.lapses = 0

        if user_conf[Config.REVERSE_THRESHOLD] > updated_card.lapses:
            if ease > 1 and updated_card.note().has_tag(LEECH_TAG) and prev_type == cards.CARD_TYPE_REV:
                updated_card.note().remove_tag(LEECH_TAG)
    return updated_card


def was_card_updated(original_card, updated_card):
    changed_items = [item for item in original_card.__dict__.items() if item[1] != updated_card.__dict__.get(item[0])]
    return changed_items is not None


def set_marker_color(color: str):
    mw.web.eval(f'document.getElementById("{marker_id}").style.textShadow = "0 0 0 {color}";')


def show_marker(show=False):
    """
Changes the display state of the leech_update marker.
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
