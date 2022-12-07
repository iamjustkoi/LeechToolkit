"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""

from __future__ import annotations

import traceback

import anki.cards
import aqt.reviewer
from anki import hooks
from anki.errors import InvalidInput
from aqt.utils import showInfo, tooltip
from aqt.webview import WebContent, AnkiWebView
from aqt import gui_hooks, mw
from aqt.reviewer import Reviewer
from aqt.qt import QShortcut, QKeySequence

from .legacy import _try_check_filtered, _try_get_config_dict_for_did, _try_get_current_did
from .actions import handle_actions, handle_reverse
from .config import LeechToolkitConfigManager, merge_fields
from .consts import (
    ANKI_LEGACY_VER,
    ANKI_UNDO_UPDATE_VER,
    CURRENT_ANKI_VER,
    Config,
    ErrorMsg,
    MARKER_POS_STYLES,
    LEECH_TAG,
    String,
)

try:
    from anki.decks import DeckId
except ImportError:
    print(f'{traceback.format_exc()}\n{ErrorMsg.MODULE_NOT_FOUND_LEGACY}')
    DeckId = int

mark_html_template = '''
<style>
    #{marker_id} {{
        color: transparent;  
        font-size: .4em !important;
        display: none;
        text-shadow: 0 0 0 {marker_color};
        float: {marker_float};
    }}
</style>
<div id="{marker_id}">{marker_text}</div>
'''

marker_id = 'leech_marker'
prev_type_attr = 'prevtype'
wrapper_attr = 'toolkit_manager'

MARKER_TEXT = '🩸'
LEECH_COLOR = 'rgb(248, 105, 86)'
ALMOST_COLOR = 'rgb(248, 197, 86)'
ALMOST_DISTANCE = 1

TOOLTIP_ENABLED = True
TOOLTIP_TIME = 5000


def build_hooks():
    from aqt.gui_hooks import (
        webview_will_set_content,
    )

    webview_will_set_content.append(try_append_wrapper)


def try_append_wrapper(content: aqt.webview.WebContent, context: object):
    """
    Attempts to attach to the current reviewer, as long as it's not a filtered deck, else removes the wrapper.

    :param content: web-content for html and page edits
    :param context: used for checking whether the webview is being set to the reviewer
    """
    if isinstance(context, Reviewer):
        reviewer: aqt.reviewer.Reviewer = context
        if _try_check_filtered(_try_get_current_did()) and hasattr(mw.reviewer, wrapper_attr):
            mw.reviewer.__delattr__(wrapper_attr)
        else:
            # Attached for calls and any future garbage collection, potentially, idk
            reviewer.toolkit_wrapper = ReviewWrapper(reviewer, content, _try_get_current_did())


def set_marker_color(color: str):
    """
    Psuedo-tints the leech marker to the input color.

    :param color: color (style) string to update the marker color to
    """
    mw.web.eval(f'document.getElementById("{marker_id}").style.textShadow = "0 0 0 {color}";')


def show_marker(show=False):
    """
    Changes the display state of the handle_input_action marker.

    :param show: new visibility
    """
    if show:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "unset"')
    else:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "none"')


