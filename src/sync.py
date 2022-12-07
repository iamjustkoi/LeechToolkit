"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import traceback

from aqt import gui_hooks, mw

from .actions import handle_actions
from .config import LeechToolkitConfigManager, merge_fields
from .consts import ANKI_SYNC_ISSUE_VER, CURRENT_ANKI_VER, Config, ErrorMsg, LEECH_TAG, String
from anki.consts import *

try:
    # noinspection PyUnresolvedReferences
    import aqt.operations
except ModuleNotFoundError:
    print(f'{traceback.format_exc()}\n{ErrorMsg.MODULE_NOT_FOUND_LEGACY}')


def build_hooks():
    if CURRENT_ANKI_VER > ANKI_SYNC_ISSUE_VER:
        # noinspection PyUnresolvedReferences
        from aqt.undo import UndoActionsInfo

        # noinspection PyUnresolvedReferences
        gui_hooks.sync_did_finish.append(sync_collection)


def get_remeasured_lapses(cid: int, reverse_conf: dict):
    """
    Remeasures lapses based on consecutive correct streaks and again answers in review logs.

    :param cid: referenced card id
    :param reverse_conf: config to use for determining measurements/returned lapses
    :return: the new lapse count
    """
    remeasured_lapses = 0
    consecutive_correct = 0

    reviews = mw.col.db.all(f'SELECT ease, type, ivl FROM revlog WHERE cid={cid} ORDER BY id DESC')

    for ease, rev_type, ivl in reviews:
        # If review type was relearn or learn, reset the consecutive count
        if rev_type not in (REVLOG_RELRN, REVLOG_LRN):
            consecutive_correct = 0

        # Card graduated (lapses reset, learn interval became positive)
        if rev_type == REVLOG_LRN and ivl > 0:
            remeasured_lapses = 0

        if rev_type == REVLOG_REV:
            if ease < BUTTON_TWO:
                remeasured_lapses += 1
                consecutive_correct = 0

            if ease >= BUTTON_TWO:
                consecutive_correct += 1

            if consecutive_correct == reverse_conf[Config.REVERSE_CONS_ANS]:
                remeasured_lapses -= 1
                consecutive_correct = 0

    return remeasured_lapses


# noinspection PyArgumentList
def sync_collection(is_manual_sync=False):
    """
    Syncs the collection's lapse count and, optionally, leech status based on the current user preferences and review
    logs.
    """
    manager = LeechToolkitConfigManager(mw)
    global_conf = manager.config

    if global_conf[Config.SYNC_ENABLED] or is_manual_sync:
        # Stash config data
        toolkit_configs: dict = manager.get_all_configs()

        thresholds: dict = {}
        for key, val in toolkit_configs.items():
            deck_conf = mw.col.decks.config_dict_for_deck_id(int(key))
            thresholds[key] = deck_conf['lapse']['leechFails']

        cards = mw.col.db.all(f'SELECT id, did, lapses, type, nid FROM cards WHERE reps > 0 ORDER BY id DESC')

        # Stored for double-checking siblings not updated, yet
        tagged_nids = set()
        updated_cids = set()

        for cid, did, lapses, card_type, nid in cards:
            # Only updates status for cards in the review queue; otherwise handled by User/Anki.
            if card_type == QUEUE_TYPE_REV:
                # noinspection PyUnresolvedReferences
                card = mw.col.getCard(cid) if CURRENT_ANKI_VER <= ANKI_SYNC_ISSUE_VER else mw.col.get_card(cid)
                toolkit_config = toolkit_configs[str(did)]

                if toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
                    card.lapses = max(get_remeasured_lapses(cid, toolkit_config[Config.REVERSE_OPTIONS]), 0)

                if card.lapses != lapses:
                    updated_cids.add(cid)

                threshold = thresholds[str(did)] \
                    if toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_USE_LEECH_THRESHOLD] \
                    else toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_THRESHOLD]

                note = card.note()
                if CURRENT_ANKI_VER <= ANKI_SYNC_ISSUE_VER:
                    note.has_tag = note.hasTag
                has_toolkit_tag = note.has_tag(String.SYNC_TAG_DEFAULT) and nid not in tagged_nids
                has_leech_tag = note.has_tag(LEECH_TAG)

                if toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED] and card.lapses < threshold:
                    # Unleech
                    if toolkit_config[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_ENABLED] and has_toolkit_tag:
                        card = handle_actions(card, toolkit_config, Config.UN_LEECH_ACTIONS, reload=False)
                        updated_cids.add(cid)

                    if has_leech_tag:
                        note = card.note()
                        if CURRENT_ANKI_VER <= ANKI_SYNC_ISSUE_VER:
                            note.remove_tag = note.delTag
                        note.remove_tag(LEECH_TAG)
                        updated_cids.add(cid)

                elif card.lapses >= threshold:
                    # Leech
                    if toolkit_config[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_ENABLED] and not has_toolkit_tag:
                        handle_actions(card, toolkit_config, Config.LEECH_ACTIONS, reload=False)
                        tagged_nids.add(nid) if nid not in tagged_nids else None
                        updated_cids.add(cid)

                    if not has_leech_tag:
                        note = card.note()
                        if CURRENT_ANKI_VER <= ANKI_SYNC_ISSUE_VER:
                            note.add_tag = note.addTag
                        note.add_tag(LEECH_TAG)
                        updated_cids.add(cid)

                if cid in updated_cids:
                    card.flush()
                    card.note().flush()

        aqt.utils.tooltip(String.TIP_UPDATED_TEMPLATE.format(len(updated_cids)))
