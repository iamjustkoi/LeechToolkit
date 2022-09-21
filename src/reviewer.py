"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import json

import anki.cards
import aqt.reviewer
from anki import cards, hooks
from anki.decks import DeckId
from aqt import reviewer, webview, gui_hooks, mw

from .updates import run_action_updates, run_reverse_updates, commit_card
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
        # Attached for garbage collection
        anki_reviewer.toolkit_manager = ReviewManager(content, mw.col.decks.get_current_id())


def mark_leeched(card: anki.cards.Card):
    setattr(card, was_leech_attr, True)


def was_card_updated(original_card, updated_card):
    changed_items = [item for item in original_card.__dict__.items() if item[1] != updated_card.__dict__.get(item[0])]
    return len(changed_items) > 0


def set_marker_color(color: str):
    mw.web.eval(f'document.getElementById("{marker_id}").style.textShadow = "0 0 0 {color}";')


def show_marker(show=False):
    """
Changes the display state of the run_action_updates marker.
    :param show: new visibility
    """
    if show:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "unset"')
    else:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "none"')


class ReviewManager:
    toolkit_config: dict
    max_fails: int
    did: DeckId
    page_content: aqt.webview.WebContent

    def __init__(self, content: aqt.webview.WebContent, did: DeckId):
        if not mw.col.decks.is_filtered(did):
            self.page_content = content
            self.load_options(did)

    def load_options(self, did: DeckId = None):
        self.did = did if did else self.did

        deck_conf_dict = mw.col.decks.config_dict_for_deck_id(self.did)
        self.max_fails = deck_conf_dict['lapse']['leechFails']

        global_conf = LeechToolkitConfigManager(mw).config
        self.toolkit_config = merge_fields(global_conf.get(str(deck_conf_dict['id']), {}), global_conf)

        self.append_marker_html()
        self.append_hooks()

    def append_marker_html(self):
        marker_float = MARKER_POS_STYLES[self.toolkit_config[Config.MARKER_OPTIONS][Config.MARKER_POSITION]]
        self.page_content.body += mark_html_shell.format(
            marker_id=marker_id,
            marker_text=MARKER_TEXT,
            marker_color=LEECH_COLOR,
            marker_float=marker_float,
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
        # print(f'orig ____ {cards.Card().__dict__}')
        # run_action_updates(card, self.toolkit_config[Config.LEECH_ACTIONS])
        # print(f'____    {run_reverse_updates(self.toolkit_config, card, 2, anki.cards.CARD_TYPE_REV).__dict__}')

    def on_answer(self, context: aqt.reviewer.Reviewer, card: cards.Card, ease: int):
        updated_card = card.col.get_card(card.id)
        was_leech = False
        if hasattr(card, prev_type_attr):
            updated_card = run_reverse_updates(self.toolkit_config, card, ease, card.__getattribute__(prev_type_attr))
            delattr(card, prev_type_attr)

        if hasattr(card, was_leech_attr):
            was_leech = True
            updated_card = run_action_updates(card, self.toolkit_config[Config.LEECH_ACTIONS])
            delattr(card, was_leech_attr)

        if was_card_updated(card, updated_card):
            commit_card(updated_card, was_leech, aqt.reviewer.OpChanges)

    def update_marker(self, card: cards.Card, is_front: bool):
        """
    Updates marker style/visibility based on user options and current card's attributes.
        :param card: referenced card
        :param is_front: current display state for card in reviewer
        """
        marker_conf = self.toolkit_config[Config.MARKER_OPTIONS]
        if not marker_conf[Config.SHOW_LEECH_MARKER] or (
                marker_conf[Config.ONLY_SHOW_BACK_MARKER] and is_front):
            show_marker(False)
        elif card.note().has_tag(LEECH_TAG):
            set_marker_color(LEECH_COLOR)
            show_marker(True)
        elif marker_conf[Config.USE_ALMOST_MARKER] \
                and card.type == cards.CARD_TYPE_REV \
                and (card.lapses + ALMOST_DISTANCE) >= self.max_fails:
            set_marker_color(ALMOST_COLOR)
            show_marker(True)
