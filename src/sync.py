"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import aqt.operations
from aqt import gui_hooks, mw

from .updates import run_action_updates, update_card, is_unique_card
from .config import LeechToolkitConfigManager, merge_fields
from .consts import Config, LEECH_TAG, String
from anki.consts import *


def build_hooks():
    gui_hooks.sync_did_finish.append(sync_collection)


def get_remeasured_lapses(cid: int, reverse_conf: dict):
    remeasured_lapses = 0
    current_consecutive = 0

    reviews = mw.col.db.all(f'SELECT ease, type, ivl FROM revlog WHERE cid={cid} ORDER BY id DESC')

    for ease, rev_type, ivl in reviews:

        if rev_type not in (REVLOG_RESCHED, REVLOG_REV, REVLOG_CRAM):
            current_consecutive = 0

        # Card graduated (lapses reset)
        if rev_type == REVLOG_LRN and ivl > 0:
            remeasured_lapses = 0

        if rev_type == REVLOG_REV:

            if ease < BUTTON_TWO:
                remeasured_lapses += 1
                current_consecutive = 0

            if ease >= BUTTON_TWO:
                current_consecutive += 1

            if current_consecutive == reverse_conf[Config.REVERSE_CONS_ANS]:
                remeasured_lapses -= 1
                current_consecutive = 0

    return remeasured_lapses


def sync_collection():
    global_conf = LeechToolkitConfigManager(mw).config

    if global_conf[Config.SYNC_ENABLED]:

        # Stash config data
        toolkit_configs: dict = {}
        thresholds: dict = {}
        for deck_name_id in mw.col.decks.all_names_and_ids():
            deck_conf = mw.col.decks.config_dict_for_deck_id(deck_name_id.id)
            config_id = mw.col.decks.get(deck_name_id.id)['conf']
            toolkit_configs[f'{deck_name_id.id}'] = merge_fields(global_conf.get(str(config_id), {}), global_conf)
            thresholds[f'{deck_name_id.id}'] = deck_conf['lapse']['leechFails']

        cards = mw.col.db.all(f'SELECT id, did, lapses, type, nid FROM cards WHERE reps > 0 ORDER BY id DESC')

        # Stored for double-checking siblings not updated, yet
        tagged_nids = []

        for cid, did, lapses, card_type, nid in cards:

            # Only updating status for cards in the review queue; otherwise letting User/Anki handle updates.
            if card_type == QUEUE_TYPE_REV:
                updated_card = mw.col.get_card(cid)
                updated_note = updated_card.note()

                toolkit_config = toolkit_configs[str(did)]

                if toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
                    updated_card.lapses = max(get_remeasured_lapses(cid, toolkit_config[Config.REVERSE_OPTIONS]), 0)

                threshold = thresholds[str(did)] \
                    if toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_USE_LEECH_THRESHOLD] \
                    else toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_THRESHOLD]

                has_toolkit_tag = updated_note.has_tag(String.SYNC_TAG_DEFAULT) and nid not in tagged_nids
                has_leech_tag = updated_note.has_tag(LEECH_TAG)

                if toolkit_config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED] and updated_card.lapses < threshold:

                    # Unleech
                    if toolkit_config[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_ENABLED] and has_toolkit_tag:
                        run_action_updates(
                            updated_card,
                            toolkit_config,
                            Config.UN_LEECH_ACTIONS,
                            reload=False
                        )

                    if has_leech_tag:
                        updated_note.remove_tag(LEECH_TAG)

                elif updated_card.lapses >= threshold:

                    # Leech
                    if toolkit_config[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_ENABLED] and not has_toolkit_tag:
                        run_action_updates(
                            updated_card,
                            toolkit_config,
                            Config.LEECH_ACTIONS,
                            reload=False
                        )

                        if nid not in tagged_nids:
                            tagged_nids.append(nid)

                    if not has_leech_tag:
                        updated_note.add_tag(LEECH_TAG)

                if is_unique_card(mw.col.get_card(cid), updated_card):
                    update_card(updated_card, aqt.operations.OpChanges)
