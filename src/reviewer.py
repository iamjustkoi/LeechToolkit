"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import anki.cards
import aqt.reviewer
from anki import cards, hooks
from anki.decks import DeckId
from aqt.webview import WebContent, AnkiWebView
from aqt import reviewer, gui_hooks, mw

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
was_leech_attr = 'was_leech'

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

    webview_will_set_content.append(
        lambda content, context:
        on_will_start(content, context) if isinstance(context, reviewer.Reviewer) else None
    )


def on_will_start(content: aqt.webview.WebContent, anki_reviewer: aqt.reviewer.Reviewer):
    if not mw.col.decks.is_filtered(mw.col.decks.get_current_id()):
        # Attached for garbage collection
        anki_reviewer.toolkit_manager = ReviewerWrapper(content, mw.col.decks.get_current_id())


def mark_leeched(card: anki.cards.Card):
    setattr(card, was_leech_attr, True)


def set_marker_color(color: str):
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


class ReviewerWrapper:
    toolkit_config: dict
    max_fails: int
    did: DeckId
    page_content: aqt.webview.WebContent
    card: anki.cards.Card
    on_front: bool

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

    def run_action(self, action_type: str):
        if action_type == Config.LEECH_ACTIONS:
            self.card = run_action_updates(self.card, self.toolkit_config, Config.LEECH_ACTIONS)
            self.card.note().add_tag(LEECH_TAG)
        elif action_type == Config.UN_LEECH_ACTIONS:
            self.card = run_action_updates(self.card, self.toolkit_config, Config.UN_LEECH_ACTIONS)
            self.card.note().remove_tag(LEECH_TAG)
        update_card(updated_card=self.card, changes=aqt.reviewer.OpChanges)
        self.update_marker()

    def append_marker_html(self):
        marker_float = MARKER_POS_STYLES[self.toolkit_config[Config.MARKER_OPTIONS][Config.MARKER_POSITION]]
        self.page_content.body += mark_html_template.format(
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
            reviewer_will_show_context_menu,
        )
        card_did_leech.append(mark_leeched)

        reviewer_did_show_question.append(self.on_show_front)
        reviewer_did_show_answer.append(self.on_show_back)
        reviewer_did_answer_card.append(self.on_answer)
        reviewer_will_show_context_menu.append(self.append_context_menu)

        reviewer_will_end.append(self.remove_hooks)

    def append_context_menu(self, webview: AnkiWebView, menu: aqt.qt.QMenu):
        leech_exists, unleech_exists = False, False
        for action in menu.actions():
            action: aqt.qt.QAction
            if action.text() == String.REVIEWER_ACTION_LEECH:
                leech_exists = True
            if action.text() == String.REVIEWER_ACTION_UNLEECH:
                unleech_exists = True

        menu.addSeparator()

        if not leech_exists:
            leech_action = menu.addAction(
                String.REVIEWER_ACTION_LEECH,
                lambda *args: self.run_action(Config.LEECH_ACTIONS),
            )
            leech_shortcut = aqt.qt.QKeySequence(self.toolkit_config[Config.MENU_OPTIONS][Config.LEECH_SHORTCUT])
            leech_action.setShortcut(leech_shortcut)

        if not unleech_exists:
            unleech_action = menu.addAction(
                String.REVIEWER_ACTION_UNLEECH,
                lambda *args: self.run_action(Config.UN_LEECH_ACTIONS),
            )
            unleech_shortcut = aqt.qt.QKeySequence(self.toolkit_config[Config.MENU_OPTIONS][Config.UNLEECH_SHORTCUT])
            unleech_action.setShortcut(unleech_shortcut)

    def remove_hooks(self):
        try:
            hooks.card_did_leech.remove(mark_leeched)
        except NameError:
            print(ErrorMsg.ACTION_MANAGER_NOT_DEFINED)

        gui_hooks.reviewer_did_show_question.remove(self.on_show_front)
        gui_hooks.reviewer_did_show_answer.remove(self.on_show_back)
        gui_hooks.reviewer_did_answer_card.remove(self.on_answer)

    def on_show_back(self, card: cards.Card):
        self.on_front = False
        if self.toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
            setattr(card, prev_type_attr, card.type)
        self.update_marker()

    def on_show_front(self, card: cards.Card):
        self.on_front = True
        self.update_marker()
        self.card = card

    def on_answer(self, context: aqt.reviewer.Reviewer, card: cards.Card, ease: int):
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
        Updates marker style/visibility based on user options and current card's attributes.
        """
        marker_conf = self.toolkit_config[Config.MARKER_OPTIONS]
        if not marker_conf[Config.SHOW_LEECH_MARKER] or (
                marker_conf[Config.ONLY_SHOW_BACK_MARKER] and self.on_front):
            show_marker(False)
        elif self.card.note().has_tag(LEECH_TAG):
            set_marker_color(LEECH_COLOR)
            show_marker(True)
        elif marker_conf[Config.USE_ALMOST_MARKER] \
                and self.card.type == cards.CARD_TYPE_REV \
                and (self.card.lapses + ALMOST_DISTANCE) >= self.max_fails:
            set_marker_color(ALMOST_COLOR)
            show_marker(True)
        elif not self.card.note().has_tag(LEECH_TAG):
            show_marker(False)