<<<<<<< HEAD
=======
def check_did_leech(context, card: anki.cards.Card, ease):
    threshold = mw.col.decks.config_dict_for_deck_id(card.did)['lapse']['leechFails']
    if ease < 1 and card.lapses >= threshold and (card.lapses - threshold) % (max(threshold // 2, 1)) == 0:
        mark_leeched(card)


>>>>>>> refs/rewritten/private-main-3
class ReviewWrapper:
    toolkit_config: dict
    max_fails: int
    did: DeckId
    content: aqt.webview.WebContent
    card: anki.cards.Card
    on_front: bool
    leeched_cids: set[int] = set()

    # queued_undo_entry: int = -1

    # queued_undo_entry: int = -1

    def __init__(self, reviewer: Reviewer, content: aqt.webview.WebContent, did: DeckId):
        """
        Wrapper used for handling events in the Anki reviewer, if not a filtered review-type.

        :param reviewer: Anki Reviewer object
        :param content: web-content used for editing the page style/html
        :param did: deck id of the current reviewer
        """
        if not _try_check_filtered(did):
            self.content = content
            self.reviewer = reviewer
            self.load_options(did)

            leech_seq = QKeySequence(self.toolkit_config[Config.SHORTCUT_OPTIONS][Config.LEECH_SHORTCUT])
            leech_shortcut = QShortcut(leech_seq, mw, lambda *args: self.handle_input_action(Config.LEECH_ACTIONS))

            self.leech_action = aqt.qt.QAction(String.REVIEWER_ACTION_LEECH, mw)
            self.leech_action.setShortcut(leech_seq)
            self.leech_action.triggered.connect(lambda *args: self.handle_input_action(Config.LEECH_ACTIONS))
            mw.stateShortcuts.append(leech_shortcut)

            unleech_seq = QKeySequence(self.toolkit_config[Config.SHORTCUT_OPTIONS][Config.UNLEECH_SHORTCUT])
            unleech_shortcut = QShortcut(
                unleech_seq,
                mw,
                lambda *args: self.handle_input_action(Config.UN_LEECH_ACTIONS)
            )

            self.unleech_action = aqt.qt.QAction(String.REVIEWER_ACTION_UNLEECH, mw)
            self.unleech_action.setShortcut(unleech_seq)
            self.unleech_action.triggered.connect(lambda *args: self.handle_input_action(Config.UN_LEECH_ACTIONS))
            mw.stateShortcuts.append(unleech_shortcut)

    def load_options(self, did: DeckId = None):
        """
        Loads options to UI elements and config-based actions, as well as appends hooks to the initialized reviewer.

        :param did: deck id used for determining config values
        """
        self.did = did if did else self.did

        deck_conf_dict = _try_get_config_dict_for_did(self.did)
        self.max_fails = deck_conf_dict['lapse']['leechFails']

        global_conf = LeechToolkitConfigManager(mw).config
        self.toolkit_config = merge_fields(global_conf.get(str(deck_conf_dict['id']), {}), global_conf)

        self.append_marker_html()
        self.append_hooks()

    def refresh_if_needed(self, changes: aqt.reviewer.OpChanges):
        """
        Function call to update the current window based on whether cards/schedules were changed.

        :param changes: OpChanges object to reference for schedule/card/note changes.
        """
        self.reviewer.op_executed(changes=changes, handler=self, focused=True)
        if not self.reviewer.refresh_if_needed():
            self.update_marker()

    def append_marker_html(self):
        """
        Appends a leech marker to the review window's html.
        """
        marker_float = MARKER_POS_STYLES[self.toolkit_config[Config.MARKER_OPTIONS][Config.MARKER_POSITION]]
        self.content.body += mark_html_template.format(
            marker_id=marker_id,
            marker_text=MARKER_TEXT,
            marker_color=LEECH_COLOR,
            marker_float=marker_float,
        )

    def append_hooks(self):
        """
        Appends hooks to the current reviewer.
        """
        from anki.hooks import card_did_leech
        from aqt.gui_hooks import (
            reviewer_did_show_question,
            reviewer_did_show_answer,
            reviewer_did_answer_card,
            reviewer_will_end,
            reviewer_will_show_context_menu
        )
        if mw.col.v3_scheduler():
<<<<<<< HEAD
            reviewer_did_answer_card.append(self.on_answer_v3)
=======
            reviewer_did_answer_card.append(check_did_leech)
>>>>>>> refs/rewritten/private-main-3
        else:
            card_did_leech.append(self.save_leech)
            reviewer_did_answer_card.append(self.on_answer)

        reviewer_did_show_question.append(self.on_show_front)
        reviewer_did_show_answer.append(self.on_show_back)
        reviewer_will_show_context_menu.append(self.append_context_menu)

        reviewer_will_end.append(self.remove_hooks)

    def save_leech(self, card: anki.cards.Card):
        """
        Appends a temporary, custom leech attribute to the selected card.

        :param card: card object to add the attribute to
        """
        self.leeched_cids.add(card.id)
        # setattr(card, was_leech_attr, True)

    def on_answer_v3(self, context, card: anki.cards.Card, ease):
        if card.note().has_tag(LEECH_TAG):
            self.save_leech(card)
        self.on_answer(context, card, ease)

    def append_context_menu(self, webview: AnkiWebView, menu: aqt.qt.QMenu):
        for action in menu.actions():
            if action.text() in (String.REVIEWER_ACTION_LEECH, String.REVIEWER_ACTION_UNLEECH):
                menu.removeAction(action)
        menu.addSeparator()
        menu.addAction(self.leech_action)
        menu.addAction(self.unleech_action)

    def remove_hooks(self):
        try:
<<<<<<< HEAD
            gui_hooks.reviewer_did_answer_card.remove(self.on_answer_v3)
            hooks.card_did_leech.remove(self.save_leech)
=======
            gui_hooks.reviewer_did_answer_card.remove(check_did_leech)
            hooks.card_did_leech.remove(mark_leeched)
>>>>>>> refs/rewritten/private-main-3
        except NameError:
            print(ErrorMsg.ACTION_MANAGER_NOT_DEFINED)

        gui_hooks.reviewer_did_show_question.remove(self.on_show_front)
        gui_hooks.reviewer_did_show_answer.remove(self.on_show_back)
        gui_hooks.reviewer_did_answer_card.remove(self.on_answer)

    def handle_card_updates(self, card: anki.cards.Card, update_callback, undo_msg=None):
        current_data = {
            'queue': card.queue.real,
            'due': card.due.real,
            'lapses': card.lapses,
            'fields': card.note().joined_fields(),
            'tags': card.note().tags,
        }
        updated_card = update_callback()
        updated_data = {
            'queue': updated_card.queue.real,
            'due': updated_card.due.real,
            'lapses': updated_card.lapses,
            'fields': updated_card.note().joined_fields(),
            'tags': updated_card.note().tags,
        }

        if CURRENT_ANKI_VER < ANKI_UNDO_UPDATE_VER:
            if current_data != updated_data:
                card.flush()
                card.note().flush()
                # Let Anki handle undo status updates
                mw.checkpoint(undo_msg)
                mw.reset()
        else:
            if current_data != updated_data:
                def push_updates():
                    if undo_msg:
                        entry = self.reviewer.mw.col.add_custom_undo_entry(undo_msg)
                    else:
                        entry = mw.col.undo_status().last_step

                    self.reviewer.mw.col.update_card(updated_card)
                    self.reviewer.mw.col.update_note(updated_card.note())

                    try:
                        changes = self.reviewer.mw.col.merge_undo_entries(entry)
                        self.refresh_if_needed(changes)
                    except InvalidInput:
                        showInfo(ErrorMsg.ERROR_TRACEBACK)

                if undo_msg or mw.col.v3_scheduler():
                    push_updates()
                else:
<<<<<<< HEAD
<<<<<<< HEAD
                    if mw.col.v3_scheduler():
                        push_updates()
=======
                    # Let reviewer handle entry and flush updates pre-logging, instead.
                    updated_card.flush()
>>>>>>> 7248e41 (Added error handling and fixed issue with V3 scheduler undo entries using a bad undo step for versions 2.1.45-2.1.49.)

                    current_field_tags = (current_data['fields'], current_data['tags'])
                    updated_field_tags = (updated_data['fields'], updated_data['tags'])

<<<<<<< HEAD
                        if (current_data['fields'], current_data['tags']) \
                                != (updated_data['fields'], updated_data['tags']):
                            updated_card.note().flush()
=======
                    # Don't create new undo entry so reviewer handles final updates
                    updated_card.flush()
                    if (current_data['fields'], current_data['tags']) != (updated_data['fields'], updated_data['tags']):
                        updated_card.note().flush()
>>>>>>> refs/rewritten/private-main-3
=======
                    if current_field_tags != updated_field_tags:
                        updated_card.note().flush()
>>>>>>> 7248e41 (Added error handling and fixed issue with V3 scheduler undo entries using a bad undo step for versions 2.1.45-2.1.49.)

        return card

    def handle_input_action(self, action_type: str):
        """
        Function for handling action calls via shortcuts/context menu actions.

        :param action_type: action type string to use as a reference for the undo entry actions to take
        """
        msg = String.ENTRY_LEECH_ACTIONS if action_type == Config.LEECH_ACTIONS else String.ENTRY_UNLEECH_ACTIONS
        updated_card = mw.col.get_card(self.card.id)

        def perform_actions():
            card = handle_actions(updated_card, self.toolkit_config, action_type)

            if action_type == Config.LEECH_ACTIONS:
                card.note().add_tag(LEECH_TAG)
                tooltip(String.TIP_LEECHED_TEMPLATE.format(1))

            elif action_type == Config.UN_LEECH_ACTIONS:
                card.note().remove_tag(LEECH_TAG)
                tooltip(String.TIP_UNLEECHED_TEMPLATE.format(1))

            return card

        self.handle_card_updates(self.card, perform_actions, msg)

    def on_show_back(self, card: anki.cards.Card):
        """
        Updates the current card, leech marker, and view state to back values.

        :param card: referenced card
        """
        self.on_front = False
        self.card = card
        if self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
            setattr(self.card, prev_type_attr, self.card.type)
        self.update_marker()

    def on_show_front(self, card: anki.cards.Card):
        """
        Updates the current card, leech marker, and view state to front values.

        :param card: referenced card
        """
        self.on_front = True
        self.card = card
        self.update_marker()

    def on_answer(self, context: aqt.reviewer.Reviewer, card: anki.cards.Card, ease: int):
        """
        Handles updates after answering cards.

        :param context: unused Reviewer object
        :param card: referenced card
        :param ease: value of the answer given
        """

        if CURRENT_ANKI_VER <= ANKI_LEGACY_VER:
            card.col.get_card = lambda cid: anki.cards.Card(mw.col, cid)

        def handle_card_answer():
            updated_card = card.col.get_card(card.id)
            if hasattr(card, prev_type_attr):
                updated_card = handle_reverse(self.toolkit_config, card, ease, card.__getattribute__(prev_type_attr))
                delattr(card, prev_type_attr)

<<<<<<< HEAD
            if card.id in self.leeched_cids:
                updated_card = handle_actions(card, self.toolkit_config, Config.LEECH_ACTIONS, reload=False)
                self.leeched_cids.remove(card.id)
=======
            if hasattr(card, was_leech_attr):
                updated_card = handle_actions(card, self.toolkit_config, Config.LEECH_ACTIONS)
                delattr(card, was_leech_attr)
>>>>>>> refs/rewritten/private-main-3

            return updated_card

        self.handle_card_updates(card, handle_card_answer)

    def update_marker(self):
        """
        Update marker style/visibility based on config options and card attributes.
        """
        marker_conf = self.toolkit_config[Config.MARKER_OPTIONS]
        show_marker(False)

        if marker_conf[Config.SHOW_LEECH_MARKER]:
            only_show_on_back = marker_conf[Config.ONLY_SHOW_BACK_MARKER]
            is_review = self.card.type == anki.cards.CARD_TYPE_REV
            almost_leech = is_review and self.card.lapses + ALMOST_DISTANCE >= self.max_fails

            if (not self.on_front and only_show_on_back) or not only_show_on_back:
                if CURRENT_ANKI_VER <= ANKI_LEGACY_VER:
                    self.card.note().has_tag = lambda tag: tag.lower() in [t.lower() for t in self.card.note().tags]

                if self.card.note().has_tag(LEECH_TAG):
                    set_marker_color(LEECH_COLOR)
                    show_marker(True)
                elif marker_conf[Config.USE_ALMOST_MARKER] and almost_leech:
                    set_marker_color(ALMOST_COLOR)
                    show_marker(True)
