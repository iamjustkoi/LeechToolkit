"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from __future__ import annotations

import datetime
import random
import re
import traceback
from datetime import date
from difflib import SequenceMatcher
from typing import List

import anki.cards
import anki.decks

from anki.consts import QUEUE_TYPE_SUSPENDED, QUEUE_TYPE_NEW, CARD_TYPE_NEW, BUTTON_ONE
from aqt import utils

from .consts import (
    ANKI_LEGACY_VER, Action,
    CURRENT_ANKI_VER, ErrorMsg, Macro,
    EditAction,
    RescheduleAction,
    QueueAction,
    Config,
    String,
    LEECH_TAG,
    REV_DECREASE,
    REV_RESET,
)
from .legacy import _try_get_config_dict_for_did, _try_get_current_did, _try_get_deck_and_child_ids, _try_has_tag

try:
    from anki.collection import OpChanges
except (ModuleNotFoundError, ImportError):
    print(f'{traceback.format_exc()}\n{ErrorMsg.MODULE_NOT_FOUND_LEGACY}')

TOOLTIP_ENABLED = True
TOOLTIP_TIME = 5000


def apply_tag_macros(card: anki.cards.Card, tag: str):
    """
    Formats the input tag string with its filled-in text macro values.
    
    :param card: card used as a reference-point for retrieved data
    :param tag: tag string to format
    :return: a new, formatted string
    """
    result = tag

    macro = Macro.DATE
    if re.search(fr'(?<!%){macro}', tag):
        result = result.replace(macro, str(date.today()))

    macro = Macro.REVIEWS
    if re.search(fr'(?<!%){macro}', tag):
        cmd = f'SELECT reps FROM cards WHERE id is {card.id}'
        result = result.replace(macro, str(card.col.db.scalar(cmd)))

    macro = r'%%'
    if re.search(macro, tag):
        result = result.replace(macro, '%')

    return result


def was_consecutively_correct(card: anki.cards.Card, times: int):
    """
    Checks if the card was correct for a certain amount of consecutive times.
    
    :param card: card to check
    :param times: total times to check the card was answered correctly, in a row
    :return: true if answers were correct for the input times, else false
    """
    total_correct = len(get_correct_answers(card))
    return total_correct > 0 and total_correct % times == 0


def get_correct_answers(card: anki.cards.Card):
    """
    Retrieves all reviews that were correct without any "again" answers.

    :param card: card to use as reference
    :return: a list of correct answers (2-4)
    """

    cmd = f'SELECT ease FROM revlog WHERE cid IS {card.id} AND ease IS NOT 0 ORDER BY id DESC'
    answers = card.col.db.list(cmd)

    last_index = len(answers) - 1 if len(answers) > 0 else 0
    if BUTTON_ONE in answers:
        last_index = answers.index(BUTTON_ONE) - 1 if answers.index(BUTTON_ONE) != 0 else 0
    return answers[:last_index]


def handle_reverse(config: dict, card: anki.cards.Card, ease: int, prev_type: anki.consts.CardType):
    """
    Runs reverse leech updates to the input card and returns an updated card object.
    
    :param config: toolkit config
    :param card: Card to update
    :param ease: review-answer input
    :param prev_type: previous type of the current card used for determining changes
    :return: updated card object
    """
    updated_card = card.col.get_card(card.id)
    tooltip_items = []

    if config[Config.REVERSE_OPTIONS][Config.REVERSE_ENABLED]:
        deck_config = _try_get_config_dict_for_did(_try_get_current_did(updated_card))
        use_leech_threshold = config[Config.REVERSE_OPTIONS][Config.REVERSE_USE_LEECH_THRESHOLD]
        threshold = deck_config['lapse']['leechFails'] if use_leech_threshold else \
            config[Config.REVERSE_OPTIONS][Config.REVERSE_THRESHOLD]

        # Lapse updates
        if was_consecutively_correct(updated_card, config[Config.REVERSE_OPTIONS][Config.REVERSE_CONS_ANS]):
            if ease > 1 and updated_card.lapses > 0 and prev_type == anki.cards.CARD_TYPE_REV:
                if config[Config.REVERSE_OPTIONS][Config.REVERSE_METHOD] == REV_DECREASE:
                    updated_card.lapses -= 1 if updated_card.lapses != 0 else 0
                    tooltip_items.append(String.LAPSES_DECREASED)
                elif config[Config.REVERSE_OPTIONS][Config.REVERSE_METHOD] == REV_RESET:
                    updated_card.lapses = 0
                    tooltip_items.append(String.LAPSES_RESET)

        # Un-leech
        if updated_card.lapses < threshold:
            if ease > 1 and _try_has_tag(updated_card.note(), LEECH_TAG) and prev_type == anki.cards.CARD_TYPE_REV:
                updated_card.note().remove_tag(LEECH_TAG)
                tooltip_items.append(String.LEECH_REVERSED)
                updated_card = handle_actions(
                    updated_card,
                    config,
                    Config.UN_LEECH_ACTIONS,
                    reload=False
                )

        if TOOLTIP_ENABLED and len(tooltip_items) > 0:
            utils.tooltip('\n\n'.join(tooltip_items), period=TOOLTIP_TIME)
    return updated_card


