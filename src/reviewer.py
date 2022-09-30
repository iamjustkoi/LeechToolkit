"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import anki.cards
import aqt.reviewer
from anki import hooks
from anki.decks import DeckId
from aqt.utils import tooltip
from aqt.webview import WebContent, AnkiWebView
from aqt import gui_hooks, mw
from aqt.reviewer import Reviewer

from .updates import run_action_updates, run_reverse_updates, update_card, is_unique_card
from .config import LeechToolkitConfigManager, merge_fields
from .consts import Config, ErrorMsg, MARKER_POS_STYLES, LEECH_TAG, String

mark_html_template = '''
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
wrapper_attr = 'toolkit_manager'
was_leech_attr = 'was_leech'

MARKER_TEXT = '🩸'
LEECH_COLOR = 'rgb(248, 105, 86)'
ALMOST_COLOR = 'rgb(248, 197, 86)'
ALMOST_DISTANCE = 1

TOOLTIP_ENABLED = True
TOOLTIP_TIME = 5000


def build_hooks():
    """
    Build Anki hooks for attaching the review wrapper to the reveiwer.
    """
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
        if mw.col.decks.is_filtered(mw.col.decks.get_current_id()) and hasattr(mw.reviewer, wrapper_attr):
            mw.reviewer.__delattr__(wrapper_attr)
        else:
            # Attached for calls and any future garbage collection, potentially, idk
            reviewer.toolkit_wrapper = ReviewWrapper(reviewer, content, mw.col.decks.get_current_id())


def mark_leeched(card: anki.cards.Card):
    """
    Appends a temporary, custom leech attribute to the selected card.
    :param card: card object to add the attribute to
    """
    setattr(card, was_leech_attr, True)


def set_marker_color(color: str):
    """
    Psuedo-tints the leech marker to the input color.
    :param color: color (style) string to update the marker color to
    """
    mw.web.eval(f'document.getElementById("{marker_id}").style.textShadow = "0 0 0 {color}";')


def show_marker(show=False):
    """
    Changes the display state of the run_action marker.
    :param show: new visibility
    """
    if show:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "unset"')
    else:
        mw.web.eval(f'document.getElementById("{marker_id}").style.display = "none"')


class ReviewWrapper:
    toolkit_config: dict
    max_fails: int
    did: DeckId
    content: aqt.webview.WebContent
    card: anki.cards.Card
    on_front: bool

    def __init__(self, reviewer: Reviewer, content: aqt.webview.WebContent, did: DeckId):
        """
        Wrapper used for handling events in the Anki reviewer, if not a filtered review-type.
        :param reviewer: Anki Reviewer object
        :param content: web-content used for editing the page style/html
        :param did: deck id of the current reviewer
        """
        if not mw.col.decks.is_filtered(did):
            self.content = content
            self.reviewer = reviewer
            self.load_options(did)

            self.leech_action = aqt.qt.QAction(String.REVIEWER_ACTION_LEECH, mw)
            leech_shortcut = aqt.qt.QKeySequence(self.toolkit_config[Config.MENU_OPTIONS][Config.LEECH_SHORTCUT])
            self.leech_action.setShortcut(leech_shortcut)
            self.leech_action.triggered.connect(lambda *args: self.run_action(Config.LEECH_ACTIONS))

            self.unleech_action = aqt.qt.QAction(String.REVIEWER_ACTION_UNLEECH, mw)
            unleech_shortcut = aqt.qt.QKeySequence(self.toolkit_config[Config.MENU_OPTIONS][Config.UNLEECH_SHORTCUT])
            self.unleech_action.setShortcut(unleech_shortcut)
            self.unleech_action.triggered.connect(lambda *args: self.run_action(Config.UN_LEECH_ACTIONS))

            mw.setStateShortcuts(
                [
                    (leech_shortcut, lambda *args: self.run_action(Config.LEECH_ACTIONS)),
                    (unleech_shortcut, lambda *args: self.run_action(Config.UN_LEECH_ACTIONS)),
                ]
            )

    def load_options(self, did: DeckId = None):
        """
        Loads options to UI elements and config-based actions, as well as appends hooks to the initialized reviewer.
        :param did: deck id used for determining config values
        """
        self.did = did if did else self.did

        deck_conf_dict = mw.col.decks.config_dict_for_deck_id(self.did)
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

    def run_action(self, action_type: str):
        """
        Function for handling action calls via shortcuts/context menu actions.
        :param action_type: action type string to use as a reference for the undo entry actions to take
        """
        msg = String.ENTRY_LEECH_ACTIONS if action_type == Config.UN_LEECH_ACTIONS else String.ENTRY_UNLEECH_ACTIONS
        entry = self.reviewer.mw.col.add_custom_undo_entry(msg)

        pre_queue, pre_due, pre_note_text = (
            self.card.queue,
            self.card.due,
            self.card.note().joined_fields(),
        )

        if action_type == Config.LEECH_ACTIONS:
            self.card = run_action_updates(self.card, self.toolkit_config, Config.LEECH_ACTIONS)
            self.card.note().add_tag(LEECH_TAG)
            tooltip(String.TIP_LEECHED_TEMPLATE.format(1))
        elif action_type == Config.UN_LEECH_ACTIONS:
            self.card = run_action_updates(self.card, self.toolkit_config, Config.UN_LEECH_ACTIONS)
            self.card.note().remove_tag(LEECH_TAG)
            tooltip(String.TIP_UNLEECHED_TEMPLATE.format(1))

        self.reviewer.mw.col.update_card(self.card)
        self.reviewer.mw.col.update_note(self.card.note())

        changes = self.reviewer.mw.col.merge_undo_entries(entry)
        changes.study_queues = True if (pre_queue != self.card.queue) or (pre_due != self.card.due) else False
        changes.note_text = True if pre_note_text != self.card.note().joined_fields() else False

        self.refresh_if_needed(changes)

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
            reviewer_will_show_context_menu,
        )
        card_did_leech.append(mark_leeched)

        reviewer_did_show_question.append(self.on_show_front)
        reviewer_did_show_answer.append(self.on_show_back)
        reviewer_did_answer_card.append(self.on_answer)
        reviewer_will_show_context_menu.append(self.append_context_menu)

        reviewer_will_end.append(self.remove_hooks)

    def append_context_menu(self, webview: AnkiWebView, menu: aqt.qt.QMenu):
        action_labels = [action.text() for action in menu.actions()]
        menu.addSeparator()
        menu.addAction(self.leech_action) if String.REVIEWER_ACTION_LEECH not in action_labels else None
        menu.addAction(self.unleech_action) if String.REVIEWER_ACTION_UNLEECH not in action_labels else None

    def remove_hooks(self):
        try:
            hooks.card_did_leech.remove(mark_leeched)
        except NameError:
            print(ErrorMsg.ACTION_MANAGER_NOT_DEFINED)

        gui_hooks.reviewer_did_show_question.remove(self.on_show_front)
        gui_hooks.reviewer_did_show_answer.remove(self.on_show_back)
        gui_hooks.reviewer_did_answer_card.remove(self.on_answer)

    def on_show_back(self, card: anki.cards.Card):
        """
        Updates the current card, leech marker, and view state to back values.

        :param card: referenced card
        """
        self.on_front = False
        self.card = card
        if self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
            setattr(card, prev_type_attr, card.type)
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
        updated_card = card.col.get_card(card.id)
        if hasattr(card, prev_type_attr):
            updated_card = run_reverse_updates(self.toolkit_config, card, ease, card.__getattribute__(prev_type_attr))
            delattr(card, prev_type_attr)

        if hasattr(card, was_leech_attr):
            updated_card = run_action_updates(card, self.toolkit_config, Config.LEECH_ACTIONS)
            delattr(card, was_leech_attr)

        if is_unique_card(card, updated_card):
            update_card(updated_card, aqt.reviewer.OpChanges)

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
                if self.card.note().has_tag(LEECH_TAG):
                    set_marker_color(LEECH_COLOR)
                    show_marker(True)
                elif marker_conf[Config.USE_ALMOST_MARKER] and almost_leech:
                    set_marker_color(ALMOST_COLOR)
                    show_marker(True)
