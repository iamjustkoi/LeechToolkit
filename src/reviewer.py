"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""

import anki.cards
import aqt.reviewer
from anki import cards, hooks
from anki.collection import OpChanges
from anki.consts import CardType
from anki.decks import DeckId
from aqt import reviewer, webview, gui_hooks, mw

from .actions import run_actions
from .config import LeechToolkitConfigManager, merge_fields
from .consts import Config, MARKER_POS_STYLES, LEECH_TAG, REV_DECREASE, REV_RESET, String

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

    webview_will_set_content.append(
        lambda content, context:
        on_will_start(content, context) if isinstance(context, reviewer.Reviewer) else None
    )


def on_will_start(content: aqt.webview.WebContent, anki_reviewer: aqt.reviewer.Reviewer):
    if not mw.col.decks.is_filtered(mw.col.decks.get_current_id()):
        anki_reviewer.toolkit_manager = ReviewManager(content, mw.col.decks.get_current_id())
        # load_action_manager(context)

        # gui_hooks.reviewer_did_show_question.append(on_show_front)
        # gui_hooks.reviewer_did_show_answer.append(on_show_back)
        # gui_hooks.reviewer_did_answer_card.append(on_answer)
        # hooks.card_did_leech.append(mark_leeched)
        #
        # append_marker_html(content)


# def remove_hooks():
#     gui_hooks.reviewer_did_show_question.remove(on_show_front)
#     gui_hooks.reviewer_did_show_answer.remove(on_show_back)
#     gui_hooks.reviewer_did_answer_card.remove(on_answer)
#     try:
#         hooks.card_did_leech.remove(mark_leeched)
#     except NameError:
#         print(f'Action manager not yet defined.')


def mark_leeched(card: anki.cards.Card):
    setattr(card, was_leech_attr, True)


def has_cons_correct(card: cards.Card, num_correct: int):
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


def was_card_updated(original_card, updated_card):
    changed_items = [item for item in original_card.__dict__.items() if item[1] != updated_card.__dict__.get(item[0])]
    return len(changed_items) > 0


def set_marker_color(color: str):
    mw.web.eval(f'document.getElementById("{marker_id}").style.textShadow = "0 0 0 {color}";')


def show_marker(show=False):
    """
Changes the display state of the run_actions marker.
    :param show: new visibility
    """
    if show:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "unset"')
    else:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "none"')


def flush_card(card: anki.cards.Card) -> OpChanges:
    card.flush()
    card.note().flush()
    return aqt.reviewer.OpChanges(card=True, note=True)