# Was considering for logging changes, etc., but opted to warn/reveal to frontend, instead.
{
    # def commit_lapses_to_revlog(col: anki.collection.Collection, card: anki.cards.Card, lapses: int):
    #     """
    #     ...
    #     :param col:
    #     :param card:
    #     :param lapses:
    #     :return:
    #     """
    #     # id -- unix ms time/review id
    #     # cid -- cid
    #     # usn -- usn (update sequence number for checking against Anki Web. -1 = push)
    #     # ease -- ease (often unused for reschedule reviews, so using as lapse data field)
    #     # ivl -- interval (negative = seconds)
    #     # lastIvl -- last interval (negative = seconds)
    #     # factor -- factor
    #     # time -- time
    #     # type -- type
    #     cmd = f'''
    #         INSERT INTO "revlog" (id, cid, usn, ease, ivl, lastIvl, factor, time, type)
    #         VALUES(
    #             {int(datetime.datetime.now().timestamp() * 1000)},
    #             {card.id},
    #             -1,
    #             {lapses + 1},
    #             {card.ivl},
    #             {card.ivl},
    #             0,
    #             0,
    #             {REVLOG_RESCHED}
    #         );
    #     '''
    #     col.db.all(cmd)
    #     col.db.commit()
}


# Actions format: actionName: {enabled: bool, key: val}
def handle_actions(card: anki.cards.Card, toolkit_conf: dict, action_type=Config.LEECH_ACTIONS, reload=True):
    """
    Performs updates to a card based on user preferences and the leech/un-leech action type.

    :param card: card to update
    :param toolkit_conf: config instance to use as a reference for updates
    :param action_type: action type string used to determine config requests and updates to perform
    :param reload: whether to create a new card object or update the input card, itself
    :return: an updated card object
    """
    updated_card = card.col.get_card(card.id) if reload else card
    actions_conf = toolkit_conf[action_type]

    def handle_deck_move():
        if actions_conf[Action.MOVE_DECK][Action.ENABLED]:
            # If the card was also in a cram/custom study deck, set it back to its original deck and due date:
            updated_card.odid = 0
            if updated_card.odue:
                updated_card.due = updated_card.odue
                updated_card.odue = 0
            if actions_conf[Action.MOVE_DECK][Action.INPUT]:
                updated_card.did = int(actions_conf[Action.MOVE_DECK][Action.INPUT])  # updated_card.col.decks.id()

    def handle_flag():
        if actions_conf[Action.FLAG][Action.ENABLED]:
            if CURRENT_ANKI_VER <= ANKI_LEGACY_VER:
                updated_card.setUserFlag(actions_conf[Action.FLAG][Action.INPUT])
            else:
                updated_card.set_user_flag(actions_conf[Action.FLAG][Action.INPUT])

    def handle_suspend():
        if actions_conf[Action.SUSPEND][Action.ENABLED] and actions_conf[Action.SUSPEND][Action.INPUT]:
            updated_card.queue = QUEUE_TYPE_SUSPENDED

    def handle_add_tags():
        if actions_conf[Action.ADD_TAGS][Action.ENABLED]:
            for tag in str(actions_conf[Action.ADD_TAGS][Action.INPUT]).split(' '):
                if CURRENT_ANKI_VER <= ANKI_LEGACY_VER:
                    updated_card.note().addTag(apply_tag_macros(updated_card, tag))
                else:
                    updated_card.note().add_tag(apply_tag_macros(updated_card, tag))

    def handle_remove_tags():
        if actions_conf[Action.REMOVE_TAGS][Action.ENABLED]:
            for tag in actions_conf[Action.REMOVE_TAGS][Action.INPUT].split(' '):
                # Formats the tag's macros then retrieves the regex pattern and replaces it from the tags string
                formatted_tag = apply_tag_macros(updated_card, tag)

                if re.search(f'(?<!%){Macro.REGEX}:.*', formatted_tag):
                    reg_cmd = formatted_tag.replace(f'{Macro.REGEX}:', '', 1)
                    # Replace "everything" character with the "no spaces" character
                    reg_match = re.search(f'((?<=^\")(.*)(?=\"$))|(^(?!\")(.*))', reg_cmd)
                    reg_string = reg_match.group(0).replace(f'.', r'\S')
                    # Remove tags from the tags string
                    if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
                        result_tags = ''.join(re.split(reg_string, updated_card.note().string_tags())).strip()
                        updated_card.note().set_tags_from_str(result_tags)
                    else:
                        result_tags = ''.join(re.split(reg_string, updated_card.note().stringTags())).strip()
                        updated_card.note().setTagsFromStr(result_tags)

                else:
                    if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
                        updated_card.note().remove_tag(formatted_tag)
                    else:
                        updated_card.note().delTag(formatted_tag)

    def handle_forget():
        if actions_conf[Action.FORGET][Action.ENABLED] and actions_conf[Action.FORGET][Action.INPUT][0]:
            if updated_card.odid:
                updated_card.odid = 0
            if actions_conf[Action.FORGET][Action.INPUT][1]:
                updated_card.odue = 0
            if actions_conf[Action.FORGET][Action.INPUT][2]:
                updated_card.reps = 0
                updated_card.lapses = 0

    def handle_edit_fields():
        if actions_conf[Action.EDIT_FIELDS][Action.ENABLED]:
            inputs: list[str] = [list(input_dict.keys())[0] for input_dict in
                                 actions_conf[Action.EDIT_FIELDS][Action.INPUT]]

            for nid in inputs:
                # nid = int(filtered_nid.split('.')[0])
                if updated_card.note_type()['id'] == nid:
                    conf_meta = actions_conf[Action.EDIT_FIELDS][Action.INPUT][nid]

                    new_text: str = conf_meta[EditAction.TEXT]
                    card_field = updated_card.note().fields[conf_meta[EditAction.FIELD]]

                    if conf_meta[EditAction.METHOD] == EditAction.APPEND_METHOD:
                        card_field += new_text
                    if conf_meta[EditAction.METHOD] == EditAction.PREPEND_METHOD:
                        card_field = new_text + card_field
                    if conf_meta[EditAction.METHOD] == EditAction.REPLACE_METHOD:
                        card_field = card_field.replace(conf_meta[EditAction.REPL], new_text)
                    if conf_meta[EditAction.METHOD] == EditAction.REGEX_METHOD:
                        card_field = new_text.join(re.split(conf_meta[EditAction.REPL], card_field))

                    updated_card.note().fields[conf_meta[EditAction.FIELD]] = card_field

    def handle_reschedule():
        if actions_conf[Action.RESCHEDULE][Action.ENABLED]:
            from_days = actions_conf[Action.RESCHEDULE][Action.INPUT][RescheduleAction.FROM]
            to_days = actions_conf[Action.RESCHEDULE][Action.INPUT][RescheduleAction.TO]
            days = random.randrange(from_days, to_days) if from_days < to_days else random.randrange(to_days, from_days)
            delta = datetime.timedelta(days=days)
            updated_card.due = int((datetime.datetime.now() + delta).timestamp())

            if actions_conf[Action.RESCHEDULE][Action.INPUT][RescheduleAction.RESET]:
                updated_card.ivl = delta.days

    def handle_add_to_queue():
        if actions_conf[Action.ADD_TO_QUEUE][Action.ENABLED]:
            queue_inputs = actions_conf[Action.ADD_TO_QUEUE][Action.INPUT]

            def get_inserted_pos(insert_type, input_pos):
                """
                Retrieves the position for the given insert type.

                :param insert_type: type of insertion to use to determine the position output
                :param input_pos: extra position value to add to/insert with the position value returned
                :return: retrieved position number
                """
                if insert_type != QueueAction.POS:

                    queue_cmd = f'SELECT min(due), max(due) FROM cards WHERE type={CARD_TYPE_NEW} AND odid=0'

                    if queue_inputs[QueueAction.CURRENT_DECK]:
                        current_did = updated_card.current_deck_id() if CURRENT_ANKI_VER > ANKI_LEGACY_VER else \
                            updated_card.did
                        deck_and_child_ids = _try_get_deck_and_child_ids(current_did)
                        dids = [int(i) for i in deck_and_child_ids]
                        queue_cmd += f' AND did IN {anki.decks.ids2str(dids)}'

                    top, bottom = card.col.db.first(queue_cmd)
                    queue_pos = top if insert_type == QueueAction.TOP else bottom
                    # Empty queue
                    queue_pos = 0 if queue_pos is None else queue_pos

                    return queue_pos + input_pos if (queue_pos + input_pos > 0) else queue_pos

                return input_pos

            from_pos = get_inserted_pos(queue_inputs[QueueAction.FROM_INDEX], queue_inputs[QueueAction.FROM_VAL])
            to_pos = get_inserted_pos(queue_inputs[QueueAction.TO_INDEX], queue_inputs[QueueAction.TO_VAL])

            # Swap positions if value range non-positive
            from_pos, to_pos = (to_pos, from_pos) if from_pos > to_pos else (from_pos, to_pos)

            filtered_ids, filtered_positions = [], []
            if queue_inputs[QueueAction.NEAR_SIBLING] or queue_inputs[QueueAction.NEAR_SIMILAR]:
                # Just in case (modular function)
                handle_deck_move() if str(updated_card.did) != actions_conf[Action.MOVE_DECK][Action.INPUT] else None

                cmd = f'''
                    SELECT {{get}} FROM cards
                    WHERE id != {updated_card.id}
                    AND did == {updated_card.did}
                    AND due BETWEEN {from_pos} AND {to_pos}
                '''
                if queue_inputs[QueueAction.NEAR_SIBLING]:
                    cmd += f'    AND nid = {updated_card.nid} AND queue = {QUEUE_TYPE_NEW}'
                else:
                    cmd += f'    AND nid != {updated_card.nid}'
                filtered_ids = card.col.db.list(cmd.format(get='id'))
                filtered_positions = card.col.db.list(cmd.format(get='due'))

                # Gets the string output of each card's data currently in the new queue and compares it to other cards
                #  using ratios/fuzzy comparison.
                if queue_inputs[QueueAction.NEAR_SIMILAR]:

                    filtered_field_ords: List[int] = []
                    for note_dict in queue_inputs[QueueAction.FILTERED_FIELDS]:
                        note_type_id = int(list(note_dict)[0])
                        if note_type_id == updated_card.note().mid:
                            for key in list(note_dict.keys()):
                                filtered_field_ords.append(int(note_dict[key]))

                    def get_excluded_strings() -> list[str]:
                        query = str(queue_inputs[QueueAction.EXCLUDED_TEXT])
                        excluded_result = []

                        # Handle quote and escape quote characters
                        pattern = r'(?<!\\)"(?:[^\\"]|\\")*"'
                        matches: List[str] = re.findall(pattern, query)
                        excluded_result += [result.strip('"').replace(r'\"', '"') for result in matches]
                        filtered_query = re.sub(pattern, '', query).replace(r'\"', '"')

                        # Concatenate, replace new lines with, and split string using space characters
                        excluded_result += re.sub('  +', ' ', filtered_query).replace('\n', ' ').split(' ')
                        return excluded_result

                    excluded_strings = get_excluded_strings()

                    def get_filtered_card_data(items: List[(str, str)]):
                        # for item in items:
                        filtered_str_data = ''
                        # INCLUDE
                        if queue_inputs[QueueAction.INCLUSIVE_FIELDS]:
                            for field_ord in filtered_field_ords:
                                filtered_str_data += items[field_ord][1]
                        # EXCLUDE
                        if not queue_inputs[QueueAction.INCLUSIVE_FIELDS]:
                            for item in items:
                                if item[0] not in filtered_field_ords:
                                    filtered_str_data += item[1]

                        for excluded_str in excluded_strings:
                            excluded_str = ' ' if excluded_str == '\\s' else excluded_str
                            filtered_str_data = filtered_str_data.replace(excluded_str, '')

                        return filtered_str_data

                    min_ratio = queue_inputs[QueueAction.SIMILAR_RATIO]
                    leech_data_str = get_filtered_card_data(updated_card.note().items())
                    for cid in filtered_ids:
                        new_card = card.col.get_card(cid)
                        is_similar_card = False
                        if new_card.note_type()['id'] == updated_card.note().mid:
                            new_data_str = get_filtered_card_data(new_card.note().items())
                            if SequenceMatcher(None, leech_data_str, new_data_str).ratio() >= min_ratio:
                                is_similar_card = True
                        if not is_similar_card:
                            filtered_positions.remove(new_card.due)

            updated_card.queue = QUEUE_TYPE_NEW
            updated_card.type = CARD_TYPE_NEW
            if len(filtered_positions) > 0:
                updated_card.due = random.choice(filtered_positions)
            else:
                updated_card.due = random.randrange(from_pos, to_pos) if from_pos != to_pos else from_pos

    def update_sync_tag():
        """
        Attaches the custom leech tag based on user preferences.
        """
        if toolkit_conf[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_ENABLED]:
            if action_type == Config.LEECH_ACTIONS:
                if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
                    updated_card.note().add_tag(toolkit_conf[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_TEXT])
                else:
                    updated_card.note().addTag(toolkit_conf[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_TEXT])
            elif action_type == Config.UN_LEECH_ACTIONS:
                if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
                    updated_card.note().remove_tag(toolkit_conf[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_TEXT])
                else:
                    updated_card.note().delTag(toolkit_conf[Config.SYNC_TAG_OPTIONS][Config.SYNC_TAG_TEXT])

    handle_flag()
    handle_deck_move()
    handle_suspend()
    handle_add_tags()
    handle_remove_tags()
    handle_forget()
    handle_edit_fields()
    handle_reschedule()
    handle_add_to_queue()

    update_sync_tag()

    return updated_card