class ReviewManager:
    toolkit_config: dict
    max_fails: int

    def __init__(self, content: aqt.webview.WebContent, did: DeckId):
        if not mw.col.decks.is_filtered(did):
            deck_conf_dict = mw.col.decks.config_dict_for_deck_id(did)
            self.max_fails = deck_conf_dict['lapse']['leechFails']

            global_conf = LeechToolkitConfigManager(mw).config
            self.toolkit_config = global_conf.get(str(deck_conf_dict['id']), {})
            merge_fields(self.toolkit_config, global_conf)

            self.append_marker_html(content)
            self.append_hooks()

    def append_marker_html(self, content: aqt.webview.WebContent):
        marker_float = MARKER_POS_STYLES[self.toolkit_config[Config.MARKER_POSITION]]
        content.body += mark_html_shell.format(
            marker_id=marker_id, marker_text=MARKER_TEXT, marker_color=LEECH_COLOR, marker_float=marker_float
        )

    def append_hooks(self):
        from anki.hooks import card_did_leech
        from aqt.gui_hooks import (
            reviewer_did_show_question,
            reviewer_did_show_answer,
            reviewer_did_answer_card,
            reviewer_will_end,
        )
        card_did_leech.append(mark_leeched)

        reviewer_did_show_question.append(self.on_show_front)
        reviewer_did_show_answer.append(self.on_show_back)
        reviewer_did_answer_card.append(self.on_answer)

        reviewer_will_end.append(self.remove_hooks)

    def remove_hooks(self):
        try:
            hooks.card_did_leech.remove(mark_leeched)
        except NameError:
            print(f'Action manager not yet defined.')

        gui_hooks.reviewer_did_show_question.remove(self.on_show_front)
        gui_hooks.reviewer_did_show_answer.remove(self.on_show_back)
        gui_hooks.reviewer_did_answer_card.remove(self.on_answer)

    def on_show_back(self, card: cards.Card):
        if self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
            setattr(card, prev_type_attr, card.type)
        self.update_marker(card, False)

    def on_show_front(self, card: cards.Card):
        self.update_marker(card, True)
        # @DEBUG
        self.reverse_update(card, 2, anki.cards.CARD_TYPE_REV)
        run_actions(card, self.toolkit_config[Config.LEECH_ACTIONS])

    def on_answer(self, context: aqt.reviewer.Reviewer, card: cards.Card, ease: int):
        updated_card = card.col.get_card(card.id)

        if hasattr(card, prev_type_attr):
            updated_card = self.reverse_update(card, ease, card.__getattribute__(prev_type_attr))
            delattr(card, prev_type_attr)

        if hasattr(card, was_leech_attr):
            updated_card = run_actions(card, self.toolkit_config[Config.LEECH_ACTIONS])
            delattr(card, was_leech_attr)

        if was_card_updated(card, updated_card):
            flush_card(updated_card)

    def reverse_update(self, card: anki.cards.Card, ease: int, prev_type: CardType):
        """
    Runs reverse leech updates to the input card and returns an updated card object.
        :param card: Card to update
        :param ease: review-answer input
        :param prev_type: previous type of the current card used for determining changes
        :return: updated card object
        """
        updated_card = card.col.get_card(card.id)
        tooltip_items = []

        if self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
            deck_config = card.col.decks.config_dict_for_deck_id(card.current_deck_id())
            use_leech_threshold = self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_USE_LEECH_THRESHOLD]
            threshold = deck_config['lapse']['leechFails'] if use_leech_threshold else \
            self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_THRESHOLD]

            # Lapse updates
            if has_cons_correct(updated_card, self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_CONS_ANS]):
                if ease > 1 and updated_card.lapses > 0 and prev_type == cards.CARD_TYPE_REV:
                    if self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_METHOD] == REV_DECREASE:
                        updated_card.lapses -= 1
                        tooltip_items.append(String.LAPSES_DECREASED)
                    elif self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_METHOD] == REV_RESET:
                        updated_card.lapses = 0
                        tooltip_items.append(String.LAPSES_RESET)

            # Un-leech
            if updated_card.lapses < threshold:
                if ease > 1 and updated_card.note().has_tag(LEECH_TAG) and prev_type == cards.CARD_TYPE_REV:
                    updated_card.note().remove_tag(LEECH_TAG)
                    tooltip_items.append(String.LEECH_REVERSED)

                    updated_card = run_actions(updated_card, self.toolkit_config[Config.UN_LEECH_ACTIONS], reload=False)

            if TOOLTIP_ENABLED and len(tooltip_items) > 0:
                aqt.utils.tooltip('\n\n'.join(tooltip_items))
        return updated_card

    def update_marker(self, card: cards.Card, is_front: bool):
        """
    Updates marker style/visibility based on user options and current card's attributes.
        :param card: referenced card
        :param is_front: current display state for card in reviewer
        """
        if not self.toolkit_config[Config.SHOW_LEECH_MARKER] or (
                self.toolkit_config[Config.ONLY_SHOW_BACK_MARKER] and is_front):
            show_marker(False)
        elif card.note().has_tag(LEECH_TAG):
            set_marker_color(LEECH_COLOR)
            show_marker(True)
        elif self.toolkit_config[Config.USE_ALMOST_MARKER] \
                and card.type == cards.CARD_TYPE_REV \
                and (card.lapses + ALMOST_DISTANCE) >= self.max_fails:
            set_marker_color(ALMOST_COLOR)
            show_marker(True)
